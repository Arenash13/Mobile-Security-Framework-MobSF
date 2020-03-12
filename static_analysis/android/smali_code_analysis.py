import os
import logging
import re
import io
from . import utils
from .rules.smali_rules import CODE_RULES
from MobSF.static_analysis_extension import StaticAnalysisExtension
from django.conf import settings
from django.template import Template

logger = logging.getLogger(__name__)


class SmaliCodeAnalysis(StaticAnalysisExtension):

    def rule_matcher(self, findings_list, source_code):
        return 0

    def perform_analysis(self, app_dir, typ, code_an_dic):
        pass
        try:
            logger.info("start verifying smali regex")
            smali_rules = CODE_RULES
            smali_src = utils.retrieve_source_code_folder(app_dir, typ, "smali")
            for dir_, sub_dir, files in os.walk(smali_src):
                for smali_file in files:
                    smali_file_path = os.path.join(smali_src, dir_, smali_file)
                    smali_file_path = utils.resolve_file_name_conflict(
                        app_dir, dir_, smali_file)
                    path = dir_.replace(smali_src, '') + os.path.sep
                    if (
                        smali_file.endswith('.smali')
                        and any(re.search(cls, path)
                                for cls in settings.SKIP_CLASSES) is False
                    ):
                        data = ''
                        with io.open(smali_file_path, mode='r', encoding='utf8',
                                     errors='ignore') as file_ptr:
                            data = file_ptr.read()
                            self.rule_matcher(code_an_dic['findings'], data)

        except Exception:
            logger.Exception("Performing smali code analysis")

    def get_template(self):
        pass
        # template = Template("<title>hello</title>")
        # vals = vars(template)
        # logger.info(", ".join("%s: %s" % item for item in vals.items()))
        # return template
