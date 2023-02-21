import numpy as np
import cv2 as cv
import main
import copy

arraySudoku = copy.deepcopy(main.sudokuUpgrade)#main class ımdan dönen sudoku matrisini copyalıyorum

sudoku =[
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
	]

a = 60
x = 18
y = 18
#Bos sudokunun her bir kutusunun(1/81) merkezinin koordinatlarını hesaplıyoruz
for i in range(9):
    y = 22 + i*a
    x = 18
    for j in range(9):
        x = 50 + j*a
        c =y,x
        sudoku[i][j] =c
        
    y = 18


img = cv.imread("BosSudokuGuncel.png",0)
cv.imshow("Sudoku",img)
#hesaplanan koordinatlara arraysudokudaki rakamsal değerleri atıyoruz
for i in range(9):
    for j in range(9):
        if arraySudoku[j][i] == 0:
            cv.putText(img," ",sudoku[i][j],cv.FONT_HERSHEY_TRIPLEX,1,(0,0,0))
        else:
            cv.putText(img,str(arraySudoku[j][i]),sudoku[i][j],cv.FONT_HERSHEY_DUPLEX,1.2,(0,0,0))
            
cv.imwrite("Sudoku_bos_dolu1.png",img)#olusturulan sudoku görselini kayıt ediyoruz

cv.imshow("Sudoku",img)#ekrana yansıtıyoruz


cv.waitKey(0)
#SONRADAN DEĞİŞTİRİLECEK KISIM
#img in dosya adını değişkene ata ve değişkeni başka classda kullanarak goruntuyu aç


