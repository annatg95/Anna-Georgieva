import maya.cmds as cmds

#create a window with 6 buttons
#left/right ik to fk
#left_right fk to ik
#tail ik to fk
#tail fk to ik

def l_leg_ik_fk(*args):
    l_snap_jntsFK=["left_thigh_FK_snap_jnt","left_shin_FK_snap_jnt","left_foot_FK_snap_jnt","left_ball_FK_snap_jnt", "left_toe_FK_snap_jnt"]
    l_ik_to_fk=["left_thigh_FK_ctrl", "left_shin_FK_ctrl", "left_foot_FK_ctrl","left_ball_FK_ctrl", "left_toe_FK_ctrl"]

    for y,z in zip(l_snap_jntsFK, l_ik_to_fk):
        x=cmds.xform(y, q=True, ws=True, ro=True)
        cmds.xform(z,ws=True, ro=(x[0], x[1], x[2]))

    cmds.setAttr("left_leg|ik_fk_switch.FK_IK_blend",0)

def r_leg_ik_fk(*args):
    l_snap_jntsFK=["right_thigh_FK_snap_jnt","right_shin_FK_snap_jnt","right_foot_FK_snap_jnt","right_ball_FK_snap_jnt", "right_toe_FK_snap_jnt"]
    l_ik_to_fk=["right_thigh_FK_ctrl", "right_shin_FK_ctrl", "right_foot_FK_ctrl","right_ball_FK_ctrl", "right_toe_FK_ctrl"]

    for y,z in zip(l_snap_jntsFK, l_ik_to_fk):
        x=cmds.xform(y, q=True, ws=True, ro=True)
        cmds.xform(z,ws=True, ro=(x[0], x[1], x[2]))

    cmds.setAttr("right_leg|ik_fk_switch.FK_IK_blend",0)

def l_arm_ik_fk(*args):
    l_snap_jntsFK=["left_arm_FK_snap_jnt","left_elbow_FK_snap_jnt", "left_wrist_FK_snap_jnt"]
    l_ik_to_fk=["left_arm_FK_jnt", "left_elbow_FK_jnt", "left_wrist_FK_jnt"]

    for y,z in zip(l_snap_jntsFK, l_ik_to_fk):
        x=cmds.xform(y, q=True, ws=True, ro=True)
        cmds.xform(z,ws=True, ro=(x[0], x[1], x[2]))

    cmds.setAttr("left_arm|ik_fk_switch1.FK_IK_blend",0)

def r_arm_ik_fk(*args):
    r_snap_jntsFK=["right_arm_FK_snap_jnt","right_elbow_FK_snap_jnt", "right_wrist_FK_snap_jnt"]
    r_ik_to_fk=["right_arm_FK_jnt", "right_elbow_FK_jnt", "right_wrist_FK_jnt"]

    z=cmds.xform(r_snap_jntsFK[0], q=True, ws=True, ro=True)
    cmds.xform(r_ik_to_fk[0], ws=True, ro=(z[0], z[1]*(-1), z[2]))

    y=cmds.xform('right_elbow_FK_snap_jnt', q=True, ws=True, ro=True)
    y1=cmds.getAttr('right_elbow_IK_jnt.rotate')
    print y
    print y1
    cmds.xform(r_ik_to_fk[1],ws=True, ro=(y[0], y[1], y[2]))

    x=cmds.xform(r_snap_jntsFK[2], q=True, ws=True, ro=True)
    cmds.xform(r_ik_to_fk[2],ws=True, ro=(x[0], x[1], x[2]))
#constraints mess up with everything
    cmds.setAttr("right_arm|ik_fk_switch1.FK_IK_blend",0)

def l_leg_fk_ik(*args):
    def_upperArm_length=1.988
    def_lowerArm_length=1.585
    curr_upper_arm_length=cmds.getAttr('left_shin_result_jnt.translateX')
    curr_lower_arm_length=cmds.getAttr('left_foot_result_jnt.translateX')

    tolerance=0.001

    rot=cmds.xform("left_foot_snap", q=True, ws=True, ro=True)
    tra=cmds.xform("left_foot_snap", q=True, ws=True, t=True)
    tra1=cmds.xform("left_shin_result_jnt", q=True, ws=True, t=True)
    '''
    res1=abs(curr_upper_arm_length-def_upperArm_length)
    res2=abs(curr_lower_arm_length-def_lowerArm_length)
    if (res1>tolerance) or (res2>tolerance):
        cmds.setAttr("left_knee_pv.kneeSnap",1)
    '''

    cmds.xform("left_foot_ctrl",ws=True, ro=(rot[0], rot[1], rot[2]))
    cmds.xform("left_foot_ctrl",ws=True, t=(tra[0], tra[1], tra[2]))
    cmds.xform("left_knee_pv",ws=True, t=(tra1[0], tra1[1], tra1[2]))
    cmds.setAttr("left_leg|ik_fk_switch.FK_IK_blend",1)

def r_leg_fk_ik(*args):
    def_upperArm_length=1.988
    def_lowerArm_length=1.585
    curr_upper_arm_length=cmds.getAttr('right_shin_result_jnt.translateX')
    curr_lower_arm_length=cmds.getAttr('right_foot_result_jnt.translateX')

    tolerance=0.001

    rot=cmds.xform("right_foot_snap", q=True, ws=True, ro=True)
    tra=cmds.xform("right_foot_snap", q=True, ws=True, t=True)
    tra1=cmds.xform("right_shin_result_jnt", q=True, ws=True, t=True)
    '''
    res1=abs(curr_upper_arm_length-def_upperArm_length)
    res2=abs(curr_lower_arm_length-def_lowerArm_length)
    if (res1>tolerance) or (res2>tolerance):
        cmds.setAttr("right_knee_pv.kneeSnap",1)
    '''

    cmds.xform("right_foot_ctrl",ws=True, ro=(rot[0], rot[1], rot[2]))
    cmds.xform("right_foot_ctrl",ws=True, t=(tra[0], tra[1], tra[2]))
    cmds.xform("right_knee_pv",ws=True, t=(tra1[0], tra1[1], tra1[2]))
    cmds.setAttr("right_leg|ik_fk_switch.FK_IK_blend",1)


def l_arm_fk_ik(*args):
    def_upperArm_length=2
    def_lowerArm_length=2.004
    curr_upper_arm_length=cmds.getAttr('left_elbow_result_jnt.translateX')
    curr_lower_arm_length=cmds.getAttr('left_wrist_result_jnt.translateX')

    tolerance=0.001

    rot=cmds.xform("left_arm_snap_grp", q=True, ws=True, ro=True)
    tra=cmds.xform("left_arm_snap_grp", q=True, ws=True, t=True)
    tra1=cmds.xform("left_elbow_result_jnt", q=True, ws=True, t=True)

    res1=abs(curr_upper_arm_length-def_upperArm_length)
    res2=abs(curr_lower_arm_length-def_lowerArm_length)
    if (res1>tolerance) or (res2>tolerance):
        cmds.setAttr("left_elbow_loc.elbowsnap",1)


    cmds.xform("left_arm_ctrl",ws=True, ro=(rot[0], rot[1], rot[2]))
    cmds.xform("left_arm_ctrl",ws=True, t=(tra[0], tra[1], tra[2]))
    cmds.xform("left_elbow_loc",ws=True, t=(tra1[0], tra1[1], tra1[2]))
    cmds.setAttr("left_arm|ik_fk_switch1.FK_IK_blend",1)

def r_arm_fk_ik(*args):
    rot=cmds.xform("right_arm_snap_grp", q=True, ws=True, ro=True)
    tra=cmds.xform("right_arm_snap_grp", q=True, ws=True, t=True)
    cmds.xform("right_arm_ctrl",ws=True, ro=(rot[0], rot[1], rot[2]))
    cmds.xform("right_arm_ctrl",ws=True, t=(tra[0], tra[1], tra[2]))

    tra1=cmds.xform("right_elbow_result_jnt", q=True, ws=True, t=True)
    cmds.xform("right_elbow_loc",ws=True, t=(tra1[0], tra1[1], tra1[2]))
    cmds.setAttr("right_arm|ik_fk_switch1.FK_IK_blend",1)


def tail_fk_ik(*args):
    tail_fk=["tail2_FK", "tail3_FK", "tail4_FK", "tail5_FK", "tail6_FK", "tail7_FK", "tail8_FK", "tail9_FK"]
    tail_ik=["tail2_IK","tail3_IK","tail4_IK", "tail5_IK","tail6_IK","tail7_IK","tail8_IK", "tail9_IK"]
    tail_grp=["tail2_grp", "tail3_grp", "tail4_grp", "tail5_grp", "tail6_grp", "tail7_grp", "tail8_grp", "tail9_grp"]

    for x,y,z in zip(tail_fk, tail_ik, tail_grp):
        rot=cmds.xform(x, q=True, ws=True, ro=True)
        tra=cmds.xform(y, q=True, ws=True, t=True)
        cmds.xform(z,ws=True, ro=(rot[0], rot[1], rot[2]), t=(tra[0], tra[1], tra[2]))

    cmds.setAttr("ik_fk_switch3.FK_IK_blend",1)

def switcher():

    windowID = 'switcher'
    if cmds.window(windowID, exists=True):
    	cmds.deleteUI(windowID)

    window = cmds.window(windowID,title="Auto Pirate Rig UI", w=200,h=200, sizeable=False)
    cmds.columnLayout( adjustableColumn=True )

    cmds.text(l="left leg")
    cmds.button( l='l_leg_ik_fk', command=l_leg_ik_fk)
    cmds.button( l='l_leg_fk_ik', command=l_leg_fk_ik)

    cmds.text(l="right leg")
    cmds.button( l='r_leg_ik_fk', command=r_leg_ik_fk)
    cmds.button( l='r_leg_fk_ik', command=r_leg_fk_ik)

    cmds.text(l="left arm")
    cmds.button( l='l_arm_ik_fk', command=l_arm_ik_fk)
    cmds.button( l='l_arm_fk_ik', command=l_arm_fk_ik)

    cmds.text(l="right arm")
    cmds.button( l='r_arm_ik_fk', command=r_arm_ik_fk)
    cmds.button( l='r_arm_fk_ik', command=r_arm_fk_ik)

    cmds.text(l="tail")
    #cmds.button(l="tail_ik_fk", command=tail_ik_fk)
    cmds.button(l="tail_fk_ik", command=tail_fk_ik)

    cmds.setParent( '..' )
    cmds.showWindow()

if __name__ == "__main__":
    switcher()
