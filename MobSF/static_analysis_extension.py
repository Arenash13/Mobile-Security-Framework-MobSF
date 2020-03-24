from abc import ABC, abstractclassmethod
class StaticAnalysisExtension(ABC):
    """
    This interface allows you to run custom analysis scripts that will be added to MobSF report
    """
    def __init__(self, app_dir, typ, mobsf_analysis):
        self.app_dir = app_dir
        self.typ = typ
        self.mobsf_analysis = mobsf_analysis

    @abstractclassmethod
    def perform_analysis(self):
        raise NotImplementedError()

    def get_template(self):
        raise NotImplementedError("Did you bind a template to your custom extension?")