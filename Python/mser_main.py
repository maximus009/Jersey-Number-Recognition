from cv2 import *
from numpy import ndarray, uint8, hstack

def morphSkeleton(im):
	''' Morphological Skeleton '''
	from skimage.morphology import skeletonize
	skel = skeletonize(im).astype(uint8)*255
	return skel
	
def BGcolor(img):
	Q = hstack((img[0,:], img[-1,:], img[:,0].flatten(), img[:,-1].flatten()))
	if Q[Q==0].shape[0] > Q[Q==1].shape[0]:
		return 0
	else:
		return 1
def drawpatchskel1(patch):
	# detect the background color and invert
	# if BG=1
	(_, patch) = threshold(patch, 128, 255, THRESH_OTSU)
	patch[patch==255] = 1
	if BGcolor(patch)==1:
		patch = 1 - patch
      return patch
def drawpatchskel(patch):
	# detect the background color and invert
	# if BG=1
	(_, patch) = threshold(patch, 128, 255, THRESH_OTSU)
	patch[patch==255] = 1
	if BGcolor(patch)==1:
		patch = 1 - patch
	sk = morphSkeleton(patch)
	return sk

def getMSERbounds(img):
	'''
	Get MSER bounded boxes
	'''
	mser = MSER() # tweak MSER parameters and run this code
	assert type(img) is ndarray
	
	#im_shape = img.shape[2]
	
	#if im_shape==3:
	#	img = cvtColor(img, COLOR_BGR2GRAY)
	
	# imshow('w', img); waitKey(0)
	regions = mser.detect(img, None)
	hulls = [convexHull(p.reshape(-1, 1, 2)) for p in regions]
	
	return hulls

def drawMSERbounds(img, hul):
	
	viz = img.copy()
	polylines(viz, hul, 1, (0,255,0))
	return viz

def refineMSER(h, i):
	""" refine the MSER bounds """
	# sh is the shape
	from skimage.measure import label
	h_prime = []
	# for the aspect ratio refining
	for ah in h:
		R = boundingRect(ah)
		reg_h, reg_w = R[3], R[2]
		a_r = float(reg_w)/float(reg_h)
		if a_r<1.2 and a_r>0.25:
			h_prime.append(ah)
	# skeleton refining
	h_pprime = []
	for ah in h_prime:
		R = boundingRect(ah)
		row_start, col_start = R[1], R[0]
		hei, wid = R[3], R[2]
		row_end = row_start + hei
		col_end = col_start + wid
		patch = i[row_start:row_end, col_start:col_end]
		p_skel = drawpatchskel(patch)
		if p_skel[p_skel==255].shape[0]>10 and label(p_skel).max()<5:
			h_pprime.append(ah)
	
	return h_pprime
def refineMSER1(h, i):
	""" refine the MSER bounds """
	# sh is the shape
	from skimage.measure import label
	h_prime = []
	# for the aspect ratio refining
	for ah in h:
		R = boundingRect(ah)
		reg_h, reg_w = R[3], R[2]
		a_r = float(reg_w)/float(reg_h)
		if a_r<1.2 and a_r>0.25:
			h_prime.append(ah)
	# skeleton refining
	h_pprime = []
	for ah in h_prime:
		R = boundingRect(ah)
		row_start, col_start = R[1], R[0]
		hei, wid = R[3], R[2]
		row_end = row_start + hei
		col_end = col_start + wid
		patch = i[row_start:row_end, col_start:col_end]
		p_skel = dp(patch)
		
	
	return p_skel	
def main():
	""" MAIN """
	
	# folder to the SVT dataset images
	folder = 'C:\\Users\\Prithviraj Dhar\\Downloads\\Jersey Numbers-New\\Jersey Numbers-New\Bhavana\\Original'
	
	# an output folder
	tgt = 'C:\\Users\\Prithviraj Dhar\\Desktop\\z1\\'
	patchesfold = 'C:\\Users\\Prithviraj Dhar\\Desktop\\z2\\'
	for I in range(19): #0->18
		for J in range(20): #0->19
                   
			fname = str(I).zfill(2)+'_'+str(J).zfill(2)+'.jpg'
			img = imread(folder+fname, CV_LOAD_IMAGE_GRAYSCALE)
			if img is None:
				continue
			h = getMSERbounds(img)
			h = refineMSER(h, img)
			img = drawMSERbounds(img, h)
			imwrite(tgt+fname, img)
			
			''' #export all patches to file
			_, ps = refineMSER(h, img)
			drawpatchesofMSER_main(ps, patchesfold, str(I).zfill(2)+'_'+str(J).zfill(2))
			'''
			#imwrite(tgt+str(I).zfill(2)+'_'+str(J).zfill(2)+'_.jpg', img)
			print fname

if __name__=='__main__':
	main()
