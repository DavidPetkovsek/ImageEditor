import sys, os
import cv2
import numpy as np
from pathlib import Path
from filedialogs import save_file_dialog, open_file_dialog, open_folder_dialog
# import matplotlib.pyplot as plt
# import skimage
# from skimage.morphology import disk, binary_dilation
# from skimage.restoration import inpaint
# from skimage.util import img_as_float as toSkImage
# from skimage.util import img_as_ubyte as toCV2

if len(sys.argv) != 2:
    print('Invalid input, please provide the path to an image as the first argument!')
    sys.exit(1)
imagePath = Path(sys.argv[1])
if not imagePath.exists():
    print(f'File {sys.argv[1]} does not exist')
    sys.exit(1)
image = cv2.imread(sys.argv[1])

points = [(0,0),(0,image.shape[0]),(image.shape[1],0),(image.shape[1],image.shape[0])]
selected = 0
moving = False

def newDims():
    global points
    p = np.array(points, dtype=np.float32)
    shapeW = max(int(np.linalg.norm(p[0]-p[1])),int(np.linalg.norm(p[2]-p[3])))
    shapeH = max(int(np.linalg.norm(p[0]-p[2])),int(np.linalg.norm(p[1]-p[3])))
    return (shapeH,shapeW)

def drawHandles(color, thickness, pointSize):
    global points, image
    cv2.line(image, points[0], points[1], color, thickness)
    cv2.line(image, points[0], points[2], color, thickness)
    cv2.line(image, points[1], points[3], color, thickness)
    cv2.line(image, points[2], points[3], color, thickness)
    for p in points:
        cv2.circle(image, p, pointSize, color, -1) # -1 to fill circle

clone = image.copy()
drawHandles((0,255,0),4,10)
roi = clone.copy()

def updateRoi():
    global points, clone, roi
    dims = newDims()
    endPoints = [(0,0),(0,dims[1]),(dims[0],0),(dims[0],dims[1])]
    homog, mask = cv2.findHomography(np.array(points,dtype=np.float32), np.array(endPoints,dtype=np.float32), cv2.RANSAC)
    roi = cv2.warpPerspective(clone, homog, dims)
    # mask = np.ones(clone.shape[:2], dtype=np.uint8)
    # mask = cv2.warpPerspective(mask, homog, (mask.shape[1],mask.shape[0]))
    # mask = ~mask.astype(bool)
    # # print(mask.shape)
    # # print(roi.shape)
    # if np.any(mask):
    #     # if np.sum(mask) > 300:
    #         # plt.imshow(mask, cmap=plt.cm.gray)
    #     msk = skimage.exposure.rescale_intensity(mask, in_range='image', out_range=(0,1))
    #     painted = skimage.restoration.inpaint_biharmonic(toSkImage(roi[:, :, ::-1]).copy(), mask, channel_axis=-1)
    #     plt.imshow(mask)
    #     plt.show()
    #     plt.imshow(painted)
    #     plt.show()
    #         # painted = inpaint.inpaint_biharmonic(toSkImage(roi[:, :, ::-1]), mask, multichannel=True)
    #         # painted = skimage.restoration.inpaint_biharmonic(toSkImage(roi[:, :, ::-1]), mask, multichannel=True)
    #         # roi = cv2.inpaint(roi,~(mask*255),3,cv2.INPAINT_TELEA)
    #         # plt.imshow(painted)
    #         # plt.show()

    # roi = inpaint.inpaint_biharmonic(roi, mask, channel_axis=-1)

def mouseCallback(event, x, y, flags, param):
    # grab references to the global variables
    global points, moving, clone, image, selected
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    x = max(min(x,clone.shape[1]), 0)
    y = max(min(y,clone.shape[0]), 0)
    mc = np.array([x,y],dtype=np.float32)
    if event == cv2.EVENT_LBUTTONDOWN:
        for i in range(len(points)):
            p = np.array(points[i],dtype=np.float32)
            if np.linalg.norm(mc-p) < 14:
                selected = i
                moving = True
                break
    elif event == cv2.EVENT_LBUTTONUP:
        moving = False
    elif moving:
        points[selected] = (x,y)
        image = clone.copy()
        updateRoi()
        drawHandles((0,255,0),4,10)

cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("image", mouseCallback)
space = np.ones((image.shape[0],10,3),dtype=np.uint8)*255

def fit(img, height):
    scale = float(height)/float(img.shape[0])
    newImage = cv2.resize(img, (int(img.shape[1]*scale),height))
    # newImage = cv2.copyMakeBorder(newImage, 0, 0, 0, , borderType)
    return newImage

# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    cv2.imshow("image", np.hstack((image,space,fit(roi,image.shape[0]))))
    key = cv2.waitKey(1) & 0xFF
    # if the 'c' key is pressed, break from the loop
    if key == ord("s"):
        save_path = save_file_dialog(title="save meme", directory=str(imagePath.parent), ext=[('Image png',('png','PNG')), ('Image jpg',('jpg','JPG'))])
        if save_path:
            cv2.imwrite(save_path, roi)
            print("Saved as '"+save_path+"'")
            break
        print("Save cancelled")
    elif key == ord('p'):
        print(points)
    elif key == ord('q'):
        print("Exiting without saving")
        break