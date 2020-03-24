import os
import logging
import importlib
import inspect
import sys
import pkgutil

from MobSF.static_analysis_extension import StaticAnalysisExtension
from Extensions import Mobsf_modules
from Extensions.Mobsf_modules import static_analysis

from abc import ABC

logger = logging.getLogger(__name__)

def static_analysis_extension(app_path, platform, typ, mobsf_analysis):
    """
    Will search for every class that extends the class StaticAnalysisExtension in this module and 
    start the assesments that are defined in it.
    """
    custom_analysis_list = []
    try:
        module_platform = importlib.import_module(
            "{}.{}".format(static_analysis.__name__, platform))
        for(_, name, _) in pkgutil.iter_modules(module_platform.__path__):
            module = importlib.import_module(
                "{}.{}.{}".format(static_analysis.__name__, platform, name))
            for name, obj in inspect.getmembers(module):
                if(inspect.isclass(obj) and issubclass(obj, StaticAnalysisExtension) and obj.__name__ != StaticAnalysisExtension.__name__):
                    analysis_class = getattr(module, name)
                    analysis = analysis_class()
                    logger.info(
                        "Starting additional static analysis defined in {}".format(module.__name__))
                    custom_analysis = analysis.perform_analysis(
                        app_path, typ, mobsf_analysis)
                    if custom_analysis != None:
                        report = {'report': custom_analysis,
                                  'template_file': analysis.get_template()}
                    # Used for the custom link in the sidebar
                        if hasattr(analysis, "get_title"):
                            report['title'] = analysis.get_title()
                        custom_analysis_list.append(report)
        return custom_analysis_list
    except Exception as e:
        logger.exception("Performing custom analysis")
        logger.exception("reason : {}".format(str(e)))
        return custom_analysis_list
