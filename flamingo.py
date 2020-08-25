import maya.cmds as cmds
import maya.mel as mel
#create first def then classes

def countCVS(curveSurfaceName):
    cvs=[]
    if cmds.objectType( curveSurfaceName+"Shape", isType='nurbsCurve' ):
        degs = cmds.getAttr( curveSurfaceName+'.degree' )
        spans = cmds.getAttr( curveSurfaceName+'.spans' )
        cvs.append(degs+spans)

    elif cmds.objectType( curveSurfaceName+"Shape", isType='nurbsSurface' ):
        numSpansU= cmds.getAttr(curveSurfaceName + ".spansU" )
        degreeU= cmds.getAttr (curveSurfaceName + ".degreeU" )

        numSpansV = cmds.getAttr(curveSurfaceName + ".spansV" )
        degreeV   = cmds.getAttr(curveSurfaceName + ".degreeV" )

        spansUV = numSpansU+numSpansV
        degreeUV=degreeU+degreeV
        cvs.append(degreeUV+spansUV)

    return cvs

def IK_FK_Res_merge(all_jnts, clusterList, jntGroup):
    '''
    for x in all_jnts:
        for y in x:
            print y
    print clusterList
    print jntGroup
    '''
    rot_nodes=[]
    tr_nodes=[]
    rib_tr_nodes=[]
    multMat_nodes=[]
    decomposeMat_nodes=[]

    for i in range(0, len(all_jnts[3])):
        tr_nodes.append(cmds.shadingNode( 'blendColors', asUtility=True, n="tr_blendNode"+str(i)))
        rot_nodes.append(cmds.shadingNode( 'blendColors', asUtility=True, n="rot_blendNode"+str(i)))
        rib_tr_nodes.append(cmds.shadingNode( 'blendColors', asUtility=True, n="rib_tr_blendNode"+str(i)))
        multMat_nodes.append(cmds.shadingNode( 'multMatrix', asUtility=True, n="multMat_nodes"+str(i)))
        decomposeMat_nodes.append(cmds.shadingNode( 'decomposeMatrix', asUtility=True, n="decomposeMat_nodes"+str(i)))

    for ik, fk, tr, rot in zip(all_jnts[1], all_jnts[2], tr_nodes, rot_nodes):
        cmds.connectAttr(ik+".translate", tr+".color1", f=True)
        cmds.connectAttr(fk+".translate", tr+".color2", f=True)
        cmds.connectAttr(ik+".rotate", rot+".color1", f=True)
        cmds.connectAttr(fk+".rotate", rot+".color2", f=True)

    for jntGrp, multMat, decomposeMat, resJnt in zip(jntGroup, multMat_nodes, decomposeMat_nodes, all_jnts[3]):
        cmds.connectAttr(jntGrp+".worldMatrix[0]", multMat+".matrixIn[0]")
        cmds.connectAttr(resJnt+".parentInverseMatrix[0]",  multMat+".matrixIn[1]")
        cmds.connectAttr(multMat+".matrixSum", decomposeMat+".inputMatrix")

    for decomposeMat, rib_tr_n in zip(decomposeMat_nodes, rib_tr_nodes):
        cmds.connectAttr(decomposeMat+".outputTranslate", rib_tr_n+".color2")

    for i in range(0, len(all_jnts[3])):
        cmds.connectAttr(rot_nodes[int(i)]+".output", all_jnts[3][i]+".rotate", f=True)
        cmds.connectAttr(tr_nodes[int(i)]+".output", rib_tr_nodes[i]+".color1", f=True)

    for x,y in zip(rib_tr_nodes, all_jnts[3] ):
        cmds.connectAttr(x+".output", y+".translate", f=True)

    #crete enum attribute ik fk for 0 and 1 to plug in the blenders
    #create enum attribute for ribbon on off 0 and 1 to plug in the blender and done



def build_spine(*args):
    nurbsProperties=[]
    #build your curve based on the joints pos
    if cmds.objExists("curve1"):
        originalCrv=cmds.rename("curve1","originalCrv")
        duplicatedCrv=cmds.duplicate(originalCrv, n="duplicatedCrv")
        cmds.xform(originalCrv,r=True, t=(-5, 0, 0) )
        cmds.xform(duplicatedCrv,r=True, t=(5, 0, 0) )
        loftName=cmds.loft(duplicatedCrv, originalCrv, ch=1, u=1, c=0, ar=1, d=3, ss=1, rn=0, po=0, rsn=True,n="originalSurface" )

        originalCrvNumber=countCVS(originalCrv)
        #print originalCrvNumber
        select_cvs=originalCrvNumber[0]-1

        cmds.select(loftName[0]+".cv[0:"+str(select_cvs)+"][0]")
        mel.eval('createHair 8 8 2 0 0 0 0 5 0 1 2 2;')
        cmds.delete('hairSystem1','pfxHair1','nucleus1')
        follicle_grp=cmds.rename('hairSystem1Follicles', 'spine_follicles_grp')

        folName = 'spine_follicle'
        folList = cmds.ls(loftName[0]+'Follicle*',transforms=True)
        for i in folList:
            cmds.rename(i,folName)

        folList = cmds.listRelatives(follicle_grp)
        crvList=cmds.ls('curve*',transforms=True)
        cmds.select(crvList, replace=True)
        cmds.delete(crvList)

        jntList=[]
        jntGroup=[]
        for i in range(0, originalCrvNumber[0]-2):
            cmds.joint(n="ribbon_jnt"+str(i), p=(0, 0, 0), rad=1 )
            cmds.group("ribbon_jnt"+str(i),n="ribbon_jnt_grp"+str(i))
            jntList.append("ribbon_jnt"+str(i))
            cmds.select(clear=True)
            jntGroup.append("ribbon_jnt_grp"+str(i))

        for i,j in zip(jntGroup, folList):
            cmds.parent(i,j)

        for i in jntGroup:
            cmds.setAttr(i+".translateX", 0)
            cmds.setAttr(i+".translateY", 0)
            cmds.setAttr(i+".translateZ", 0)

        #redo the nurbsSurface
        loftName2=cmds.duplicate(loftName, n="duplicatedSurface")
        set_su=4    #user input
        set_sv=1    #preferrably one no user input
        cmds.rebuildSurface(loftName2, rpo=1, rt=0, end=1, kr=0, kcp=0, kc=0, su=set_su, du=3, sv=set_sv, dv=1, tol=12, fr=0, dir=2)

        # connect the created joints to the loftName2
        cmds.connectAttr(loftName2[0]+"Shape.local", folName+"Shape.inputSurface", force=True)
        cmds.connectAttr(loftName2[0]+"Shape.parentInverseMatrix[0]", folName+"Shape.inputWorldMatrix", force=True)
        for i in range(1,  originalCrvNumber[0]):
            cmds.connectAttr(loftName2[0]+"Shape.local", folName+"Shape"+str(i)+".inputSurface", force=True)
            cmds.connectAttr(loftName2[0]+"Shape.parentInverseMatrix[0]", folName+"Shape"+str(i)+".inputWorldMatrix", force=True)

        #create clusters
        duplicatedCrvNumber=countCVS(loftName2[0])
        clusterList=[]
        for i in range(0, duplicatedCrvNumber[0]-2):
            clusterName=cmds.cluster(loftName2[0]+".cv["+str(i)+"][0:1]")
            clusterList.append(clusterName)

        clusterList=cmds.ls('cluster*',transforms=True)
        cmds.select(clusterList)
        cmds.group(n="clusterGrp")

        for i in ["originalSurface", "duplicatedCrv", "originalCrv"]:
            cmds.setAttr(i+".v", 0)
        #create controllers and parentConstraint Done

        ik_jnts=[]
        fk_jnts=[]
        res_jnts=[]
        all_jnts=[jntList,ik_jnts, fk_jnts, res_jnts]
        for j in range(0, len(all_jnts[0])):
            cmds.duplicate(all_jnts[0][j], n="IK_jnt"+str(j),rr=True)
            ik_jnts.append("IK_jnt"+str(j))

            cmds.duplicate(all_jnts[0][j], n="FK_jnt"+str(j),rr=True)
            fk_jnts.append("FK_jnt"+str(j))

            cmds.duplicate(all_jnts[0][j], n="RES_jnt"+str(j),rr=True)
            res_jnts.append("RES_jnt"+str(j))


        for x,y,z in zip(all_jnts[1], all_jnts[2], all_jnts[3]):
            cmds.parent(x,y,z,world=True)

        a=len(jntList)-1
        while(a>0):
            for b in [all_jnts[1], all_jnts[2], all_jnts[3]]:
                cmds.parent(b[a],b[a-1])
            a=a-1

        return all_jnts, clusterList, jntGroup
    else:
        print("create a curve1 first")
        return None


jnts, cls, rib_jnt_grp=build_spine()
IK_FK_Res_merge(jnts, cls, rib_jnt_grp)

'''
def a(b):
    print b

def init_window():
    window="window"
    if cmds.window(window, exists=True):
		cmds.deleteUI(window)
    window = cmds.window( title="Ribbon Rig", widthHeight=(200, 300) )
    cmds.columnLayout( adjustableColumn=True )

    cmds.text(label='nurbsW')
    set_nurbsW = cmds.textField("set_nurbsW", tx="enter integer number here")
    cmds.text(label='nurbsL')
    set_nurbsL = cmds.textField("set_nurbsL", tx="enter integer number here")
    get_nurbsW= cmds.textField(set_nurbsW, q=True, text=True)
    get_nurbsL = cmds.textField(set_nurbsL, q=True, text=True)
    cmds.button(label="get_nurbsW", command=lambda _:a(get_nurbsW))
    cmds.button(label="get_nurbsL", command=lambda _:a(get_nurbsL))

    all_jnts=[] ###fix 47
    cmds.button( label='Build the Ribbon', command=lambda _: build_spine())
    cmds.button( label='Merge with IK/FK the Ribbon', command=lambda _: IK_FK_Res_merge(all_jnts))
    cmds.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') )
    cmds.setParent( '..' )
    cmds.showWindow( window )

init_window()
'''
