import os
import logging
import importlib
import inspect
import sys
import pkgutil
from .static_analysis import android
from MobSF.static_analysis_extension import StaticAnalysisExtension
from abc import ABC

logger = logging.getLogger(__name__)


def static_analysis_extension(app_path, platform, typ, code_an_dic):
    """
    Will search for every class that extends the class StaticAnalysisExtension in this module and 
    start the assesments that are defined in it.
    """
    module_platform = importlib.import_module(
        "Extensions.static_analysis.{}".format(platform))
    custom_analysis_list = []
    for(_, name, _) in pkgutil.iter_modules(module_platform.__path__):
        module = importlib.import_module(
            "{}.{}".format(android.__name__, name))
        for name, obj in inspect.getmembers(module):
            if(inspect.isclass(obj) and issubclass(obj, StaticAnalysisExtension) and obj.__name__ != StaticAnalysisExtension.__name__):
                analysis_class = getattr(module, name)
                analysis = analysis_class()
                logger.info(
                    "Starting additional static analysis defined in {}".format(module.__name__))
                custom_analysis = analysis.perform_analysis(
                    app_path, typ, code_an_dic)
                if custom_analysis != None:
                    custom_analysis_list.append(
                        {'report': custom_analysis, 'template_file': analysis.get_template()})
                    logger.info(custom_analysis_list[-1]['report'])
    return custom_analysis_list                
                
