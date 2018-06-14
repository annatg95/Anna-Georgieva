import maya.cmds as mc
import math
import random

def uniformRandom():
    for i in range(100):
        mc.polyCube()
        x = random.uniform(-1,1) * 5  # these are the same
        z = random.random() * 10 - 5  # this does the same as above
        mc.move(x,0.,z)


def triangularRandom():
    for i in range(100):
        mc.polySphere(r=0.2)
        x = random.triangular(-10,10,-9)
        z = random.triangular(0,-5, 0)
        mc.move(x,0.,z)    
        
        
def betavariateRandom():
    for i in range(100):
        mc.polySphere(r=0.2)
        x = random.betavariate(0.5,0.5) * 10
        z = random.betavariate(1.,3.) * 10
        mc.move(x,0.,z)


def randomSquareDistribution():
    for i in range(100):
        mc.polyCube()
        x = ( random.random() * 6 - 3 ) + 2  
        z = ( random.random() * 6 - 3 ) - 6  
        mc.move(x,0.,z)
        

def randomCircularDistribution():
    radius = 10
    for i in range(200):
        mc.polyCube()
        r = random.random() * radius
        theta = random.random() * 2 * math.pi
        x = r * math.cos(theta)
        z = r * math.sin(theta) 
        mc.move(x,0.,z)
        
def CircularDistribution():
    radius = 10
    for i in range(200):
        mc.polyCube()
        r = random.random() * radius
        theta =  2 * math.pi
        x = r * math.cos(theta)
        z = r * math.sin(theta) 
        mc.move(x,0.,z)
