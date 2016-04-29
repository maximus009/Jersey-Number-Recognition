from numpy import uint8, hstack, ndarray
import cv2
from skimage import morphology
from skimage import measure
import os

class MSER:
  def __init__(self,im):
    self.image = im
    self.gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    self.mser = cv2.MSER()
    self.regions = self.mser.detect(self.gray)
        
  def get_regions(self):
    return self.regions
        
  def morph_skeleton(self, patch):
    return morphology.skeletonize(patch).astype(uint8)*255
  
  def BG_color(self):
    Q = hstack((self.gray[0:,], self.gray[-1:,], self.gray[:,0].flatten(),
      self.gray[:,-1].flatten()))
    return int(Q[Q==0].shape[0] <= Q[Q==1].shape[0])
  
  def draw_patch_skel1(self,patch):
    (_, patch) = cv2.threshold(patch, 128, 255, cv2.THRESH_OTSU)
    patch[patch == 255] = 1
    if self.BG_color(patch) == 1:
      patch = 1 - patch
    return patch

  def draw_patch_skel(self, patch):
    (_,patch) = cv2.threshold(patch, 128, 255, cv2.THRESH_OTSU)
    patch[patch==255] = 1
    if self.BG_color(patch) == 1:
      patch = 1 - patch
      return self.morph_skeleton(patch)
  
  def get_MSER_bounds(self):
    self.hulls = [cv2.convexHull(p.reshape(-1,1,2)) for p in self.regions]
    return self.hulls

  def _get_filtered_Regions_bounds(self):
    self.f_hulls = [cv2.convexHull(p.coords) for p in
        self.filteredRegions]
    return self.f_hulls


  def draw_MSER_bounds(self):
    image_dummy = self.image.copy()
    cv2.polylines(image_dummy, self.hulls, 1, (255,0,0))
    ##cv2.polylines(image_dummy, self.f_hulls, 1, (0,255,255))
    return image_dummy

  def return_MSER_crops(self):
    #ctr = 0
    for ah in self.hulls:
      R = cv2.boundingRect(ah)
      row_start, col_start = R[1], R[0]
      h, w = R[3], R[2]
      row_end, col_end = row_start+h, col_start+w
      patch = self.gray[row_start:row_end, col_start:col_end]
      im_patch = self.image[row_start:row_end, col_start:col_end]
      yield im_patch
      #cv2.imwrite(str(ctr)+".jpg",im_patch)
      #ctr+=1

  def _filter_regions(self):
    self.connectedComps = morphology.label(self.gray,
        return_num = False)
    mserStats = measure.regionprops(self.connectedComps)
    self.filteredRegions = []
    for region in mserStats:
      if region.eccentricity < 0.995 and region.solidity > 0.3 and 0.2 < region.extent < 0.9 and region.euler_number > -4:
        self.filteredRegions.append(region)
    print len(self.filteredRegions),": Regions filtered"
     
  def _draw_filtered_regions(self):
    for region in self.filteredRegions:
      print region.convex_image

def gather_data(path):
  ctr = 0
  for dirname, dirnames, filenames in os.walk(path):
    for filename in filenames:
      image = cv2.imread(os.path.join(path, filename))
      Obj = MSER(image)
      Obj.get_MSER_bounds()
      
      for patch in Obj.return_MSER_crops():
        cv2.imwrite("../test_patches/"+str(ctr)+".jpg",patch)
        ctr+=1

  return

if __name__ == "__main__":
  #main()
  gather_data('../test_patches/')

