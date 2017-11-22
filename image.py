from PIL import Image, ImageFilter
from urllib.request import urlopen

# Multiply the difference by this value to increase contrast of the result image
contrast = int(input('Enter contrast of the difference (probably 2 - 5?): '))
n = int(input('Enter how many frames do you want this to run for: '))

for z in range(n):
	# Download the image
	with urlopen("http://128.164.158.1/jpg/image.jpg") as conn:
		img1 = Image.open(conn)
		px1 = img1.load()

	# Download the next frame
	with urlopen("http://128.164.158.1/jpg/image.jpg") as conn:
		img2 = Image.open(conn)
		px2 = img2.load()

	# w and h should be the same from both images
	w = img1.width
	h = img1.height

	px3 = [[[]for y in range(h)] for z in range(w)]
	img3 = Image.new('RGB', (w, h))


	for i in range(w):
		for j in range(h):
			for k in range(3):
				# Add the difference * contrast on to the output pixels 
				px3[i][j].append((px1[i, j][k] - px2[i, j][k]) * contrast)

				# If it was negative, change it to 0
				if px3[i][j][k] < 0:
					px3[i][j].pop(k)
					px3[i][j].append(0)

	for i in range(w):
		for j in range(h):
			img3.putpixel((i, j), tuple(px3[i][j]))

	img3.show()
