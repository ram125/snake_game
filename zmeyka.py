# -*- coding: utf-8 -*-
file_name = 'file_with_name.txt'
GlobalFile = open(file_name, 'r')
s = 0
for i in GlobalFile:
    list_line = list(i)
    if ',' in list_line:
        i = i.rstrip('\n')
        ready_list = i.split(',')
        if s == 0:
            FileList = ready_list
            s += 1
        else:
            list_with_variables = ready_list
        
GlobalFile.close()
from tkinter import *
import time
GameOver = True
BorderDataX= []
BorderDataY= []
Error = False
list_with_vars = []
'''этот алгоритм конвртирует данные из файла с данными. в список который другой алорим может использовать для построения стен'''
'''этот класс отвеает за построение стен и других объектов на основе данных полученых из указанного списка'''
class border():
    def __init__(self, color, size, distance, canvas, global_list):
        self.global_list = global_list
        self.c = canvas
        self.color = color
        self.size = int(size) # так как стена состоит из квадратиков здесь указывается размер одной стороны квадрата
        self.distance = int(distance) # разстояние между квадратамми
        self.AllSize = int(size) + int(distance )# полный размер квадрат + дистанция до следующего
    def creating_border(self):
        
        self.global_list = self.global_list.split(',')
        x = len(self.global_list)//2 #х это количество мини-списков в большом списке 
        self.List = []  #first_list это основной список который состоит из мини-списков которые содержат в себе информацию о крайних точках каждой стены
        for i in range(x):   #этот цикл отвечает за то построение мини-списков в большом списке
            x =  i*2
            self.List.append([int(self.global_list[x]), int(self.global_list[x+1])])
        file.close()

        if len(self.List)> 1:   #проверяет не пустой ли список
            for i in range(len(self.List) // 2 ): #в основном списке два мини списка отвечают за одну и ту же стену
                self.time = 0                       #И для того чтобы узнать сколько раз нужно повторить цикл он делит колиество элементов списка на 2
                self.f = i*2                          # f это номер элемента который сейчас будет обрабатывать цикл
                self.h = self.List[self.f][1] - self.List[self.f][0]   #в следущих 12 строках алгоритм определяет направлние стены: горизонтальное или вертикальное
                self.g = self.List[self.f+1][1] - self.List[self.f+1][0]
                self.d = 0
                self.direction = None
                if self.g > 1 and self.h == 1:
                    self.d = self.g
                    self.direction  = 'Vertical'
                elif self.g == 1 and self.h > 1:
                    self.d = self.h
                    self.direction = 'Horizontal'
                else:
                    print('bad list')
                    GameOver = True
                BorderDataY.append([self.List[self.f+1][1] * self.AllSize, self.List[self.f+1][0] * self.AllSize]) # в этих строках алгоритм добавляет данные в специальны списки
                BorderDataX.append([self.List[self.f][1] * self.AllSize, self.List[self.f][0] * self.AllSize]) # которые в дальнейшем будут исольззованы для того что бы определить касается ли змейка
                # одной из стен
                for i in range(self.d):
                    if self.time == 0: #time это переменная которая показывает в первый ли раз исполняется данный цикл
                        self.LeftX =( self.List[self.f][0] * self.AllSize) + self.distance  # дальнейшие строки рисуют стену
                        self.RightX = self.LeftX + self.size
                        self.TopY = (self.List[self.f+1][0] * self.AllSize) + self.distance
                        self.BottomY  = self.TopY + self.size
                        self.c.create_rectangle(self.RightX, self.BottomY, self.LeftX, self.TopY, fill=self.color, outline="black")
                        self.time += 1
                    else:
                        if self.direction == 'Horizontal':
                            self.LeftX = self.RightX + self.distance
                            self.RightX = self.LeftX + self.size
                            self.c.create_rectangle(self.RightX, self.BottomY, self.LeftX, self.TopY, fill=self.color, outline="black")
                        if self.direction == 'Vertical':
                            self.TopY = self.BottomY + self.distance
                            self.BottomY = self.TopY + self.size
                            self.c.create_rectangle(self.RightX, self.BottomY, self.LeftX, self.TopY, fill=self.color, outline="black")

class SnakeHead():          #SnakeHead это класс отвечают за прорисовку и управление головой змейки
    def __init__(self, color, direction, TimeSleep, root, c, border, spawnX, spawnY):
        self.Border = border
        self.root =  root
        self.c = c
        self.step = self.Border.AllSize    #какое разстояние проходит змейка за один цикл
        self.color = color    #какого цвета будет голова змейки
        self.direction = direction  #какое будет изначальное направление змейки
        self.TimeSleep = TimeSleep
        self.X = spawnX
        self.Y = spawnY
    def locating(self):      #следющие две функции отвечают за определение кооррдинат и прорисовку головы
        self.TopY = (self.X*self.step)+ self.Border.distance
        self.BottomY = self.TopY + self.Border.size
        self.LeftX = (self.Y*self.step)+ self.Border.distance
        self.RightX = self.LeftX + self.Border.size
    def creating(self):
        self.locating()
        self.head = self.c.create_rectangle(self.RightX, self.BottomY, self.LeftX, self.TopY, fill=self.color, outline="black", tag="head")
    def KeyStrokes(self, event):  # эта функция отлавливает нажатия нужных клавиш 
        if GameOver == False:
            if event.keysym == "w":
                if self.direction != "Down":   #эта конструкция не дает игроку возможности изменять направление движения змейки на противоположное  
                    self.direction = "Up" #такимм образом игрок может менять направление  движения змейки
            elif event.keysym == "a":
                if self.direction != "Right":
                    self.direction = "Left"
            elif event.keysym == "s":
                if self.direction != "Up":
                    self.direction = "Down"
            elif event.keysym == "d":
                if self.direction != "Left":
                    self.direction = "Right"
    def KeyStrokes2(self):  #эта функция привязывает события к нужной нам функции
        self.c.bind_all('<Key>', self.KeyStrokes)
    def deleting(self):
        self.c.delete("head")
    def moving(self):
        global GameOver
        self.root.update()   #перерисовывает холст с изображением
        self.KeyStrokes2()  # проверяет была ли какая-нибудь клавиша нажата
        if self.direction == "Up":  #в зависимости от направления змейки выполняет разные действия
            if self.TopY == self.Border.distance:
                self.c.move(self.head, 0, +1000)
                self.BottomY += 1000   
                self.TopY += 1000 
            for i in range(len(BorderDataY)):   #что бы проверить все элемменты на предмет соприкосновения с головой змейки алоритм измеряет длинну змейки
                if self.LeftX <= BorderDataX[i][0] and self.LeftX >= BorderDataX[i][1]:  #проверяет находится ли голова между двумя крайними точками стены по координате Х
                    if self.TopY <= BorderDataY[i][0] + self.Border.AllSize and self.TopY >= BorderDataY[i][1]: # а потом коснулась ли она одной из стен
                        GameOver = True    #если да то игра заканчивается
            if GameOver == False:   #если же змейка не касается ни одной из стен то игра продолжается
                self.BottomY -= self.step   
                self.TopY -= self.step  #  прибавляет к пременным один шаг указанный выше
                self.c.move(self.head, 0, -self.step)  #двигает изображение
                time.sleep(self.TimeSleep) #ждет указаное время чтобы игра не была слишком быстрой
        if self.direction == "Right":
            if self.LeftX == 1920+self.Border.distance:
                self.c.move(self.head, -(1920+self.Border.AllSize), 0)
                self.RightX -= 1920+self.Border.AllSize   
                self.LeftX -= 1920+self.Border.AllSize  
            for i in range(len(BorderDataY)):
                if self.TopY <= BorderDataY[i][0] and self.TopY >= BorderDataY[i][1]:
                    if self.LeftX >= BorderDataX[i][1] - self.Border.AllSize and self.LeftX <= BorderDataX[i][0]:
                        GameOver = True
            if GameOver == False:
                self.RightX += self.step
                self.LeftX += self.step
                self.c.move(self.head, +self.step, 0)
                time.sleep(self.TimeSleep)
        if self.direction == "Down":
            if self.TopY == 1000+ self.Border.distance:
                self.c.move(self.head, 0, -(1000+self.Border.AllSize))
                self.BottomY -= 1000+ self.Border.AllSize   
                self.TopY -= 1000+ self.Border.AllSize  
            for i in range(len(BorderDataY)):
                if self.LeftX <= BorderDataX[i][0] and self.LeftX >= BorderDataX[i][1]:
                    if self.TopY >= BorderDataY[i][1] - self.Border.AllSize and self.TopY <= BorderDataY[i][0]:
                        GameOver = True
            if GameOver == False:
                self.BottomY += self.step
                self.TopY += self.step
                self.c.move(self.head, 0, +self.step)
                time.sleep(self.TimeSleep)
        if self.direction == "Left":
            if self.LeftX == self.Border.distance:
                self.c.move(self.head, +1920, 0)
                self.RightX += 1920   
                self.LeftX += 1920  
            for i in range(len(BorderDataY)):
                if self.TopY <= BorderDataY[i][0] and self.TopY >= BorderDataY[i][1]:
                    if self.LeftX <= BorderDataX[i][0] + self.Border.AllSize and self.LeftX >= BorderDataX[i][1]:
                        GameOver = True
            if GameOver == False:
                self.RightX -= self.step
                self.LeftX -= self.step
                self.c.move(self.head, -self.step, 0)
                time.sleep(self.TimeSleep)
            

class SnakeBody():
    def __init__(self, DistanceFromHead, canvas, border, head):
        self.c = canvas
        self.Border = border
        self.head = head
        self.DFH = DistanceFromHead
        self.color = self.head.color
        self.BodyDirection = self.head.direction
        self.TurningCoordinatesX = []
        self.TurningCoordinatesY = []
        self.TurningDirection = []
    def locating(self):
        self.RightX = self.head.RightX
        self.LeftX = self.head.LeftX
        self.TopY = self.head.TopY
        self.BottomY = self.head.BottomY
        self.BodyDirection2 = "Up"
        for i in range(self.DFH):
            self.TopY = self.BottomY + self.Border.distance
            self.BottomY = self.TopY + self.Border.size
    def creating(self):
        self.locating()
        self.body = self.c.create_rectangle(self.RightX, self.BottomY, self.LeftX, self.TopY, fill=self.color, outline="black", tag="body")
    def funk(self):
        if self.BodyDirection != self.head.direction:
            if self.head.direction == "Right":
                self.TurningCoordinatesX.append(self.head.LeftX - self.head.step)
                self.TurningCoordinatesY.append(self.head.TopY)
                self.TurningDirection.append("Right")
            if self.head.direction == "Left":
                self.TurningCoordinatesX.append(self.head.LeftX + self.head.step)
                self.TurningCoordinatesY.append(self.head.TopY)
                self.TurningDirection.append("Left")
            if self.head.direction == "Up":
                self.TurningCoordinatesX.append(self.head.LeftX)
                self.TurningCoordinatesY.append(self.head.TopY + self.head.step)
                self.TurningDirection.append("Up")
            if self.head.direction == "Down":
                self.TurningCoordinatesX.append(self.head.LeftX)
                self.TurningCoordinatesY.append(self.head.TopY - self.head.step)
                self.TurningDirection.append("Down")
            self.BodyDirection = self.head.direction
    def funk2(self):
        self.funk()
        self.x = len(self.TurningDirection)
        if self.x != 0:
            if self.LeftX == self.TurningCoordinatesX[0] and self.TopY == self.TurningCoordinatesY[0]:
                self.BodyDirection2 = self.TurningDirection[0]
                del self.TurningCoordinatesX[0]
                del self.TurningCoordinatesY[0]
                del self.TurningDirection[0]
    def deleting(self):
        self.c.delete("body")
    def MovingBody(self):
        self.funk2()
        if GameOver == False:
            if self.BodyDirection2 == "Right":
                if self.LeftX == 1920+self.Border.distance:
                    self.c.move(self.body, -(1920+self.Border.AllSize), 0)
                    self.RightX -= 1920+self.Border.AllSize  
                    self.LeftX -= 1920+self.Border.AllSize  
                self.c.move(self.body, self.head.step, 0)
                self.LeftX += self.head.step
            elif self.BodyDirection2 == "Left":
                if self.LeftX == self.Border.distance:
                    self.c.move(self.body, +1920, 0)
                    self.RightX += 1920   
                    self.LeftX += 1920  
                self.c.move(self.body, -self.head.step, 0)
                self.LeftX -= self.head.step
            elif self.BodyDirection2 == "Down":
                if self.TopY == 1000+ self.Border.distance:
                    self.c.move(self.body, 0, -(1000+self.Border.AllSize))
                    self.BottomY -= 1000+self.Border.AllSize
                    self.TopY -= 1000+self.Border.AllSize  
                self.c.move(self.body, 0, self.head.step)
                self.TopY += self.head.step
            elif self.BodyDirection2 == "Up":
                if self.TopY ==  self.Border.distance:
                    self.c.move(self.body, 0, +1000)
                    self.BottomY += 1000   
                    self.TopY += 1000  
                self.c.move(self.body, 0, -self.head.step)
                self.TopY -= self.head.step

class Callback:
    callback = {}
 
    def __init__(self, callback, pydata, start):
        self.callback = callback
        self.start  = start
        self.pydata = pydata
        Callback.callback[self.pydata] = lambda: self.click(self.start)
    def click(self, start):
        self.callback(self.pydata, self.start)

GameOver = True
root = Tk()
root.minsize(1925, 1000)
root.maxsize(1925, 1000)
c = Canvas(root, width=1925, height=1015, bg="black")  
c.place(x=-2, y=-2)


start = None
 
def click(data, start):
    game(data, start)
ButtonList = []
def start(FileList):
    global ButtonList
    for i in range(len(ButtonList)):
        ButtonList[i-1].destroy()
    x = len(FileList)
    c = Canvas(root, width=1925, height=1015, bg="black")   
    c.place(x=-2, y=-2)
    Callback.callback = {}
    if x>0:
        x = len(FileList)
        for i in range(x):
            cname = FileList[i]
            Callback(click, cname, start)
            ButtonList.append(Button(root, text=cname, bg='light blue', fg='dark blue', height=3, width=6, command=Callback.callback[cname]))
            ButtonList[len(ButtonList) - 1].place(x=175+(i*50), y=270)


def start1():
    global ButtonList
    for i in range(len(ButtonList)):
        ButtonList[i-1].destroy()
    ButtonList .append(Button(root, text='Start', bg='light blue', fg='dark blue', height=3, width=6, command=lambda: start(FileList)))
    ButtonList[len(ButtonList) - 1].place(x=175, y=270)
file = None
def game(FileName, start):
    global GameOver, done, c, ButtonList, file
    file = open(FileName, 'r')
    list_with_vars = []
    for i in file:
        line_without_rr = i.rstrip('\n')
        lwr = line_without_rr
        list_line = list(lwr)
        if '=' in list_line:
            ready_list = lwr.split('=')
            for i in range(len(list_with_variables)):
                if ready_list[0] == list_with_variables[i]:
                    list_with_vars.append(ready_list[1])
        else:
            lists = i
    file.close()
    c = Canvas(root, width=1925, height=1015, bg="black")   
    c.place(x=-2, y=-2)
    c.delete("all")
    GameOver = False
    done = False
    Border = border(list_with_vars[0], list_with_vars[1], list_with_vars[2], c, lists)
    Border.creating_border()
    head = SnakeHead(list_with_vars[4], "Up", float(list_with_vars[3]), root, c, Border, int(list_with_vars[6]), int(list_with_vars[7]))
    head.creating()
    body = []
    times = (int(list_with_vars[5]))
    for i in range(times):
        body.append([])
        body[i] = SnakeBody(i+1, c, Border, head)
        body[i].creating()
    for i in  range(123123):
        if GameOver == False:
            head.moving()
            for i in range(times):
                 body[i].MovingBody()
        elif GameOver == True and done == False:
            c.delete("all")
            ButtonList.append(Button(c, text='restart', bg='light blue', fg='dark blue', height=3, width=6, command=lambda: game(FileName, start)))
            ButtonList[len(ButtonList) - 1].place(x=175, y=270)
            ButtonList.append(Button(c, text='main munu', bg='light blue', fg='dark blue', height=3, width=6, command=start1))
            ButtonList[len(ButtonList) - 1].place(x=225, y=170)
            done = True





start1()

root.mainloop()
