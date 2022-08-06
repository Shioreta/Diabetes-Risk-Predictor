# FINAL PROJECT: Diabetes Risk Predictor using Naive Bayes Algorithm
# MEMBERS:
#   Bengco, Dana Kirstie
#   Chua, Jericka
#   Tablanza, Krys
# BSCS 4 - 2 
# Polytechnic University of the Philippines

import pandas 
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import tkinter
import customtkinter
from tkinter import *
from tkinter import messagebox
customtkinter.set_appearance_mode("Dark")  
customtkinter.set_default_color_theme("green")  

entry_boxes = []
answer = list()
final_answer = 0
final_accuracy = 0
final_answer_text = ""
choice = 0

class App(customtkinter.CTk):
    WIDTH = 1080
    HEIGHT = 720

    def __init__(self):
        super().__init__()        
        self.title("Diabetes Risk Prediction")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed
        
        container = customtkinter.CTkFrame(self)
        container.pack(expand=True, fill='both')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frames['homescreen'] = HomeScreen(container, self)
        self.frames['page_1'] = MainBayesian(container, self)

        for F in ('homescreen', 'page_1'):        
            self.frames[F].grid(row = 0, column = 0, sticky='nsew')
    
        self.show_frame('homescreen')       
    
    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()
    
    def on_closing(self, event=0):
            self.destroy()

class HomeScreen(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
            
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # ============ frame_info ============
        self.frame_info = customtkinter.CTkFrame(self)
        self.frame_info.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")
        self.frame_info.grid_columnconfigure(0, weight=1)

        self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info,
                                                   text="Diabetes Health Indicators",                                                   
                                                   text_font=("Lithos Pro Regular", 26),
                                                   fg_color=("white", "gray38"),  
                                                   height=150,
                                                   justify=tkinter.CENTER)
        self.label_info_1.grid(column=0, row=0, sticky="nswe", padx=30, pady=30)

        # Label choose file
        self.label_radio_group = customtkinter.CTkLabel(master=self.frame_info,
                                                        text="Please choose a dataset:",
                                                        text_font=("Roboto Medium", 16))
        self.label_radio_group.grid(row=2, column=0, pady=(100,10), sticky="")
                    
        # Dropdown choose a file
        self.choosefile = customtkinter.CTkOptionMenu(master=self.frame_info,
                                                        height = 50, 
                                                        width = 400,
                                                        corner_radius=50,
                                                        values=["Select", "US-Based Dataset", "PH Dataset"],
                                                        text_font=("Roboto Medium", 16),
                                                        command=self.switchDataset)
        self.choosefile.grid(row=3, column=0, padx=20, pady=20, sticky="n")
        self.choosefile.config(width=400)

        self.buttonStart = customtkinter.CTkButton(master=self.frame_info,                                                 
                                                text="START",
                                                text_font=("Roboto Medium", 12),
                                                height = 50, 
                                                width = 400,
                                                corner_radius=50,
                                                command=lambda: controller.show_frame('page_1'))
        self.buttonStart.grid(row=4, column=0, pady=30, padx=20)
       
    # ============ button function ============
    def switchDataset(self, selectedFile):
        global choice
        print(selectedFile)
        if selectedFile == "US-Based Dataset":
            choice = 1      
        elif selectedFile == "PH Dataset":
            choice = 2

class MainBayesian(customtkinter.CTkFrame):
    def __init__(self, parent, controller):
        customtkinter.CTkFrame.__init__(self, parent)
        features = ["High BP", "High Cholesterol", "Cholesterol Check", "BMI", "Smoker", 
                    "Stroke", "Heart Disease or Attack", "Physical Activity","Daily Fruits Intake", "Daily Veggies Intake"]
        features2 = ["Heavy Alcohol Consumption", "Any Healthcare","Cant Afford Doc Checkup", "General Health",
                     "Mental Health", "Physical Health", "Difficulty Walking", "Sex", "Age", "Income"]
 
        self.controller = controller
        self.grid_columnconfigure((0, 1), weight=1) 
        self.grid_rowconfigure(1, weight=6) 

        # ============ frame_main info ============
        self.frame_main = customtkinter.CTkFrame(self)
        self.frame_main.grid(row=0, column=0, pady=(20,0), padx=20, columnspan = 2, sticky="nsew")

        self.labelInput = customtkinter.CTkLabel(master=self.frame_main,
                                                        text="Please input values:",
                                                        text_font=("Roboto Medium", 13))
        self.labelInput.grid(row=1, column=0, padx=20, pady=10, sticky="")
     
        self.frame2 = customtkinter.CTkFrame(self) 
        self.frame2.grid(row=1, column=0, pady=(10, 0), padx=20, columnspan = 2, sticky="nsew")        
        self.frame2.grid_columnconfigure((0,1,2,3), weight=1)    

        # ============ frame2 contents ============
        # Text boxes and labels in loop
        for y in range (10):
            self.label_1 = customtkinter.CTkLabel(master=self.frame2,
                                        text=features[y],
                                        text_font=("Roboto Medium", 13))  
            self.label_1.grid(row=y, column=0, pady=(15,0), padx=0, sticky="")
            
            entry_box = customtkinter.CTkEntry(master=self.frame2)
            entry_box.grid(row=y, column=1, pady=(15,0), padx=20, sticky="nsew")
            entry_boxes.append(entry_box)            
        
        for x in range (10):
            self.label_2 = customtkinter.CTkLabel(master=self.frame2,
                                        text=features2[x],
                                        text_font=("Roboto Medium", 13)) 
            self.label_2.grid(row=x, column=2, pady=(15,0), padx=0, sticky="")
            
            entry_box2 = customtkinter.CTkEntry(master=self.frame2)
            entry_box2.grid(row=x, column=3, pady=(15,0), padx=20, sticky="nsew")
            entry_boxes.append(entry_box2)
        
        # Results
        self.labelResult_1 = customtkinter.CTkLabel(self,
                                                   text="",                                                   
                                                   fg_color=("white", "gray38"),  
                                                   height=80,
                                                   corner_radius=10,
                                                   justify=tkinter.CENTER,
                                                   text_font=("Lithos Pro Regular", 16))
        self.labelResult_1.grid(column=0, row=2, sticky="nswe", padx=20, pady=(20,20)) 

        self.labelResult_2 = customtkinter.CTkLabel(self,
                                                   text="",                                                   
                                                   fg_color=("white", "gray38"),  
                                                   height=80,
                                                   corner_radius=10,
                                                   justify=tkinter.CENTER,
                                                   text_font=("Lithos Pro Regular", 16))
        self.labelResult_2.grid(column=1, row=2,sticky="nswe", padx=20, pady=(20,20)) 

        # Predict button
        self.predict_button = customtkinter.CTkButton(master=self.frame2,
                                               text='PREDICT',
                                               height=40,
                                               corner_radius=20,
                                               text_font=("Roboto Medium", 12),
                                               command=self.button_predict)
        self.predict_button.grid(row=11, column=3,  pady=(30,0), padx=20, sticky="nsew")
  
    def button_predict(self):        
        global answer, result      
        # string
        for ans in entry_boxes:
            answer.append(ans.get())

        # convert string list to int list
        result = [int(item) for item in answer]
        print(result)        
        startbayesian(result)      

        if final_answer == 1:
            final_answer_text = "PREDIABETES"
        elif final_answer == 0:
            final_answer_text = "NO DIABETES"
        elif final_answer == 2:
            final_answer_text = "DIABETES"

        # accuracy in percent and two decimal places
        acc = final_accuracy*100
        res = "{:.2f}".format(acc)
        
        # print final output in bottom textbox
        self.labelResult_1.configure(text="Model Accuracy: " + str(res)+"%")
        self.labelResult_2.configure(text="Final Prediction: "+final_answer_text)
        messagebox.showinfo("Result", final_answer_text)


# ============ start the model ============
def startbayesian(result):       
    global final_accuracy, final_answer
    
    features = ["HighBP", "HighChol", "CholCheck", "BMI", "Smoker", "Stroke", "HeartDiseaseorAttack", 
                "PhysActivity","Fruits", "Veggies", "HvyAlcoholConsump", "AnyHealthcare","NoDocbcCost", 
                "GenHlth","MentHlth" , "PhysHlth", "DiffWalk", "Sex", "Age", "Income"]
    target = "Diabetes_012"

    if choice == 1: # US dataset
        diabetes_risk = pandas.read_csv("US_diabetes_health_indicators.csv")   
    elif choice == 2: # local dataset
        diabetes_risk = pandas.read_csv("LOCAL_diabetes_health_indicators.csv")   

    features_train, features_test, target_train, target_test = train_test_split(diabetes_risk[features],
        diabetes_risk[target], test_size = 0.19, random_state = 40)

    print('\tTraining Features\n ',features_train)  
    print('\tTesting Features\n ',features_test)
    print('\tTraining Target\n ',target_train)
    print('\tTesting Target\n ',target_test)

    model = GaussianNB()
    model.fit(features_train, target_train)

    # After fitting, we will make predictions using the testing dataset
    pred = model.predict(features_test)    
    accuracy = accuracy_score(target_test, pred)

    # Displaying the accuracy of the model
    print("\nModel Accuracy = ",accuracy*100,"%")   
    
    ans = model.predict([result]) 
    final_answer = ans
    final_accuracy = accuracy
    return final_answer, final_accuracy


if __name__ == "__main__":
    app = App()
    app.mainloop()