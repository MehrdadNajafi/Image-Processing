import cv2
import numpy as np

img = np.arange(0, 40000, 1, np.uint8)
img = np.reshape(img, (200, 200))

count = 0

img[:, :] = 255

img[50:150, 40:50] = 0

for i in range(50, 100):
    for j in range(50, 100):
        if -5 < i - j < 5:
            img[i, j] = 0

for i in range(50, 100):
    for j in range(100, 150):
        if 190 < i + j < 200:
            img[i, j] = 0

img[50:150, 150:160] = 0

cv2.imwrite('M.jpg', img)
cv2.imshow('image', img)
cv2.waitKey()