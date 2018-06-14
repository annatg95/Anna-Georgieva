import maya.cmds as cmds
import random
import maya.mel as mel

def randomSquareDistribution():
	selected = cmds.ls(sl=True)
	print len(selected)
	for item in selected:
		x = ( random.random() * 6 - 3 ) + 2  
		z = ( random.random() * 6 - 3 ) - 6
		cmds.xform(item,cp=True )
                mel.eval('move -rpr -y 0')
                mel.eval('SnapToGrid')
                mel.eval('dR_enterForSnap')
		cmds.move(x,0.,z,item,r=True)
                
randomSquareDistribution()        


import maya.cmds as cmds
import random

def applyLambertRandocmdsolour():
	selected = cmds.ls(sl=True)
	size=len(selected)
	for item in selected:
		cmds.shadingNode('lambert', asShader=True)
		cmds.sets(r=True,nss=True,em=True,n='lambert'+str(i)+'SG')
		cmds.sets(e=True,fe='lambert'+str(item)+'SG')
		cmds.defaultNavigation(ce=True,s='lambert'+str(item), d='lambert'+str(item)+'SG')
		#cmds.connectAttr('lambert'+str(item)+'.outColor', 'lambert'+str(i)+'SG'+'.surfaceShader',f=True)
		#r=random.random();
		#g=random.random();
		#b=random.random();
		#cmds.setAttr(lambert+item+'.colour',r,g,b)
		
		
def printstuff():
	selected = cmds.ls(sl=True)
	size=len(selected)
	for i in range(0,size):
		print(i)
		
		
		
applyLambertRandocmdsolour()

for i in range(0,5):
    print("str"+str(i))

import maya.cmds as cmds
x=1
selected = cmds.ls(sl=True)
size=len(selected)
for i in range(1,size):
	shader=cmds.shadingNode("lambert",asShader=True)
	cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name="lambert" )
	shading_group= cmds.sets(renderable=True,noSurfaceShader=True,empty=True)
	cmds.connectAttr('%s.outColor' %shader ,'%s.surfaceShader' %shading_group)
	
for item in selected:
	#print len(selected)
	while x<size:
		cmds.select(item)
		print(cmds.listConnections(selected, c=True))
		cmds.sets(item, e=True,fe="set"+str(x))
		x+=1
		print x


def getConnections( selected ):
    connections = cmds.listConnections(selected, c=True)
    for connection in connections: 
        print connection
		
import maya.cmds as mc

Shader = mc.ls(type = 'surfaceShader')
for i in Shader:
    con = mc.listConnections('%s.outColor' % i)
    names = mc.listConnections(con, type="mesh")
    print i, "->", ", ".join(names)
	
	
metal = cmds.shadingNode("blinn", asShader=True, name ="metalMat")
cmds.setAttr(metal + ".color", 0.667,0.317,0.131)
cmds.setAttr(metal + ".eccentricity", 0.421)
cmds.setAttr(metal + ".specularRollOff", 0.972)
cmds.setAttr(metal + ".specularColor", 0.703,0.703,0.703)
cmds.setAttr(metal + ".reflectivity", 0.538)
cmds.setAttr(metal + ".reflectedColor", 0.310,0.310,0.310)

# Assing Material
# Create Sureface Shader
cmds.sets( renderable=True, noSurfaceShader=True, empty=True, name="gearShader" )
# Connect material to shader
cmds.connectAttr("metalMat.outColor", "gearShader.surfaceShader")
# Assign shader to objects
cmds.sets("smallGearGeo", edit=True, forceElement="gearShader")
cmds.sets("largeGearGeo", edit=True, forceElement="gearShader")



string $materials[] = `ls -sl` ;

for($mat in $materials)
{
	string $attrs[] = `listAttr -v -k -u $mat` ;

	for($a in $attrs)
	{
		$randomR = rand(0,1);
		$randomG = rand(0,1);
		$randomB = rand(0,1);
		
		if($a == "colorR")
		{
			setAttr ($mat + ".colorR") $randomR  ;
		}
		if($a == "colorG")
		{
			setAttr ($mat + ".colorG") $randomG  ;
		}       
		if($a == "colorB")
		{
			setAttr ($mat + ".colorB") $randomB  ;
		}     
	}
}