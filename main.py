# -*- coding:utf-8 -*-
import pygame
from pygame.locals import *
import sys
import copy
import time
import random
import heapq

MAP_WIDTH = 500
MAP_HEIGHT = 500
map_chip = 5
start_point = [0,0]
GOAL_FLAG = False
GOAL_INIT = True

def pygame_init():
    pygame.init()  # Pygameの初期化
    pygame.display.set_caption("simulation")
    font1=pygame.font.Font("font/JF-Dot-k12x10.ttf", 24)
    return gui_object.screen,font1

class gui_object:
    global map_chip
    width, height = MAP_WIDTH, MAP_HEIGHT
    screen = pygame.display.set_mode((width, height))

class Map(gui_object):
    before_map = [[0 for i in range(int(MAP_WIDTH/map_chip))] for j in range(int((MAP_HEIGHT-100)/map_chip))]
    after_map = [[0 for i in range(int(MAP_WIDTH/map_chip))] for j in range(int((MAP_HEIGHT-100)/map_chip))]
    row, col = len(before_map), len(before_map[0])  #row:x cal:y
    init_flag=True

    def draw(self,cell_map):
        global start_point
        for i in range(self.row):
            for j in range(self.col):
                if cell_map[i][j]==1 and self.init_flag:
                     start_point=i,j
                     self.init_flag=False
                elif cell_map[i][j]==1:
                    pygame.draw.rect(self.screen,(0,255,127),Rect(j*map_chip,i*map_chip,map_chip,map_chip),0)
                elif cell_map[i][j]>=2:
                    pygame.draw.rect(self.screen,(204,255,255),Rect(j*map_chip,i*map_chip,map_chip,map_chip),0)
                elif cell_map[i][j]==-2:
                    pygame.draw.rect(self.screen,(0,0,255),Rect(j*map_chip,i*map_chip,map_chip,map_chip),0)
                elif cell_map[i][j]==-3:
                    pygame.draw.rect(self.screen,(0,255,0),Rect(j*map_chip,i*map_chip,map_chip,map_chip),0)
                elif cell_map[i][j]==-1:
                    pygame.draw.rect(self.screen,(105,105,105),Rect(j*map_chip,i*map_chip,map_chip,map_chip),0)
                else:
                    pygame.draw.rect(self.screen, (255, 255, 255), Rect(j * map_chip, i * map_chip, map_chip, map_chip),0)
                if start_point[0]==i and start_point[1]==j:
                    pygame.draw.rect(self.screen, (255, 0, 0), Rect(j * map_chip, i * map_chip, map_chip, map_chip), 0)

class gui_window(gui_object):
    def __init__(self):
        gui_window.imgs=pygame.image.load("pic/window.png").convert_alpha()
        gui_window.rect_img = gui_window.imgs.get_rect()
        gui_window.rect_img = (0,MAP_HEIGHT-100) #(x,y)
    def draw(self):
        self.screen.blit(self.imgs,gui_window.rect_img)

class pen_button(gui_object):
    def __init__(self):
        pen_button.imgs=pygame.image.load("pic/pen.png").convert_alpha()
        pen_button.rect_img = pen_button.imgs.get_rect()
        pen_button.rect_img = (300,MAP_HEIGHT-60) #(x,y)
        pen_button.imgs_push = pygame.image.load("pic/pen_push.png").convert_alpha()
        pen_button.rect_img_push = pen_button.imgs_push.get_rect()
        pen_button.rect_img_push = (300, MAP_HEIGHT - 60)  # (x,y)
    def draw(self,push):
        if push==1:
            self.screen.blit(self.imgs_push, pen_button.rect_img_push)
        else:
            self.screen.blit(self.imgs,pen_button.rect_img)

class era_button(gui_object):
    def __init__(self):
        era_button.imgs=pygame.image.load("pic/era.png").convert_alpha()
        era_button.rect_img = era_button.imgs.get_rect()
        era_button.rect_img = (350,MAP_HEIGHT-60) #(x,y)
        era_button.imgs_push = pygame.image.load("pic/era_push.png").convert_alpha()
        era_button.rect_img_push = era_button.imgs_push.get_rect()
        era_button.rect_img_push = (350, MAP_HEIGHT - 60)  # (x,y)
    def draw(self,push):
        if push==2:
            self.screen.blit(self.imgs_push, era_button.rect_img_push)
        else:
            self.screen.blit(self.imgs, era_button.rect_img)

class next_button(gui_object):
    def __init__(push):
        next_button.imgs=pygame.image.load("pic/next.png").convert_alpha()
        next_button.rect_img = next_button.imgs.get_rect()
        next_button.rect_img = (400,MAP_HEIGHT-60) #(x,y)
        next_button.imgs_push = pygame.image.load("pic/next_push.png").convert_alpha()
        next_button.rect_img_push = next_button.imgs_push.get_rect()
        next_button.rect_img_push = (400, MAP_HEIGHT - 60)  # (x,y)
    def draw(self,push):
        if push==3:
            self.screen.blit(self.imgs_push, next_button.rect_img_push)
        else:
            self.screen.blit(self.imgs, next_button.rect_img)

class stop_button(gui_object):
    def __init__(push):
        stop_button.imgs=pygame.image.load("pic/stop.png").convert_alpha()
        stop_button.rect_img = stop_button.imgs.get_rect()
        stop_button.rect_img = (450,MAP_HEIGHT-60) #(x,y)
        stop_button.imgs_push = pygame.image.load("pic/stop_push.png").convert_alpha()
        stop_button.rect_img_push = stop_button.imgs_push.get_rect()
        stop_button.rect_img_push = (450, MAP_HEIGHT - 60)  # (x,y)
    def draw(self,push):
        if push==4:
            self.screen.blit(self.imgs_push, stop_button.rect_img_push)
        else:
            self.screen.blit(self.imgs, stop_button.rect_img)

class cur_button(gui_object):
    def __init__(self):
        cur_button.imgs=pygame.image.load("pic/cur.png").convert_alpha()
        cur_button.rect_img = cur_button.imgs.get_rect()
        cur_button.rect_img = (250,MAP_HEIGHT-60) #(x,y)
        cur_button.imgs_push = pygame.image.load("pic/cur_push.png").convert_alpha()
        cur_button.rect_img_push = cur_button.imgs_push.get_rect()
        cur_button.rect_img_push = (250, MAP_HEIGHT - 60)  # (x,y)
    def draw(self,push):
        if push==5:
            self.screen.blit(self.imgs_push, cur_button.rect_img_push)
        else:
            self.screen.blit(self.imgs,cur_button.rect_img)

def object_draw(push):
    window = gui_window()
    pen = pen_button()
    era = era_button()
    next = next_button()
    stop = stop_button()
    cur = cur_button()
    window.draw()
    pen.draw(push)
    era.draw(push)
    next.draw(push)
    stop.draw(push)
    cur.draw(push)

def around_counter(cells,_x,_y):
    cell_count = 0
    destination = -1
    global GOAL_INIT
    cnt=0
    goal = 0
    min_num = [0,0,0,0]
    cell = Map()
    for y in range(-1,2):
        for x in range(-1,2):
            if x==0 and y==0:
                continue
            elif x==1 and y==-1:
                continue
            elif x==-1 and y==1:
                continue
            elif x==1 and y==1:
                continue
            elif x==-1 and y==-1:
                continue
            x2 = _x+x
            y2 = _y+y
            if x2<0:
                x2=0
            if y2<0:
                y2=0
            if get_error(cells,x2,y2)!=0:
                if cells[x2][y2]>=1:
                    cell_count+=1
                if cells[x2][y2]==-2:
                    goal+=1
                min_num[cnt]=cells[x2][y2]
            cnt+=1


    return cell_count,goal,destination

def get_error(cells,x,y):
    if is_exist(cells,x,y):
        return cells[x][y]
    else:
        return 0

def is_exist(cells,x,y):
    try:
        _ = cells[x][y]
    except IndexError:
        return False
    else:
        return True

def step_cells(b,a):
    cell = Map()
    n = 0
    goal=0
    global GOAL_FLAG
    for y in range(cell.col):
        for x in range(cell.row):
            n,goal,_ = around_counter(b,x,y)
            cell_checker = 0
            if b[x][y]==0:
                if n>=1:
                    cell_checker=1

            elif b[x][y]>=1:
                cell_checker=b[x][y]+1
                if goal>=1:
                    GOAL_FLAG=True
            elif b[x][y] == -1:
                cell_checker = -1
            elif b[x][y] == -2:
                cell_checker = -2

            a[x][y]=cell_checker

def Dijkstra(array):
    cell = Map()
    goal=0
    destination=0
    x=start_point[0]
    y=start_point[1]
    while True:
        _,goal,destination = around_counter(array,x,y)
        if destination==-1:
            continue
        if destination==0:
            y-=1
        if destination==1:
            x-=1
        if destination==2:
            x+=1
        if destination==3:
            y+=1
        array[x][y]=-3
        if goal>=1:
            break


def main():
    (x,y)=(0,0)
    map_y=0
    counter=0
    timer_start = False
    global map_chip
    mouse_btn_check = 0
    screen,font1 = pygame_init()
    clock = pygame.time.Clock()
    cell = Map()
    push = 0
    flag = True
    on_map = True
    fps_timer = True
    while (1):
        screen.fill((220, 220, 220))
        text1 = font1.render("X:{:3d} Y:{:3d}".format(x, y), True, (0, 0, 0))
        text2 = font1.render("GEN:"+str(counter), True, (0, 0, 0))
        text3 = font1.render("TOOL:" + str(mouse_btn_check), True, (0, 0, 0))
        if GOAL_FLAG:
            timer_start = False
            if flag:
                Dijkstra(cell.before_map)
            else:
                Dijkstra(cell.after_map)

        if flag:
            cell.draw(cell.before_map)
        else:
            cell.draw(cell.after_map)
        object_draw(push)
        screen.blit(text1, (20, MAP_HEIGHT - 80))
        screen.blit(text2, (20, MAP_HEIGHT - 60))
        screen.blit(text3, (20, MAP_HEIGHT - 40))
        pygame.display.update()  # 画面を更新
        pygame.time.wait(10)
        if fps_timer:
            fps_timer = False
            time_stack=pygame.time.get_ticks()
        if timer_start:
            if 500<=pygame.time.get_ticks() - time_stack:
                counter += 1
                fps_timer=True
                if flag:
                    step_cells(cell.before_map, cell.after_map)
                else:
                    step_cells(cell.after_map, cell.before_map)
                flag = not flag
        # イベント処理
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                x, y = event.pos
                map_y = y
                if map_y > MAP_HEIGHT - 101:
                    map_y = MAP_HEIGHT - 101
                    on_map = False
                else:
                    on_map = True
                #x -= int(player.get_width() / 2)
                #y -= int(player.get_height() / 2)
            if event.type == MOUSEBUTTONDOWN and event.button == 3:
                if x>=300 and y>=MAP_HEIGHT-60 and x<=336 and y<MAP_HEIGHT-60+36:
                    mouse_btn_check +=1
                    if mouse_btn_check>4:mouse_btn_check=1
                    push = 1
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                push = 10
                if x>=250 and y>=MAP_HEIGHT-60 and x<=286 and y<MAP_HEIGHT-60+36:
                    mouse_btn_check = -1
                    push = 5
                if x>=300 and y>=MAP_HEIGHT-60 and x<=336 and y<MAP_HEIGHT-60+36:
                    mouse_btn_check = 1
                    push = 1
                if x>=350 and y>=MAP_HEIGHT-60 and x<=386 and y<MAP_HEIGHT-60+36:
                    mouse_btn_check = 0
                    push = 2
                if x>=400 and y>=MAP_HEIGHT-60 and x<=436 and y<MAP_HEIGHT-60+36:
                    push = 3
                    timer_start=True
                if x >= 450 and y >= MAP_HEIGHT - 60 and x <= 486 and y < MAP_HEIGHT - 60 + 36 or GOAL_FLAG:
                    push = 4
                    timer_start=False
                else:
                    pass
                if mouse_btn_check == 2:
                    pass
            if event.type == MOUSEBUTTONUP:
                push = 0
                #mouse_btn_check = 0

            if mouse_btn_check == 1 and push!=0:
                if on_map:
                    if flag:
                        cell.before_map[int(map_y / map_chip)][int(x / map_chip)] = -1
                    else:
                        cell.after_map[int(map_y / map_chip)][int(x / map_chip)] = -1
            elif mouse_btn_check == 0 and push!=0:
                if on_map:
                    if flag:
                        cell.before_map[int(map_y / map_chip)][int(x / map_chip)] = 0
                    else:
                        cell.after_map[int(map_y / map_chip)][int(x / map_chip)] = 0
            elif mouse_btn_check == 2 and push!=0:
                if on_map:
                    if flag:
                        cell.before_map[int(map_y / map_chip)][int(x / map_chip)] = 1
                    else:
                        cell.after_map[int(map_y / map_chip)][int(x / map_chip)] = 1
            elif mouse_btn_check == 3 and push!=0:
                if on_map:
                    if flag:
                        cell.before_map[int(map_y / map_chip)][int(x / map_chip)] = -2
                    else:
                        cell.after_map[int(map_y / map_chip)][int(x / map_chip)] = -2
            elif mouse_btn_check == 4 and push!=0:
                if on_map:
                    if flag:
                        cell.before_map[int(map_y / map_chip)][int(x / map_chip)] = 4
                    else:
                        cell.after_map[int(map_y / map_chip)][int(x / map_chip)] = 4


            if event.type == QUIT:  # 閉じるボタンが押されたら終了
                pygame.quit()  # Pygameの終了(画面閉じられる)
                sys.exit()
            if event.type == KEYDOWN:       # キーを押したとき
                if event.key == K_UP:
                    pass
                elif event.key == K_DOWN:
                    pass
                elif event.key == K_RIGHT:
                    pass
                elif event.key == K_LEFT:
                    pass
                elif event.key == K_r:   # Escキーが押されたとき
                    counter+=1
                    if flag:
                        step_cells(cell.before_map,cell.after_map)
                    else:
                        step_cells(cell.after_map,cell.before_map)
                    flag = not flag
                elif event.key == K_ESCAPE:
                    pygame.quit()  # Pygameの終了(画面閉じられる)
                    sys.exit()
if __name__ == "__main__":
    main()