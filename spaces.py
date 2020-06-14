import maya.cmds as cmds

widgets={}

def spaceMatchUI():
    if cmds.window("window", exists=True):
        cmds.deleteUI("window", window=True)

    widgets["win"]=cmds.window("window", title="spaceMatch",w=300, h=400)
    widgets["topFrame"]=cmds.frameLayout(l="object.selection", w=300)
    widgets["topColumn"]=cmds.columnLayout()

    widgets["objTFG"]=cmds.textFieldGrp(l="selected Object", w=300)
    widgets["objButton"]=cmds.button(l="select obj", w=300, c=getObj)

    cmds.setParent(widgets["win"])
    widgets["bottomFrame"]=cmds.frameLayout(l="space seelction", w=300)
    widgets["topColumn"]=cmds.columnLayout()

    cmds.showWindow(widgets["win"])

def getObj():
    sel=cmds.ls(sl=True)[0]
    cmds.textFieldGrp(widgets["objTFG"], e=True, tx=sel)

    attrT="%s.translate"%sel
    attrR="%s.rotate"%sel
    valuesT=cmds.attributeQuery("translate", node=sel, le=True)[0]
    valuesR=cmds.attributeQuery("rotate", node=sel, le=True)[0]
    print valuesT
    print valuesR


def spaceMatchTute():
    spaceMatchUI()
