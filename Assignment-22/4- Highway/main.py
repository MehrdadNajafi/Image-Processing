import cv2
import numpy as np

images = []
for i in range(15):
    img = cv2.imread(f"highway/h{i}.jpg", 0)
    images.append(img)

rows, cols = images[0].shape

result = np.zeros((rows, cols), dtype='uint8')
for i in range(len(images)):
    result += images[i] // len(images)

cv2.imwrite('result.jpg', result)
cv2.imshow('image', result)
cv2.waitKey()