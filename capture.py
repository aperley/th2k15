import cv2

cam = cv2.VideoCapture(0)
cv2.namedWindow('image')

while True:
	ret, im = cam.read()
	cv2.imshow('image', im)
	cv2.imwrite('test3.png', im)
	if cv2.waitKey(1) >= 0:
		cam.release()
		cv2.destroyAllWindows()
		break
