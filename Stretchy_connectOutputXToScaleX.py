import maya.cmds as cmds
import random

#select the wanted joint chain  
selected = cmds.ls(sl=True)
print len(selected)
for item in selected:
	print(item+'.scaleX')
	cmds.connectAttr('multiplyDivide1.outputX', item+'.scaleX' ,f=True) 
	

