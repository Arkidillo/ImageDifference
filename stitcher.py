import imutils
import cv2
from panorama import Stitcher

imageA = cv2.imread("image-1.jpg")
imageB = cv2.imread("image0.jpg")
imageC = cv2.imread("image1.jpg")
imageD = cv2.imread("image2.jpg")

imageA = imutils.resize(imageA, width=960)
imageB = imutils.resize(imageB, width=960)
imageC = imutils.resize(imageC, width=960)
imageD = imutils.resize(imageD, width=960)

stitcher = Stitcher()

# Combine A and B
(imageAB, vis) = stitcher.stitch([imageA, imageB], showMatches=True)
#imageAB = imutils.resize(imageAB, width=960)

# Combine C and D
(imageCD, vis) = stitcher.stitch([imageC, imageD], showMatches=True)
#imageCD = imutils.resize(imageCD, width=960)

# Combine the 2 results:
(result, vis) = stitcher.stitch([imageAB, imageCD], showMatches=True)

cv2.imshow("Image AB", imageAB)
cv2.imshow("Image CD", imageCD)
cv2.imshow("Result", result)
cv2.waitKey(0)