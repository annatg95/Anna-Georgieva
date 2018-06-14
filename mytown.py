import maya.cmds as cmds
import math as math
import random as random

'''creates a window for the user '''
'''title of the window = city generator, width = 300, height = 400'''


myWindow = cmds.window( t= "City generator", w=300, h=400)
cmds.columnLayout(adj=True)
cmds.text("Name of city:")

myName = cmds.textFieldGrp( ann='Name of City:', tx='Enter the name here')
cmds.button(l="Create city",width = 150, align = 'center', c ="makeCity()")



''' creates a building, the user inputs the h and w and d '''
'''number to define the width between the houses'''

cmds.text("Enter the h, w ,d of a building and their number of rows and columns, also the width between houses ")
myHeight = cmds.intSliderGrp(l = 'height ', min=3, max = 20, f = True)
myWidth = cmds.intSliderGrp(l = 'width ', min=3, max = 10, f = True)
myDepth = cmds.intSliderGrp(l = 'depth ', min=3, max = 10, f = True)
widthBetweenHouses = cmds.intSliderGrp(l = 'width between houses ', min=15, max = 20, f = True)

'''makes two types of different villages'''

cmds.button(l="Create number of buildings",width = 150, align = 'center', c ="makeaBuilding()")
cmds.button(l="Create Village",width = 150, align = 'center', c ="makeVillage()")
cmds.button(l="Create Another Village",width = 150, align = 'center', c ="makeVillage2()")


'''create trees next to the buildings '''
'''the user choose the height of the tree'''

cmds.text("Enter the height Of trees")
myTHeight = cmds.intSliderGrp(l = "height", min=3, max =10 , f = True)

cmds.button(l="Create trees",width = 150, align = 'center', c ="makeTree()")


'''create clouds '''
cmds.button(l="Create clouds",width = 150, align = 'center', c = "makeClouds()")


'''create sun and choose the r of the sphere'''

cmds.text("Create the SUN")
mySun = cmds.intSliderGrp(l = "number", min=10, max = 20, f = True)
cmds.button(l="Create the SUN",width = 150, align = 'center', c = "makeSun()")


''' delete city'''

cmds.text("Delete city")
cmds.button(l="Delete",width = 150, align = 'center', c ="deleteCity()")



'''fetch the city name'''
cmds.textFieldGrp(myName, query = True, text = True)

'''fetch the data from the user's input for buildings'''
cmds.intSliderGrp(myHeight, query = True, value = True)
cmds.intSliderGrp(myWidth, query = True, value = True)
cmds.intSliderGrp(myDepth, query = True, value = True)
cmds.intSliderGrp(widthBetweenHouses, query = True, value = True)


'''fetch the data from the user's input for tree'''
cmds.intSliderGrp(myTHeight, query = True, value = True)



'''fetch the data user's input from the sun'''
cmds.intSliderGrp(mySun, query = True, value = True)

'''creates plane with for loop'''

def makeCity():

    cmds.select(all=True)
    cmds.delete()
    for i in range( 0,10):
        cmds.polyPlane( sx=10,sy=10, w=25, h=25, name = 'myP'+str(i))
        cmds.move(i*25, 0, 0, 'myP'+str(i), a=True, ws=True)
        for j in range(0,10):
            cmds.duplicate('myP'+str(i), n='myP'+str(i)+str(j))
            cmds.move(i*25, 0, j*25+25, 'myP'+str(i), a=True, ws=True)

'''creates block of buildings with a slope'''
'''for loops, group, duplicate and move them around'''
def makeaBuilding():
    myFinalH = cmds.intSliderGrp(myHeight, query = True, value = True)
    myFinalW = cmds.intSliderGrp(myWidth, query = True, value = True)
    myFinalD = cmds.intSliderGrp(myDepth, query = True, value = True)
    myFinalWBH = cmds.intSliderGrp(widthBetweenHouses, query = True, value = True)


    for i in range (0, 3):
        cube = cmds.polyCube(h = myFinalH, w = myFinalW, d = myFinalD,  n='myCube'+str(i))
        cmds.move(i* myFinalWBH, myFinalH *0.5, 0, 'myCube'+str(i), a=True, ws=True)
        for j in range (0, 3):
            cmds.polyExtrudeFacet( 'myCube'+str(i) + ".f[1]", ltz = 5 , ls =(1,1,1))
            cmds.duplicate('myCube'+str(i),  n='myCube'+str(i)+str(j))
            cmds.move(i* myFinalWBH, myFinalH *0.5 , j* myFinalWBH+myFinalWBH, 'myCube'+str(i), a=True, ws=True)
    cmds.group('myCube0','myCube00', 'myCube01', 'myCube02', 'myCube11', 'myCube12', 'myCube1', 'myCube2', 'myCube21','myCube22' ,'myCube10','myCube20', n = 'g1')
    cmds.move( 190, 0, 190,'g1')

    cmds.duplicate( 'g1', n= 'g2')
    cmds.rotate(0, -180, 0, 'g2')
    cmds.move( 0, 0, 0, 'g2')

    cmds.duplicate('g1', n= 'g4')
    cmds.duplicate('g2', n = 'g5')

    cmds.rotate(0, -90, 0, 'g4')
    cmds.move(180, 0, -10, 'g4')

    cmds.rotate(0, 90, 0, 'g5')
    cmds.move(5, 0, 200, 'g5')

    cmds.refresh(f = True)


'''makes one type of village, uses the same for loop, uses random function'''
'''group the houses, duplicate and move them'''
def makeVillage():
    for i in range(0, 10):
        cmds.polyCube(h=10, w = 10, d=10, n = 'village'+str(i))
        cmds.polyExtrudeFacet( 'village'+str(i) + ".f[1]", ltz = 1.5 , ls =(.6,.4,.0))
        x = random.uniform (10, 80)
        z = random.uniform (10, 80)
        cmds.move( x, 10*0.5 , z, 'village'+str(i))
    cmds.group('village0','village1','village2', 'village3', 'village4', 'village5', 'village6', 'village7', 'village8', 'village9',  n = 'v1')
    cmds.move(80, 0, -15, 'v1')

    cmds.duplicate('v1', n='v3')
    cmds.move(-10, 0, 50)

    cmds.refresh(f = True)


'''makes another type of village, uses for loop, uses random function'''
'''group the houses, duplicate and move them'''
def makeVillage2():
    for j in range(0,10):
        cmds.polyCube(h=10, w = 10, d=10, n = 'vill'+str(j))
        cmds.polyExtrudeFacet( 'vill'+str(j) + ".f[1]", ltz = 1.5 , ls =(.6,.4,.0))
        x = random.uniform (10, 80)
        z = random.uniform (10, 80)
        cmds.move( x, 10*0.5 , z, 'vill'+str(j))
    cmds.group('vill0','vill1','vill2', 'vill3', 'vill4', 'vill5', 'vill6', 'vill7', 'vill8', 'vill9',  n = 'v2')
    cmds.move(85, 0, 60, 'v2')

    cmds.duplicate('v2', n ='v4')
    cmds.move(55, 0, 175, 'v4')

    cmds.refresh(f = True)

'''makes a tree, from a cylinder and a sphere'''
'''the user has to choose the height of the tree'''
'''uses the same input as the width between houses '''
'''for loop, group, duplicate, move'''


def makeTree():
    myFinalTH = cmds.intSliderGrp(myTHeight, query = True, value = True)
    myFinalWBH = cmds.intSliderGrp(widthBetweenHouses, query = True, value = True)

    for i in range (0,3):
        cmds.polyCylinder( h = myFinalTH, sh = 3,  n='tree'+str(i))
        cmds.move(i*myFinalWBH+12, myFinalTH*0.5 , 12, 'tree'+str(i))
        cmds.polySphere(r = 6, sx=6, sy=6, n='sphere'+str(i))
        cmds.move(i*myFinalWBH+12, myFinalTH*0.5+8 , 12, 'sphere'+str(i))
        for j in range (0, 3):
            cmds.duplicate('tree'+str(i), n='tree'+str(i)+str(j) )
            cmds.move(i*myFinalWBH+12, myFinalTH*0.5 , j*myFinalWBH+12, 'tree'+str(i)+str(j),a=True, ws=True)
            cmds.duplicate('sphere'+str(i), n='sphere'+str(i)+str(j) )
            cmds.move(i*myFinalWBH+12, myFinalTH*0.5+8, j*myFinalWBH+12, 'sphere'+str(i)+str(j),a=True, ws=True)
    cmds.group('tree0','tree00', 'tree01', 'tree02', 'tree11', 'tree12', 'tree1', 'tree2', 'tree21','tree22' ,'tree10','tree20', 'sphere0','sphere00', 'sphere01', 'sphere02', 'sphere11', 'sphere12', 'sphere1', 'sphere2', 'sphere21','sphere22' ,'sphere10','sphere20', n = 'g1')
    cmds.move(35, 0, -5,'g6')

    cmds.duplicate('g6', n ='g7')
    cmds.move(-5, 0, 150, 'g7')

    cmds.duplicate('g7', n ='g8')
    cmds.move(170, 0, 35, 'g8')

    cmds.duplicate('g8', n ='g9')
    cmds.move(130, 0, 190, 'g9')

    cmds.refresh(f = True)


'''creates scaled spheres randomly in the sky'''

def makeClouds():
    for i in range (0, 3):
        cmds.polySphere(r = 20, sx=6, sy=6, n='cloud'+str(i))
        cmds.scale(1,0.2,0.5, 'cloud'+str(i))
        x = random.uniform (10,100)
        y = random.uniform (60, 80)
        z = random.uniform (10, 100)
        cmds.move( i*x, y, z, 'cloud'+str(i))
        for j in range(0, 3):
            cmds.duplicate('cloud'+str(i), n = 'cloud'+str(i) +str(j))
            x = random.uniform (10, 100)
            y = random.uniform (60, 80)
            z = random.uniform (10, 100)
            cmds.move( i*x, y, j*z, 'cloud'+str(i) +str(j))
    cmds.refresh(f = True)

'''makes The Sun above the city'''

def makeSun():
    myFinalS =cmds.intSliderGrp(mySun, query = True, value = True)
    cmds.polySphere(r=myFinalS, n = 'sun')
    x = random.uniform (10, 25)
    z = random.uniform (10, 25)
    cmds.move(x,100,z, 'sun')

    cmds.refresh(f = True)

'''deletes city'''

def deleteCity():
    cmds.select(all = True)
    cmds.delete()


'''shows window'''

cmds.showWindow()

