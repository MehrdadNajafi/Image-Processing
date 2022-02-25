import cv2

img1 = cv2.imread('a.tif', 0)
img2 = cv2.imread('b.tif', 0)

img1 = 255 - img1
img2 = 255 - img2

result = cv2.subtract(img1, img2)

cv2.imwrite('result.jpg', result)
cv2.imshow('image', result)
cv2.waitKey()