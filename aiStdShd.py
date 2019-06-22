import maya.cmds as cmds
import random

sel_obj=[] #selected objects
shapesInSel=[] #shapes
shadingGrps=[] #SG
shaders=[] #materials

sel_obj=cmds.ls( selection=True )
shapesInSel=cmds.ls( dag=1,o=1,s=1,sl=1 )
shadingGrps = cmds.listConnections(shapesInSel,type='shadingEngine')
shaders = cmds.ls(cmds.listConnections(shadingGrps),materials=1)

#remove u from the list aka conv to string
sel_obj=[str(r) for r in sel_obj]
shapesInSel=[str(r) for r in shapesInSel]
shadingGrps=[str(r) for r in shadingGrps]
shaders=[str(r) for r in shaders]
print sel_obj
print shapesInSel
print shadingGrps
print shaders

aiStd=[]
shdSG=[]
for i in shaders:
    if i=='lambert1':
        aiStd.append( cmds.shadingNode('aiStandardSurface', asShader=True))
        shdSG.append( cmds.sets(name=aiStd[-1]+'SG', empty=True, renderable=True, noSurfaceShader=True))
        cmds.connectAttr(aiStd[-1]+'.outColor', shdSG[-1]+'.surfaceShader')

for i in range(0, len(sel_obj)):
    cmds.select(sel_obj[i])
    cmds.sets( e=True, forceElement=shdSG[i])
    rgb= [random.uniform(0,1),random.uniform(0,1),random.uniform(0,1)]
    cmds.setAttr(aiStd[i]+'.baseColor',rgb[0],rgb[1],rgb[2],type='double3')
