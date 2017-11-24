import imutils
import cv2
import numpy as np
from panorama import Stitcher
from urllib.request import urlopen
import webbrowser
from PIL import Image, ImageFilter

# Ask the user how many pictures they want to use in the panorama
frames = int(input('How many frames do you want in the panorama (max 5)?'))

pilImage = []
# Download first frame
print('Image 1 downloading...')
with urlopen("http://128.164.158.1/jpg/image.jpg") as conn:
	pilImage.append(Image.open(conn))
	print('Image 1 downloaded!\n')

# Instruct the user to roate, and open website if needed
print('Please pan the camera left by a reasonable amount (10-15deg) on the website')
print('Enter y to open website')
yn = input('Enter n if you already have it open: ')
if yn == 'y' or yn == 'Y':
	webbrowser.open("http://128.164.158.1/view/view.shtml?id=2197&imagepath=%2Fmjpg%2Fvideo.mjpg&size=1", new=2)

# For the rest of the frames, need to repeat the instruction and download
for i in range(frames - 1):

	# Don't print this on the first frame, they were already told
	if i != 0:
		print('Please pan the camera left by a reasonable amount (10-15deg) on the website')
	input('Once you have rotated the camera, hit enter')

	# Download the current frame
	print('Image ' + str(i + 2) + ' downloading...')
	with urlopen("http://128.164.158.1/jpg/image.jpg") as conn:
		pilImage.append(Image.open(conn))
		print('Image ' + str(i + 2) + ' downloaded!\n')

# Convert PIL images to cv2 images
images = []
for i in range(frames):
	npImage = np.array(pilImage[frames - 1 - i])
	images.append(npImage[:,:,::-1].copy())
	images[i] = imutils.resize(images[i], width=960, height=540)

stitcher = Stitcher()

# Stitch from right to left
result = images[frames - 1]
for i in range(frames - 1):
	(result, vis) = stitcher.stitch([images[frames - 2 - i], result], showMatches=True)

cv2.imshow("Result", result)
cv2.waitKey(0)
