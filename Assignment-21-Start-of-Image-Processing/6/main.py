import cv2
import numpy as np

img = np.arange(0, 65025, 1, np.uint8)
img = np.reshape(img, (255, 255))

for i in range(255):
    img[i, :] = 255 - i

print(img)
cv2.imshow('image', img)
cv2.imwrite('6.jpg', img)
cv2.waitKey()