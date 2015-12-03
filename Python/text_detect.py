import cv2
img = cv2.imread('ynk.jpg');
mser = cv2.MSER()
regions = mser.detect(img)

class MSER:
    def __init__(self,im):
        self.image = im
        self.gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        self.mser = cv2.MSER()
        self.regions = mser.detect(self.gray)
        
    def get_regions(self):
        return self.regions
    
    def filter_text(self):
        pass
m = MSER(img)
m.filter_text()
