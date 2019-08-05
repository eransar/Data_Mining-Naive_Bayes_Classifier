import os
import tkMessageBox
import ModelBuilder
import ModelTrainer
from Tkinter import Tk, Label, Button, Entry,StringVar
from tkFileDialog import askdirectory



class GUI:

    def __init__(self, master):
        self.master = master
        master.title("Bayesian Classifier")
        #set up vars for gui logic
        self.browse_text = StringVar()
        self.val_bins = master.register(self.validate_bins)
        self.isBin=False
        self.isBrowse=False
        self.isTest=''
        self.isBrowse=''
        self.isTrain=''
        #buttons
        self.button_browse=Button(master, text='Browse', command=lambda: self.DisplayDir())
        self.button_build = Button(master, text="Build", command=lambda: self.build())
        self.button_classify = Button(master, text="Classify", command=lambda: self.classify())
        #labels
        self.label_directory_path = Label(master, text="Directory Path")
        self.label_bins = Label(master, text="Discretization Bins")
        self.label_error = Label(master, text="" , fg='red')
        #entries
        self.entry_browse = Entry(master,width=50)
        self.entry_bins = Entry(master,width=50,validatecommand=(self.val_bins, "%P", "%d") , validate='key')
        # LAYOUT
        self.button_browse.grid(row=1, column=4)
        self.entry_browse.grid(row=1, column=2,columnspan=2)
        self.label_directory_path.grid(row=1,column=1)

        self.label_bins.grid(row=2,column=1)
        self.entry_bins.grid(row=2,column=2)

        self.button_build.grid(row=3, column=1)
        self.button_classify.grid(row=3, column=2)
        self.label_error.grid(row=4,column=2)
        self.master.minsize(width=700, height=200)
        #control buttons

        self.button_build['state'] = 'disabled'
        self.button_classify['state'] = 'disabled'

        # #Logic
        # self.ModelBuilder # build the model
        # self.ModelClassifier #classification

    def validate_bins(self,v,d):
        try:
            value = int(v)
            if value >1:
                    if self.isBrowse:
                        self.button_build['state'] = 'normal'
                        self.button_classify['state'] = 'normal'
                    return True
            else:
                self.isBin=False
                tkMessageBox.showinfo("Alert Message", "Invalid number")
                return False
        except:
            if d == '0' and v=='':
                self.entry_bins.delete(1, 'end')
                if len(self.entry_bins.get())==1:
                    self.button_build['state'] = 'disabled'
                    self.button_classify['state'] = 'disabled'
                    self.isBin = False
                return True
            tkMessageBox.showinfo("Alert Message", "Invalid number")
            return False



    def build(self):
        self.label_error.config(text="Begin building")
        self.ModelBuilder = ModelBuilder.ModelBuilder(self.isStructure)
        self.ModelTrainer = ModelTrainer.ModelTrainer(self.isTrain,self.ModelBuilder,self.entry_bins.get())
        maxbins=self.ModelTrainer.getMaxbins()
        if maxbins < int(self.entry_bins.get()):
            tkMessageBox.showinfo("Alert Message", "Invalid number of bins")
        else:
            self.ModelTrainer.fillMissingValues()
            self.ModelTrainer.discretization()


    def classify(self):
        print("5")

    def DisplayDir(self):
        feedback = askdirectory()
        self.browse_text.set(feedback)
        self.entry_browse.config(state='normal')
        self.entry_browse.delete(0, 'end')
        self.entry_browse.insert(0, self.browse_text.get())
        self.entry_browse.config(state='readonly')
        self.isTest = os.path.join(self.browse_text.get(),"test.csv")
        self.isTrain = os.path.join(self.browse_text.get(),"train.csv")
        self.isStructure = os.path.join(self.browse_text.get(),"Structure.txt")

        self.texterror="";
        if(
                    os.path.exists(self.isTest)
                and os.path.exists(self.isTrain)
                and os.path.exists(self.isStructure)
        ):
            if self.isBin:
                self.button_build['state'] = 'normal'
                self.button_classify['state'] = 'normal'
                self.label_error.config(text='folder content is valid !')

            else :
                self.texterror = "please fill bin text field"
                self.isBrowse=True

        else:
            if(
                    not os.path.exists(self.isTrain)
                    # and not os.path.exists(self.isStructure)
                    and not os.path.exists(self.isTest)
            ):
                self.texterror = "train.csv , structure.txt and test.csv were not found"

            elif (not os.path.exists(self.isTrain)):
                self.texterror = "train.csv was not found"
            elif (not os.path.exists(self.isStructure)):
                self.texterror = "Structure.txt was not found"
            elif (not os.path.exists(self.isTest)):
                self.texterror = "test.csv was not found"
            self.isBrowse=False

        self.label_error.config(text=self.texterror)


root = Tk()
my_gui = GUI(root)
root.mainloop()
