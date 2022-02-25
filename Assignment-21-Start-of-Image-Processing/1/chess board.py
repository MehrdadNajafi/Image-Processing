import cv2
import numpy as np

img = np.arange(640000, dtype=np.uint8)
img = img.reshape(800, 800) #Reshapes 1d array in to 2d, containing 800 rows and 800 columns.

c_for_row = 0 #count for rows
c_for_col = 0 #count for columns

for i in range(0, 800, 100):
    for j in range(0, 800, 100):
        if c_for_row % 2 == 0:
            if c_for_col % 2 == 0:
                img[i:i+100, j:j+100] = 255
            else:
                img[i:i+100, j:j+100] = 0
        
        elif c_for_row % 2 != 0:
            if c_for_col % 2 == 0:
                img[i:i+100, j:j+100] = 0
            else:
                img[i:i+100, j:j+100] = 255
        c_for_col += 1
    c_for_row += 1

print(img)
cv2.imshow('chess board', img)
cv2.imwrite('chess board.jpg', img)
cv2.waitKey()