import maya.cmds as cmds
import os.path

sel=cmds.ls( selection=True )
cmds.select( sel )
outputDir = cmds.workspace (query = True, dir = True)

for i in sel:
    path = os.path.join(outputDir,"redo_shapes_final/"+str(i)+".obj")
    cmds.select(i,replace=True)
    cmds.file(path,pr=1,typ="OBJexport",es=1,op="groups=0; ptgroups=0;materials=0; smoothing=0; normals=0")
    cmds.select(clear)
#exports everything the same 
