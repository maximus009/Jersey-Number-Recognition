from skimage import measure
from skimage import morphology
import cv2, numpy as np
image = cv2.imread('../test_images/o_y16.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
mserObject = cv2.MSER()
mserRegions = mserObject.detect(gray)
connectedComp, numOfComps = morphology.label(gray, return_num = True)
print connectedComp, numOfComps
mserStats = measure.regionprops(connectedComp)
print len(mserStats)
filtered = []

# NEED to speed it up
for region in mserStats:
    if region.eccentricity < 0.995 and region.solidity > 0.7 and region.euler_number > -4 and region.extent > 0.75:
        x1,y1,x2,y2 = region.bbox
        cv2.rectangle(image, (int(y1),int(x1)),(int(y2),int(x2)),255)
        filtered.append(region)
cv2.imwrite('../test_patches/out_text.jpg',image)
print len(filtered)
