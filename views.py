from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from paitent.models import paitentmodel
from django.views.decorators.http import require_GET
import random

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

import nltk
nltk.download('punkt')

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# import googlemaps # pip install -U googlemaps
# gmaps = googlemaps.Client(key='YOUR_API_KEY')
# gmaps = []

# Create your views here.
def paitent(request):
    return render(request, "paitent.html")

def userregisterAction(request):
    if request.method == 'POST':
        name = request.POST.get('uname')
        email = request.POST.get('uemail')
        password = request.POST.get('upassword')
        phoneno = request.POST.get('uphone')
        print(name, email, password, phoneno)
        form1 = paitentmodel(name=name, email=email, password=password, phoneno=phoneno, status='waiting')
        form1.save()
        return render(request, "paitent.html")
    else:
        return render(request, "paitent.html")
    
def userloginaction(request):
    if request.method == 'POST':
        sname = request.POST.get('email')
        spasswd = request.POST.get('password')
        print(sname, spasswd)
        try:
            check = paitentmodel.objects.get(email=sname, password=spasswd)
            status = check.status
            if status == 'activated':
                context = {'username': check.name}
                return render(request, "user/Userhome.html", context)
            else:
                messages.error(request, 'Login Unsuccessful')
                return render(request, "paitent.html")
        except:
            messages.error(request, 'Login Unsuccessful')
            return render(request, "paitent.html")
    else:
        messages.error(request, 'Login Unsuccessful')
        return render(request, "paitent.html")
    
def userhome(request):
    return render(request, "user/userhome.html")

def userlogout(request):
    return render(request, "paitent.html")

def connectchatbot(request):
    return render(request, "user/chatbot.html")

def get_bot_response(request):
    message = request.GET.get('msg')
    response = ""
    
    # Greeting and goodbye responses
    greeting_responses = ["Hello!, enter the symptom" , "Hi there!, enter the symptom", "Greetings!, enter the symptom"]
    goodbye_responses = ["Goodbye!", "See you later!", "Take care!"]

    hospital_remedy_map = {
        "headache"  : "",
    }

    # Symptom-remedy mapping
    symptom_remedy_map = {
    "headache"  : "Drink plenty of water and get some rest.",
    "fever"     : "Take acetaminophen and drink fluids to stay hydrated.",
    "cough"     : "Try over-the-counter cough syrup and warm liquids.",
    "drugreaction":"stop irritation	consult nearest hospital	stop taking drug	follow up",
    "malaria"   : "Consult nearest hospital	avoid oily food	avoid non veg food	keep mosquitos out",
    "allergy"   :"apply calamine	cover area with bandage		use ice to compress itching",
    "hypothyroidism":"reduce stress	exercise	eat healthy	get proper sleep",
    "psoriasis"	:"wash hands with warm soapy water	stop bleeding using pressure	consult doctor	salt baths",
    "gERD"      :"avoid fatty spicy food	avoid lying down after eating	maintain healthy weight	exercise",
    "chroniccholestasis":"	cold baths	anti itch medicine	consult doctor	eat healthy",
    "hepatitis" :"A	Consult nearest hospital	wash hands through	avoid fatty spicy food	medication",
    "osteoarthristis":"	acetaminophen	consult nearest hospital	follow up	salt baths",
    "paroymsalpositionalvertigo "  :"	lie down	avoid sudden change in body	avoid abrupt head movment	relax",
    "hypoglycemia":	"lie down on side	check in pulse	drink sugary drinks	consult doctor",
    "acne"	    :"bath twice	avoid fatty spicy food	drink plenty of water	avoid too many products",
    "diabetes"  :"	have balanced diet	exercise	consult doctor	follow up",
    "impetigo"	:"soak affected area in warm water	use antibiotics	remove scabs with wet compressed cloth	consult doctor",
    "hypertension" :	"meditation	salt baths	reduce stress	get proper sleep",
    "pepticulcerdiseae":	"avoid fatty spicy food	consume probiotic food	eliminate milk	limit alcohol",
    "dimorphichemmorhoids"	:"avoid fatty spicy food	consume witch hazel	warm bath with epsom salt	consume alovera juice",
    "commoncold":	"drink vitamin c rich drinks	take vapour	avoid cold food	keep fever in check",
    "chickenpox":"	use neem in bathing 	consume neem leaves	take vaccine	avoid public places",
    "cervicalspondylosis"	:"use heating pad or cold pack	exercise	take otc pain reliver	consult doctor",    
    "hyperthyroidism"	:"eat healthy	massage	use lemon balm	take radioactive iodine treatment",
    "urinarytractinfection":"	drink plenty of water	increase vitamin c intake	drink cranberry juice	take probiotics",
    "varicoseveins":"	lie down flat and raise the leg high	use oinments	use vein compression	dont stand still for long",
    "aids"      :"	avoid open cuts	wear ppe if possible	consult doctor	follow up",
    "paralysis ":	"massage	eat healthy	exercise	consult doctor",
    "typhoid"	:"eat high calorie vegitables	antiboitic therapy	consult doctor	medication",
    "hepatitis" :	"consult nearest hospital	vaccination	eat healthy	medication",
    "fungalinfection":	"bath twice	use detol or neem in bathing water	keep infected area dry	use clean cloths",
    "hepatitisc" :	"Consult nearest hospital	vaccination	eat healthy	medication",
    "migraine"  :	"meditation	reduce stress	use poloroid glasses in sun	consult doctor",
    "bronchialasthma":	"switch to loose cloothing	take deep breaths	get away from trigger	seek help",
    "alcoholichepatitis":	"stop alcohol consumption	consult doctor	medication	follow up",
    "jaundice"  :	"drink plenty of water	consume milk thistle	eat fruits and high fiberous food	medication",
    "hepatitise" :	"stop alcohol consumption	rest	consult doctor	medication",
    "dengue"	:"drink papaya leaf juice	avoid fatty spicy food	keep mosquitos away	keep hydrated",
    "hepatitisd":	"consult doctor	medication	eat healthy	follow up",
    "heartattack":	"chew or swallow asprin	keep calm	",
    "pneumonia"	:"consult doctor	medication	rest	follow up",
    "arthritis"	:"exercise	use hot and cold therapy	try acupuncture	massage",
    "gastroenteritis":"	stop eating solid food for while	try taking small sips of water	rest	ease back into eating",
    "tuberculosis":	"	cover mouth	consult doctor	medication	rest",
    # Add more symptoms and remedies as needed

    }

    hospital_remedy_map = {

    "hyderabad": "https://www.google.com/search?sca_esv=c7d05ac6ad01166f&tbs=lf:1,lf_ui:2&tbm=lcl&sxsrf=ACQVn08vRIMOLDfN5joSfZYbnZMdhlxOzg:1708140976828&q=best+hospitals+in+hyderabad&rflfq=1&num=10&sa=X&ved=2ahUKEwi3o5mBubGEAxV2SWwGHQDaBbQQjGp6BAgcEAE&biw=1536&bih=742&dpr=1.25#rlfi=hd:;si:;mv:[[17.4516185,78.5505848],[17.363694499999998,78.3275073]];tbs:lrf:!1m5!1u2!3m2!2m1!2e8!4e2!1m4!1u3!2m2!3m1!1e1!1m4!1u2!2m2!2m1!1e1!2m1!1e2!2m1!1e3!3sCg8SDXJhdGluZ19maWx0ZXIgAQ,lf:1,lf_ui:2",

    # Add more remedies and links as needed
}
    

    if message:
        # Tokenize the message
        tokens = nltk.word_tokenize(message.lower())

        if "hello" in tokens:
            response = random.choice(greeting_responses)
        elif "goodbye" in tokens:
            response = random.choice(goodbye_responses)
        else:
            symptom_list = [token for token in tokens if token in symptom_remedy_map]

            if symptom_list:
                remedy_list = [f"For {symptom} : {symptom_remedy_map[symptom]}, Enter state name to prefer Best hospitals" for symptom in symptom_list]
                response = remedy_list
            else:
                # Check if the token is present in hospital_remedy_map
                for token in tokens:
                    if token in hospital_remedy_map:
                        remedy = hospital_remedy_map[token]
                        hyperlink = f'<a href="{remedy}" target="_blank">Click here for more information</a>'
                        response = f"For {token}, you can try: {hyperlink}"
                        break
                else:
                    response = "Please consult a doctor for a proper diagnosis."
    else:
        response = random.choice(greeting_responses)

    return JsonResponse({'response': response})

        # elif "hospital" in tokens:
        #     nearest_hospital = [] #  find_nearest_hospital()  # Assuming find_nearest_hospital() is defined elsewhere
        #     if nearest_hospital:
        #         response = f"The nearest hospital is {nearest_hospital}."
        #     else:
        #         response = "Sorry, I couldn't find any hospitals nearby."

# def find_nearest_hospital():
#     # Use Google Maps Places API to find the nearest hospital
#     try:
#         # Perform a nearby search for hospitals around a specific location (e.g., your city)
#         places = gmaps.places_nearby(location='YOUR_LOCATION', radius=5000, type='hospital')
        
#         if places['results']:
#             nearest_hospital = places['results'][0]['name']
#             return nearest_hospital
#         else:
#             return None
#     except Exception as e:
#         print("Error occurred while finding nearest hospital:", e)
#         return None

def userdisease(request):
    return render(request, 'user/userdisease.html')

def userdiseasepredictionaction(request):
    if request.method == 'POST':
        joint_pain = request.POST.get('joint_pain')
        muscle_pain = request.POST.get('muscle_pain')
        loss_of_appetite = request.POST.get('loss_of_appetite')
        fatigue = request.POST.get('fatigue')
        itching = request.POST.get('itching')
        chest_pain = request.POST.get('chest_pain')
        weight_loss = request.POST.get('weight_loss')
        dark_urine = request.POST.get('dark_urine')
        nausea = request.POST.get('nausea')
        altered_sensorium = request.POST.get('altered_sensorium')
        print(joint_pain, muscle_pain, loss_of_appetite, fatigue, itching, chest_pain, weight_loss, dark_urine, nausea, altered_sensorium)
        df = pd.read_csv(os.path.join(BASE_DIR, 'media/Training.csv'))
        df.drop('Unnamed: 133', axis=1, inplace=True)
        df.isnull().sum()
        X = df[['muscle_pain','joint_pain','loss_of_appetite','fatigue', 'itching', 'chest_pain', 'weight_loss', 'dark_urine', 'nausea', 'altered_sensorium']]
        y = df['prognosis']
        X
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)
        model = SVC(kernel='linear', C=1.0, random_state=42)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print("Accuracy:", accuracy)
        custom_data = [[muscle_pain, joint_pain, loss_of_appetite, fatigue, itching, chest_pain, weight_loss, dark_urine, nausea, altered_sensorium]]
        custom_data_scaled = scaler.transform(custom_data)
        custom_predictions = model.predict(custom_data_scaled)
        print("Custom predictions:", custom_predictions)
        messages.success(request, f"Your Prediction: {custom_predictions}")
        return render(request, 'user/userdisease.html')
    else:
        return render(request, 'user/userdisease.html')