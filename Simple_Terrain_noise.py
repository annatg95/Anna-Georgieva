import maya.cmds as cmds
import math
import random
import maya.mel as mel

#simple terrain noise

def getVtxPos(objectname,minX,minY,minZ,maxX,maxY,maxZ):
	
	vtxWorldPos = []
	vtxIndexList = cmds.getAttr( objectname+".vrts", multiIndices=True )

	for i in range(1,8):
		for j in range(1,8):
			t=(i+10)*j #formula (1+10)*1=11 (2+10)*1=12 starts from 11th vtx and continues until the end. 0-10 vtx not changed!
		   
			curPointPos = cmds.xform(str(objectname)+".pnts["+str(t)+"]", q=True, t=True, ws=True ) 
			moveX=random.randint(minX,maxX)/100.0
			moveZ=random.randint(minY,maxY)/100.0
			moveY=random.randint(minZ,maxZ)/100.0 
			curPointPos[0]+=moveX
			curPointPos[1]+=moveY		
			curPointPos[2]+=moveZ
			cmds.xform( str(objectname)+".vtx["+str(t)+"]", t=curPointPos, ws=True )   
	   
			vtxWorldPos.append( curPointPos )

def createPlane(height,width):
	cmds.polyPlane(h=height,w=width, ch=0)
	dimensions=[height,width]
	print dimensions[0]
	print dimensions[1]
	return dimensions

def UI():
	windowID = 'terrainGen'
	if cmds.window(windowID, exists=True):
		cmds.deleteUI(windowID)

	
	#creates the window
	window = cmds.window(windowID,title="Terrain UI", w=100,h=200, sizeable=True)
	cmds.columnLayout(cmds.columnLayout( adjustableColumn=True ))
	cmds.text( l='Create a plane h/w')
	height=cmds.intSliderGrp(field=True, label='height', minValue=0, maxValue=100, value=10)
	width=cmds.intSliderGrp(field=True, label='width', minValue=0, maxValue=100, value=10)

	cmds.button( l='1.PLANE', command=lambda *args:createPlane((cmds.intSliderGrp(height ,query = True, value = True)),
																(cmds.intSliderGrp(width ,query = True, value = True))))
	minX=cmds.intSliderGrp(field=True, label='minX', minValue=-50, maxValue=1, value=-20)
	minY=cmds.intSliderGrp(field=True, label='minY', minValue=-50, maxValue=1, value=-45)
	minZ=cmds.intSliderGrp(field=True, label='minZ', minValue=-50, maxValue=1, value=-30)
	maxX=cmds.intSliderGrp(field=True, label='maxX', minValue=1, maxValue=50, value=20)
	maxY=cmds.intSliderGrp(field=True, label='maxY', minValue=1, maxValue=50, value=35)
	maxZ=cmds.intSliderGrp(field=True, label='maxZ', minValue=1, maxValue=50, value=40)

	cmds.button( l='1.Create', command=lambda *args:getVtxPos('pPlane1',(cmds.intSliderGrp(minX ,query = True, value = True)),
															(cmds.intSliderGrp(minY ,query = True, value = True)),
															(cmds.intSliderGrp(minZ ,query = True, value = True)),
															(cmds.intSliderGrp(maxX ,query = True, value = True)),
															(cmds.intSliderGrp(maxY ,query = True, value = True)),
															(cmds.intSliderGrp(maxZ ,query = True, value = True))))

	cmds.showWindow() 

if __name__ == "__main__":
	UI()
