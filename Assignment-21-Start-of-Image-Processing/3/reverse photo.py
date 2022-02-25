import cv2

img = cv2.imread('3.jpg')
height, width, channel = img.shape

# img2 = cv2.rotate(img, cv2.ROTATE_180)

img[:, :] = img[height::-1, width::-1]
show_img = cv2.resize(img, (width // 2, height// 2))

cv2.imshow('Reverse', show_img)
cv2.imwrite('3_Reverse.jpg', img)
cv2.waitKey()