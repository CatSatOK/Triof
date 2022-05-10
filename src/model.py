from keras.models import load_model
from keras.preprocessing import image
import os
import numpy as np


#load the saved model
classifier = load_model("C:/Users/catri/OneDrive/Simplon/IA-P2-Euskadi with my Triof project/Projets/Projet P8 - Triof/triof/clean or dirty classifier")

#classification function
def clean_or_dirty(img):
    #path = "C:/Users/catri/OneDrive/Simplon/IA-P2-Euskadi with my Triof project/Projets/Projet P8 - Triof/triof/camera"
    #prediction
    #with open(os.path.join (path, img), "rb") as image:
        img = image.load_img(img,target_size=(64,64))
        img = np.asarray(img)
        img = np.expand_dims(img, axis=0)

        #making prediction
        output = classifier.predict(img)

        #returning prediction
        if output <= 0.5:
            print('Item is clean')
        else:
            print('Item is dirty')

#test
img = "C:/Users/catri/OneDrive/Simplon/IA-P2-Euskadi with my Triof project/Projets/Projet P8 - Triof/triof/camera/couverts-plastique-noirs.jpg"
clean_or_dirty(img)

