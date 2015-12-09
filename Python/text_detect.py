import cv2
from numpy import uint8, hstack, ndarray
from skimage.measure import regionprops
from skimage.morphology import skeletonize
import skimage
#from skimage.measure import label
print skimage.__version__
import skimage.measure.label as label

class MSER:
  def __init__(self,im):
    self.image = im
    self.gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    self.mser = cv2.MSER()
    self.regions = mser.detect(self.gray)
        
  def get_regions(self):
    return self.regions
        
  def morph_skeleton(patch):
    return skeletonize(patch).astype(uint8)*255
  
  def BG_color():
    Q = hstack((self.gray[0:,], self.gray[-1:,], self.gray[:,0].flatten(),
      self.gray[:,-1].flatten()))
    return int(Q[Q==0].shape[0] <= Q[Q==1].shape[0])
  
  def draw_patch_skel1(patch):
    (_, patch) = cv2.threshold(patch, 128, 255, cv2.THRESH_OTSU)
    patch[patch == 255] = 1
    if self.BG_color(patch) == 1:
      patch = 1 - patch
    return patch

  def draw_patch_skel(patch):
    (_,patch) = cv2.threshold(patch, 128, 255, cv2.THRESH_OTSU)
    patch[patch==255] = 1
    if self.BG_color(patch) == 1:
      patch = 1 - patch
      return self.morph_skeleton(patch)
  
  def get_MSER_bounds():
    self.hulls = [cv2.convexHull(p.reshape(-1,1,2)) for p in self.regions]
    return self.hulls

  def draw_MSER_bounds():
    image_dummy = self.image.copy()
    cv2.polylines(image_dummy, self.hulls, 1, (255,0,0))
    return image_dummy

  def refine_MSER():
    h_prime = []
    for ah in self.hulls:
      R = cv2.boundingRectangle(ah)
      reg_h, reg_w = float(R[3]), float(R[2])
      a_r = reg_w/reg_h
      if 1.2 < a_r < 0.25:
        h_prime.append(ah)
    
    h_pprime = []
    for ah in h_prime:
      R = cv2.boundingRectangle(ah)
      row_start, col_start = R[1], R[0]
      h, w = R[3], R[2]
      row_end, col_end = row_start+h, col_start+w
      patch = self.gray[row_start:row_end, col_start:col_end]
      skeleton = draw_patch_skel(patch)
      if skeleton[skeleton==255].shape[0]>10 and label(skeleton).max()<5:
        h_pprime.append(ah)
    return h_pprime  
if __name__ == "__main__":
  img = cv2.imread('../test_images/o_y10.jpg');
  Obj = MSER(img)
  Obj.get_MSER_bounds()
  Obj.refine_MSER()
  out = Obj.draw_MSER_bounds()
  cv2.imwrite('../test_patches/out.jpg',out)
 
