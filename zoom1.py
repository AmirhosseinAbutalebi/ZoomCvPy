#!/bin/python3

import argparse
import cv2

'''
This variable for location of mouse in picture and use it as global
'''
locX = 0
locY = 0

'''
This dic use for size picture if input is wrong
'''
DEFAULT = {
    "x" : 400,
    "y" : 600,
}

'''
This def change str to num and if wrong set default
'''
def arg_to_num(size, x_or_y):
    true = True
    while true:
        if size.isnumeric():
            size = int(size)
            true = False
        else:
            size = DEFAULT[x_or_y]
            true = False

    return size

'''
This def for use mouse and set x,y location mouse
'''
def clickAndZoom(event, x, y, flags, param):
	global locX,locY
	if event == cv2.EVENT_LBUTTONUP:
		locX = x
		locY = y

'''
get argument in terminal and set width and height and get size
'''
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-y", "--height", required=True, help="Please Enter a number for height")
ap.add_argument("-x", "--width", required=True, help="Please Enter a number for width")
args = vars(ap.parse_args())

'''
use input argument
'''
image = cv2.imread(args["image"])
sizeX = arg_to_num(args["height"], "x")
sizeY = arg_to_num(args["width"], "y")

image = cv2.resize(image, (sizeY, sizeX))#resize image by new size
clone = image.copy()
cv2.namedWindow("image")
cv2.setMouseCallback("image", clickAndZoom)#use def mouse

'''
This while help locX,locY zoom in picture
'''
while True:
	key = cv2.waitKey(1) & 0xFF
	cv2.imshow("image", image)
	'''
	if press e to exit
	'''
	if key == ord("e"):
		break

	'''
	if press r to reload original picture
	'''
	if key == ord("r"):
		image = clone.copy()
		cv2.imshow("image", image)
		continue

	elif locX > 0:#for click in picture and zoom
		(sizeXn, sizeYn) = (image.shape[0], image.shape[1])
		if locX >= sizeXn/2 and locY >= sizeYn/2:
			image = image[sizeXn//15:sizeXn, sizeYn//15:sizeYn]

		elif locX > sizeXn/2 and locY < sizeYn/2:
			image = image[ :14*sizeXn//15, sizeYn//15:sizeYn]

		elif locX < sizeXn/2 and locY > sizeYn/2:
			image = image[sizeXn//15:sizeXn, :14*sizeYn//15]

		elif locX < sizeXn/2 and locY < sizeYn/2:
			image = image[ :14*sizeXn//15, :14*sizeYn//15]

		locX=0
		image = cv2.resize(image, (sizeY, sizeX))

cv2.destroyAllWindows()