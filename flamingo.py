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

def hide_obj(*args):
    for i in args:
        cmds.setAttr(i+".v", 0)

def create_ctrl(ctrl_name, jnt, choice, radius):
    cmds.select(all=True)
    created_ctrl=cmds.circle( n=ctrl_name, nr=(0, 0, 1), c=(0, 0, 0),r=radius )
    rubbishGrp=cmds.group(ctrl_name,n=ctrl_name+"_grp")
    parent_constr=cmds.parentConstraint(jnt, rubbishGrp)
    cmds.delete(parent_constr[0])

    if choice==1:
        for i in ["X", "Y", "Z"]:
            cmds.setAttr(created_ctrl[0]+".translate"+i, 0)
            cmds.setAttr(created_ctrl[0]+".rotate"+i, 0)
    elif choice==2:
        cmds.makeIdentity(created_ctrl[0], apply=True, t=1, r=1, s=1)

    return rubbishGrp

def IK_FK_Res_merge(all_jnts, jntGroup, duplicatedCrv):

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

    #controllers for the ribbon and the ik/fk
    ribbon_ctrl=cmds.listRelatives(create_ctrl("ribbon_switch", all_jnts[3][0], 2, 10 ))
    ik_fk_ctrl=cmds.listRelatives(create_ctrl("ikFk_switch",all_jnts[3][-1], 2, 10 ))

    cmds.addAttr(ribbon_ctrl[0],ln="ribbon",at="enum",en="on:off:", keyable=True)
    cmds.addAttr(ik_fk_ctrl[0],ln="neck_spine_ctrl",at="enum",en="ik:fk:", keyable=True)

    reverse_Node=cmds.shadingNode( 'reverse', asUtility=True, n="ik_fk_reverseNode")
    cmds.connectAttr( ik_fk_ctrl[0]+".neck_spine_ctrl", reverse_Node+".inputX", f=True)

    for i, j, k in zip(tr_nodes, rot_nodes, rib_tr_nodes):
        cmds.connectAttr(reverse_Node+".outputX", i+".blender", f=True)
        cmds.connectAttr(reverse_Node+".outputX", j+".blender", f=True)
        cmds.connectAttr( ribbon_ctrl[0]+".ribbon", k+".blender", f=True)

    #create ik spline handle and clusters
    ik_spline_crv=cmds.duplicate(duplicatedCrv, n="ik_spline_crv")
    cmds.setAttr(ik_spline_crv[0]+".visibility",1)
    cmds.ikHandle(n="spine_ikSpline", sj=all_jnts[1][0], ee=all_jnts[1][-1], c=ik_spline_crv[0], sol="ikSplineSolver", ccv=False)

    #add clusters for ik curve
    ik_curve_cvs=countCVS(ik_spline_crv[0])
    ik_clusterList=[]
    for i in range(0, ik_curve_cvs[0]-2):
        clusterName=cmds.cluster(ik_spline_crv[0]+".cv["+str(i)+"]", n="ik_clu_"+str(i))
        ik_clusterList.append(clusterName)

    ik_clusterList=cmds.ls('ik_clu_*',transforms=True)
    cmds.group(ik_clusterList , n="ik_clusterGrp")

    ik_clu_ctrlList=[]
    for i in ik_clusterList:
        ik_clu_ctrlList.append(create_ctrl(str(i)+"_ctrl", i, 2, 5))
    cmds.group( ik_clu_ctrlList, n="ik_cluCtrlGrp")

    return ik_clusterList,ik_clu_ctrlList

def grouping_main():

    cmds.group("originalCrv", "duplicatedCrv", "originalSurface", "duplicatedSurface", "spine_follicles_grp", "ribbon_clusterGrp", n="spine_rib_rig")
    cmds.group("IK_jnt0", "FK_jnt0", "RES_jnt0", n="spine_actual_jnts")
    cmds.group("ribbon_switch_grp", "ikFk_switch_grp", "rib_cluCtrlGrp", "ik_cluCtrlGrp", "ik_spline_crv", n="spine_ctrl_grp")
    cmds.group("spine_ikSpline", "ik_clusterGrp", n="spine_ik_rig")

    cmds.group("spine_ctrl_grp", "r_leg_ik_ctrl_grp","l_leg_ik_ctrl_grp", "r_leg_fk_ctrl_grp","l_leg_fk_ctrl_grp", n="CTRL_grp")
    cmds.group("l_leg_jnt", n="l_leg_jnts")
    cmds.group("r_leg_jnt", n="r_leg_jnts")
    cmds.group("spine_rib_rig", "spine_ik_rig", "spine_actual_jnts", "r_all_ik_grp","l_all_ik_grp", "r_leg_jnts", "l_leg_jnts", n="RIG_grp")

def parent_ctrl_clu(name_clu, name_ctrl):
    for i, j in zip(name_clu, name_ctrl):
        cmds.parentConstraint(cmds.listRelatives(j), i)

def keyVisibility(jnts, ik_ctrl):
    cmds.setAttr("ribbon_clusterGrp"+".v", 0)
    cmds.setAttr("ik_clusterGrp"+".v", 0)
    fk_jnts=jnts[2]

    fk_ctrl=[]
    del_grp=[]
    #havent done the fk_ctrls so parenting shapes not using create_ctrl
    #MESSY
    for i in fk_jnts:
        cmds.circle( n=i+"_ctrl", nr=(0, 0, 1), c=(0, 0, 0),r=3 )
        del_grp.append(i+"_ctrl")
        fk_ctrl.append(i+"_ctrlShape")

    for x, y in zip(fk_ctrl, fk_jnts):
        cmds.parent(x,y, r=1, s=1)
    cmds.delete(del_grp)

    if cmds.getAttr("ribbon_switch.ribbon")==0: #original value is on==0
        revN_rib_Vis=cmds.shadingNode( 'reverse', asUtility=True, n="revN_ribbonVis")
        conditionNode=cmds.shadingNode("condition", asUtility=True, n="VisCondition")
        cmds.connectAttr("ribbon_switch.ribbon", conditionNode+".firstTerm", f=True)
        cmds.connectAttr(conditionNode+".outColorR", revN_rib_Vis+".inputX", f=True)
        cmds.connectAttr(conditionNode+".outColorR" , "ikFk_switch.v", f=True)
        cmds.connectAttr(conditionNode+".outColorR" , "FK_jnt0.v", f=True)
        cmds.connectAttr(conditionNode+".outColorR" , "ik_cluCtrlGrp.v", f=True)
        cmds.connectAttr(revN_rib_Vis+".outputX",  "rib_cluCtrlGrp.v", f=True)

    for i in ik_ctrl:
        cmds.connectAttr("ik_fk_reverseNode.outputX", i+".v", f=True)

    cmds.group(fk_jnts[0], n="FK_vis_grp")
    cmds.connectAttr("ikFk_switch.neck_spine_ctrl", "FK_vis_grp.v", f=True)

    cmds.setAttr("IK_jnt0.v", 0)
    cmds.setAttr("spine_follicles_grp.v", 0)

def build_spine(*args):
    nurbsProperties=[]
    #build your curve based on the joints pos
    if cmds.objExists("curve1"):
        originalCrv=cmds.rename("curve1","originalCrv")
        duplicatedCrv=cmds.duplicate(originalCrv, n="duplicatedCrv")
        cmds.xform(originalCrv,r=True, t=(-1, 0, 0) )
        cmds.xform(duplicatedCrv,r=True, t=(0, 0, 0) )  #the joints lie here
        loftName=cmds.loft(duplicatedCrv, originalCrv, ch=1, u=1, c=0, ar=1, d=3, ss=1, rn=0, po=0, rsn=True,n="originalSurface" )

        originalCrvNumber=countCVS(originalCrv)
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
        set_su=8    #user input 15
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
        rib_clusterList=[]
        for i in range(0, duplicatedCrvNumber[0]-2):
            clusterName=cmds.cluster(loftName2[0]+".cv["+str(i)+"][0:1]", n="rib_clu_"+str(i) )
            rib_clusterList.append(clusterName)

        rib_clusterList=cmds.ls('rib_clu_*',transforms=True)
        cmds.group(rib_clusterList, n="ribbon_clusterGrp" )

        rib_clu_ctrlList=[]
        for i in rib_clusterList:
            rib_clu_ctrlList.append(create_ctrl(str(i)+"_ctrl", i, 2, 5))

        cmds.group( rib_clu_ctrlList, n="rib_cluCtrlGrp")
        hide_obj("originalSurface", "duplicatedCrv", "originalCrv")

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

        return  all_jnts, rib_clusterList, rib_clu_ctrlList, jntGroup, duplicatedCrv
    else:
        print("create a curve1 first")
        return None

def setPrefAngle(jnt, rot_angle):
    cmds.setAttr(jnt+".rotateZ", rot_angle)
    cmds.joint(jnt, e=True, spa=True ,ch=True)
    cmds.setAttr(jnt+".rotateZ", 0)

def build_RP_IK_handle(startJnt, endEffetor,side_leg, addPV):
    ik_objects=cmds.ikHandle(n=endEffetor+"_ik_hdl", sj=startJnt, ee=endEffetor)
    cmds.rename(ik_objects[1], endEffetor+"_effector")

    if addPV==True:
        mid_jnt=cmds.listRelatives(startJnt)

        PV_locator=cmds.spaceLocator(n=mid_jnt[0]+"_knee_loc")
        mid_jnt_pos=cmds.xform(mid_jnt[0], t=True, q=True, ws=True)
        cmds.xform(PV_locator[0], t=mid_jnt_pos)

        if mid_jnt[0].endswith("_ankle_jnt"):
            cmds.setAttr(mid_jnt[0]+"_knee_loc.translateZ", -20)
            for i in ["X", "Y", "Z"]:
                cmds.setAttr(mid_jnt[0]+"_knee_locShape.localScale"+i, 15)
        elif mid_jnt[0].endswith("extra_toe_jnt"):
            cmds.setAttr(mid_jnt[0]+"_knee_loc.translateY", 7)
            cmds.setAttr(mid_jnt[0]+"_knee_loc.translateZ", -8)
            for i in ["X", "Y", "Z"]:
                cmds.setAttr(mid_jnt[0]+"_knee_locShape.localScale"+i, 5)
        else:
            cmds.setAttr(mid_jnt[0]+"_knee_loc.translateY", 5)
            for i in ["X", "Y", "Z"]:
                cmds.setAttr(mid_jnt[0]+"_knee_locShape.localScale"+i, 5)

        cmds.makeIdentity(PV_locator[0], apply=True, t=1, r=1, s=1)

        PV_name=cmds.poleVectorConstraint(PV_locator[0] , ik_objects[0] )
        cmds.rename(PV_name[0], PV_name[0]+"_PV_constr")
    else:
        print("no need for PV")

    return ik_objects

def build_SC_IK_handle(startJnt, endEffetor):
    sc_handle=cmds.ikHandle(n=endEffetor+"_sc_ik_hdl",sj=startJnt, ee=endEffetor,  sol="ikSCsolver")
    return sc_handle

def build_limbs(leg_side):
    leg_side_jnt_list=[ leg_side+"_leg_jnt", leg_side+"_knee_jnt", leg_side+"_ankle_jnt",  leg_side+"_help_jnt", leg_side+"_toes_jnt"]
    leg_side_l_jnts=[leg_side+"_l_toe_jnt", leg_side+"_l_toe_jnt_1", leg_side+"_l_toe_jnt_2", leg_side+"_l_toe_jnt_3"]
    leg_side_mid_jnts=[leg_side+"_middle_toe_jnt", leg_side+"_middle_toe_jnt_1", leg_side+"_middle_toe_jnt_2",  leg_side+"_middle_toe_jnt_3"]
    leg_side_r_jnts=[leg_side+"_right_toe_jnt", leg_side+"_right_toe_jnt_1", leg_side+"_right_toe_jnt_2", leg_side+"_right_toe_jnt_3"]
    leg_side_extra_jnts=[leg_side+"_extra_toe_jnt", leg_side+"_extra_toe_jnt_1", leg_side+"_extra_toe_jnt_2", leg_side+"_extra_toe_jnt_3"]
    all_limbs_jnts=[leg_side_jnt_list, leg_side_l_jnts, leg_side_mid_jnts, leg_side_r_jnts, leg_side_extra_jnts]

    for x in all_limbs_jnts:
        for y in x:
            if cmds.objExists(y)!=1:
                print("missing jnt", y)
            else:
                pass

    if leg_side=="l":
        for i in all_limbs_jnts:
            cmds.joint(i[0], e=True, oj="xyz", sao="yup", ch=True, zso=True)
    else:
        pass

    first_toe_jnts=[leg_side_l_jnts[0],leg_side_mid_jnts[0],leg_side_r_jnts[0]]
    cmds.parent(first_toe_jnts, leg_side_jnt_list[-1])
    cmds.parent(leg_side_extra_jnts[0], leg_side_jnt_list[3])

    #which jnts need RP IK with a PV
    setPrefAngle(leg_side_jnt_list[2], 15)
    ik_main=build_RP_IK_handle(leg_side_jnt_list[1], leg_side_jnt_list[3], leg_side,True) #main leg
    sc_main=build_SC_IK_handle(leg_side_jnt_list[3], leg_side_jnt_list[-1])
    ik_main_grp=cmds.group( ik_main[0], sc_main[0], n=leg_side+"_main_ik_grp")

    ik_rp_List=[]
    ik_sc_List=[]
    ctrl_List=[]
    for i in [leg_side_l_jnts, leg_side_mid_jnts, leg_side_r_jnts, leg_side_extra_jnts]:
        setPrefAngle(i[1], -15)
        ctrl_List.append(create_ctrl(i[1]+"_FK_ctrl",i[-1], 1, 5))
        ik_sc_List.append(build_SC_IK_handle(i[-2], i[-1]))
        ik_rp_List.append(build_RP_IK_handle(i[0], i[2], leg_side ,True))

    #create IK_controller for the main leg and FK_controller for the startJoint
    ik_controller=create_ctrl(leg_side+"_leg_ik_ctrl", leg_side_jnt_list[3], 1, 10 )
    fk_controller=create_ctrl(leg_side+"_leg_fk_ctrl", leg_side_jnt_list[0], 1, 8 )

    name_List=[leg_side+"_l_ik_grp", leg_side+"_m_ik_grp",  leg_side+"_r_ik_grp", leg_side+"_e_ik_grp"]
    grp_returnList=[]
    for x,a,b in zip(name_List, ik_sc_List, ik_rp_List):
        grp_returnList.append(cmds.group(a[0], b[0], n=x))


    ik_ctrl=cmds.listRelatives(ik_controller)
    for x in ctrl_List:
        cmds.parent(x,ik_ctrl)

    cmds.parent(cmds.ls(type="locator"), cmds.listRelatives(ik_controller))
    fk_ctrl=cmds.listRelatives(fk_controller)
    cmds.connectAttr(fk_ctrl[0]+".rotate",  leg_side_jnt_list[0]+".rotate", f=True)

    ctrl_ToeList=[]
    for i in ctrl_List:
        ctrl_ToeList.append(cmds.listRelatives(i))

    for i, j in zip(name_List, ctrl_List):
        ctrl_pos=cmds.xform(j, t=True, q=True, ws=True)
        cmds.xform(i, piv=ctrl_pos)
    ctrl_main_pos=cmds.xform(leg_side_jnt_list[4], t=True, q=True, ws=True)
    cmds.xform(ik_main_grp, piv=ctrl_main_pos)

    for i, j in zip(ctrl_ToeList, name_List):
        cmds.parentConstraint(i[0], j ,mo=True)
    cmds.parentConstraint(ik_ctrl,ik_main_grp ,mo=True)
    leg_side_all_ik_grp=cmds.group( grp_returnList, ik_main_grp, n=leg_side+"_all_ik_grp")
    cmds.parent(leg_side+"_ankle_jnt_knee_loc", leg_side+"_leg_ik_ctrl_grp")
    #cmds.setAttr("spine_ikSpline.v",0)

def build_wings():
    print("aaa")

jnts, rib_clu, rib_ctrl, rib_jnt_grp, dup_crv=build_spine()
ik_clu,ik_ctrl=IK_FK_Res_merge(jnts ,rib_jnt_grp, dup_crv)

build_limbs("l")
build_limbs("r")

grouping_main()
parent_ctrl_clu(ik_clu, ik_ctrl)
parent_ctrl_clu(rib_clu, rib_ctrl)
keyVisibility(jnts, ik_ctrl)

'''
def init_window():
    window="window"
    if cmds.window(window, exists=True):
		cmds.deleteUI(window)
    window = cmds.window( title="Ribbon Rig", widthHeight=(200, 300) )
    cmds.columnLayout( adjustableColumn=True )

    cmds.text(label='nurbsW')


    cmds.button( label='Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') )
    cmds.setParent( '..' )
    cmds.showWindow( window )

init_window()
'''
