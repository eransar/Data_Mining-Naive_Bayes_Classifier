from __future__ import division
import pandas as pd
import os
class ModelClassifier:

    def __init__(self,path,train,test='',builder='',bins=''):
        self.path=path
        self.train=train
        self.test=test
        self.builder=builder
        self.bins=bins
        self.resultdictionary=dict()
        self.output=[]


    def buildNaiveDictionary(self):
        traindata=pd.DataFrame(self.train)
        self.yes_count = pd.DataFrame(traindata[traindata['class']=='Y']).count()[0]
        self.no_count = pd.DataFrame(traindata[traindata['class'] == 'N']).count()[0]
        _m=2


        for column in traindata:
            column_values=traindata[column].unique()
            for value in column_values:
                try:
                    value_and_no=pd.DataFrame(traindata[traindata['class'] == 'N'][traindata[column] == value])[column].count()
                    value_and_yes = pd.DataFrame(traindata[traindata['class'] == 'Y'][traindata[column] == value])[column].count()
                except:
                    pass
                value_probability=(1.0/len(column_values)*1.0)
                m_estimate_yes=((1.0*value_and_yes+value_probability*_m)/(self.yes_count+_m))
                m_estimate_no = ((1.0 * value_and_no + value_probability * _m) / (self.no_count + _m))
                self.resultdictionary[(column,value,'Y')]=m_estimate_yes
                self.resultdictionary[(column, value, 'N')] = m_estimate_no

    def classify(self):
        testdata=pd.DataFrame(self.test)
        features=[names for names in self.builder.getModel()['Name']]
        for (idx, row) in testdata.iterrows():
            no_probabilities=[(1.0*self.no_count)/(self.no_count+self.yes_count)]
            yes_probabilities=[(1.0*self.yes_count)/(self.no_count+self.yes_count)]
            for feature in features:
                if feature!='class':
                        yes_conditional_prob=self.resultdictionary.get((feature,row[feature],'Y'))
                        if yes_conditional_prob!=None:
                            yes_probabilities.append(self.resultdictionary.get((feature, row[feature], 'Y')))
                        no_conditional_prob = self.resultdictionary.get((feature, row[feature], 'N'))
                        if no_conditional_prob != None:
                            no_probabilities.append(self.resultdictionary.get((feature, row[feature], 'N')))
                            k=5
            naive_yes = reduce(lambda x, y: x * y, yes_probabilities)
            naive_no = reduce(lambda x, y: x * y, no_probabilities)
            if naive_yes>naive_no:
                self.output.append("{} {}".format(idx+1,"yes"))
            else:
                self.output.append("{} {}".format(idx+1, "no"))


    def writeOutput(self):
        file_path=os.path.join(self.path,'output.txt')
        with open(file_path, 'w') as f:
            for item in self.output:
                f.write("%s\n" % item)


    def getdictionary(self):
        return self.resultdictionary


