import cv2

img = cv2.imread('4.jpg', 0)
# print(img.shape)

height, width = img.shape
for i in range(height):
    for j in range(width):
        if img[i, j] < 125:
            img[i, j] = 0
            
# cv2.imshow('image', img)
cv2.imwrite('4_wolf.jpg', img)
cv2.waitKey()