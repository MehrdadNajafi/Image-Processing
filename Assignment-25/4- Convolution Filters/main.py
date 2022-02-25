import cv2
import numpy as np

def convolution(img, size):
    size = str(size).split('*')
    size = int(size[0])
    if size%2 == 0:
        return 'Wrong size, Please enter a odd size! ( example: 3*3, 5*5, 7*7, ... )'

    rows, cols = img.shape
    result = np.zeros((rows, cols), 'uint8')

    mask = np.ones((size, size)) / size**2

    selected_range = size // 2
    for i in range(selected_range, rows-selected_range):
        for j in range(selected_range, cols-selected_range):
            small_img = img[i-selected_range:i+selected_range+1, j-selected_range:j+selected_range+1]
            result[i, j] = np.sum(small_img * mask)
    
    return result

img = cv2.imread('Rick.jpg', 0)
user_choice = input('Please enter the size of mask ( example: 3*3, 5*5, 7*7, ... ): ')
print('Please wait ...')
result = convolution(img, user_choice)
try:
    cv2.imwrite('result.jpg', result)
    print('Done !')
except:
    print(result)

# without function
# rows, cols = img.shape
# result_1 = np.zeros((rows, cols))
# result_2 = np.zeros((rows, cols))
# result_3 = np.zeros((rows, cols))
# result_4 = np.zeros((rows, cols))

# mask_1 = np.ones((3, 3)) / 9
# mask_2 = np.ones((5, 5)) / 25
# mask_3 = np.ones((7, 7)) / 49
# mask_4 = np.ones((15, 15)) / 225

# for i in range(1, rows-1):
#     for j in range(1, cols-1):
#         small_img = img[i-1:i+2, j-1:j+2]
#         result_1[i, j] = np.sum( small_img * mask_1 )

# for i in range(2, rows-2):
#     for j in range(2, cols-2):
#         small_img = img[i-2:i+3, j-2:j+3]
#         result_2[i, j] = np.sum( small_img * mask_2 )

# for i in range(3, rows-3):
#     for j in range(3, cols-3):
#         small_img = img[i-3:i+4, j-3:j+4]
#         result_3[i, j] = np.sum( small_img * mask_3 )

# for i in range(7, rows-7):
#     for j in range(7, cols-7):
#         small_img = img[i-7:i+8, j-7:j+8]
#         result_4[i, j] = np.sum( small_img * mask_4 )

# cv2.imwrite('result 1.jpg', result_1)
# cv2.imwrite('result 2.jpg', result_2)
# cv2.imwrite('result 3.jpg', result_3)
# cv2.imwrite('result 4.jpg', result_4)