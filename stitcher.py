import imutils
import cv2
from panorama import Stitcher

imageA = cv2.imread("image1.jpg")
imageB = cv2.imread("image2.jpg")

imageA = imutils.resize(imageA, width=960)
imageB = imutils.resize(imageB, width=960)

stitcher = Stitcher()
(result, vis) = stitcher.stitch([imageA, imageB], showMatches=True)

cv2.imshow("Image A", imageA)
cv2.imshow("Image B", imageB)
cv2.imshow("Result", result)
cv2.waitKey(0)