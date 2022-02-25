import cv2
import numpy as np

img = cv2.imread('building.tif', 0)
rows, cols = img.shape

result_1 = np.zeros((rows, cols))
result_2 = np.zeros((rows, cols))

filter_1 = [[-1, 0, 1]] * 3

filter_2 = [[-1, -1, -1],
            [0, 0, 0],
            [1, 1, 1]]

for i in range(1, rows-1):
    for j in range(1, cols-1):
        small_img = img[i-1:i+2, j-1:j+2]
        result_1[i ,j] = np.sum(small_img * filter_1)
        result_2[i ,j] = np.sum(small_img * filter_2)

cv2.imshow('', result_1)
cv2.waitKey()
cv2.imshow('', result_2)
cv2.waitKey()
cv2.imwrite('result 1.jpg', result_1)
cv2.imwrite('result 2.jpg', result_2)