from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid

#updated to other account
ENDPOINT = "https://troifprojectimagerecogmodel-prediction.cognitiveservices.azure.com/"
training_key = "2c6017c538354222bf2a6b5dfa1994f9"
prediction_key = "8dce5921b976481685a08e22f2e875e0"
prediction_resource_id = "/subscriptions/f7757cb3-149c-4e5f-8695-4e01df88e19b/resourceGroups/Simplon/providers/Microsoft.CognitiveServices/accounts/Troifprojectimagerecogmodel-Prediction"

#credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
#trainer = CustomVisionTrainingClient(ENDPOINT, credentials)
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(ENDPOINT, prediction_credentials)

#link to project
iteration_name = "Iteration2"
#project = "CatTriofproject"
#project = trainer.create_project(project_name)
project_id = "a761d3df-e490-4ded-b1eb-042baf905854"
base_image_location = "/Users/catri/OneDrive/Simplon/IA-P2-Euskadi with my Triof project/Projets/Projet P8 - Triof/triof"

"""
#test the predictor
with open(os.path.join (base_image_location, "Test/test.jfif"), "rb") as image_contents:
    results = predictor.classify_image(
        project_id, iteration_name, image_contents.read())

    # Display all the results.
    for prediction in results.predictions:
        print("\t" + prediction.tag_name +
             ": {0:.2f}%".format(prediction.probability * 100))
    
    #print just the first (think usually the highest?)
    print("\t" + results.predictions[0].tag_name +
            ": {0:.2f}%".format(results.predictions[0].probability * 100))
    

    # incase first isn't highest - this checks
    for prediction in results.predictions:
        if (results.predictions[0].probability > results.predictions[1].probability) or (results.predictions[0].probability > results.predictions[2].probability):
            resultat = results.predictions[0].tag_name
        elif results.predictions[1].probability > results.predictions[0].probability or (results.predictions[1].probability > results.predictions[2].probability):
            resultat = results.predictions[1].tag_name
        else:
            resultat = results.predictions[2].tag_name
        
    print(resultat)

"""

#function 
def waste_predictor(path, img):
    #path = 'camera' #need full address for photo?
    with open(os.path.join (path, img), "rb") as image_contents:
        results = predictor.classify_image(project_id, iteration_name, image_contents.read())

    #print just the first (think usually the highest?)
    print("\t" + results.predictions[0].tag_name +
            ": {0:.2f}%".format(results.predictions[0].probability * 100))

    waste_type = results.predictions[0].tag_name
    return waste_type

#test run of function
path = "/Users/catri/OneDrive/Simplon/IA-P2-Euskadi with my Triof project/Projets/Projet P8 - Triof/triof"
img = "Test/test.jfif"
waste_predictor(path, img)



