import cv2
import numpy as np

images = [[0 for i in range(5)] for j in range(4)]

for i in range(4):
    for j in range(5):
        images[i][j] = cv2.imread(f"{i+1}/{j+1}.jpg", 0)

without_noise = 0
for i in range(4):
    for j in range(5):
        without_noise += images[i][j] // 5
    cv2.imwrite(f"without noise/{i+1}.jpg", without_noise)
    without_noise = 0

images.clear()
for i in range(1, 5):
    img = cv2.imread(f"without noise/{i}.jpg", 0)
    images.append(img)

result = np.zeros((2000, 2000), dtype='uint8')
count = 0
for i in range(0, 2000, 1000):
    for j in range(0, 2000, 1000):
        result[i:i+1000, j:j+1000] = images[count]
        count += 1

cv2.imwrite('result.jpg', result)
cv2.imshow('image', result)
cv2.waitKey()