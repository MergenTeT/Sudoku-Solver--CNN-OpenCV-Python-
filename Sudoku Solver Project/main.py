import random
import copy
import numpy as np

"""sudoku =[
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
	]"""
sudoku = np.zeros((9, 9), dtype="int")
M = 9
counters = []



def control_row(i,sudoku,selNumber):#satır control
    for j in range(0,9):
        if sudoku[i][j] == selNumber:
            return False
    return True

def control_col(j,sudoku,selNumber):#sutun control
    for i in range(0,9):
        if sudoku[i][j] == selNumber:
            return False
    return True

def control_cell(i,j,sudoku,selNumber):# burası hücre kontrolu
    x1,x2,y1,y2 = for_control_cell(i, j)
    #print("girdi x1 ==> {} , x2 ==> {} , y1 ==> {} , y2 ==> {}".format(x1,x2,y1,y2))
    for k in range(x1,x2+1):
        for l in range(y1,y2+1):
            if sudoku[k][l] == selNumber :
                return False
    return True



def for_control_cell(i,j):
      # cell control for için sınır degerleri tespit edilir
    
    if i<3 : 
        x1,x2 = 0,2
        
    elif i<6 and i>=3 :
        x1,x2 = 3,5
    elif i<9 and i>=6 :
        x1,x2 = 6,8
    
    if j<3 : 
        y1,y2 = 0,2
    elif j<6 and j>=3 :
        y1,y2 = 3,5
    elif j<9 and j>=6 :
        y1,y2 = 6,8 
    
    return x1,x2,y1,y2

#kosulların sorgulanıp rakam ataması yapılacak kısım
def generate_number(i,j,sudoku):
    numbers = [1,2,3,4,5,6,7,8,9]
    
    
    while True :
        
        if len(numbers) == 0 :
            counters.append(1)#123. satırda debug işlemi için kullanılan değişken
            numbers = [1,2,3,4,5,6,7,8,9]
            for a in range(9) :
                sudoku[i][a] = 0#geriye yayılım algoritması
                sudoku[i-1][a] = 0
            j = 0 
            i=i-1
            #problem 
        indisSec = random.randrange(len(numbers))#numbersLİst uzunlugunda tahmin
        selNumber = numbers[indisSec]#sectiğimiz sayı
        numbers.remove(selNumber)#secilen sayıyı numbers dan siliyoruz
        
        if control_cell(i, j, sudoku, selNumber) and control_col(j, sudoku, selNumber) and control_row(i, sudoku, selNumber) :
            print("onaylanan sayi {}".format(selNumber))#onaylanan sayıyı consol ekranında görüyorum
            
                
            return i,j,selNumber
            break
        print("{}. satırdaki {}. sutunda onaylanmayan rakam{}".format(i,j,selNumber))
        print(numbers)
        
#İLk çağrılan sınıff        
def generater_sudoku():
    i,j = 0,0
    numbers = [1,2,3,4,5,6,7,8,9]
    while sudoku[8][8]==0:# en son atama yapılacak blok 0 haricinde bir rakama eşitlenirse, döngüden çıkılır.
        
        if j == 9 :
            j = 0
            i +=1
        i,j,sudoku[i][j] = generate_number(i, j, sudoku)
        j +=1
        


#Buraya kadar tamamlanmış sudoku matrisi var
#Buradan sonra Sudokunun zorluguna göre random indislerden silinecek rakamlara karar veriliyor
def selected_level():#%25çok zor, %30 zor, %40 orta, %50 kolay, %70 cok kolay
    probablity = random.randint(0, 10)
    if probablity <3:
        return True
    return False

#silinecek rakamlara karar verilirken işlemin uygulanma classı
def sudoku_upgrade():
    counter = 0
     
    for i in range(9):
        for j in range(9):
            if selected_level():
                sudokuUpgrade[i][j] = 0
                counter =counter + 1
    print(" {} tane sayi atandı. {} tane sayi silindi ve {} kere backtracking uygulandı".format(81-counter,counter,len(counters)))
                
#Consol kısmında çıktıyı gösteren kısım        
def Puzzle(a):
    for i in range(M):
        for j in range(M):
            print(a[i][j],end=' ') 
            if j %3 ==2:
                print(' ',end='')
        print()
        if i %3 ==2:
            print()








generater_sudoku()
Puzzle(sudoku)
sudokuUpgrade = copy.deepcopy(sudoku)# no change first list with this method copy.deepcopy

sudoku_upgrade()
Puzzle(sudokuUpgrade)




#düzeltme 59. satırdaki metotda numbers array elemanlarını , uygun olmayan elemanları siliyorken uygun olan onaylanmış elemanlarıda silsin
#boylelikle atanan elemanlar tekrardan sorgulanmasın 




