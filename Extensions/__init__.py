import logging
import importlib
import inspect
import pkgutil

from MobSF.analysis_extension import StaticAnalysisExtension, DynamicAnalysisExtension

from Extensions.Mobsf_modules import dynamic_analysis, static_analysis

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
        return custom_analysis_list
    except Exception as e:
        logger.exception('Performing custom static analysis')
        logger.exception('reason : %s', str(e))
        return custom_analysis_list


def dynamic_analysis_extension(platform, motor, md5_hash, package):
    """
    Search for every class that extends the class DynamicAnalysisExtension
    in this module and start the assessments that are defined in it.    
    """
    try:
        custom_dynamic_analysis = []
        module_motor = importlib.import_module('{}.{}.{}'.format(dynamic_analysis.__name__, platform, motor))
        for(_, name, _) in pkgutil.iter_modules(module_motor.__path__):
            module = importlib.import_module(
                '{}.{}.{}.{}'.format(dynamic_analysis.__name__, platform,
                motor, name)
            )
            for name, obj in inspect.getmembers(module):
                if(inspect.isclass(obj)
                   and issubclass(obj, DynamicAnalysisExtension)
                   and obj.__name__ != DynamicAnalysisExtension.__name__):
                   
                   analysis_class = getattr(module, name)
                   custom_dynamic_analysis.append(analysis_class(md5_hash, package))
                   logger.info(
                       'Starting additional dynamic analysis defined in %s',
                       module.__name__
                   ) 
        return custom_dynamic_analysis
    except Exception as e:
        logger.exception('Performing custom dynamic analysis')
        logger.exception('reason : %s', str(e))
