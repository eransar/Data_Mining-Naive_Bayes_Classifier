import pandas as pd


class ModelBuilder:

    def __init__(self,path):
        self.features = pd.read_csv(path, sep=' ', names=["Attribute", "Name", "Values"])
    def getModel(self):
        return self.features[["Attribute","Name","Values"]]


