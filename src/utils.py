from importlib.resources import path
import os
import random
from matplotlib.image import imread
from PIL import Image
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid
#from src.predictor import *

def open_waste_slot():

    """
        open the machine so that
        a user can enter the machine
    :return:
    """

    send_command_to_machine("open_waste_slot")
    return True


def close_waste_slot():
    """
    close the waste box for user safety
    :return:
    """

    send_command_to_machine("close_waste_slot")
    return True


def process_waste(waste_type):

    """
    move the good slot and shredd the waste
    :return:
    """

    move_container(waste_type)
    was_sucessful = shred_waste()

    return was_sucessful


def move_container(waste_type):

    BOTTLE_BOX = 0
    GLASS_BOX = 1
    command_name = "move_container"

    if waste_type == "bottle":
        send_command_to_machine(command_name, BOTTLE_BOX)
    elif waste_type == "glass":
        send_command_to_machine(command_name, GLASS_BOX)

    return True


def send_command_to_machine(command_name, value=None):

    """
    simulate command sending to rasberry pi
    do nothing to work even if the machine is not connected

    :param command_name:
    :param value:
    :return:
    """
    return True



def shred_waste():

    send_command_to_machine("shred_waste")

    return True


def take_trash_picture():
    """"
        function simulating the picture taking
        inside the machine. 

        Call this function to ask the machine to 
        take picture of the trash

        return : np array of the picture
    """
    send_command_to_machine("take_picture")

    paths = os.listdir('C:/Users/catri/OneDrive/Simplon/IA-P2-Euskadi with my Triof project/Projets/Projet P8 - Triof/triof/camera')
    path = random.choice(paths)
    path_return = path

    return (imread(os.path.join("C:/Users/catri/OneDrive/Simplon/IA-P2-Euskadi with my Triof project/Projets/Projet P8 - Triof/triof/camera", path)),path_return)

    """
    #hardcoded path
    global path
    global img
    path = "C:/Users/catri/OneDrive/Simplon/IA-P2-Euskadi with my Triof project/Projets/Projet P8 - Triof/triof/camera"
    files = os.listdir(path)
    img = random.choice(files)
    return path, img
    """

#updated to other account
ENDPOINT = "https://troifprojectimagerecogmodel-prediction.cognitiveservices.azure.com/"
training_key = "2c6017c538354222bf2a6b5dfa1994f9"
prediction_key = "8dce5921b976481685a08e22f2e875e0"
prediction_resource_id = "/subscriptions/f7757cb3-149c-4e5f-8695-4e01df88e19b/resourceGroups/Simplon/providers/Microsoft.CognitiveServices/accounts/Troifprojectimagerecogmodel-Prediction"
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)
    
#link to project
iteration_name = "Iteration2"
project_id = "a761d3df-e490-4ded-b1eb-042baf905854"

#the first function
def waste_predictor(path, img):

    #prediction
    with open(os.path.join (path, img), "rb") as image_contents:
        results = predictor.classify_image(
            project_id, iteration_name, image_contents.read())

    #print just the first (think usually the highest?)
    print("\t" + results.predictions[0].tag_name +
            ": {0:.2f}%".format(results.predictions[0].probability * 100))

    waste_type = results.predictions[0].tag_name
    
    #read the image
    im = Image.open(os.path.join (path, img))
    #show image
    #im.show()

    return waste_type, im


"""
#show pic
def print_image(path, img):
    #read the image
    im = Image.open(os.path.join (path, img))
    #show image
    im.show()
"""

from PIL import Image
from io import BytesIO
from base64 import b64encode
import numpy as np

picture, path_return = take_trash_picture()
PIL_image = Image.fromarray(np.uint8(picture)).convert('RGB')
data = BytesIO()
PIL_image.save(data, "JPEG")
data64 = b64encode(data.getvalue())
PIL_image = u'data:img/jpeg;base64,'+data64.decode('utf-8') 


#updated prediction function
def waste_predictor2(img):
    path = "C:/Users/catri/OneDrive/Simplon/IA-P2-Euskadi with my Triof project/Projets/Projet P8 - Triof/triof/camera"
    #prediction
    with open(os.path.join (path, img), "rb") as image_contents:
        results = predictor.classify_image(
            project_id, iteration_name, image_contents.read())

    #print just the first (think usually the highest?)
    result = "\t" + results.predictions[0].tag_name
    prob =  ": {0:.2f}%".format(results.predictions[0].probability * 100)

    return result, prob

#take_trash_picture()
#waste_predictor2(path_return)

#updated classification model function
from keras.models import load_model
from keras.preprocessing import image

def clean_or_dirty(img):
    #load the saved model
    classifier = load_model("C:/Users/catri/OneDrive/Simplon/IA-P2-Euskadi with my Triof project/Projets/Projet P8 - Triof/triof/clean or dirty classifier")
    path = "C:/Users/catri/OneDrive/Simplon/IA-P2-Euskadi with my Triof project/Projets/Projet P8 - Triof/triof/camera"
    #prediction
    image_address = os.path.join (path, img)
    img = image.load_img(image_address,target_size=(64,64))
    img = np.asarray(img)
    img = np.expand_dims(img, axis=0)

    #making prediction
    output = classifier.predict(img)

    #returning prediction
    res = ""
    if output <= 0.5:
        res = 'Item is clean'
    else:
        res = 'Item is dirty'
    return res

#testing
take_trash_picture()
clean_or_dirty(path_return)

