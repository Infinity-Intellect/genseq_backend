import numpy as np
from PIL import Image
from flask import Flask,request,jsonify
from flask_cors import CORS, cross_origin
import json
app=Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#convert json keys from character to integer
def convertJSON_keys_to_integer(x):
    return {int(k): v for k, v in x.items()}

@app.route("/")
def main():
    return "This is GenSeq !"

@app.route("/getSequence",methods=['POST'])
def calculateSequence():
    
    #defining constants
    imgWidth = 1430 #define image width
    imgHeight = 2230 #define image height   
    basePairings={'C':'G','G':'C','T':'A','A':'T'}
    
    #Loading data from request parameter
        #key is 'image' change depeding on the request    
    image=request.files.get('image','')
        #order of the base as per input image        
    bases=json.loads(request.form["columnOrder"], object_hook=convertJSON_keys_to_integer)
    
    #Declare the resultant sequence
    resultSequence=""
    
    try:
        img=Image.open(image).convert('L')
        img=img.resize((imgWidth,imgHeight))
        imgArr=np.asarray(img)
        #print(imgArr)
    except Exception as e:
    	print(e)
    
    #column Segmentation
    colRange1=imgWidth//4
    colRange2=imgWidth//4 + 1 * (imgWidth//4)
    colRange3=imgWidth//4 + 2 * (imgWidth//4)
    threshold = 180 #define treshold for seperation
    skipFactor = 1 # define thickness of the line
    rowCount = 0
    strips = {}
    stripFlag = False
    stripInit = 0
    stripEnd = 0
    i=0
    while i<imgHeight:
        for j in range(0,imgWidth):
            pixelVal = imgArr[i,j]
            if(pixelVal > threshold):
                if(stripFlag):
                    stripEnd = j
                else:
                    stripInit = j
                    stripFlag = True
            else:
                if(stripFlag):
                    stripFlag = False
                    rowCount+=1
                    j = (stripInit + stripEnd)//2
    				#print("Strip",stripInit,stripEnd)
                    pixelVal = imgArr[i,j]
                    while(pixelVal > threshold):
                        i += skipFactor
                        pixelVal = imgArr[i,j]
    					#print("True",i)
                    if(j < colRange1):
                        strips[rowCount] = 'C1'
                        resultSequence+=basePairings[bases[0]]
    					#print(i,j)
                    elif(j < colRange2):
                        strips[rowCount] = 'C2'
                        resultSequence+=basePairings[bases[1]]
    					#print(i,j)
                    elif(j < colRange3):
                        strips[rowCount] = 'C3'
                        resultSequence+=basePairings[bases[2]]
    					#print(i,j)
                    else:
                        strips[rowCount] = 'C4'
                        resultSequence+=basePairings[bases[3]]
    					#print(i,j)
        i+=1
    #print(strips)  
    print(resultSequence)
    responseData={"message":"okay","sequence":resultSequence}
    response=app.response_class(response=json.dumps(responseData),status=200,mimetype='application/json')
    return response

if(__name__ == "__main__"):
    app.run()