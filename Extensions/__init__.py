import logging
import importlib
import inspect
import pkgutil

from MobSF.static_analysis_extension import StaticAnalysisExtension

from Extensions.Mobsf_modules import static_analysis

logger = logging.getLogger(__name__)


def static_analysis_extension(app_path, platform, typ, mobsf_analysis):
    """
    Search for every class that extends the class StaticAnalysisExtension
    in this module and start the assessments that are defined in it.
    """
    custom_analysis_list = []
    try:
        module_platform = importlib.import_module(
            '{}.{}'.format(static_analysis.__name__, platform))
        for(_, name, _) in pkgutil.iter_modules(module_platform.__path__):
            module = importlib.import_module(
                '{}.{}.{}'.format(static_analysis.__name__, platform, name))
            for name, obj in inspect.getmembers(module):
                if(inspect.isclass(obj)
                   and issubclass(obj, StaticAnalysisExtension)
                   and obj.__name__ != StaticAnalysisExtension.__name__):

                    analysis_class = getattr(module, name)
                    analysis = analysis_class(app_path, typ, mobsf_analysis)
                    logger.info(
                        'Starting additional static analysis defined in %s',
                        module.__name__)
                    custom_analysis = analysis.perform_analysis()
                    if custom_analysis is not None:
                        report = {'report': custom_analysis,
                                  'template_file': analysis.get_template()}
                    # Used for the custom link in the sidebar
                        if hasattr(analysis, 'get_title'):
                            report['title'] = analysis.get_title()
                        custom_analysis_list.append(report)
        logger.info(custom_analysis_list)
        return custom_analysis_list
    except Exception as e:
        logger.exception('Performing custom analysis')
        logger.exception('reason : %s', str(e))
        return custom_analysis_list
