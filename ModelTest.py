import ModelBuilder
import ModelTrainer

class ModelTest:

    def __init__(self,test='',builder='',bins='_amount='):
        self.test = ''
        self.builder = ''
        self.trainer = ''
        self.build=''

    def setdata(self,test,builder,bins_amount):
        self.test = test
        self.builder = builder
        self.trainer = ModelTrainer.ModelTrainer(test, builder, bins_amount)
        self.trainer.readFile()

    def cleanData(self):
        self.trainer.fillMissingValues()
        self.trainer.discretization()


    def getData(self):
        return self.trainer.getData()