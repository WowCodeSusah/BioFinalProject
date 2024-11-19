# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 11:38:45 2020

@author: Admin
"""
import pygame
import queue

clock = pygame.time.Clock()
pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)
BLUE = (0,0,255)

screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Play with graphs!")

left_background = pygame.image.load('resources/background.png')
node1 = pygame.image.load('resources/r_circle.png')
node2 = pygame.image.load('resources/b_circle.png')
node3 = pygame.image.load('resources/y_circle.png')
plus = pygame.image.load('resources/plus.png')
add = pygame.image.load('resources/add.png')
cross = pygame.image.load('resources/cross.png')
algo_button = pygame.image.load('resources/algo_button.png')

button_font = pygame.font.Font('resources/roboto.ttf', 20)
msg_font = pygame.font.Font('resources/roboto.ttf', 15)

add_node = button_font.render('Add Nodes', True, WHITE)
add_edge = button_font.render('Add Edges', True, WHITE)
dfs_button = button_font.render('DFS', True, WHITE) 
bfs_button = button_font.render('BFS', True, WHITE)
find_bridges_button = button_font.render('Find Bridges', True, WHITE)
clear_button = button_font.render('Clear Screen', True, WHITE) 
msg_box = msg_font.render('', True, BLUE)

node_button = plus
edge_button = add
nodes = []
edges = []
yellow_edges = []
blue_edges = []
color = [node2,node1,node3]
node_color = []
pos = (-1,-1)
pointA = -1
pointB = -1
point = -1
state = 'start'
msg = ''
    
def make_equal(listA, listB):
    for i in range(len(listA)):
        listA[i] =listB[i]

def isClicked(x1,y1,x2,y2,mos_x,mos_y):
    if mos_x>x1 and (mos_x<x2):
        x_inside = True
    else: x_inside = False
    if mos_y>y1 and (mos_y<y2):
        y_inside = True
    else: y_inside = False
    if x_inside and y_inside:
        return True
    else:
        return False

def ishovering(x1,y1,x2,y2):
    mos_x, mos_y = pygame.mouse.get_pos()
    if mos_x>x1 and (mos_x<x2):
        x_inside = True
    else: x_inside = False
    if mos_y>y1 and (mos_y<y2):
        y_inside = True
    else: y_inside = False
    if x_inside and y_inside:
        return True
    else:
        return False

def getNode(mos_x,mos_y):
    for i in range(len(nodes)):
        x1 = nodes[i][0]
        y1 = nodes[i][1]
        if isClicked(x1, y1, x1 + node2.get_width(), y1 + node2.get_height(), mos_x, mos_y):
            return i
    return -1

def show_nodes():
    if(len(nodes)==0): return
    for i in range(len(nodes)):
        screen.blit(node_color[i],nodes[i])

def show_edges():
    if(len(edges)==0): return
    for i in range(len(edges)):
            pygame.draw.line(screen,BLACK,(nodes[edges[i][0]][0]+16,nodes[edges[i][0]][1]+16),(nodes[edges[i][1]][0]+16,nodes[edges[i][1]][1]+16),1)
    for i in range(len(yellow_edges)):
            pygame.draw.line(screen,YELLOW,(nodes[yellow_edges[i][0]][0]+16,nodes[yellow_edges[i][0]][1]+16),(nodes[yellow_edges[i][1]][0]+16,nodes[yellow_edges[i][1]][1]+16),1)
    for i in range(len(blue_edges)):
            pygame.draw.line(screen,BLUE,(nodes[blue_edges[i][0]][0]+16,nodes[blue_edges[i][0]][1]+16),(nodes[blue_edges[i][1]][0]+16,nodes[blue_edges[i][1]][1]+16),2)

def show_buttons():
    if(state == 'start'):
        screen.blit(algo_button,(7,550))
        screen.blit(clear_button,(7+algo_button.get_width()/2-53,550+algo_button.get_height()/2-13))
        screen.blit(algo_button,(7,498))
        screen.blit(dfs_button,(7+algo_button.get_width()/2-20,498+algo_button.get_height()/2-13))
        screen.blit(algo_button,(7,446))
        screen.blit(bfs_button,(7+algo_button.get_width()/2-20,446+algo_button.get_height()/2-13))
        screen.blit(algo_button,(7,394))
        screen.blit(find_bridges_button,(7+algo_button.get_width()/2-50,394+algo_button.get_height()/2-13))
        
def show_msg():
    msg_box = msg_font.render(msg, True, BLUE)
    screen.blit(msg_box,(215,570))
    
running = True

while running:
    screen.fill(WHITE)
    screen.blit(left_background,(0,0))
    
    if(state == 'start' or state == 'add_node' or state == 'exit'):
        screen.blit(node_button,(5,5))
        
    if(state == 'start' or state == 'add_edge1' or state == 'add_edge2'):
        screen.blit(edge_button,(5,42))
        
    show_buttons()
    show_msg()
    
    if state == 'start':
        node_button = plus
        edge_button = add
        if(ishovering(5,5,5+node_button.get_width(),5+node_button.get_height())):
            screen.blit(add_node,(60,12))
        if(ishovering(5,42,5+edge_button.get_width(),42+edge_button.get_height())):
            screen.blit(add_edge,(60,48))
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if(pos[0]!=-1 & pos[1]!=-1):
                if state == 'start':
                    if(isClicked(7,498,7+algo_button.get_width(),498+algo_button.get_height(),pos[0],pos[1])):
                        if len(nodes) != 0:
                            state = 'choose start point for dfs'
                            msg = 'Choose source for the Depth First Search.'
                        else: state = 'start'
                    elif(isClicked(5,5,5+node_button.get_width(),5+node_button.get_height(),pos[0],pos[1])):
                        state = 'add_node'
                        msg = 'Click on the screen to add a node there.'
                        node_button = cross
                        edge_button = cross
                    elif(isClicked(5,42,5+edge_button.get_width(),42+edge_button.get_height(),pos[0],pos[1])):
                        msg = 'Choose initial vertex of the edge.'
                        state = 'add_edge1'
                        node_button = cross
                        edge_button = cross
                    elif(isClicked(7,446,7+algo_button.get_width(),446+algo_button.get_height(),pos[0],pos[1])):
                        if len(nodes) != 0:
                            state = 'choose start point for bfs'
                            msg = 'Choose source for the Breadth First Search.'
                        else: state = 'start'
                    elif(isClicked(7,394,7+algo_button.get_width(),394+algo_button.get_height(),pos[0],pos[1])):
                        if len(nodes) != 0:
                            node_button = cross
                            state = 'find_bridges'
                            msg = 'Articution Points: Yellow nodes    Bridges: Blue edges'
                        else: state = 'start'
                    elif(isClicked(7,550,7+algo_button.get_width(),550+algo_button.get_height(),pos[0],pos[1])):
                        nodes.clear()
                        node_color.clear()
                        edges.clear()
                elif state == 'add_node':
                    if pos[0]>200 and pos[1]<550:
                        nodes.append((pos[0]-16,pos[1]-16))
                        node_color.append(color[0])
                    if(isClicked(5,5,5+node_button.get_width(),5+node_button.get_height(),pos[0],pos[1])):
                        state = 'start'
                        msg = ''
                elif state == 'add_edge1':
                    pointA = getNode(pos[0],pos[1])
                    if(pointA != -1):
                        state = 'add_edge2'
                        msg = 'Choose terminal vertex of the edge.'
                    if(isClicked(5,42,5+edge_button.get_width(),42+edge_button.get_height(),pos[0],pos[1])):
                        state = 'start'
                        msg = ''
                elif state == 'add_edge2':
                    pointB = getNode(pos[0],pos[1])
                    if pointB != -1 and pointB != pointA:
                        edges.append((pointA,pointB))
                        edges.append((pointB,pointA))
                        state = 'add_edge1'
                        msg = 'Choose initial vertex of the edge.'
                        pointA = -1
                        pointB = -1
                    if(isClicked(5,42,5+edge_button.get_width(),42+edge_button.get_height(),pos[0],pos[1])):
                        state = 'start'
                        msg = ''
                elif state == 'choose start point for dfs':
                    point  = getNode(pos[0],pos[1])
                    if point != -1:
                        state = 'dfs'
                        msg = ''
                elif state == 'choose start point for bfs':
                    point  = getNode(pos[0],pos[1])
                    if point != -1:
                        state = 'bfs'
                        msg = ''
                elif state == 'exit':
                    if(isClicked(5,5,5+node_button.get_width(),5+node_button.get_height(),pos[0],pos[1])):
                        yellow_edges.clear()
                        blue_edges.clear()
                        state = 'start'
                        msg = ''
            pos = (-1,-1)
            
    show_edges()
    show_nodes()
    pygame.display.update()
    clock.tick(60)
    
pygame.quit()
