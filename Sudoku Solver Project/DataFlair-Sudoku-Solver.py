# DataFlair Sudoku solver

import cv2
import numpy as np
from tensorflow.keras.models import load_model
import imutils
from solver import *

classes = np.arange(0, 10)

model = load_model('model-OCR.h5')
#model = load_model('enYeniEgitilmisModel.h5')
# print(model.summary())
input_size = 48


def get_perspective(img, location, height = 900, width = 900):
    """Takes an image and location os interested region.
        And return the only the selected region with a perspective transformation"""
    pts1 = np.float32([location[0], location[3], location[1], location[2]])
    print("location ı aldı")
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)#pts1 koordinatlarını pts2 koordinatlarına çevirir
    result = cv2.warpPerspective(img, matrix, (width, height))# yeni görsel açıga çıkar
    return result

def get_InvPerspective(img, masked_num, location, height = 900, width = 900):
    """Takes original image as input"""
    pts1 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    pts2 = np.float32([location[0], location[3], location[1], location[2]])

    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(masked_num, matrix, (img.shape[1], img.shape[0]))
    return result





def find_board(img):
    """Takes an image as input and finds a sudoku board inside of the image"""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 13, 20, 20)
    edged = cv2.Canny(bfilter, 30, 180)
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)#görseli copyaladık çünkü girilen görsel orjinal haline geri dönemez.
    contours  = imutils.grab_contours(keypoints)#48. satırda bug almıştım yeni versiyonda imutils.grab_contours eklemem gerekiyordu. Konturları yakalamamızı sağlar

    newimg = cv2.drawContours(img.copy(), contours, -1, (0, 255, 0), 3)#2. arguman konturların listesi 3. arguman konturların indeksi
    # cv2.imshow("Contour", newimg)


    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]
    location = None
    
    
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 15, True)#koordinat bilgisi verir
        if len(approx) == 4:#dörtgen olduğunu belirtiyor
            location = approx
            break
    result = get_perspective(img, location)
    return result, location


# split the board into 81 individual images
def split_boxes(board):
    """Takes a sudoku board and split it into 81 cells. 
        each cell contains an element of that board either given or an empty cell."""
    rows = np.vsplit(board,9)
    boxes = []
    for r in rows:
        cols = np.hsplit(r,9)
        for box in cols:
            box = cv2.resize(box, (input_size, input_size))/255.0
            # cv2.imshow("Splitted block", box)
            # cv2.waitKey(50)
            boxes.append(box)
    cv2.destroyAllWindows()
    return boxes

def displayNumbers(img, numbers, color=(0, 255, 0)):
    """Displays 81 numbers in an image or mask at the same position of each cell of the board"""
    W = int(img.shape[1]/9)
    H = int(img.shape[0]/9)
    for i in range (9):
        for j in range (9):
            if numbers[(j*9)+i] !=0:
                cv2.putText(img, str(numbers[(j*9)+i]), (i*W+int(W/2)-int((W/4)), int((j+0.7)*H)), cv2.FONT_HERSHEY_COMPLEX, 2, color, 2, cv2.LINE_AA)
    return img

# Read image
#img = cv2.imread('sudoku1.jpg')
img = cv2.imread("Sudoku_bos_dolu.png")

# extract board from input image
board, location = find_board(img)


gray = cv2.cvtColor(board, cv2.COLOR_BGR2GRAY)
# print(gray.shape)
rois = split_boxes(gray)
rois = np.array(rois).reshape(-1, input_size, input_size, 1)

# get prediction
prediction = model.predict(rois)
# print(prediction)

predicted_numbers = []
# get classes from prediction
for i in prediction: 
    index = (np.argmax(i)) # returns the index of the maximum number of the array
    predicted_number = classes[index]
    predicted_numbers.append(predicted_number)

# print(predicted_numbers)

# reshape the list 
board_num = np.array(predicted_numbers).astype('uint8').reshape(9, 9)


solved_board_nums = get_board(board_num)


binArr = np.where(np.array(predicted_numbers)>0, 0, 1)#boş blokları 0 dolu blokları 1 yapıyoruz
print(binArr)
# get only solved numbers for the solved board
flat_solved_board_nums = solved_board_nums.flatten()*binArr#matrisi düzleştiriyoruz ve sonradan çözülmüş olan sayıları yazıp, diğer kısımlara 0 veriyoruz 

# create a mask
mask = np.zeros_like(board)
# displays solved numbers in the mask in the same position where board numbers are empty
solved_board_mask = displayNumbers(mask, flat_solved_board_nums)
#cv2.imshow("Solved Mask", solved_board_mask)
inv = get_InvPerspective(img, solved_board_mask, location)
# cv2.imshow("Inverse Perspective", inv)
combined = cv2.addWeighted(img, 0.7, inv, 1, 0)#ilk görüntü ile 2. görüntüyü karıştırıyoruz(ilk görsel 0.7 oranında 2. görsel 1 oranında karısacak)
cv2.imshow("Final result", combined)
# cv2.waitKey(0)
# solve the board


cv2.imshow("Input image", img)
# cv2.imshow("Board", board)
cv2.waitKey(0)
cv2.destroyAllWindows()