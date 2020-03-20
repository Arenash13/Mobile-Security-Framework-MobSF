from abc import ABC, abstractclassmethod
class StaticAnalysisExtension(ABC):
    """
    This interface allows you to run custom analysis scripts that will be added to MobSF report
    """

    @abstractclassmethod
    def perform_analysis(self, app_dir, typ, mobsf_analysis):
        raise NotImplementedError()

    @abstractclassmethod
    def get_template(self):
        raise NotImplementedError("Did you bind a template to your custom extension?")