import cv2
img = cv2.imread('1.jpg', 0)
img_2 = cv2.imread('2.jpg', 0)

invert = 255 - img[:, :]
invert_2 = 255 - img_2[:, :]

#invert = cv2.bitwise_not(img)
#invert_2 = cv2.bitwise_not(img_2)

cv2.imwrite('1_invert.jpg', invert)
cv2.imwrite('2_invert.jpg', invert_2)
cv2.waitKey()