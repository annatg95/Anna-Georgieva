import maya.cmds as cmds
import random

selected = cmds.ls(sl=True)
print len(selected)
for item in selected:
	number=random.uniform(0.8,1.0)
	cmds.move( 0, -1.45, 0,item+'.scalePivot',r=True )
	cmds.setAttr( item+'.scaleY', number )	