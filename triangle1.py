import pygame
import time
import random
import numpy as np
from math import *
from objfileloader import *
pygame.init() #Start Pygame=
width , height = 640  , 640
screen = pygame.display.set_mode((width , height)) #Start the screen
pygame.display.set_caption('3d Viewer')

cameraZoffset = 2
def conv(x , y , z , w = width , h = height):
    z = z + cameraZoffset
    Xn = (h / w)*x/(z)
    Yn = (h / w)*y/(z)
    Xs = (w / 2)*(Xn + 1)
    Ys = (h / 2)*(1 - Yn)
    return (int(Xs) , int(Ys))




def returnTriangle(u , v , w): #draws triangles in clockwise order
    coord = [u , v , w]
    for i in range(0 , len(coord)):
        for j in range(0 , len(coord) - i - 1):
            if coord[j][0] > coord[j + 1][0]:
                temp = coord[j]
                coord[j] = coord[j + 1]
                coord[j + 1] = temp
    if coord[0][1] < coord[1][1]:
        return (coord[0] , coord[1] , coord[2])
    else:
        return (coord[0] , coord[2] , coord[1])

def drawTriangle(u , v , w): #takes 3 vertices
    u = conv(*u)
    v = conv(*v)
    w = conv(*w)
    points = returnTriangle(u , v , w)
    pygame.draw.line(screen , (200 , 200 , 200) , points[0] , points[1])
    pygame.draw.line(screen , (200 , 200 , 200) , points[1] , points[2])
    pygame.draw.line(screen , (200 , 200 , 200) , points[2] , points[0])


def translate(points , tx , ty , tz):  #returns list of transformed vertices
    tMatrix = np.eye(4 , 4)
    result = []
    tMatrix[0][3] = tx / 2
    tMatrix[1][3] = ty / 2
    tMatrix[2][3] = tz / 2 
    for point in points:
        vertex = list(point)
        vertex.append(1)
        vertex = np.array(vertex)
        vertex = np.vstack(vertex)
        vertex = np.matmul(tMatrix , vertex)
        vertex = vertex.reshape(1 , 4)
        vertex = vertex[0]
        vertex = np.matmul(tMatrix , vertex)
        vertex = vertex.tolist()
        del vertex[3]
        result.append(tuple(vertex))
    return result

def rotateX(points , rx):
    rx = radians(rx)
    result = []
    rMatrix = np.eye(4 , 4)
    rMatrix[1][1] = cos(rx)
    rMatrix[1][2] = -sin(rx)
    rMatrix[2][1] = sin(rx)
    rMatrix[2][2] = cos(rx)
    for point in points:
        vertex = list(point)
        vertex.append(1)
        vertex = np.array(vertex)
        vertex = np.vstack(vertex)
        vertex = np.matmul(rMatrix , vertex)
        vertex = vertex.reshape(1 , 4)
        vertex = vertex[0]
        vertex = vertex.tolist()
        del vertex[3]
        result.append(tuple(vertex))
    return result

def rotateZ(points , rz):
    rz = radians(rz)
    result = []
    rMatrix = np.eye(4 , 4)
    rMatrix[0][0] = cos(rz)
    rMatrix[0][1] = -sin(rz)
    rMatrix[1][0] = sin(rz)
    rMatrix[1][1] = cos(rz)
    for point in points:
        vertex = list(point)
        vertex.append(1)
        vertex = np.array(vertex)
        vertex = np.vstack(vertex)
        vertex = np.matmul(rMatrix , vertex)
        vertex = vertex.reshape(1 , 4)
        vertex = vertex[0]
        vertex = vertex.tolist()
        del vertex[3]
        result.append(tuple(vertex))
    return result

def rotateY(points , ry):
    ry = radians(ry)
    result = []
    rMatrix = np.eye(4 , 4)
    rMatrix[0][0] = cos(ry)
    rMatrix[0][2] = sin(ry)
    rMatrix[2][0] = -sin(ry)
    rMatrix[2][2] = cos(ry)
    for point in points:
        vertex = list(point)
        vertex.append(1)
        vertex = np.array(vertex)
        vertex = np.vstack(vertex)
        vertex = np.matmul(rMatrix , vertex)
        vertex = vertex.reshape(1 , 4)
        vertex = vertex[0]
        vertex = vertex.tolist()
        del vertex[3]
        result.append(tuple(vertex))
    return result


def drawMesh(vertices): #[() , () , () , ...]
    tris = []
    if len(vertices) % 3 != 0:
        print("can't draw mesh. \nnumber of vertices has to be a multiple of 3.")
    else:
        for i in range(0 , len(vertices) , 3):
            for j in range(i , i + 3):
                tris.append(vertices[j])
            drawTriangle(*tris)
            tris.clear()

def drawMeshIndices(vertices , indices):
    tris = []
    if len(indices) % 3 != 0:
        print("can't draw mesh. \nnumber of indices has to be a multiple of 3.")
    else:
        for i in range(0 , len(indices) , 3):
            for j in range(i , i + 3):
                tris.append(vertices[indices[j] - 1])
            drawTriangle(*tris)
            tris.clear()


def main():
    running = True
    points = getVerts('suzanne.obj')
    indices = getIndices('suzanne.obj')
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #The user closed the window!
                running = False #Stop running
        # Logic goes here
        screen.fill((0 , 0 , 0))
        drawMeshIndices(points , indices)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                points = translate(points , -0.1 , 0 , 0)
                drawMeshIndices(points , indices)
            elif event.key == pygame.K_RIGHT:
                points = translate(points , 0.1 , 0 , 0)
                drawMeshIndices(points , indices)
            elif event.key == pygame.K_UP:
                points = translate(points , 0 , 0.1 , 0)
                drawMeshIndices(points , indices)
            elif event.key == pygame.K_DOWN:
                points = translate(points , 0 , -0.1 , 0)
                drawMeshIndices(points , indices)
            elif event.key == pygame.K_w:
                points = rotateZ(points , 5)
                drawMeshIndices(points , indices)
            elif event.key == pygame.K_s:
                points = rotateZ(points , -5)
                drawMeshIndices(points , indices)
            elif event.key == pygame.K_d:
                points = rotateY(points , 5)
                drawMeshIndices(points , indices)
            elif event.key == pygame.K_a:
                points = rotateY(points , -5)
                drawMeshIndices(points , indices)
            elif event.key == pygame.K_f:
                points = rotateX(points , 5)
                drawMeshIndices(points , indices)
            elif event.key == pygame.K_r:
                points = rotateX(points , -5)
                drawMeshIndices(points , indices)
            elif event.key == pygame.K_1:
                points = translate(points , 0 , 0 , 0.1)
                drawMeshIndices(points , indices)
            elif event.key == pygame.K_2:
                points = translate(points , 0 , 0 , -0.1)
                drawMeshIndices(points , indices)
        pygame.display.flip()
        time.sleep(1 / 90)
    pygame.quit() #Close the window

main()
def test():
    pass

#test()