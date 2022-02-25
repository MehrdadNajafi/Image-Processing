import argparse
import cv2
import imutils
from imutils.perspective import four_point_transform

parser = argparse.ArgumentParser(description="Mehrdad Sudoku Detector v1.0")
parser.add_argument("--input", type=str, help="Path of input image")
parser.add_argument("--output", type=str, help="Path of output image")
parser.add_argument("--filter-size", type=int, help="Size of GaussianBlur mask", default=7)
args = parser.parse_args()

img = cv2.imread(args.input)
original_img = img.copy()
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img_blurred = cv2.GaussianBlur(gray_img, (args.filter_size, args.filter_size), 3)

thresh = cv2.adaptiveThreshold(img_blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
thresh = 255 - thresh

contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# contours = contours[0]

contours = imutils.grab_contours(contours)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

sudoku_contour = None

for contour in contours:
    
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    if len(approx) == 4:
        sudoku_contour = approx
        break
    
if sudoku_contour is None:
    print("Can't find any Sudoku, Try again")
else:
    result = cv2.drawContours(img, [sudoku_contour], -1, (0, 255, 0), 20)
    warped = four_point_transform(original_img, sudoku_contour.reshape(4, 2))

    cv2.imwrite(args.output, warped)