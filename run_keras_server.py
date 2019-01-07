
import keras
from keras.models import load_model
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image
import numpy as np
import flask
import io
import zipfile
import os
import shutil

########################
# Initialise Flask application, declare global var
########################
app = flask.Flask(__name__)
model = None
classes = ['aircon vent',
 'bolting',
 'cctv',
 'ceilings',
 'door',
 'electric socket',
 'fire alarm',
 'gutter',
 'pipe',
 'railing',
 'window']
classDict = {}
for i in enumerate(classes):
    classDict[i[0]]=i[1]

########################
# Load the trained model from 'trainModel.py'
########################
def loadModel():
    global model
    model = load_model('weights.05-0.83-0.76.h5')
    
########################
# Preprocess image
########################
def getImg(img, imgSize=224):
    #if the image mode is not RGB, convert it
    if img.mode != "RGB":
        img = img.convert("RGB")

    #preprocess image
    image = img.resize((imgSize, imgSize))
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)

    return image
    
    
def getXlsxImg(xlsxFile):
    #xlsxFile = '/Users/tengtinghuan/CNN/nucon/sample_issue_report.xlsx'
    namelist = zipfile.ZipFile(xlsxFile).namelist()
    ImageFiles = [F for F in namelist if F.count('.jpg')]

    for Image in ImageFiles:
        imgPath = zipfile.ZipFile(xlsxFile).extract(Image, path = 'temporary_folder')
        print('IMG PATH',imgPath)
        img = Image.open(imgPath)
        #shutil.rmtree('temporary_folder')
        
    return img
    
    
########################
# Define predict() function to generate API response
########################
@app.route("/predict", methods=["POST"])
def predict():
   
    #initialize the data dictionary
    data = {"success": False}
    
    #ensure image is properly uploaded 
    if flask.request.method == "POST":
        #data["POST"]=True
        
        if flask.request.files.get("image"):
            #data["IMAGE"]=True
            
            #read the image in PIL format
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))
            
            #preprocess the image and prepare it for classification
            image = getImg(image)
            
            #run image through the model to obtain label and probability
            preds = model.predict(image)[0] #give probabilities
            predClass = model.predict_classes(image)[0] #gives index
            prob = preds[predClass]
            label = classDict[predClass]
            data["predictions"] = []
            
            #add predictions to dictionary
            r = {"label": label, "probability": float(prob)}
            data["predictions"].append(r)
            
            data["success"] = True
            
    return flask.jsonify(data)


    
'''    
@app.route("/predictXlsx", methods=["POST"])
def predictXlsx():
   
    #initialize the data dictionary
    data = {"success": False}
    
    if flask.request.method == "POST":
        data["POST"]=True
        
        if flask.request.files.get("xlsxFile"):
            data["XLSX"]=True
            
            xlsxFile = flask.request.files["xlsxFile"]#.read()
            image = getXlsxImg(xlsxFile)
            
            #preprocess the image and prepare it for classification
            image = getImg(image)
            
            #run image through the model to obtain label and probability
            preds = model.predict(image)[0] #give probabilities
            predClass = model.predict_classes(image)[0] #gives index
            prob = preds[predClass]
            label = classDict[predClass]
            data["predictions"] = []
            
            #add predictions to dictionary
            r = {"label": label, "probability": float(prob)}
            data["predictions"].append(r)
            
            data["success"] = True
            
    return flask.jsonify(data)

'''

if __name__ == "__main__":
	print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
	loadModel()
	app.run()