import ModelBuilder
import ModelTrainer

class ModelTest:

    def __init__(self,test,builder,bins_amount):
       self.test=test
       self.trainer=ModelTrainer.ModelTrainer(test, builder, bins_amount)

    def handleData(self):
        self.trainer.fillMissingValues()
        self.trainer.discretization()
        k=5

    def getData(self):
        return self.trainer.getData()