import imutils
import cv2
import numpy as np
from panorama import Stitcher
from urllib.request import urlopen
import webbrowser
from PIL import Image, ImageFilter

frames = int(input('How many frames do you want in the panorama (max 5)?'))

pilImage = []
print('Image 1 downloading...')
with urlopen("http://128.164.158.1/jpg/image.jpg") as conn:
	pilImage.append(Image.open(conn))
	print('Image 1 downloaded!\n')

print('Please rotate the camera by a reasonable amount (~15deg) on the website')
print('Enter y to open website')
yn = input('Enter n if you already have it open: ')
if yn == 'y' or yn == 'Y':
	webbrowser.open("http://128.164.158.1/view/view.shtml?id=2197&imagepath=%2Fmjpg%2Fvideo.mjpg&size=1", new=2)

for i in range(frames - 1):

	print('Please rotate the camera by a reasonable amount (~15deg) on the website')
	input('Once you have rotated the camera, hit enter')

	print('Image ' + str(i + 2) + ' downloading...')
	with urlopen("http://128.164.158.1/jpg/image.jpg") as conn:
		pilImage.append(Image.open(conn))
		print('Image ' + str(i + 2) + ' downloaded!\n')

images = []
for i in range(frames):
	npImage = np.array(pilImage[frames - 1 - i])
	images.append(npImage[:,:,::-1].copy())
	images[i] = imutils.resize(images[i], width=960, height=540)

stitcher = Stitcher()

result = images[frames - 1]
for i in range(frames - 1):
	(result, vis) = stitcher.stitch([images[frames - 2 - i], result], showMatches=True)

#cv2.imshow("Image A", imageA)
#cv2.imshow("Image B", imageB)
#cv2.imshow("Image BC", imageBC)
#cv2.imshow("Image C", imageC)
cv2.imshow("Result", result)
cv2.waitKey(0)
