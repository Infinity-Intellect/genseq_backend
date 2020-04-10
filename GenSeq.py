import numpy as np
from PIL import Image
import os

imgWidth = 1430 #define image width
imgHeight = 2230 #define image height

folder = './' 
filename="input.jpg" #define file path
try:
    img = Image.open(os.path.join(folder, filename)).convert('L')
    img = img.resize((imgWidth,imgHeight))
    imgArr=np.asarray(img)
    print(imgArr)
    x=set()
	#for i in range(0,imgHeight):
	#	for j in range(0,imgWidth):
	#		x.add(imgArr[i,j])
#	print(x)
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
					#print(i,j)
				elif(j < colRange2):
					strips[rowCount] = 'C2'
					#print(i,j)
				elif(j < colRange3):
					strips[rowCount] = 'C3'
					#print(i,j)
				else:
					strips[rowCount] = 'C4'
					#print(i,j)
	i+=1
print(strips)