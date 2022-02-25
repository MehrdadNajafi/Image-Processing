import cv2
import numpy as np

img1 = cv2.imread("my photo.jpg", 0)
img2 = cv2.imread('joel.jpg', 0)

height, width = img1.shape
img2 = cv2.resize(img2, (width, height))

result_img1 = img1//2 + img2//4
result_img2 = img1//4 + img2//2

final_result = np.zeros((height, width * 4), dtype='uint8')

final_result[:, :width] = img1
final_result[:, width:width*2] = result_img1
final_result[:, width*2:width*3] = result_img2
final_result[:, width*3:width*4] = img2

cv2.imwrite('result.jpg', final_result)