selection=cmds.ls(sl=1)
for i in selection:
	facesE=cmds.polyExtrudeFacet(ch=1, kft=1)
	cmds.select(clear=1)
	faceN = [str(j) for j in facesE]
	cmds.setAttr(faceN[0]+".thickness", 3)
	cmds.select(clear=1)
	cmds.setAttr(faceN[0]+".localTranslateZ", 0.1)
	cmds.select(clear=1)
	cmds.setAttr(faceN[0]+".divisions", 2)
	cmds.select(clear=1)
	cmds.setAttr(faceN[0]+".offset", 0.5)
	cmds.select(clear=1)
