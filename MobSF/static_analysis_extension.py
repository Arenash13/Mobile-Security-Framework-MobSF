from abc import ABC, abstractclassmethod
class StaticAnalysisExtension(ABC):
    '''
    This interface allows you to run custom analysis scripts that will be added to MobSF report
    '''

    @abstractclassmethod
    def perform_analysis(self, app_dir, typ, code_an_dic):
        raise NotImplementedError()

    @abstractclassmethod
    def generate_template(self):
        raise NotImplementedError()