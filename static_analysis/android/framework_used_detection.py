from MobSF.static_analysis_extension import StaticAnalysisExtension
from .rules.framework_rules import FRAMEWORK_RULES
from django.template import loader
import logging
from django.conf import settings
from . import utils
import os
import re
import io

logger = logging.getLogger(__name__)


def framework_matcher(data, rules):
    for rule in rules:
        if rule['type'] == 'regex':
            if rule['match'] == 'single_regex':
                if re.findall(rule['regex1'], str(data)):
                    return rule
    return None


class FrameworkUsedDetection(StaticAnalysisExtension):
    """
    This class is used to detect which Framework has been used to develop the app 
    (Xamarin, Cordova, Flutter,...). It will also detect some frequently used library (okhttp,...)
    """

    def perform_analysis(self, app_dir, typ, code_an_dic):
        try:
            logger.info("start Framework used regex")
            framework_rules = FRAMEWORK_RULES
            java_src = utils.retrieve_source_code_folder(app_dir, typ, "java")
            for dir_, sub_dir, files in os.walk(java_src):
                for java_file in files:
                    java_file_path = os.path.join(java_src, dir_, java_file)
                    java_file_path = utils.resolve_file_name_conflict(
                        app_dir, dir_, java_file)
                    path = dir_.replace(java_src, '') + os.path.sep
                    logger.info(java_file_path)
                    data = utils.retrieve_raw_content_from_file(
                        java_file, java_file_path, path, ".java", utils.get_expanded_Mobsf_skipped_classes())
                    framework = framework_matcher(data, framework_rules)
                    # If it founded the framework, it's useless to analyse the other
                    # files
                    if framework != None:
                        return framework
            return {'desc': 'Native android'}

        except Exception as e:
            logger.exception("Performing framework analysis")
            logger.exception("reason : {}".format(str(e)))

    def get_template(self):
        return "framework_used.html"
    
    def get_title(self):
        return "Framework Analysis"
