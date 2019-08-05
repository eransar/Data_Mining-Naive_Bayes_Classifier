import pandas as pd
from scipy.stats import mode
import numpy as np
class ModelTrainer:


    def __init__(self,path, modelbuilder, bins_amount):
        self.trainer = pd.read_csv(path, sep=",")
        self.modelbuilder = modelbuilder.getModel()
        self.bins_amount = bins_amount

    def getMaxbins(self):
        return len(self.trainer.index)-1

    def fillMissingValues(self):
        #fill missing values by comparing to the structure model from the ModelBuilder



        # modelbuilder_df=pd.DataFrame(self.modelbuilder.getModel()[['Name','Values']])
        for feature in self.trainer:
            if self.isNUMERIC(feature):
                self.trainer[feature].fillna((self.trainer[feature].mean()), inplace=True)
            else:
                self.trainer[feature].fillna(mode(self.trainer[feature]).mode[0], inplace=True)

        # len(self.modelbuilder.loc[0]['Values'].split(',')) >2:
    def discretization(self):
        for feature in self.trainer:
            if self.isNUMERIC(feature):
                minval=self.trainer[feature].min()
                maxval=self.trainer[feature].max()
                bins=int(self.bins_amount)
                equalwidth=((maxval-minval)/bins)
                cut_points = list(np.arange(minval + equalwidth, maxval - 0.1, equalwidth))
                labels=range(len(cut_points) + 1)
                self.trainer[feature]=self.binning(feature,cut_points,minval,maxval,labels)

    def isNUMERIC(self,feature_name):
        return self.modelbuilder.loc[self.modelbuilder['Name'] == feature_name]['Values'].values == 'NUMERIC'

    def binning(self,col, cut_points,minval,maxval, labels=None,):


        break_points = [minval] + cut_points + [maxval]

        if not labels:
            labels = range(len(cut_points) + 1)

        colBin = pd.cut(self.trainer[col], bins=break_points, labels=labels, include_lowest=True)
        return colBin
