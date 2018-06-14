import maya.cmds as cmds
import random
import maya.mel as mel
import time
import os
#import pyttsx 

'''
@author Anna Georgieva 
@title Speech tool 
@brief Auto-rigging face using locators and Speech tool containing all the 44 sounds in the English alphabet
	   It can be used for other languages as well. Has some facial expressions and sound.


'''
#storing keyframe values for the timeline
timeR=[]

#variables alphabet
alphabet_listUpper=[]
alphabet_listLower=[]

file_names_list=[]

#locators names Upper part
faceUpC=['center_eyebrow', 'center_nose',
		'left_eye_base', 'right_eye_base', 'center_fh_1', 'left_fh_1', 'left_fh_2',
		 'right_fh_1', 'right_fh_2', 'left_cheecks_1', 'left_cheecks_2', 'left_cheecks_3', 'left_cheecks_4', 
		 'left_eyelid_1', 'left_eyelid_2', 'left_eyelid_3', 'left_eyelid_4', 'left_eyelid_5', 'left_eyelid_6', 
		 'left_lip_1', 'left_lip_2', 'left_lip_3', 
		 'left_e_1', 'left_e_2', 'left_e_3', 'left_e_4', 'left_e_5',
		  'left_nose', 'center_nose_1', 'right_cheecks_1', 'right_cheecks_2', 'right_cheecks_3', 'right_cheecks_4', 
		 'right_eyelid_1', 'right_eyelid_2', 'right_eyelid_3', 'right_eyelid_4', 'right_eyelid_5','right_eyelid_6',
		 'right_lip_1', 'right_lip_2', 'right_lip_3', 
		  'right_e_1', 'right_e_2', 'right_e_3', 'right_e_4', 'right_e_5', 'right_nose', 
		 'center_up_lid_1', 'left_up_lid_1', 'left_up_lid_2', 'right_up_lid_1', 'right_up_lid_2']

#tongue locators
tongue_=['tongue_1','tongue_2','tongue_3','tongue_4']

###
t_list=tongue_[:-1]

reset_list=['tx','ty','tz','rx','ry','rz']
lips_list=[ 'left_up_lid_1_ctrl','right_up_lid_1_ctrl' ,
			'center_up_lid_1_ctrl','right_lip_low_ctrl' ,
			'mid_low_ctrl' ,'left_lip_low_ctrl',
			'left_up_lid_2_ctrl','right_up_lid_2_ctrl']
			
faceUpNoCC=[ 'left_fh_1', 'left_fh_2',
		 'right_fh_1', 'right_fh_2', 'left_cheecks_1', 'left_cheecks_2', 'left_cheecks_3', 'left_cheecks_4', 
		 'left_eyelid_1', 'left_eyelid_2', 'left_eyelid_3', 'left_eyelid_4', 'left_eyelid_5', 'left_eyelid_6', 
		 'left_lip_1', 'left_lip_2', 'left_lip_3', 
		 'left_e_1', 'left_e_2', 'left_e_3', 'left_e_4', 'left_e_5',
		  'left_nose', 'center_nose_1', 'right_cheecks_1', 'right_cheecks_2', 'right_cheecks_3', 'right_cheecks_4', 
		 'right_eyelid_1', 'right_eyelid_2', 'right_eyelid_3', 'right_eyelid_4', 'right_eyelid_5','right_eyelid_6',
		 'right_lip_1', 'right_lip_2', 'right_lip_3', 
		  'right_e_1', 'right_e_2', 'right_e_3', 'right_e_4', 'right_e_5', 'right_nose', 'left_up_lid_1', 'left_up_lid_2', 'right_up_lid_1', 'right_up_lid_2']
faceUpCC=[]
for i in faceUpC:
	if i.startswith('center'):
		faceUpCC.append(i)
	
faceUpL=[]
for i in faceUpC:
	if i.startswith('left'):
		faceUpL.append(i)
		
faceUpR=[]
for i in faceUpC:
	if i.startswith('right'):
		faceUpR.append(i)
		
jointList=['main_jnt_loc','spine_jnt_1','spine_jnt_2','spine_jnt_3',
				'spine_jnt_4','spine_jnt_5','upper_jaw','before_jaw']

faceLow=['center_chin' ,'right_lip_low', 'left_lip_low', 'mid_low', 'left_chin_1', 'left_chin_2', 'right_chin_1', 'right_chin_2']
faceLow2=faceLow[1:]

faceLowL=[]
faceLowR=[]
for i in faceLow:
	if i.startswith('left'):
		faceLowL.append(i)
for i in faceLow:
	if i.startswith('right'):
		faceLowR.append(i)

ctrlsAllU=[]
ctrlsAllL=[]

'''
j=cmds.ls(type='joint')
#cmds.select(j)
for i in j:
	cmds.setAttr(i+".drawStyle",0)
	
'''
tongue_jnt=[]

def spineHead():
	'''
	creates the main spine hierarchy that joints are attatched to
	'''
	#face upper part joints list
	faceUp_jnt=[]
	for i in faceUpC:
		faceUp_jnt.append(str(i)+'_jnt')
	#face main hierarchy joints list	
	jointList_jnt=[]
	for i in jointList:
		jointList_jnt.append(str(i)+'_jnt')
	#face lower part joints
	faceLow_jnt=[]
	for i in faceLow:
		faceLow_jnt.append(str(i)+'_jnt')
	#tongue joints list
	for i in tongue_:
		tongue_jnt.append(str(i)+'_jnt')	
	
	###all joints in the scene	
	allJnt=faceUp_jnt+jointList_jnt+faceLow_jnt+tongue_jnt
	for i in allJnt:
		cmds.parent(i, w=True)
	
	cmds.group(faceLow_jnt,n='faceLow_grp')
	cmds.group(faceUp_jnt,n='faceUp_grp')
	
	cmds.duplicate('spine_jnt_2_jnt',n='jaw_attach')
		
	cmds.parent('spine_jnt_1_jnt','main_jnt_loc_jnt')
	cmds.parent('spine_jnt_5_jnt','spine_jnt_1_jnt')
	cmds.parent('spine_jnt_2_jnt','spine_jnt_5_jnt')
	cmds.parent('spine_jnt_3_jnt','spine_jnt_2_jnt')
	cmds.joint('main_jnt_loc_jnt',e=True,oj='xyz', sao='yup',ch=True,zso=True)
	
	cmds.parent('center_chin_jnt','before_jaw_jnt')
	cmds.joint('before_jaw_jnt',e=True,oj='xyz', sao='yup',ch=True,zso=True)

	cmds.parent('before_jaw_jnt','jaw_attach')
	cmds.parent('jaw_attach', 'spine_jnt_2_jnt')
	cmds.parent('upper_jaw_jnt', 'spine_jnt_2_jnt')

	cmds.parentConstraint('spine_jnt_2_jnt','faceUp_grp',mo=True, w=1)
	cmds.parentConstraint('before_jaw_jnt','faceLow_grp',mo=True, w=1)
	cmds.group('main_jnt_loc_jnt',n='root_grp')
	cmds.parent('faceLow_grp','root_grp')
	cmds.parent('faceUp_grp','root_grp')

	cmds.parent('spine_jnt_4_jnt','root_grp')
	cmds.parent('tongue_4_jnt','tongue_3_jnt')
	cmds.parent('tongue_3_jnt', 'tongue_2_jnt')
	cmds.parent('tongue_2_jnt','tongue_1_jnt')
	
	cmds.joint('tongue_1_jnt',e=True,oj='xyz', sao='yup',ch=True,zso=True)
	cmds.duplicate('tongue_1_jnt',n='tongue_1_jnt_IK')
	cmds.rename('tongue_1_jnt_IK|tongue_2_jnt','tongue_2_jnt_IK')
	cmds.rename('tongue_1_jnt_IK|tongue_2_jnt_IK|tongue_3_jnt','tongue_3_jnt_IK')
	cmds.rename('tongue_1_jnt_IK|tongue_2_jnt_IK|tongue_3_jnt_IK|tongue_4_jnt','tongue_4_jnt_IK')
	cmds.duplicate('tongue_1_jnt',n='tongue_1_jnt_FK')
	cmds.rename('tongue_1_jnt_FK|tongue_2_jnt','tongue_2_jnt_FK')
	cmds.rename('tongue_1_jnt_FK|tongue_2_jnt_FK|tongue_3_jnt','tongue_3_jnt_FK')
	cmds.rename('tongue_1_jnt_FK|tongue_2_jnt_FK|tongue_3_jnt_FK|tongue_4_jnt','tongue_4_jnt_FK')
	
	tongue_IK=['tongue_1_jnt_IK','tongue_2_jnt_IK','tongue_3_jnt_IK','tongue_4_jnt_IK']
	tongue_FK=['tongue_1_jnt_FK','tongue_2_jnt_FK','tongue_3_jnt_FK','tongue_4_jnt_FK']
	
	#neck controller
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=0.2,d=3,ut=0,tol=0.01,s=8,ch=1, n='neck_head_ctrl')
	cmds.setAttr('neck_head_ctrl.rx', 22)
	cmds.setAttr('neck_head_ctrl.ty', 14)
	cmds.setAttr('neck_head_ctrl.s', 7,7,7)
	cmds.makeIdentity('neck_head_ctrl',apply=True,t=1,r=1,s=1,n=0,pn=1)
	cmds.orientConstraint('neck_head_ctrl','spine_jnt_5_jnt',mo=True, w=1)
	'''
	###squash and stretch tongue FK/IK 
	blendNodesRot=[]
	blendNodesTr=[]
	
	for item in tongue_: 
		cmds.shadingNode('blendColors',au=True,n=item+'rot_IK_FK')
		cmds.shadingNode('blendColors',au=True,n=item+'tr_IK_FK')
		
		blendNodesRot.append(item+'rot_IK_FK')
		blendNodesTr.append(item+'tr_IK_FK')

	for x, y, z, z1, o in zip(tongue_IK, tongue_FK, blendNodesRot, blendNodesTr,tongue_jnt ):
		cmds.connectAttr(x+'.rotate', z+'.color1', f=True)
		cmds.connectAttr(y+'.rotate', z+'.color2', f=True)
		cmds.connectAttr(z+'.output', o+'.rotate', f=True)
	
		cmds.connectAttr(x+'.translate', z1+'.color1', f=True)
		cmds.connectAttr(y+'.translate', z1+'.color2', f=True)
		cmds.connectAttr(z1+'.output', o+'.translate', f=True)
		
	###settings ik/fk blend
	mel.eval('curve -d 1 -p 0 0 -2 -p 0 0 2 -p -2 0 0 -p 2 0 0 -p 0 0 2 -p -2 0 0 -p 0 0 -2 -p 2 0 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 ;')
	cmds.rename('curve1', '_Tongue_settingsCTRL')
	cmds.xform('_Tongue_settingsCTRL',t=(0,1,0))
	cmds.xform('_Tongue_settingsCTRL',s=(1,1,1))
	cmds.setAttr('_Tongue_settingsCTRL'+".overrideEnabled", 1)
	cmds.setAttr('_Tongue_settingsCTRL'+".overrideColor", 4)
	cmds.setAttr('_Tongue_settingsCTRL.s',0.5,0.5,0.5)
	
	cmds.rotate( 0, 90, 0, '_Tongue_settingsCTRL', r=True, os=True, fo=True )
	cmds.parentConstraint('tongue_1_jnt','_Tongue_settingsCTRL',mo=True, w=1)
	cmds.group('_Tongue_settingsCTRL', n='T_settings_GRP')
		
	#fk controls	
	cmds.addAttr('_Tongue_settingsCTRL',ln="FK_IK_blend", nn="FK/IK_blend", at='double', min=0, max=1, dv=0 )
	cmds.setAttr('_Tongue_settingsCTRL.FK_IK_blend',e=True,keyable=True)
	
	for item,item1 in zip(blendNodesRot,blendNodesTr):
		cmds.connectAttr('_Tongue_settingsCTRL.FK_IK_blend',item+'.blender',f=True)
		cmds.connectAttr('_Tongue_settingsCTRL.FK_IK_blend',item1+'.blender',f=True)
	'''
	for x,y in zip(tongue_jnt,tongue_FK):
		cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=0.05,d=3,ut=0,tol=0.01,s=8,ch=1, n=x+'ctrl')
		cmds.setAttr(x+'ctrl.rz', 90)
		cmds.setAttr(x+'ctrl.s', 10,10,10)
		cmds.makeIdentity(x+'ctrl',apply=True,t=1,r=1,s=1,n=0,pn=1)
		cmds.parent(x+'ctrlShape', y,r=True,s=True)	
		cmds.delete(x+'ctrl')
	cmds.setAttr("tongue_4_jnt_FK.visibility",0)
	'''
	#squash and stretch	
	cmds.distanceDimension(sp=(0,-1,0),ep=(0,1,0))
	cmds.rename('locator1', 'start_tongue_loc')
	cmds.rename('locator2', 'end_tongue_loc')
	
	t_s_x=cmds.getAttr('tongue_1.tx')
	t_s_y=cmds.getAttr('tongue_1.ty')
	t_s_z=cmds.getAttr('tongue_1.tz')
	
	t_e_x=cmds.getAttr('tongue_4.tx')
	t_e_y=cmds.getAttr('tongue_4.ty')
	t_e_z=cmds.getAttr('tongue_4.tz')
	
	cmds.setAttr('start_tongue_loc.translate',t_s_x,t_s_y,t_s_z)
	cmds.setAttr('end_tongue_loc.translate',t_e_x,t_e_y,t_e_z)
	cmds.rename('distanceDimension1', 'tongue_distance' )	
		
	cmds.duplicate('tongue_1_jnt_IK', n='t_ctrl1')	
	cmds.pickWalk('t_ctrl1|tongue_2_jnt_IK',d='down')
	cmds.pickWalk('t_ctrl1|tongue_2_jnt_IK|tongue_3_jnt_IK',d='down')
	cmds.parent(w=True)
	cmds.rename('|tongue_4_jnt_IK', 't_ctrl4')
	cmds.delete('t_ctrl1|tongue_2_jnt_IK')
	cmds.ikHandle(n='ik_tongue',sj='tongue_1_jnt_IK',ee='tongue_4_jnt_IK',sol='ikSplineSolver')
	cmds.rename('curve1', 'tongue_crv')
	cmds.skinCluster('t_ctrl4','t_ctrl1','tongue_crv',mi=2)
	cmds.parent('start_tongue_loc', 't_ctrl1')
	cmds.parent('end_tongue_loc', 't_ctrl4')
	
	###
	cmds.shadingNode('multiplyDivide', au=True, n='tongue_mulDiv')
	cmds.setAttr("tongue_mulDiv.operation",2)
	cmds.connectAttr('tongue_distance.distance', 'tongue_mulDiv.input1X', f=True)
	cmds.shadingNode('multiplyDivide', au=True, n='tongue_result')
	cmds.setAttr("tongue_result.operation",1)
	cmds.connectAttr('tongue_mulDiv.output.outputX', 'tongue_result.input1X', f=True)
	cmds.setAttr('tongue_result.input2X', 5)
	cmds.setAttr("tongue_mulDiv.input2X", 15)
	
	for i in range(1,5):
		cmds.connectAttr( 'tongue_result.outputX', 'tongue_'+str(i)+'_jnt_IK.translateX', f=True)

	cmds.shadingNode('multiplyDivide', au=True, n='tongue_sqrtStretch_pow')
	cmds.setAttr("tongue_sqrtStretch_pow.operation", 3)
	cmds.shadingNode('multiplyDivide', au=True, n='tongue_stretchInvert_Div')
	cmds.setAttr("tongue_stretchInvert_Div.operation", 2)
	cmds.connectAttr('tongue_mulDiv.output.outputX','tongue_sqrtStretch_pow.input1.input1X')
	cmds.connectAttr('tongue_sqrtStretch_pow.output.outputX','tongue_stretchInvert_Div.input2.input2X')
	cmds.setAttr("tongue_sqrtStretch_pow.input2X",0.5)
	cmds.setAttr("tongue_stretchInvert_Div.input1X",1)

	for i in tongue_jnt:
		cmds.connectAttr( 'tongue_stretchInvert_Div.output.outputX', i+'.scale.scaleY', f=True) 
		cmds.connectAttr( 'tongue_stretchInvert_Div.output.outputX', i+'.scale.scaleZ', f=True) 
	
	#create controllers for the tongue joints
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=0.4,d=3,ut=0,tol=0.01,s=8,ch=1, n='t_end_ctrl')
	cmds.setAttr('t_end_ctrl.tx',cmds.getAttr('t_ctrl4.tx'))
	cmds.setAttr('t_end_ctrl.ty',cmds.getAttr('t_ctrl4.ty'))
	cmds.setAttr('t_end_ctrl.tz',cmds.getAttr('t_ctrl4.tz')+1)
	cmds.makeIdentity('t_end_ctrl', apply=True,t=1,r=1,s=1,n=0,pn=1)
	cmds.parent('t_ctrl4','t_end_ctrl')
	'''
	

	
def mirrorBehaviourLoc(*args):
	'''
	mirrored behavior locators using nodes
	'''
	mulDivU=[]
	mulDivL=[]
	
	for i in faceUpL:
		cmds.shadingNode('multiplyDivide', au=True,n=i+'_mulDiv')
		cmds.setAttr(i+"_mulDiv.input2X",-1)
		mulDivU.append(i+'_mulDiv')
	
	for i in faceLowL:
		cmds.shadingNode('multiplyDivide', au=True,n=i+'_mulDiv')
		cmds.setAttr(i+"_mulDiv.input2X",-1)
		mulDivL.append(i+'_mulDiv')
	
	for i, j, z in zip(faceUpL,faceUpR, mulDivU):
		cmds.connectAttr( i+'.tx', z+'.input1X',f=True)
		cmds.connectAttr( z+'.outputX', j+'.tx', f=True)
		cmds.connectAttr( i+'.ty', j+'.ty')
		cmds.connectAttr( i+'.tz', j+'.tz')
	
	for i, j, z in zip(faceLowL,faceLowR, mulDivL):
		cmds.connectAttr( i+'.tx', z+'.input1X',f=True)
		cmds.connectAttr( z+'.outputX', j+'.tx', f=True)
		cmds.connectAttr( i+'.ty', j+'.ty')
		cmds.connectAttr( i+'.tz', j+'.tz')
		
	print "mirror locators success"	

def mirrorBehaviourNURBS(*args):
	'''
	mirrored behavior groups using nodes
	'''
	
	if cmds.objExists('main_jnt_loc_jnt'):
		###create groups so that animation wont be affected
		mulDivNurbsU=[]
		mulDivNurbsL=[]
		
		faceUpL_nurbs=['left_cheecks_1_grp', 'left_cheecks_2_grp', 'left_cheecks_3_grp', 'left_cheecks_4_grp', 'left_eyelid_1_grp',
					'left_eyelid_2_grp', 'left_eyelid_3_grp', 'left_eyelid_4_grp', 'left_eyelid_5_grp', 'left_eyelid_6_grp', 
					'left_lip_1_grp', 'left_lip_2_grp', 'left_lip_3_grp', 'left_e_1_grp', 'left_e_2_grp', 'left_e_3_grp', 
					'left_e_4_grp', 'left_e_5_grp','left_nose_grp','left_fh_1_grp', 'left_fh_2_grp']
					
		faceUpR_nurbs=['right_cheecks_1_grp', 'right_cheecks_2_grp', 'right_cheecks_3_grp', 'right_cheecks_4_grp', 'right_eyelid_1_grp',
						'right_eyelid_2_grp', 'right_eyelid_3_grp', 'right_eyelid_4_grp', 'right_eyelid_5_grp', 'right_eyelid_6_grp',
						 'right_lip_1_grp', 'right_lip_2_grp', 'right_lip_3_grp', 'right_e_1_grp', 'right_e_2_grp', 'right_e_3_grp', 
						 'right_e_4_grp', 'right_e_5_grp', 'right_nose_grp','right_fh_1_grp', 'right_fh_2_grp']
		
		faceLowL_nurbs=['left_lip_low_grp','left_chin_1_grp','left_chin_2_grp']
		faceLowR_nurbs=['right_lip_low_grp','right_chin_1_grp','right_chin_2_grp']
		
		for i in faceUpL_nurbs:
			cmds.shadingNode('multiplyDivide', au=True,n=i+'_mulDivNURBS')
			cmds.setAttr(i+"_mulDivNURBS.input2X",-1)
			mulDivNurbsU.append(i+'_mulDivNURBS')
		
		for i in faceLowL_nurbs:
			cmds.shadingNode('multiplyDivide', au=True,n=i+'_mulDivNURBS')
			cmds.setAttr(i+"_mulDivNURBS.input2X",-1)
			mulDivNurbsL.append(i+'_mulDivNURBS')
		
		for i, j, z in zip(faceUpL_nurbs,faceUpR_nurbs, mulDivNurbsU):
			cmds.connectAttr( i+'.tx', z+'.input1X',f=True)
			cmds.connectAttr( z+'.outputX', j+'.tx', f=True)
			cmds.connectAttr( i+'.ty', j+'.ty')
			cmds.connectAttr( i+'.tz', j+'.tz')
		
		for i, j, z in zip(faceLowL_nurbs,faceLowR_nurbs, mulDivNurbsL):
			cmds.connectAttr( i+'.tx', z+'.input1X',f=True)
			cmds.connectAttr( z+'.outputX', j+'.tx', f=True)
			cmds.connectAttr( i+'.ty', j+'.ty')
			cmds.connectAttr( i+'.tz', j+'.tz')
	else:
		print "create the joints first"

		
def controlFace():
	'''
	i thought of face control box but buttons worked better
	'''
	cmds.curve(d=1.0, p=[(-92,229,0),(-92,203,0),(-40,203,0),(-40,229,0),(-92,229,0)],k=[0,1,2,3,4],n='faceBox')
	cmds.setAttr("faceBox.overrideEnabled", 1)
	cmds.setAttr("faceBox.overrideColor", 16)
	
	cmds.xform('faceBox', cp=True)
	boxNames=['blinkBox', 'eyebrowsLBox','eyebrowsRBox', 'noseBox', 'frownBox','smileBox']
	
	ctrlNames=[]
	for i in boxNames:
		ctrlNames.append(i+'_ctrl')
		
	for i in range(0,6):
		cmds.curve(d=1.0, p=[(-95,227,0),(-95,205,0),(-89,205,0),(-89,227,0),(-95,227,0)],k=[0,1,2,3,4],n=boxNames[i])
		cmds.curve(d=1.0, p=[(-95,227,0),(-95,224,0),(-89,224,0),(-89,227,0),(-95,227,0)], k=[0,1,2,3,4],n=ctrlNames[i])
		cmds.setAttr(boxNames[i]+'.translateX',i*8+5)
		cmds.setAttr(ctrlNames[i]+'.translateX',i*8+5)
		cmds.transformLimits(ctrlNames[i],ty=(-19, 0),ety=(1, 1)) 
		cmds.xform(ctrlNames[i], cp=True)
		cmds.xform(boxNames[i], cp=True)
		cmds.setAttr(boxNames[i]+".overrideEnabled", 1)
		cmds.setAttr(boxNames[i]+".overrideColor", 16)
		cmds.setAttr(ctrlNames[i]+".overrideEnabled", 1)
		cmds.setAttr(ctrlNames[i]+".overrideColor", 16)
		cmds.annotate(boxNames[i], tx=boxNames[i], p=(-90+i*10, 232, 0))
	
	cmds.makeIdentity(boxNames,ctrlNames, apply=True,t=1,r=1,s=1,n=0,pn=1)
	cmds.group('faceBox','annotation1','annotation2','annotation3','annotation4','annotation5','annotation6',boxNames, ctrlNames, n='face_box_grp')
	cmds.setAttr('face_box_grp.t',0,-170,13)		
		
def setEmotionHappy(*args):
	print ("happy")
	##smile
	tr_x=random.randint(0,10)
	tr_x1=random.randint(0,10)
	tr_y=random.randint(-3,3)
	tr_y1=random.randint(-3,3)
	
	if len(timeR)==0:
		print 'create the animation first'
	else:
		
		time_defined=[timeR[0],timeR[len(timeR)-1]]

		value_zero=[0,0,0,0]
		value_different_eyebrows=[1.5, 1, 0.5 , 0]
		
		setKeys(time_defined[0],'l_eye_ctrl', 'translateX',tr_x)
		setKeys(time_defined[0],'l_eye_ctrl', 'translateY',tr_y)
		setKeys(time_defined[0],'r_eye_ctrl', 'translateX',tr_x)
		setKeys(time_defined[0],'r_eye_ctrl', 'translateY',tr_y)
		setKeys(time_defined[0],'neck_head_ctrl', 'rotateX',random.randint(-10,10))
		setKeys(time_defined[0],'neck_head_ctrl', 'rotateY',random.randint(-3,3))
		closeOpenEyes(time_defined[0])
		symmetry_list=['left','right']  #only x difference
		for i in symmetry_list:
			setKeys(time_defined[0], i+"_up_lid_2_ctrl", 'translateZ', 0)
			setKeys(time_defined[0],i+"_up_lid_2_ctrl", 'translateY',0)

			setKeys(time_defined[0], i+'_eyelid_4_ctrl','translateY',0)
			setKeys(time_defined[0], i+'_eyelid_6_ctrl','translateY',0)
			setKeys(time_defined[0], i+'_eyelid_5_ctrl','translateY',0)
			
			setKeys(time_defined[0], i+'_cheecks_3_ctrl','translateY',0)
			setKeys(time_defined[0], i+'_cheecks_3_ctrl','translateZ',0)
			
			setKeys(time_defined[0], i+'_cheecks_2_ctrl','translateY',0)
			setKeys(time_defined[0], i+'_cheecks_2_ctrl','translateZ',0)
			
			eyebrows_up(time_defined[0], i, value_zero)
			
			setKeys(time_defined[1], i+"_up_lid_2_ctrl", 'translateZ', -2)
			setKeys(time_defined[1],i+"_up_lid_2_ctrl", 'translateY', 1.5)

			setKeys(time_defined[1], i+'_eyelid_4_ctrl','translateY',0.8)
			setKeys(time_defined[1], i+'_eyelid_6_ctrl','translateY',0.8)
			setKeys(time_defined[1], i+'_eyelid_5_ctrl','translateY',0.8)
			
			setKeys(time_defined[1], i+'_cheecks_3_ctrl','translateY',3.5)
			setKeys(time_defined[1], i+'_cheecks_3_ctrl','translateZ',2.7)
			
			setKeys(time_defined[1], i+'_cheecks_2_ctrl','translateY',3.5)
			setKeys(time_defined[1], i+'_cheecks_2_ctrl','translateZ',2)
			
			eyebrows_up(time_defined[1], i,value_different_eyebrows)
		closeOpenEyes(time_defined[1])
		setKeys(time_defined[1],'l_eye_ctrl', 'translateX',tr_x1)
		setKeys(time_defined[1],'l_eye_ctrl', 'translateY',tr_y1)
		setKeys(time_defined[1],'r_eye_ctrl', 'translateX',tr_x1)
		setKeys(time_defined[1],'r_eye_ctrl', 'translateY',tr_y1)
		setKeys(time_defined[1],'neck_head_ctrl', 'rotateX',random.randint(-10,10))
		setKeys(time_defined[1],'neck_head_ctrl', 'rotateY',random.randint(-3,3))
			
		a= timeR[len(timeR)-1]
		b=a+10
		print "b", b
		for i in symmetry_list:
			setKeys(b,i+'_up_lid_2_ctrl','translateY',2.4)
			setKeys(b,i+'_up_lid_2_ctrl','translateZ',-2)
			setKeys(b,i+'_up_lid_2_ctrl','translateX',0)


def eyebrows_up(t,i,value):
	setKeys(t, i+'_e_1_ctrl', 'translateY',value[0])
	setKeys(t, i+'_e_2_ctrl', 'translateY',value[1])
	setKeys(t, i+'_e_3_ctrl', 'translateY',value[2])
	setKeys(t, i+'_e_4_ctrl', 'translateY',value[3])
		
def setEmotionSad(*args):
	print ("sad")
	
	tr_x=random.randint(-10,10)
	tr_x1=random.randint(-10,10)
	tr_y=random.randint(-3,3)
	tr_y1=random.randint(-3,3)
	
	print tr_x
	print tr_y
	print tr_x1
	print tr_y1
	
	if len(timeR)==0:
		print 'create the animation first'
	else:
	
		time_defined=[timeR[0],timeR[len(timeR)-1]]
		print time_defined
		
		setKeys(time_defined[0],'l_eye_ctrl', 'translateX',tr_x)
		setKeys(time_defined[0],'l_eye_ctrl', 'translateY',tr_y)
		setKeys(time_defined[0],'r_eye_ctrl', 'translateX',tr_x)
		setKeys(time_defined[0],'r_eye_ctrl', 'translateY',tr_y)
		setKeys(time_defined[0],'neck_head_ctrl', 'rotateX',random.randint(-10,10))
		setKeys(time_defined[0],'neck_head_ctrl', 'rotateY',random.randint(-3,3))
		
		
		symmetry_list=['left','right']  #only x difference
		for i in symmetry_list:
			#setKeys(time_defined[0], i+"_up_lid_2_ctrl", 'translateZ', 0)
			setKeys(time_defined[0],i+"_e_1_ctrl", 'translateX',0)
			setKeys(time_defined[0],i+"_e_2_ctrl","translateX", 0)
			setKeys(time_defined[0],i+"_e_3_ctrl","translateX",0)
			setKeys(time_defined[0],i+"_e_4_ctrl","translateX", 0)
			setKeys(time_defined[0],i+"_e_5_ctrl","translateX", 0)
			setKeys(time_defined[0],i+"_eyelid_5_ctrl","translateX", 0)
			setKeys(time_defined[0],i+"_e_1_ctrl",'translateY', 0)
			setKeys(time_defined[0],i+"_e_2_ctrl","translateY", 0)
			setKeys(time_defined[0],i+"_e_3_ctrl","translateY", 0)
			setKeys(time_defined[0],i+"_e_4_ctrl","translateY", 0)
			setKeys(time_defined[0],i+"_e_5_ctrl","translateY", 0)
			setKeys(time_defined[0],i+"_eyelid_5_ctrl","translateY", 0)
			setKeys(time_defined[0],i+"_eyelid_5_ctrl","translateZ", 0)
			setKeys(time_defined[0],i+"_eyelid_4_ctrl","translateZ",0)
			setKeys(time_defined[0],i+"_eyelid_6_ctrl","translateY",0)
			setKeys(time_defined[0],i+"_eyelid_6_ctrl","translateZ", 0)
		
		setKeys(time_defined[1],"left_e_1_ctrl", 'translateX',-2)
		setKeys(time_defined[1],"right_e_1_ctrl","translateX", 2)
		setKeys(time_defined[1],"left_e_2_ctrl","translateX", -1.6)
		setKeys(time_defined[1],"right_e_2_ctrl","translateX", 1.6)
		setKeys(time_defined[1],"left_e_3_ctrl","translateX", -1.2)
		setKeys(time_defined[1],"right_e_3_ctrl","translateX", 1.2)
		setKeys(time_defined[1],"left_e_4_ctrl","translateX", -1.2)
		setKeys(time_defined[1],"right_e_4_ctrl","translateX", 1.2)
		setKeys(time_defined[1],"left_e_5_ctrl","translateX", -0.5)
		setKeys(time_defined[1],"right_e_5_ctrl","translateX", 0.5)
		setKeys(time_defined[1],"left_eyelid_5_ctrl","translateX", -0.5)
		setKeys(time_defined[1],"right_eyelid_5_ctrl","translateX", 0.5)
		for i in symmetry_list:
			#setKeys(time_defined[0], i+"_up_lid_2_ctrl", 'translateZ', 0)
			setKeys(time_defined[1],i+"_e_1_ctrl",'translateY', 3)
			setKeys(time_defined[1],i+"_e_2_ctrl","translateY", 1)
			setKeys(time_defined[1],i+"_e_3_ctrl","translateY", -0.8)
			setKeys(time_defined[1],i+"_e_4_ctrl","translateY", -2)
			setKeys(time_defined[1],i+"_e_5_ctrl","translateY", -2)
			setKeys(time_defined[1],i+"_eyelid_5_ctrl","translateY", 1.5)
			setKeys(time_defined[1],i+"_eyelid_5_ctrl","translateZ", 1.2)
			setKeys(time_defined[1],i+"_eyelid_4_ctrl","translateZ",-0.4)
			setKeys(time_defined[1],i+"_eyelid_6_ctrl","translateY",2)
			setKeys(time_defined[1],i+"_eyelid_6_ctrl","translateZ", 1.5)

		setKeys(time_defined[1],'l_eye_ctrl', 'translateX',tr_x1)
		setKeys(time_defined[1],'l_eye_ctrl', 'translateY',tr_y1)
		setKeys(time_defined[1],'r_eye_ctrl', 'translateX',tr_x1)
		setKeys(time_defined[1],'r_eye_ctrl', 'translateY',tr_y1)
		setKeys(time_defined[1],'neck_head_ctrl', 'rotateX',random.randint(-10,10))
		setKeys(time_defined[1],'neck_head_ctrl', 'rotateY',random.randint(-3,3))
		
		
		a= timeR[len(timeR)-1]
		b=a+10
		print "b", b

		setKeys(b,'mid_low_ctrl', 'translateY',2)
		for i in symmetry_list:
			setKeys(b,i+'_lip_low_ctrl','translateY',3)
			setKeys(b,i+'_up_lid_2_ctrl','translateZ',-5)
			setKeys(b,i+'_up_lid_2_ctrl','translateY',-2)
			setKeys(b,i+'_up_lid_2_ctrl','translateX',0)
	
def setEmotionAngry(*args):
	print ("angry")
	
	tr_x=random.randint(-10,10)
	tr_x1=random.randint(-10,10)
	tr_y=random.randint(-3,3)
	tr_y1=random.randint(-3,3)
	
	
	if len(timeR)==0:
		print 'create the animation first'
	else:
		
		time_defined=[timeR[0],timeR[len(timeR)-1]]
		print time_defined
		
		setKeys(time_defined[0],'l_eye_ctrl', 'translateX',tr_x)
		setKeys(time_defined[0],'l_eye_ctrl', 'translateY',tr_y)
		setKeys(time_defined[0],'r_eye_ctrl', 'translateX',tr_x)
		setKeys(time_defined[0],'r_eye_ctrl', 'translateY',tr_y)
		setKeys(time_defined[0],'neck_head_ctrl', 'rotateX',random.randint(-10,10))
		setKeys(time_defined[0],'neck_head_ctrl', 'rotateY',random.randint(-3,3))
		

		symmetry_list=['left','right']  #only x difference
		for i in symmetry_list:
			setKeys(time_defined[0], i+"_e_1_ctrl","translateX", 0)
			setKeys(time_defined[0], i+"_e_1_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_e_1_ctrl","translateX", 0)
			setKeys(time_defined[0], i+"_e_2_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_e_3_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_nose_ctrl","translateY", 0)
		
		setKeys(time_defined[1], "left_e_1_ctrl","translateX", -1)
		setKeys(time_defined[1], "right_e_1_ctrl","translateX", 1)
		symmetry_list=['left','right']  #only x difference
		for i in symmetry_list:
			setKeys(time_defined[1], i+"_e_1_ctrl","translateY", -3)
			setKeys(time_defined[1], i+"_e_2_ctrl","translateY", -2.5)
			setKeys(time_defined[1], i+"_e_3_ctrl","translateY", -3)
			setKeys(time_defined[1], i+"_nose_ctrl","translateY", 1)
		
		setKeys(time_defined[1],'l_eye_ctrl', 'translateX',tr_x1)
		setKeys(time_defined[1],'l_eye_ctrl', 'translateY',tr_y1)
		setKeys(time_defined[1],'r_eye_ctrl', 'translateX',tr_x1)
		setKeys(time_defined[1],'r_eye_ctrl', 'translateY',tr_y1)
		setKeys(time_defined[1],'neck_head_ctrl', 'rotateX',random.randint(-10,10))
		setKeys(time_defined[1],'neck_head_ctrl', 'rotateY',random.randint(-3,3))
		
		a= timeR[len(timeR)-1]
		b=a+10

		setKeys(b,'center_up_lid_1_ctrl', 'translateY',1.6)
		setKeys(b,'center_up_lid_1_ctrl', 'translateX',0)
		setKeys(b,"mid_low_ctrl", 'translateY',-0.5)
		for i in symmetry_list:
			setKeys(b,i+'_up_lid_1_ctrl','translateY',1.6)
			setKeys(b,i+'_up_lid_1_ctrl','translateX',0)
			
			setKeys(b,i+'_up_lid_2_ctrl','translateY',1.5)
			setKeys(b,i+'_up_lid_2_ctrl','translateX',0)
			setKeys(b,i+'_up_lid_2_ctrl','translateZ',-2)
			
			setKeys(b,i+'_lip_low_ctrl','translateY',-1.5)
			setKeys(b,i+'_chin_2_ctrl','translateY',-1.7)
			
	
		
def setEmotionRandom(*args):
	##random experiment
	#########
	print ("random")
	
	tr_x=random.randint(-10,10)
	tr_x1=random.randint(-10,10)
	tr_y=random.randint(-3,3)
	tr_y1=random.randint(-3,3)
	
	if len(timeR)==0:
		print 'create the animation first'
	else:
		
		time_defined=[timeR[0],timeR[len(timeR)-1]]
		print time_defined
		
		setKeys(time_defined[0],'l_eye_ctrl', 'translateX',tr_x)
		setKeys(time_defined[0],'l_eye_ctrl', 'translateY',tr_y)
		setKeys(time_defined[0],'r_eye_ctrl', 'translateX',tr_x)
		setKeys(time_defined[0],'r_eye_ctrl', 'translateY',tr_y)
		setKeys(time_defined[0],'neck_head_ctrl', 'rotateX',random.randint(-10,10))
		setKeys(time_defined[0],'neck_head_ctrl', 'rotateY',random.randint(-3,3))

		symmetry_list=['left','right']  #only x difference
		for i in symmetry_list:
			setKeys(time_defined[0], i+"_e_1_ctrl","translateX", 0)
			setKeys(time_defined[0], i+"_e_1_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_e_1_ctrl","translateX", 0)
			setKeys(time_defined[0], i+"_e_2_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_e_3_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_nose_ctrl","translateY", 0)
		
		setKeys(time_defined[1], "left_e_1_ctrl","translateX", -1)
		setKeys(time_defined[1], "right_e_1_ctrl","translateX", 1)
		symmetry_list=['left','right']  #only x difference
		for i in symmetry_list:
			setKeys(time_defined[1], i+"_e_1_ctrl","translateY",random.randint(-3,3))
			setKeys(time_defined[1], i+"_e_2_ctrl","translateY", random.randint(-3,3))
			setKeys(time_defined[1], i+"_e_3_ctrl","translateY",random.randint(-4,3))
			
		setKeys(time_defined[1],'l_eye_ctrl', 'translateX',tr_x1)
		setKeys(time_defined[1],'l_eye_ctrl', 'translateY',tr_y1)
		setKeys(time_defined[1],'r_eye_ctrl', 'translateX',tr_x1)
		setKeys(time_defined[1],'r_eye_ctrl', 'translateY',tr_y1)
		setKeys(time_defined[1],'neck_head_ctrl', 'rotateX',random.randint(-10,10))
		setKeys(time_defined[1],'neck_head_ctrl', 'rotateY',random.randint(-3,3))
		
def setEmotionSurprised(*args):
	print ("surprised")
	##smile
	tr_x=random.randint(0,10)
	tr_x1=random.randint(0,10)
	tr_y=random.randint(-3,3)
	tr_y1=random.randint(-3,3)
	
	print tr_x
	print tr_y
	print tr_x1
	print tr_y1
	if len(timeR)==0:
		print 'create the animation first'
	else:
		
		time_defined=[timeR[0],timeR[len(timeR)-1]]
		
		setKeys(time_defined[0],'l_eye_ctrl', 'translateX',tr_x)
		setKeys(time_defined[0],'l_eye_ctrl', 'translateY',tr_y)
		setKeys(time_defined[0],'r_eye_ctrl', 'translateX',tr_x)
		setKeys(time_defined[0],'r_eye_ctrl', 'translateY',tr_y)
		setKeys(time_defined[0],'neck_head_ctrl', 'rotateX',random.randint(-10,10))
		setKeys(time_defined[0],'neck_head_ctrl', 'rotateY',random.randint(-3,3))

		
		symmetry_list=['left','right']  #only x difference
		for i in symmetry_list:
			setKeys(time_defined[0], i+"_e_1_ctrl","translateX", 0)
			setKeys(time_defined[0], i+"_e_1_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_e_1_ctrl","translateX", 0)
			setKeys(time_defined[0], i+"_e_2_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_e_3_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_eyelid_1_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_eyelid_2_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_eyelid_3_ctrl","translateY", 0)
		
		setKeys(time_defined[1], "left_e_1_ctrl","translateY", 2)
		setKeys(time_defined[1], "right_e_1_ctrl","translateY", 2)
		symmetry_list=['left','right']  #only x difference
		for i in symmetry_list:
			setKeys(time_defined[1], i+"_eyelid_1_ctrl","translateY", 1)
			setKeys(time_defined[1], i+"_eyelid_2_ctrl","translateY", 1)
			setKeys(time_defined[1], i+"_eyelid_3_ctrl","translateY", 1)
			setKeys(time_defined[1], i+"_e_2_ctrl","translateY", 1)
			setKeys(time_defined[1], i+"_e_3_ctrl","translateY", 1)
		
		setKeys(timeR[len(timeR)-2], "jaw_drop","jaw_drop", -10)
		
		setKeys(time_defined[1],'l_eye_ctrl', 'translateX',tr_x1)
		setKeys(time_defined[1],'l_eye_ctrl', 'translateY',tr_y1)
		setKeys(time_defined[1],'r_eye_ctrl', 'translateX',tr_x1)
		setKeys(time_defined[1],'r_eye_ctrl', 'translateY',tr_y1)
		setKeys(time_defined[1],'neck_head_ctrl', 'rotateX',random.randint(-10,10))
		setKeys(time_defined[1],'neck_head_ctrl', 'rotateY',random.randint(-3,3))

		a= timeR[len(timeR)-1]
		b=a+10

		setKeys(b,'jaw_drop', 'jaw_drop',-10)
		setKeys(b,'center_up_lid_1_ctrl', 'translateY',1)
		setKeys(b,"mid_low_ctrl", 'translateY',-0.5)
		for i in symmetry_list:
			setKeys(b,i+'_lip_low_ctrl','translateX',1.5)
			setKeys(b,i+'_up_lid_1_ctrl','translateY',1)
			
		for t in t_list:
			setKeys(b, t, 'rotateZ', 0)
	
def setEmotionFear(*args):
	print ("Fear")
	##smile
	tr_x=random.randint(0,10)
	tr_x1=random.randint(0,10)
	tr_y=random.randint(-3,3)
	tr_y1=random.randint(-3,3)
	
	if len(timeR)==0:
		print 'create the animation first'
	else:
		
		time_defined=[timeR[0],timeR[len(timeR)-1]]
		
		setKeys(time_defined[0],'l_eye_ctrl', 'translateX',tr_x)
		setKeys(time_defined[0],'l_eye_ctrl', 'translateY',tr_y)
		setKeys(time_defined[0],'r_eye_ctrl', 'translateX',tr_x)
		setKeys(time_defined[0],'r_eye_ctrl', 'translateY',tr_y)
		setKeys(time_defined[0],'neck_head_ctrl', 'rotateX',random.randint(-10,10))
		setKeys(time_defined[0],'neck_head_ctrl', 'rotateY',random.randint(-3,3))
		
		closeOpenEyes(time_defined[0])
		
		symmetry_list=['left','right']  #only x difference
		for i in symmetry_list:
			setKeys(time_defined[0], i+"_e_1_ctrl","translateX", 0)
			setKeys(time_defined[0], i+"_e_1_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_e_1_ctrl","translateX", 0)
			setKeys(time_defined[0], i+"_e_2_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_e_3_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_eyelid_1_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_eyelid_2_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_eyelid_3_ctrl","translateY", 0)
		
		setKeys(time_defined[1], "left_e_1_ctrl","translateY", 2)
		setKeys(time_defined[1], "right_e_1_ctrl","translateY", 2)
		symmetry_list=['left','right']  #only x difference
		for i in symmetry_list:
			setKeys(time_defined[1], i+"_eyelid_1_ctrl","translateY", 1)
			setKeys(time_defined[1], i+"_eyelid_2_ctrl","translateY", 1)
			setKeys(time_defined[1], i+"_eyelid_3_ctrl","translateY", 1)
			setKeys(time_defined[1], i+"_e_2_ctrl","translateY", 1)
			setKeys(time_defined[1], i+"_e_3_ctrl","translateY", 1)
		
		setKeys(timeR[len(timeR)-2], "jaw_drop","jaw_drop", -10)
		
		closeOpenEyes(time_defined[1])
		setKeys(time_defined[1],'l_eye_ctrl', 'translateX',tr_x1)
		setKeys(time_defined[1],'l_eye_ctrl', 'translateY',tr_y1)
		setKeys(time_defined[1],'r_eye_ctrl', 'translateX',tr_x1)
		setKeys(time_defined[1],'r_eye_ctrl', 'translateY',tr_y1)
		setKeys(time_defined[1],'neck_head_ctrl', 'rotateX',random.randint(-10,10))
		setKeys(time_defined[1],'neck_head_ctrl', 'rotateY',random.randint(-3,3))

		a= timeR[len(timeR)-1]
		b=a+10

		setKeys(b,'center_up_lid_1_ctrl', 'translateY',0.8)
		setKeys(b,'left_up_lid_1_ctrl', 'translateY',1.8)
		setKeys(b,"left_up_lid_2_ctrl", 'translateZ',-4)
		setKeys(b,"left_lip_low_ctrl", 'translateX',1.5)
		setKeys(b,"left_lip_low_ctrl", 'translateY',-1.8)
		setKeys(b,"left_chin_2_ctrl", 'translateY',-2)

def setEmotionDisgust(*args):
	print ("Disgust")
	##smile
	tr_x=random.randint(0,10)
	tr_x1=random.randint(0,10)
	tr_y=random.randint(-3,3)
	tr_y1=random.randint(-3,3)
	

	if len(timeR)==0:
		print 'create the animation first'
	else:
		
		time_defined=[timeR[0],timeR[len(timeR)-1]]
		
		setKeys(time_defined[0],'l_eye_ctrl', 'translateX',tr_x)
		setKeys(time_defined[0],'l_eye_ctrl', 'translateY',tr_y)
		setKeys(time_defined[0],'r_eye_ctrl', 'translateX',tr_x)
		setKeys(time_defined[0],'r_eye_ctrl', 'translateY',tr_y)
		setKeys(time_defined[0],'neck_head_ctrl', 'rotateX',random.randint(-10,10))
		setKeys(time_defined[0],'neck_head_ctrl', 'rotateY',random.randint(-3,3))

		closeOpenEyes(time_defined[0])
		
		symmetry_list=['left','right']  #only x difference
		for i in symmetry_list:
			setKeys(time_defined[0], i+"_e_1_ctrl","translateX", 0)
			setKeys(time_defined[0], i+"_e_1_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_e_1_ctrl","translateX", 0)
			setKeys(time_defined[0], i+"_e_2_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_e_3_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_eyelid_1_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_eyelid_2_ctrl","translateY", 0)
			setKeys(time_defined[0], i+"_eyelid_3_ctrl","translateY", 0)
		
		setKeys(time_defined[1], "left_e_1_ctrl","translateY", 2)
		setKeys(time_defined[1], "right_e_1_ctrl","translateY", 2)
		symmetry_list=['left','right']  #only x difference
		for i in symmetry_list:
			setKeys(time_defined[1], i+"_eyelid_1_ctrl","translateY", 1)
			setKeys(time_defined[1], i+"_eyelid_2_ctrl","translateY", 1)
			setKeys(time_defined[1], i+"_eyelid_3_ctrl","translateY", 1)
			setKeys(time_defined[1], i+"_e_2_ctrl","translateY", 1)
			setKeys(time_defined[1], i+"_e_3_ctrl","translateY", 1)
		
		setKeys(timeR[len(timeR)-2], "jaw_drop","jaw_drop", -10)
		closeOpenEyes(time_defined[1])
		setKeys(time_defined[1],'l_eye_ctrl', 'translateX',tr_x1)
		setKeys(time_defined[1],'l_eye_ctrl', 'translateY',tr_y1)
		setKeys(time_defined[1],'r_eye_ctrl', 'translateX',tr_x1)
		setKeys(time_defined[1],'r_eye_ctrl', 'translateY',tr_y1)
		setKeys(time_defined[1],'neck_head_ctrl', 'rotateX',random.randint(-10,10))
		setKeys(time_defined[1],'neck_head_ctrl', 'rotateY',random.randint(-3,3))

		a= timeR[len(timeR)-1]
		b=a+10
	
		
		setKeys(b,'center_up_lid_1_ctrl', 'translateY',1.5)
		setKeys(b,"mid_low_ctrl", 'translateY',0.8)
		for i in symmetry_list:
			setKeys(b,i+'_up_lid_1_ctrl','translateY',1.5)
			setKeys(b,i+'_lip_low_ctrl','translateY',-1.3)
			setKeys(b,i+'_chin_2_ctrl','translateY',-0.9)
		
		setKeys(b,'left_e_4_ctrl', 'translateY',1)
		setKeys(b,'left_e_4_ctrl', 'translateX',1)
		setKeys(b,'left_e_3_ctrl', 'translateY',-1.7)
		setKeys(b,'left_e_3_ctrl', 'translateX',-1)
		setKeys(b,'left_e_2_ctrl', 'translateY',-2)
		setKeys(b,'left_e_2_ctrl', 'translateX',-1)
		setKeys(b,'left_e_1_ctrl', 'translateY',-2)
		setKeys(b,'left_e_1_ctrl', 'translateX',-1)
		setKeys(b,"left_e_5_ctrl", 'translateX',0.8)	
	
	
def createCtrls():
	'''
	creates the nurbs spheres
	'''
	
	faceUpGrp=[]
	faceLowGrp=[]
	for i in faceUpC:
		cmds.sphere(p=(cmds.getAttr(i+'.tx'), cmds.getAttr(i+'.ty'), cmds.getAttr(i+'.tz')+0.5),
		 ax=(0, 1, 0), ssw=0 ,esw=360,r=0.2, d=3,ut=0,tol=0.01,s=8, nsp=4,ch=1, n=i+'_ctrl')
		cmds.group(i+'_ctrl', n=i+'_grp')
		cmds.xform(i+'_ctrl', cp=True)
		cmds.setAttr(i+'_ctrl.sz',0.2)
		cmds.makeIdentity(i+'_ctrl', apply=True,t=1,r=1,s=1,n=0,pn=1)
		cmds.parent(i+'_jnt', i+'_ctrl')
		ctrlsAllU.append(i+'_ctrl')
		faceUpGrp.append(i+'_grp')
		
	faceLow_without_chin=faceLow[1:]
	for i in faceLow_without_chin:
		cmds.sphere(p=(cmds.getAttr(i+'.tx'), cmds.getAttr(i+'.ty'), cmds.getAttr(i+'.tz')+0.5),
		 ax=(0, 1, 0), ssw=0 ,esw=360,r=0.2, d=3,ut=0,tol=0.01,s=8, nsp=4,ch=1, n=i+'_ctrl')
		cmds.group(i+'_ctrl', n=i+'_grp')
		cmds.xform(i+'_ctrl', cp=True)
		cmds.setAttr(i+'_ctrl.sz',0.2)
		cmds.makeIdentity(i+'_ctrl', apply=True,t=1,r=1,s=1,n=0,pn=1)
		cmds.parent(i+'_jnt', i+'_ctrl')
		ctrlsAllL.append(i+'_ctrl')
		faceLowGrp.append(i+'_grp')
		
	cmds.parent(ctrlsAllU, 'faceUp_grp')	
	cmds.parent(ctrlsAllL, 'faceLow_grp')	
	
	cmds.circle(c=(0,0,-1),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n='mainRoot')
	cmds.setAttr('mainRoot.s',1,1,1)
	cmds.xform('mainRoot',cp=True)
	cmds.setAttr("mainRoot.translateZ",0)
	cmds.makeIdentity('mainRoot', apply=True,t=1,r=1,s=1,n=0,pn=1)
	cmds.parent('root_grp','mainRoot')

	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n='l_eye_ctrl')
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n='r_eye_ctrl')
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n='jaw_drop')

	cmds.setAttr('l_eye_ctrl.rx',90 )	
	cmds.setAttr('r_eye_ctrl.rx',90 )	
	
	cmds.setAttr('l_eye_ctrl.tx',cmds.getAttr('left_eye_base.tx') )	
	cmds.setAttr('l_eye_ctrl.ty',cmds.getAttr('left_eye_base.ty') )	
	cmds.setAttr('l_eye_ctrl.tz',cmds.getAttr('left_eye_base.tz')+1 )	
	cmds.setAttr('r_eye_ctrl.tx',cmds.getAttr('right_eye_base.tx') )	
	cmds.setAttr('r_eye_ctrl.ty',cmds.getAttr('right_eye_base.ty') )	
	cmds.setAttr('r_eye_ctrl.tz',cmds.getAttr('right_eye_base.tz')+1 )	
	
	cmds.setAttr('jaw_drop.tx',cmds.getAttr('center_chin.tx'))
	cmds.setAttr('jaw_drop.ty',cmds.getAttr('center_chin.ty'))
	cmds.setAttr('jaw_drop.tz',cmds.getAttr('center_chin.tz')+1)
	cmds.setAttr('jaw_drop.s',5,5,5 )	
	cmds.setAttr('jaw_drop.rx',-45 )	
	
	cmds.makeIdentity('jaw_drop','l_eye_ctrl','r_eye_ctrl',apply=True,t=1,r=1,s=1,n=0,pn=1)
	
	#add jaw drop
	listAdd=['jaw_drop','Jaw_left_right','rotatejaw_x']
	for i in listAdd:
		cmds.addAttr('jaw_drop',ln=i,at='double',dv=1)
		cmds.setAttr('jaw_drop.'+i,e=True,keyable=True)
		
	cmds.connectAttr('jaw_drop.jaw_drop','before_jaw_jnt.rotate.rotateZ',f=True)
	cmds.connectAttr('jaw_drop.Jaw_left_right','before_jaw_jnt.rotate.rotateY',f=True)	
	cmds.connectAttr('jaw_drop.rotatejaw_x','before_jaw_jnt.rotate.rotateX',f=True)	
	
		
	cmds.parent('left_eye_base_jnt','faceUp_grp')	
	cmds.parent('right_eye_base_jnt','faceUp_grp')	
	
	cmds.delete('left_eye_base_ctrl','right_eye_base_ctrl')
	cmds.aimConstraint('l_eye_ctrl','left_eye_base_jnt' ,mo=True ,w=1 )
	cmds.aimConstraint('r_eye_ctrl','right_eye_base_jnt' ,mo=True ,w=1 )
	
	cmds.parent('jaw_drop','l_eye_ctrl','r_eye_ctrl', 'mainRoot')
	cmds.group( 'mainRoot', n='ROOT_ctrl')
	
	#cmds.addAttr('|ROOT_ctrl|t_end_ctrl',ln="value",at='double',dv=0.5)
	#cmds.setAttr('|ROOT_ctrl|t_end_ctrl.value',e=True,keyable=True)
	#cmds.connectAttr('t_end_ctrl.value', 'tongue_sqrtStretch_pow.input2X',f=True)
	
	cmds.parent('neck_head_ctrl', 'ROOT_ctrl')	
#	cmds.parent('tongue_distance', 't_ctrl1', 'ik_tongue', 'tongue_crv', 't_end_ctrl','ROOT_ctrl')
	
	#scale global for the tongue
	'''	
	cmds.shadingNode('multiplyDivide', au=True, n='global_scale_tongue')	
	cmds.setAttr("global_scale_tongue.operation", 2)
	cmds.connectAttr('tongue_distanceShape.distance','global_scale_tongue.input1X',f=True )
	cmds.connectAttr('ROOT_ctrl.scaleY','global_scale_tongue.input2X', f=True )
	cmds.connectAttr('global_scale_tongue.outputX','tongue_mulDiv.input1X', f=True )
	cmds.setAttr("tongue_crv.inheritsTransform",0)
	'''
	#cleaning the scene
	for i in faceUpGrp:
		cmds.parent(i,'faceUp_grp')
		cmds.makeIdentity(i, apply=True,t=1,r=1,s=1,n=0,pn=1)
	
	for i in faceLowGrp:
		cmds.parent(i,'faceLow_grp')
		cmds.makeIdentity(i, apply=True,t=1,r=1,s=1,n=0,pn=1)
	
	for i in faceLow2:
		cmds.parent(i+'_ctrl',i+'_grp')
	for i in faceUpNoCC:
		cmds.parent(i+'_ctrl',i+'_grp')
	
	
def skinMesh():
	'''
	attatching the mesh to the joints
	'''
	
	cmds.skinCluster('left_eye_base_jnt','pSphere1')
	cmds.skinCluster('right_eye_base_jnt','pSphere2')
	
	j=cmds.ls(type='joint')
	j_without_tongue=[]
	unwanted = ['tongue_1_jnt','tongue_2_jnt','tongue_3_jnt','tongue_4_jnt',
				'tongue_1_jnt_IK','tongue_2_jnt_IK','tongue_3_jnt_IK','tongue_4_jnt_IK',
				'tongue_1_jnt_FK','tongue_2_jnt_FK','tongue_3_jnt_FK','tongue_4_jnt_FK']
	item_list = j
	j_without_tongue= list(set(item_list).difference(set(unwanted)))
	
	#print j_without_tongue
	cmds.skinCluster(j_without_tongue, 'low')
	cmds.parent('tongue_1_jnt', 'tongue_1_jnt_IK','tongue_1_jnt_FK' ,'before_jaw_jnt')
	cmds.parent('lowerjaw','before_jaw_jnt')
	cmds.parent('Upperjaw','upper_jaw_jnt')
	
	cmds.skinCluster('tongue_1_jnt', 'tongue_2_jnt', 'tongue_3_jnt', 'tongue_4_jnt','tongue',tsb=True)

def measureDistance():
	'''
	measuring the avg meeting point of two joints
	'''
	measureList=['left','right','center']
	
	left_up_lid_1_xyz=[cmds.getAttr('left_up_lid_1.tx'),cmds.getAttr('left_up_lid_1.ty'),cmds.getAttr('left_up_lid_1.tz')]
	left_lip_low_xyz=[cmds.getAttr('left_lip_low.tx'),cmds.getAttr('left_lip_low.ty'),cmds.getAttr('left_lip_low.tz')]
	cmds.distanceDimension(sp=(left_up_lid_1_xyz[0],left_up_lid_1_xyz[1],left_up_lid_1_xyz[2]),ep=(left_lip_low_xyz[0],left_lip_low_xyz[1],left_lip_low_xyz[2]))
	cmds.parent('left_up_lid_1', 'left_up_lid_1_ctrl')	
	cmds.parent('left_lip_low', 'left_lip_low_ctrl')	
	
	center_up_lid_1_xyz=[cmds.getAttr('center_up_lid_1.tx'),cmds.getAttr('center_up_lid_1.ty'),cmds.getAttr('center_up_lid_1.tz')]
	mid_low_xyz=[cmds.getAttr('mid_low.tx'),cmds.getAttr('mid_low.ty'),cmds.getAttr('mid_low.tz')]
	cmds.distanceDimension(sp=(center_up_lid_1_xyz[0],center_up_lid_1_xyz[1],center_up_lid_1_xyz[2]),ep=(mid_low_xyz[0],mid_low_xyz[1],mid_low_xyz[2]))
	cmds.parent('center_up_lid_1', 'center_up_lid_1_ctrl')	
	cmds.parent('mid_low', 'mid_low_ctrl')	
	
	right_up_lid_1_xyz=[cmds.getAttr('right_up_lid_1.tx'),cmds.getAttr('right_up_lid_1.ty'),cmds.getAttr('right_up_lid_1.tz')]
	right_lip_low_xyz=[cmds.getAttr('right_lip_low.tx'),cmds.getAttr('right_lip_low.ty'),cmds.getAttr('right_lip_low.tz')]
	cmds.distanceDimension(sp=(right_up_lid_1_xyz[0],right_up_lid_1_xyz[1],right_up_lid_1_xyz[2]),ep=(right_lip_low_xyz[0],right_lip_low_xyz[1],right_lip_low_xyz[2]))
	cmds.parent('right_up_lid_1', 'right_up_lid_1_ctrl')	
	cmds.parent('right_lip_low', 'right_lip_low_ctrl')	
	
	cmds.rename('distanceDimension1', 'left_lips_dist')
	cmds.rename('distanceDimension2', 'center_lips_dist')
	cmds.rename('distanceDimension3', 'right_lips_dist')
	
	cmds.shadingNode('transform',au=True ,n='minus_plus_one')
	cmds.setAttr("minus_plus_one.translateX",-1)
	cmds.setAttr("minus_plus_one.translateY",1)
	#multiply divide nodes
	for i in measureList:
		cmds.shadingNode('multiplyDivide',au=True ,n=i+'_lips_mulDiv_measure')
		cmds.setAttr(i+"_lips_mulDiv_measure.input2X", 2)
		cmds.connectAttr(i+"_lips_distShape.distance", i+"_lips_mulDiv_measure.input1X", f=True)
		cmds.setAttr(i+"_lips_mulDiv_measure.operation",2)
		
		cmds.shadingNode('plusMinusAverage',au=True, n=i+'_plusMinusAvg_up')
		cmds.shadingNode('plusMinusAverage',au=True, n=i+'_plusMinusAvg_down')
		
		cmds.connectAttr('minus_plus_one.translateX', i+'_plusMinusAvg_up.input1D[1]',f=True)
		cmds.connectAttr(i+'_lips_mulDiv_measure.outputX', i+'_plusMinusAvg_up.input1D[0]',f=True)
		
		cmds.connectAttr('minus_plus_one.translateY', i+'_plusMinusAvg_down.input1D[0]',f=True)  
		cmds.connectAttr(i+'_lips_mulDiv_measure.outputX',  i+'_plusMinusAvg_down.input1D[1]',f=True)
		
		for j in range(0,2):
			if j==0:
				cmds.shadingNode('transform',au=True,n=i+'_answer_UP')
			if j==1:
				cmds.shadingNode('transform',au=True,n=i+'_answer_DOWN')
		cmds.connectAttr(i+'_plusMinusAvg_down.output1D', i+'_answer_DOWN.translateY',f=True)
		cmds.connectAttr(i+'_plusMinusAvg_up.output1D', i+'_answer_UP.translateY',f=True)
		cmds.setAttr(i+"_plusMinusAvg_down.operation",2)

		###helps closing and opening the mouth by taking the values from the transform groups

	cmds.group('left_lips_dist', 'center_lips_dist','right_lips_dist', 'minus_plus_one', 'left_answer_UP', 'left_answer_DOWN', 'right_answer_UP', 'right_answer_DOWN', 'center_answer_UP', 'center_answer_DOWN',n='distances_grp')
	cmds.parent('distances_grp','ROOT_ctrl')
	
def checkFound(found, nameOfJnts):
	'''
	checks if the locators are named appropriately and creates the joints
	'''
	if len(found) == len(nameOfJnts):
		print('all '+str(nameOfJnts)+' exist')
		for i in nameOfJnts:
			cmds.joint(i,n=str(i)+'_jnt',rad=0.2)
	else:
		print( str(nameOfJnts)+'is not named properly')				
	 ###

def checkLocExist(*args):
	'''
	checks if the locators exist and creates FK IK and results joints 
	'''
	arrayBody=[cmds.ls(faceUpCC,r=True),cmds.ls(faceUpL,r=True),cmds.ls(faceUpR,r=True),cmds.ls(jointList,r=True),cmds.ls(tongue_,r=True),cmds.ls(faceLow,r=True)] 
	funcBody=[faceUpCC,faceUpL,faceUpR, jointList, tongue_, faceLow] 
	for i in range(0,len(arrayBody)):
		checkFound(arrayBody[i],funcBody[i])
	spineHead()
	createCtrls()
	#skinMesh()
	#measureDistance()

def importSounds():
	'''
	imporing the sounds
	'''
	###sound folder with all the letter sounds 
	###change if another machine is used
	source = 'C:\Users\Anna Georgieva\Documents\Audacity'
	for root, dirs, filenames in os.walk(source):
		for f in filenames:
			fullpath = os.path.join(source, f)
			file_names_list.append(fullpath)
		
	for j in file_names_list:	
		cmds.file(j,i=True ,type="audio",  ignoreVersion=True, ra=True,mergeNamespacesOnClash=False, pr=True)
		temp=os.path.basename(j)
		cmds.setAttr(os.path.splitext(temp)[0]+'.mute',1)
		print j 
		
	print len(file_names_list),' sounds imported'	
	
def sayText(*args):
	'''
	playing the animation
	'''
	#engine = pyttsx.init()
	#engine.say(textInput)
	#engine.runAndWait()
	
	#play the animation
	cmds.currentTime(0, update=True)
	cmds.playbackOptions( loop='continuous',ps=1)
	cmds.play( forward=True )
	
	
	#gPlayBackSlider = maya.mel.eval( '$tmpVar=$gPlayBackSlider' )
	#cmds.timeControl( gPlayBackSlider, edit=True, sound='audio1' )



def advanceWithTime(direction='forward'):
	snd=cmds.timeControl(mel.eval('$var=$gPlayBackSlider'),q=True,s=True)
	if direction=='forward':
		cmds.play( forward=True, sound=snd,playSound=True, st=True)
		time.sleep(0.2)
		cmds.currentTime(cmds.currentTime(q=True) + 1, e=True)
		cmds.play( forward=True, sound=snd,playSound=True, st=False)
	else:
		cmds.play( forward=False, sound=snd,playSound=True, st=True)
		time.sleep(0.2)
		cmds.currentTime(cmds.currentTime(q=True) - 1, e=True)
		cmds.play( forward=False, sound=snd,playSound=True, st=False)

#Call for forward 
#advanceWithTime('forward')

#Call for backward
#advanceWithTime('back')
	
def sum(n):
    if n == 0:
        return 0
    return n + sum(n - 1)	

def closeOpenEyes(i):
	symmetry_list=['left','right']
	before=i-3
	after=i+3

	for j in symmetry_list:
		setKeys(before, j+'_eyelid_1_ctrl', 'translateY', 0)
		setKeys(before, j+'_eyelid_2_ctrl', 'translateY', 0)
		setKeys(before, j+'_eyelid_2_ctrl', 'translateZ', 0)
		setKeys(before, j+'_eyelid_3_ctrl', 'translateY', 0)
		setKeys(before, j+'_eyelid_3_ctrl', 'translateZ', 0)
		setKeys(before, j+'_eyelid_4_ctrl', 'translateY', 0)
		setKeys(before, j+'_eyelid_4_ctrl', 'translateZ', 0)
		setKeys(before, j+'_eyelid_5_ctrl', 'translateY', 0)
		setKeys(before, j+'_eyelid_5_ctrl', 'translateZ', 0)
		setKeys(before, j+'_eyelid_6_ctrl', 'translateY', 0)
		setKeys(before, j+'_eyelid_6_ctrl', 'translateZ', 0)
		
	for j in symmetry_list:
		setKeys(i, j+'_eyelid_1_ctrl', 'translateY', -2.5)
		setKeys(i, j+'_eyelid_2_ctrl', 'translateY', -3)
		setKeys(i, j+'_eyelid_2_ctrl', 'translateZ', 0.3)
		setKeys(i, j+'_eyelid_3_ctrl', 'translateY', -2)
		setKeys(i, j+'_eyelid_3_ctrl', 'translateZ', 0.3)
		setKeys(i, j+'_eyelid_4_ctrl', 'translateY', 0.3)
		setKeys(i, j+'_eyelid_4_ctrl', 'translateZ', 0.4)
		setKeys(i, j+'_eyelid_5_ctrl', 'translateY', 1)
		setKeys(i, j+'_eyelid_5_ctrl', 'translateZ', 1)
		setKeys(i, j+'_eyelid_6_ctrl', 'translateY', 0.3)
		setKeys(i, j+'_eyelid_6_ctrl', 'translateZ', 0.4)

	for j in symmetry_list:
		setKeys(after, j+'_eyelid_1_ctrl', 'translateY', 0)
		setKeys(after, j+'_eyelid_2_ctrl', 'translateY', 0)
		setKeys(after, j+'_eyelid_2_ctrl', 'translateZ', 0)
		setKeys(after, j+'_eyelid_3_ctrl', 'translateY', 0)
		setKeys(after, j+'_eyelid_3_ctrl', 'translateZ', 0)
		setKeys(after, j+'_eyelid_4_ctrl', 'translateY', 0)
		setKeys(after, j+'_eyelid_4_ctrl', 'translateZ', 0)
		setKeys(after, j+'_eyelid_5_ctrl', 'translateY', 0)
		setKeys(after, j+'_eyelid_5_ctrl', 'translateZ', 0)
		setKeys(after, j+'_eyelid_6_ctrl', 'translateY', 0)
		setKeys(after, j+'_eyelid_6_ctrl', 'translateZ', 0)

def readText(text, startFrame, endFrame, pauseFrame,user_answer):
	'''
	
	text = text input
	startFrame = begin the animation from the startFrame
	endFrame = end the animation from the stopFrame
	user_answer = yes or no depending on the answer of the user
	
	'''
		 
	#import the sounds
	if not file_names_list:
		print("sound list is empty")
		importSounds() 
	else:
		print("sound list is not empty")
	if not timeR:
		print("timeR list is empty")
	else:
		print("timeR list is not empty")
		del timeR[:]
		print("timeR is clean now, press the button again")
		
		
	#takes the written text
	textInput=cmds.textField(text, q=True, text=True)
	#if empty check
	if not textInput:
		print("enter a text first")
	else:
		#print check
		print "startFrame", startFrame
		print "endFrame", endFrame
		print "pauseFrame", pauseFrame
		print textInput
		
		#loading the Alphabet upper and lower case chars
		for i in range(65, 91):
			alphabet_listUpper.append(chr(i))
		for i in range(97,123):
			alphabet_listLower.append(chr(i))
		
		# n_chars storing the total characters in a text
		n_chars=len(textInput)-1
		
		#words list stores the split sentences in list of words
		words=split_words(textInput)
		 
		#n_words stores how many letters does the word have
		#n_letters checks if there is more than one sentence
		n_words=[]
		n_letters=[]
	
		for i in words:
			n_words.append(len(i)) 
			for j in i:
				n_letters.append(len(j))
		
		#print check
		print 'there are: ', n_words, ' number of words'		
		print 'there are: ', n_letters,' letters in each word'	
		print 'there are: [', n_chars,'] number of characters'	
	
		 
		#if the user wants equally keyframed animation
		if user_answer=='yes':
			endMinusStart=endFrame-startFrame
			frameByLetter=endMinusStart/n_chars
			for j in range(0, n_chars):
				add=startFrame+frameByLetter*j
				timeR.append(add)
			#print timeR
		
		#sum_array stores the sum between the pause frame and the previous one depending on the length of the word
		sumArray=[] 
		#pause array that stores the positions of all the spacebars entered so that they can be included later
		pauseArray=[]
		
		#if the user wants non-equally keyframed animation
		if user_answer=='no':
			#print 'non-equally keyframed' 
			#count the spaces if needed 
			charSpace=' '
			n_space=count_letter(textInput, charSpace) 
			#print 'n_space', n_space 
			
			#space indexes stored in spaceArray
			spaceArray=[pos for pos, char in enumerate(textInput) if char == charSpace]
			#empty array for calculations
			newTimeRate=[]		
			
			#the rule is 6 frames per letter as they are zeroed before and after 3 frames 
			for i in n_letters:
				#if a word is has a 10 characters
				for j in range(0, 10):
					#if the length of the current word equals the number from 0(min) to 10(max)
					#define the time range allocated for the word
					if i==j:
						timeFrames=j*6
						newTimeRate.append(timeFrames)
				#print newTimeRate
			
			#assign for every space the pauseFrame number
			for i in range(0, len(newTimeRate)-1):
				pauseArray.append(pauseFrame)	
			#print pauseArray
		
			#insert the pause frames numbers in between the allocated times for the letters
			for i,v in enumerate(pauseArray):
				newTimeRate.insert(2*i+1,v)
			#print newTimeRate
			
			#calculates the first keyframe position of the first letter in each word
			sum_=0
			for i in range(0, len(newTimeRate)-1):
				sum_ += newTimeRate[i]
				sumArray.append(sum_)
			#print sumArray
			
			#start from zero 
			add_six=0

			for i in range(0,n_letters[0]):
				add_six+=6
				timeR.append(add_six)				
			
			arr1=[]
			arr2=[]
			for i in range(2,len(n_letters)):
				arr1.append(i)
			for i in range(3,arr1[len(arr1)-1]+5,2):
				arr2.append(i)
			#print arr1
			#print arr2
			
			for i in range(0,n_letters[1]):
				sumArray[1]+=6
				timeR.append(sumArray[1])
				
			for x,y in zip(arr1,arr2):
				for i in range(0, n_letters[x]):
					#print i
					sumArray[y]+=6
					timeR.append(sumArray[y])
			
			#insert the spaces into their indexes
			for i in range(0, len(spaceArray)):
				timeR.insert(spaceArray[i], 0)
	
		#two dictionaries for timeR and characters from the text, each enumerated.
		enum_list=[]
		char_list=[]
		for i, character in enumerate(textInput):
			 enum_list.append(i)
			 char_list.append(str(character))
			
		dictionary_frames={}
		dictionary_letters={}
		
		keys1=range(n_chars)
		keys2=range(n_chars)
	
		values1=timeR
		values2=char_list
		
		for i, k in zip(keys1,keys2): 
			dictionary_frames[i]=values1[i]
			dictionary_letters[k]=values2[k]
			
		diffkeys = [k for k in dictionary_frames if dictionary_frames[k] != dictionary_letters[k]]
		for k in diffkeys:
			print k, ':', dictionary_frames[k], '->', dictionary_letters[k]
		
		# main loop
		searchALL=alphabet_listLower+alphabet_listUpper
		for i in searchALL:
			search(dictionary_letters,i)
			temp_pos=(search.a)
			#print 'letter appears on spaces', i, 'position', temp_pos
			for k in temp_pos:
				unknown_key(dictionary_frames[k],i)
		
def search(myDict, search1):
    search.a=[]
    for key, value in myDict.items():
        if search1 in value:
            search.a.append(key)
            

t_list=[ 'tongue_1_jnt_FK', 'tongue_2_jnt_FK', 'tongue_3_jnt_FK']	
lips_list=['left_chin_2_ctrl','right_chin_2_ctrl','left_lip_1_ctrl','right_lip_1_ctrl', 'left_up_lid_2_ctrl','right_up_lid_2_ctrl', 'left_up_lid_1_ctrl','right_up_lid_1_ctrl' ,'center_up_lid_1_ctrl','right_lip_low_ctrl' ,'mid_low_ctrl' ,'left_lip_low_ctrl']
reset_list=['tx','ty','tz','rx','ry','rz']
	

def clear_lips(time):
	for x in lips_list:
		for y in reset_list:
			cmds.setAttr(x+'.'+y,0)
			setKeys(time, x,y,0)


def unknown_key(t_temp,letter):
	#for i,k in zip (alphabet_listLower, alphabet_listUpper):
	if letter == 'a' or letter=='A':
		a_short_key(t_temp, t_list)
	if letter == 'b' or letter=='B':
		b_key( t_temp)
	if letter == 'c' or letter=='C':
		c_key( t_temp,t_list)
	if letter == 'd' or letter=='D':
		d_key( t_temp)
	if letter == 'e' or letter=='E':
		e_key( t_temp)
	if letter == 'f' or letter=='F':
		f_key( t_temp)
	if letter == 'g' or letter=='G':
		g_key( t_temp)
	if letter == 'h' or letter=='H':
		h_key( t_temp)
	if letter == 'i' or letter=='I':
		i_key(t_list, t_temp)
	if letter == 'j' or letter=='J':
		j_key( t_temp)
	if letter == 'k' or letter=='K':
		k_key( t_temp)
	if letter == 'l' or letter=='L':
		l_key( t_temp)
	if letter == 'm' or letter=='M':
		m_key( t_temp)
	if letter == 'n' or letter=='N':
		n_key( t_temp)
	if letter == 'o' or letter=='O':
		o_key( t_temp)
	if letter == 'p' or letter=='P':
		p_key( t_temp)
	if letter == 'q' or letter=='Q':
		q_key( t_temp)
	if letter == 'r' or letter=='R':
		r_key( t_temp)
	if letter == 's' or letter=='S':
		s_key( t_temp,t_list)
	if letter == 't' or letter=='T':
		t_key( t_temp)
	if letter == 'u' or letter=='U':
		u_key( t_temp)
	if letter == 'v' or letter=='V':
		v_key( t_temp)
	if letter == 'w' or letter=='W':
		w_key( t_temp)
	if letter == 'x' or letter=='X':
		x_key( t_temp)
	if letter == 'y'or letter=='Y':
		y_key( t_temp)
	if letter == 'z' or letter=='Z':
		z_key( t_temp)
	

def a_long_key(i):  #a==ei
	#ei 
	
	#e 
	before=i-3
	after=i+3
	
	clear_lips(before)
	setKeys(i, 'jaw_drop','jaw_drop', -10)
	setKeys(i,'tongue_2_jnt_FK','rotateZ',-30)
	setKeys(i,'tongue_1_jnt_FK','rotateZ',20)
	setKeys(i,'tongue_3_jnt_FK','rotateZ',33)
	
	#i
	setKeys(i+1, 'jaw_drop', 'jaw_drop', -2)
	setKeys(i+1, 'tongue_1_jnt_FK', 'rotateZ', 3)
	setKeys(i+1, 'tongue_2_jnt_FK', 'rotateZ', -3)
	setKeys(i+1, 'tongue_3_jnt_FK', 'rotateZ', 25)
	
	cmds.sound( offset=i+1, file=file_names_list[2]) #ei sound 
	clear_lips(after)
	
	
def a_short_key(i,t_list): 
	#a
	before=i-3
	after=i+3
	
	clear_lips(before)
	for t in t_list:
		setKeys(i, t, 'rotateZ', 0)
	setKeys(i, 'jaw_drop', 'jaw_drop', -10)
	cmds.sound( offset=i, file=file_names_list[2])
	
	clear_lips(after)

def b_key(i):  
	#b
	
	before=i-3
	after=i+3
	
	clear_lips(before)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateY',2.6)
	setKeys(i, 'right_lip_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'right_lip_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'left_lip_low_ctrl', 'translateY',2.6)
	setKeys(i, 'left_lip_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'mid_low_ctrl', 'translateY',2.4)
	setKeys(i, 'mid_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'mid_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY',-1.6)
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'right_up_lid_1_ctrl', 'rotateX',-3)
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY',-1.6)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'left_up_lid_1_ctrl', 'rotateX',-3)
	
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY',-3)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'center_up_lid_1_ctrl', 'rotateX',15)
	
	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	
	cmds.sound( offset=i, file=file_names_list[6])
	clear_lips(after)
	
def bl_key(i):
	#b
	before=i-3
	after=i+3
	
	clear_lips(before)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateY',2.6)
	setKeys(i, 'right_lip_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'right_lip_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'left_lip_low_ctrl', 'translateY',2.6)
	setKeys(i, 'left_lip_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'mid_low_ctrl', 'translateY',2.4)
	setKeys(i, 'mid_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'mid_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY',-1.6)
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'right_up_lid_1_ctrl', 'rotateX',-3)
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY',-1.6)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'left_up_lid_1_ctrl', 'rotateX',-3)
	
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY',-3)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'center_up_lid_1_ctrl', 'rotateX',15)
	
	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	cmds.sound( offset=i, file=file_names_list[6])
	
	#
	setKeys(i, "center_up_lid_1_ctrl","rotateX", 0)
	#l
	
	setKeys(i+1,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i+1,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i+1,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i+1, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	
	setKeys(i+1, 'jaw_drop', 'jaw_drop', 0)
	clear_lips(after)
	cmds.sound( offset=i+1, file=file_names_list[23])
	
	
	
def c_short_key(i):
	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 6)
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', -6)
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 12)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 1)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY',2)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 1)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'mid_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'left_lip_low_ctrl', 'translateY', -0.8)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', 0.8)
	
	setKeys(i, 'right_lip_low_ctrl', 'rotateX', 0)
	setKeys(i, 'mid_low_ctrl', 'rotateX',0)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX', 0)
	cmds.sound( offset=i, file=file_names_list[34])

def c_key(i,t_list): #c==s
	#c
	before=i-3
	after=i+3
	
	clear_lips(before)
	
	for t in t_list:
		setKeys(before, t, 'rotateZ', 0)

	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 6)
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', -6)
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 12)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 1)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY',2)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 1)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'mid_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'left_lip_low_ctrl', 'translateY', -0.8)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', 0.8)
	
	setKeys(i, 'right_lip_low_ctrl', 'rotateX', 0)
	setKeys(i, 'mid_low_ctrl', 'rotateX',0)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX', 0)
	
	cmds.sound( offset=i, file=file_names_list[34])

	for t in t_list:
		setKeys(after, t, 'rotateZ', 0)
	clear_lips(after)
	
		
def cl_key(i):	
	before=i-3
	after=i+3
	
	clear_lips(before)
	#c
	for t in t_list:
		setKeys(before, t, 'rotateZ', 0)

	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 6)
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', -6)
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 12)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 1)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY',2)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 1)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'mid_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'left_lip_low_ctrl', 'translateY', -0.8)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', 0.8)
	
	setKeys(i, 'right_lip_low_ctrl', 'rotateX', 0)
	setKeys(i, 'mid_low_ctrl', 'rotateX',0)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX', 0)
	cmds.sound( offset=i, file=file_names_list[34])
	#
	setKeys(i, "center_up_lid_1_ctrl","rotateX", 0)
	#l 
	
	setKeys(i+1,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i+1,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i+1,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i+1, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	cmds.sound( offset=i+1, file=file_names_list[23])
	
	clear_lips(after)
		
def d_key(i): #d
	
	#set the time 
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	
	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	
	cmds.sound( offset=i, file=file_names_list[8])
	clear_lips(after)
	

def e_key(i):
	#e
	
	before=i-3
	after=i+3
	clear_lips(before)
	setKeys(i, 'jaw_drop','jaw_drop', -10)
	
	setKeys(i,'tongue_2_jnt_FK','rotateZ',-30)
	setKeys(i,'tongue_1_jnt_FK','rotateZ',20)
	setKeys(i,'tongue_3_jnt_FK','rotateZ',33)
	cmds.sound( offset=i, file=file_names_list[11])
	
	clear_lips(after)
	
def e_long_key(i):
	##ee
	setKeys(i, 'jaw_drop','jaw_drop', -5)
	
	setKeys(i,'tongue_2_jnt_FK','rotateZ',-30)
	setKeys(i,'tongue_1_jnt_FK','rotateZ',20)
	setKeys(i,'tongue_3_jnt_FK','rotateZ',33)
	cmds.sound( offset=i, file=file_names_list[14])


def f_short(i):
	setKeys(i, 'right_lip_low_ctrl', 'translateY', 1.5)		
	setKeys(i, 'right_lip_low_ctrl', 'translateZ', -1)	
	setKeys(i, 'right_lip_low_ctrl', 'rotateX', -18)	
			
	setKeys(i, 'left_lip_low_ctrl', 'translateY', 1.5)		
	setKeys(i, 'left_lip_low_ctrl', 'translateZ', -1)		
	setKeys(i, 'left_lip_low_ctrl', 'rotateX', -18)		
	
	setKeys(i, 'mid_low_ctrl', 'translateY', 2)		
	setKeys(i, 'mid_low_ctrl', 'translateZ', -1)		
	setKeys(i, 'mid_low_ctrl', 'rotateX', -16)		
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', -0.4)		
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', -1.2)		
	setKeys(i, 'right_up_lid_1_ctrl', 'rotateX', -18)		
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', -0.4)		
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', -1.2)		
	setKeys(i, 'left_up_lid_1_ctrl', 'rotateX', -18)		
	
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', -0.4)		
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', -1)		
	setKeys(i, 'center_up_lid_1_ctrl', 'rotateX', -18)		
	cmds.sound( offset=i, file=file_names_list[16])

def f_key(i):
	#print 'f_key', i
	
	#set the time 
	before=i-3
	after=i+3
	clear_lips(before)
		
	setKeys(i, 'right_lip_low_ctrl', 'translateY', 1.5)		
	setKeys(i, 'right_lip_low_ctrl', 'translateZ', -1)	
	setKeys(i, 'right_lip_low_ctrl', 'rotateX', -18)	
			
	setKeys(i, 'left_lip_low_ctrl', 'translateY', 1.5)		
	setKeys(i, 'left_lip_low_ctrl', 'translateZ', -1)		
	setKeys(i, 'left_lip_low_ctrl', 'rotateX', -18)		
	
	setKeys(i, 'mid_low_ctrl', 'translateY', 2)		
	setKeys(i, 'mid_low_ctrl', 'translateZ', -1)		
	setKeys(i, 'mid_low_ctrl', 'rotateX', -16)		
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', -0.4)		
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', -1.2)		
	setKeys(i, 'right_up_lid_1_ctrl', 'rotateX', -18)		
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', -0.4)		
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', -1.2)		
	setKeys(i, 'left_up_lid_1_ctrl', 'rotateX', -18)		
	
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', -0.4)		
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', -1)		
	setKeys(i, 'center_up_lid_1_ctrl', 'rotateX', -18)		
	
	cmds.sound( offset=i, file=file_names_list[16])
	setKeys(i, 'jaw_drop','jaw_drop', 2)
	
	clear_lips(after)
	
def fl_key(i):
	#f
	before=i-3
	after=i+3
	clear_lips(before)
		
	setKeys(i, 'right_lip_low_ctrl', 'translateY', 1.5)		
	setKeys(i, 'right_lip_low_ctrl', 'translateZ', -1)	
	setKeys(i, 'right_lip_low_ctrl', 'rotateX', -18)	
			
	setKeys(i, 'left_lip_low_ctrl', 'translateY', 1.5)		
	setKeys(i, 'left_lip_low_ctrl', 'translateZ', -1)		
	setKeys(i, 'left_lip_low_ctrl', 'rotateX', -18)		
	
	setKeys(i, 'mid_low_ctrl', 'translateY', 2)		
	setKeys(i, 'mid_low_ctrl', 'translateZ', -1)		
	setKeys(i, 'mid_low_ctrl', 'rotateX', -16)		
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', -0.4)		
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', -1.2)		
	setKeys(i, 'right_up_lid_1_ctrl', 'rotateX', -18)		
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', -0.4)		
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', -1.2)		
	setKeys(i, 'left_up_lid_1_ctrl', 'rotateX', -18)		
	
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', -0.4)		
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', -1)		
	setKeys(i, 'center_up_lid_1_ctrl', 'rotateX', -18)	
	cmds.sound( offset=i, file=file_names_list[16])	
	#
	setKeys(i, 'jaw_drop','jaw_drop', 2)
	#l
	setKeys(i+1,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i+1,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i+1,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i+1, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	cmds.sound( offset=i+1, file=file_names_list[23])
	
	clear_lips(after)
	
def g_key(i): ##g==j==sh==zh==ch
#	print 'G keys on joints', '::',i
	
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i, 'mid_low_ctrl','translateY', -0.8)	
	setKeys(i, 'mid_low_ctrl','translateZ', 1.2)	
	
	setKeys(i, 'right_lip_low_ctrl','translateY', -0.3)
	setKeys(i, 'right_lip_low_ctrl',	'translateZ', 1.5)
	setKeys(i, 'right_lip_low_ctrl',	'rotateX', 20)
	setKeys(i, 'right_lip_low_ctrl',	'rotateY', -10)
	setKeys(i, 'right_lip_low_ctrl',	'rotateZ', 3)
	
	setKeys(i, 'left_lip_low_ctrl','translateY', -0.3)
	setKeys(i, 'left_lip_low_ctrl',	'translateZ', 1.5)
	setKeys(i, 'left_lip_low_ctrl',	'rotateX', 20)
	setKeys(i, 'left_lip_low_ctrl',	'rotateY', -10)
	setKeys(i, 'left_lip_low_ctrl',	'rotateZ', -3)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 2.6)		
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', 0.5)
	setKeys(i, 'right_up_lid_1_ctrl', 'rotateX', -30)
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 2.6)		
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', 0.5)
	setKeys(i, 'left_up_lid_1_ctrl', 'rotateX', -30)
	
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', 3.5)		
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', 0.5)
	setKeys(i, 'center_up_lid_1_ctrl', 'rotateX', -30)
	
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 20)		
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', -25)		
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 33)		

	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	cmds.sound( offset=i, file=file_names_list[9])
	clear_lips(after)
	
def g_short_key(i): ##g==k
	
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i, 'mid_low_ctrl','translateY', -0.8)	
	setKeys(i, 'mid_low_ctrl','translateZ', 1.2)	
	
	setKeys(i, 'right_lip_low_ctrl','translateY', -0.3)
	setKeys(i, 'right_lip_low_ctrl',	'translateZ', 1.5)
	setKeys(i, 'right_lip_low_ctrl',	'rotateX', 20)
	setKeys(i, 'right_lip_low_ctrl',	'rotateY', -10)
	setKeys(i, 'right_lip_low_ctrl',	'rotateZ', 3)
	
	setKeys(i, 'left_lip_low_ctrl','translateY', -0.3)
	setKeys(i, 'left_lip_low_ctrl',	'translateZ', 1.5)
	setKeys(i, 'left_lip_low_ctrl',	'rotateX', 20)
	setKeys(i, 'left_lip_low_ctrl',	'rotateY', -10)
	setKeys(i, 'left_lip_low_ctrl',	'rotateZ', -3)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 2.6)		
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', 0.5)
	setKeys(i, 'right_up_lid_1_ctrl', 'rotateX', -30)
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 2.6)		
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', 0.5)
	setKeys(i, 'left_up_lid_1_ctrl', 'rotateX', -30)
	
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', 3.5)		
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', 0.5)
	setKeys(i, 'center_up_lid_1_ctrl', 'rotateX', -30)
	
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 20)		
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', -25)		
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 33)		

	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	cmds.sound( offset=i, file=file_names_list[9])
	clear_lips(after)

def kl_key(i):
	#k
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	
	setKeys(i, 'left_lip_low_ctrl', 'translateY', -1.2)
	setKeys(i, 'right_lip_low_ctrl', 'translateY', -1.2)
	setKeys(i, 'mid_low_ctrl', 'translateY', -1.2)
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', -0.3)
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', -0.3)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', -0.3)
	
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 0)		
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', 0)		
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 0)	
	cmds.sound( offset=i, file=file_names_list[22])
		
	#
	setKeys(i, 'jaw_drop','jaw_drop', 2)
	#l
	setKeys(i+1,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i+1,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i+1,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i+1, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	cmds.sound( offset=i+1, file=file_names_list[23])
	
	clear_lips(after)
	
def pl_key(i):
	#p
	before=i-3
	after=i+3
	
	clear_lips(before)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateY',2.6)
	setKeys(i, 'right_lip_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'right_lip_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'left_lip_low_ctrl', 'translateY',2.6)
	setKeys(i, 'left_lip_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'mid_low_ctrl', 'translateY',2.4)
	setKeys(i, 'mid_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'mid_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY',-1.6)
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'right_up_lid_1_ctrl', 'rotateX',-3)
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY',-1.6)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'left_up_lid_1_ctrl', 'rotateX',-3)
	
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY',-3)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'center_up_lid_1_ctrl', 'rotateX',15)
	
	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	
	cmds.sound( offset=i, file=file_names_list[31])
		
	#
	setKeys(i, 'jaw_drop','jaw_drop', 2)
	#l
	setKeys(i+1,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i+1,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i+1,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i+1, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	cmds.sound( offset=i+1, file=file_names_list[23])
	
	clear_lips(after)
	
def br_key(i):
	#b
	before=i-3
	after=i+3
	
	clear_lips(before)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateY',2.6)
	setKeys(i, 'right_lip_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'right_lip_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'left_lip_low_ctrl', 'translateY',2.6)
	setKeys(i, 'left_lip_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'mid_low_ctrl', 'translateY',2.4)
	setKeys(i, 'mid_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'mid_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY',-1.6)
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'right_up_lid_1_ctrl', 'rotateX',-3)
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY',-1.6)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'left_up_lid_1_ctrl', 'rotateX',-3)
	
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY',-3)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'center_up_lid_1_ctrl', 'rotateX',15)
	
	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	cmds.sound( offset=i, file=file_names_list[6])
	
	#
	setKeys(i, 'jaw_drop','jaw_drop', 2)
	#r
	
	setKeys(i+1,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i+1,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i+1,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i+1, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	
	setKeys(i+1, 'jaw_drop', 'jaw_drop', 0)
	
	cmds.sound( offset=i+1, file=file_names_list[32])
	clear_lips(after)
	
def cr_key(i):
	
	clear_lips(before)
	#c
	for t in t_list:
		setKeys(before, t, 'rotateZ', 0)

	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 6)
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', -6)
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 12)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 1)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY',2)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 1)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'mid_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'left_lip_low_ctrl', 'translateY', -0.8)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', 0.8)
	
	setKeys(i, 'right_lip_low_ctrl', 'rotateX', 0)
	setKeys(i, 'mid_low_ctrl', 'rotateX',0)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX', 0)
	cmds.sound( offset=i, file=file_names_list[34])
	
	#
	setKeys(i, 'jaw_drop','jaw_drop', 2)
	#r
	
	setKeys(i+1,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i+1,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i+1,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i+1, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	
	setKeys(i+1, 'jaw_drop', 'jaw_drop', 0)
	
	cmds.sound( offset=i+1, file=file_names_list[32])
	clear_lips(after)
	
def dr_key(i):
	
	clear_lips(before)
	#set the time 
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	
	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	cmds.sound( offset=i, file=file_names_list[8])
	
	#
	setKeys(i, 'jaw_drop','jaw_drop', 2)
	#r
	
	setKeys(i+1,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i+1,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i+1,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i+1, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	
	setKeys(i+1, 'jaw_drop', 'jaw_drop', 0)
	
	cmds.sound( offset=i+1, file=file_names_list[32])
	clear_lips(after)

	
def fr_key(i):
	
	#set the time 
	before=i-3
	after=i+3
	clear_lips(before)
		
	setKeys(i, 'right_lip_low_ctrl', 'translateY', 1.5)		
	setKeys(i, 'right_lip_low_ctrl', 'translateZ', -1)	
	setKeys(i, 'right_lip_low_ctrl', 'rotateX', -18)	
			
	setKeys(i, 'left_lip_low_ctrl', 'translateY', 1.5)		
	setKeys(i, 'left_lip_low_ctrl', 'translateZ', -1)		
	setKeys(i, 'left_lip_low_ctrl', 'rotateX', -18)		
	
	setKeys(i, 'mid_low_ctrl', 'translateY', 2)		
	setKeys(i, 'mid_low_ctrl', 'translateZ', -1)		
	setKeys(i, 'mid_low_ctrl', 'rotateX', -16)		
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', -0.4)		
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', -1.2)		
	setKeys(i, 'right_up_lid_1_ctrl', 'rotateX', -18)		
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', -0.4)		
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', -1.2)		
	setKeys(i, 'left_up_lid_1_ctrl', 'rotateX', -18)		
	
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', -0.4)		
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', -1)		
	setKeys(i, 'center_up_lid_1_ctrl', 'rotateX', -18)		
	
	cmds.sound( offset=i, file=file_names_list[16])
	#
	setKeys(i, 'jaw_drop','jaw_drop', 2)
	#r
	
	setKeys(i+1,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i+1,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i+1,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i+1, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	
	setKeys(i+1, 'jaw_drop', 'jaw_drop', 0)
	
	cmds.sound( offset=i+1, file=file_names_list[32])
	clear_lips(after)

	
def h_key(i):   #h==k   
	
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	
	setKeys(i, 'left_lip_low_ctrl', 'translateY', -1.2)
	setKeys(i, 'right_lip_low_ctrl', 'translateY', -1.2)
	setKeys(i, 'mid_low_ctrl', 'translateY', -1.2)
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', -0.3)
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', -0.3)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', -0.3)
	
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 0)		
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', 0)		
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 0)	
	cmds.sound( offset=i, file=file_names_list[18])
	clear_lips(after)
def pr_key(i):
	
	#p
	before=i-3
	after=i+3
	
	clear_lips(before)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateY',2.6)
	setKeys(i, 'right_lip_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'right_lip_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'left_lip_low_ctrl', 'translateY',2.6)
	setKeys(i, 'left_lip_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'mid_low_ctrl', 'translateY',2.4)
	setKeys(i, 'mid_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'mid_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY',-1.6)
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'right_up_lid_1_ctrl', 'rotateX',-3)
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY',-1.6)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'left_up_lid_1_ctrl', 'rotateX',-3)
	
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY',-3)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'center_up_lid_1_ctrl', 'rotateX',15)
	
	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	
	cmds.sound( offset=i, file=file_names_list[31])
	#
	setKeys(i, 'jaw_drop','jaw_drop', 2)
	#r
	
	setKeys(i+1,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i+1,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i+1,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i+1, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	
	setKeys(i+1, 'jaw_drop', 'jaw_drop', 0)
	
	cmds.sound( offset=i+1, file=file_names_list[32])
	clear_lips(after)
	
def tr_key(i):
	#t
	#set the time 
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	
	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	
	cmds.sound( offset=i, file=file_names_list[35])
	#
	setKeys(i, 'jaw_drop','jaw_drop', 2)
	#r
	
	setKeys(i+1,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i+1,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i+1,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i+1, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	
	setKeys(i+1, 'jaw_drop', 'jaw_drop', 0)
	
	cmds.sound( offset=i+1, file=file_names_list[32])
	clear_lips(after)
	
def sk_key(i):
	#s
	before=i-3
	after=i+3
	
	clear_lips(before)
	
	for t in t_list:
		setKeys(before, t, 'rotateZ', 0)

	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 6)
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', -6)
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 12)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 1)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY',2)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 1)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'mid_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'left_lip_low_ctrl', 'translateY', -0.8)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', 0.8)
	
	setKeys(i, 'right_lip_low_ctrl', 'rotateX', 0)
	setKeys(i, 'mid_low_ctrl', 'rotateX',0)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX', 0)
	
	cmds.sound( offset=i, file=file_names_list[34])
	#
	setKeys(i+1, 'jaw_drop','jaw_drop', 2)
	#r
	setKeys(i+1, 'jaw_drop', 'jaw_drop', 0)
	
	setKeys(i+1, 'left_lip_low_ctrl', 'translateY', -1.2)
	setKeys(i+1, 'right_lip_low_ctrl', 'translateY', -1.2)
	setKeys(i+1, 'mid_low_ctrl', 'translateY', -1.2)
	
	setKeys(i+1, 'left_up_lid_1_ctrl', 'translateY', -0.3)
	setKeys(i+1, 'right_up_lid_1_ctrl', 'translateY', -0.3)
	setKeys(i+1, 'center_up_lid_1_ctrl', 'translateY', -0.3)
	
	setKeys(i+1, 'tongue_1_jnt_FK', 'rotateZ', 0)		
	setKeys(i+1, 'tongue_2_jnt_FK', 'rotateZ', 0)		
	setKeys(i+1, 'tongue_3_jnt_FK', 'rotateZ', 0)	
	cmds.sound( offset=i+1, file=file_names_list[22])

	clear_lips(after)
def sp_key(i):
	#s
	before=i-3
	after=i+3
	
	clear_lips(before)
	
	for t in t_list:
		setKeys(before, t, 'rotateZ', 0)

	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 6)
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', -6)
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 12)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 1)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY',2)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 1)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'mid_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'left_lip_low_ctrl', 'translateY', -0.8)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', 0.8)
	
	setKeys(i, 'right_lip_low_ctrl', 'rotateX', 0)
	setKeys(i, 'mid_low_ctrl', 'rotateX',0)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX', 0)
	
	cmds.sound( offset=i, file=file_names_list[34])
	#
	setKeys(i+1, 'jaw_drop','jaw_drop', 2)
	#p
	
	setKeys(i+1, 'right_lip_low_ctrl', 'translateY',2.6)
	setKeys(i+1, 'right_lip_low_ctrl', 'translateZ',-0.7)
	setKeys(i+1, 'right_lip_low_ctrl', 'rotateX',-15)
	
	setKeys(i+1, 'left_lip_low_ctrl', 'translateY',2.6)
	setKeys(i+1, 'left_lip_low_ctrl', 'translateZ',-0.7)
	setKeys(i+1, 'left_lip_low_ctrl', 'rotateX',-15)
	
	setKeys(i+1, 'mid_low_ctrl', 'translateY',2.4)
	setKeys(i+1, 'mid_low_ctrl', 'translateZ',-0.7)
	setKeys(i+1, 'mid_low_ctrl', 'rotateX',-15)
	
	setKeys(i+1, 'right_up_lid_1_ctrl', 'translateY',-1.6)
	setKeys(i+1, 'right_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i+1, 'right_up_lid_1_ctrl', 'rotateX',-3)
	
	setKeys(i+1, 'left_up_lid_1_ctrl', 'translateY',-1.6)
	setKeys(i+1, 'left_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i+1, 'left_up_lid_1_ctrl', 'rotateX',-3)
	
	setKeys(i+1, 'center_up_lid_1_ctrl', 'translateY',-3)
	setKeys(i+1, 'center_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i+1, 'center_up_lid_1_ctrl', 'rotateX',15)
	
	setKeys(i+1, 'jaw_drop', 'jaw_drop', 0)
	
	cmds.sound( offset=i+1, file=file_names_list[31])

	clear_lips(after)
def sl_key(i):
	#s
	before=i-3
	after=i+3
	
	clear_lips(before)
	
	for t in t_list:
		setKeys(before, t, 'rotateZ', 0)

	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 6)
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', -6)
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 12)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 1)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY',2)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 1)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'mid_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'left_lip_low_ctrl', 'translateY', -0.8)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', 0.8)
	
	setKeys(i, 'right_lip_low_ctrl', 'rotateX', 0)
	setKeys(i, 'mid_low_ctrl', 'rotateX',0)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX', 0)
	
	cmds.sound( offset=i, file=file_names_list[34])
	#
	setKeys(i+1, 'jaw_drop','jaw_drop', 2)
	#l

	setKeys(i+1,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i+1,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i+1,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i+1, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	cmds.sound( offset=i+1, file=file_names_list[23])

	clear_lips(after)
def st_key(i):
	#s
	before=i-3
	after=i+3
	
	clear_lips(before)
	
	for t in t_list:
		setKeys(before, t, 'rotateZ', 0)

	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 6)
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', -6)
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 12)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 1)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY',2)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 1)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'mid_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'left_lip_low_ctrl', 'translateY', -0.8)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', 0.8)
	
	setKeys(i, 'right_lip_low_ctrl', 'rotateX', 0)
	setKeys(i, 'mid_low_ctrl', 'rotateX',0)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX', 0)
	
	cmds.sound( offset=i, file=file_names_list[34])
	#
	setKeys(i+1, 'jaw_drop','jaw_drop', 2)
	#t
	
	setKeys(i+1,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i+1,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i+1,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i+1, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	
	setKeys(i+1, 'jaw_drop', 'jaw_drop', 0)
	
	cmds.sound( offset=i+1, file=file_names_list[35])
	clear_lips(after)
def sw_key(i):
	#s
	before=i-3
	after=i+3
	
	clear_lips(before)
	
	for t in t_list:
		setKeys(before, t, 'rotateZ', 0)

	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 6)
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', -6)
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 12)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 1)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY',2)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 1)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'mid_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'left_lip_low_ctrl', 'translateY', -0.8)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', 0.8)
	
	setKeys(i, 'right_lip_low_ctrl', 'rotateX', 0)
	setKeys(i, 'mid_low_ctrl', 'rotateX',0)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX', 0)
	
	cmds.sound( offset=i, file=file_names_list[34])
	#
	setKeys(i+1, 'jaw_drop','jaw_drop', 2)
	#l
	setKeys(i+1,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i+1,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i+1,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i+1, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i+1, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	cmds.sound( offset=i+1, file=file_names_list[41])
	clear_lips(after)

	
def oi_key(i):
	#o
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i,'left_up_lid_1_ctrl','translateX',-1.5)
	setKeys(i,'left_up_lid_1_ctrl','translateY',0)
	setKeys(i,'left_up_lid_1_ctrl','translateZ',1)
	
	setKeys(i,'center_up_lid_1_ctrl','translateX',0)
	setKeys(i,'center_up_lid_1_ctrl','translateY',0)
	setKeys(i,'center_up_lid_1_ctrl','translateZ',0)
	
	setKeys(i,'mid_low_ctrl','translateX',0)
	setKeys(i,'mid_low_ctrl','translateY',0)
	setKeys(i,'mid_low_ctrl','translateZ',0)
	
	setKeys(i,'right_up_lid_1_ctrl','translateX',1.5)
	setKeys(i,'right_up_lid_1_ctrl','translateY',0)
	setKeys(i,'right_up_lid_1_ctrl','translateZ',1)
	
	setKeys(i,'right_up_lid_2_ctrl','translateX',4)
	setKeys(i,'right_up_lid_2_ctrl','translateY',-2)
	setKeys(i,'right_up_lid_2_ctrl','translateZ',-1)
	
	setKeys(i,'left_up_lid_2_ctrl','translateX',-4)
	setKeys(i,'left_up_lid_2_ctrl','translateY',-2)
	setKeys(i,'left_up_lid_2_ctrl','translateZ',-1)
	
	setKeys(i,'left_lip_low_ctrl','translateX',-1.8)
	setKeys(i,'left_lip_low_ctrl','translateY',0)
	setKeys(i,'left_lip_low_ctrl','translateZ',0)
	
	setKeys(i,'right_lip_low_ctrl','translateX',1.8)
	setKeys(i,'right_lip_low_ctrl','translateY',0)
	setKeys(i,'right_lip_low_ctrl','translateZ',0)
	setKeys(i, 'jaw_drop', 'jaw_drop', -8)
	
	setKeys(i,'left_lip_1_ctrl','translateX',-2)
	setKeys(i,'right_lip_1_ctrl','translateX',2)
	setKeys(i,'left_chin_2_ctrl','translateX',-1)
	setKeys(i,'right_chin_2_ctrl','translateX',1)

	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 0)		
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', 0)		
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 0)		
	cmds.sound( offset=i, file=file_names_list[28])
	#
	setKeys(i+1, 'jaw_drop', 'jaw_drop', -2)
	setKeys(i+1, 'tongue_1_jnt_FK', 'rotateZ', 3)
	setKeys(i+1, 'tongue_2_jnt_FK', 'rotateZ', -3)
	setKeys(i+1, 'tongue_3_jnt_FK', 'rotateZ', 25)
	cmds.sound( offset=i+1, file=file_names_list[19])
	clear_lips(after)

	
def ow_key(i):
	#o
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i,'left_up_lid_1_ctrl','translateX',-1.5)
	setKeys(i,'left_up_lid_1_ctrl','translateY',0)
	setKeys(i,'left_up_lid_1_ctrl','translateZ',1)
	
	setKeys(i,'center_up_lid_1_ctrl','translateX',0)
	setKeys(i,'center_up_lid_1_ctrl','translateY',0)
	setKeys(i,'center_up_lid_1_ctrl','translateZ',0)
	
	setKeys(i,'mid_low_ctrl','translateX',0)
	setKeys(i,'mid_low_ctrl','translateY',0)
	setKeys(i,'mid_low_ctrl','translateZ',0)
	
	setKeys(i,'right_up_lid_1_ctrl','translateX',1.5)
	setKeys(i,'right_up_lid_1_ctrl','translateY',0)
	setKeys(i,'right_up_lid_1_ctrl','translateZ',1)
	
	setKeys(i,'right_up_lid_2_ctrl','translateX',4)
	setKeys(i,'right_up_lid_2_ctrl','translateY',-2)
	setKeys(i,'right_up_lid_2_ctrl','translateZ',-1)
	
	setKeys(i,'left_up_lid_2_ctrl','translateX',-4)
	setKeys(i,'left_up_lid_2_ctrl','translateY',-2)
	setKeys(i,'left_up_lid_2_ctrl','translateZ',-1)
	
	setKeys(i,'left_lip_low_ctrl','translateX',-1.8)
	setKeys(i,'left_lip_low_ctrl','translateY',0)
	setKeys(i,'left_lip_low_ctrl','translateZ',0)
	
	setKeys(i,'right_lip_low_ctrl','translateX',1.8)
	setKeys(i,'right_lip_low_ctrl','translateY',0)
	setKeys(i,'right_lip_low_ctrl','translateZ',0)
	setKeys(i, 'jaw_drop', 'jaw_drop', -8)
	
	setKeys(i,'left_lip_1_ctrl','translateX',-2)
	setKeys(i,'right_lip_1_ctrl','translateX',2)
	setKeys(i,'left_chin_2_ctrl','translateX',-1)
	setKeys(i,'right_chin_2_ctrl','translateX',1)

	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 0)		
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', 0)		
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 0)		
	cmds.sound( offset=i, file=file_names_list[28])
	l_short_key(i+1)
	
	clear_lips(after)
def aw_key(i):
	#o
	before=i-3
	after=i+3
	
	clear_lips(before)
	for t in t_list:
		setKeys(i, t, 'rotateZ', 0)
	setKeys(i, 'jaw_drop', 'jaw_drop', -10)
	cmds.sound( offset=i, file=file_names_list[2])
	
	l_short_key(i+1)
	
	clear_lips(after)

	
def h_key(i):   #h==k   
	
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	
	setKeys(i, 'left_lip_low_ctrl', 'translateY', -1.2)
	setKeys(i, 'right_lip_low_ctrl', 'translateY', -1.2)
	setKeys(i, 'mid_low_ctrl', 'translateY', -1.2)
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', -0.3)
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', -0.3)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', -0.3)
	
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 0)		
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', 0)		
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 0)	
	cmds.sound( offset=i, file=file_names_list[18])
	clear_lips(after)

	
def i_key(t_list,i):
	#i
	
	before=i-3
	after=i+3
	clear_lips(before)

	setKeys(before, 'jaw_drop', 'jaw_drop', 2)
	for t in t_list:
		setKeys(before, t, 'rotateZ', 0)
	
	setKeys(i, 'jaw_drop', 'jaw_drop', -10)
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 10)
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', -10)
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', -2)
	cmds.sound( offset=i, file=file_names_list[19])
	
	setKeys(i+1, 'jaw_drop', 'jaw_drop', -10)
	setKeys(i+1, 'tongue_1_jnt_FK', 'rotateZ', 10)
	setKeys(i+1, 'tongue_2_jnt_FK', 'rotateZ', -10)
	setKeys(i+1, 'tongue_3_jnt_FK', 'rotateZ', -2)
		
	clear_lips(after)
	
def i_short_key(i):
	
	setKeys(i, 'jaw_drop', 'jaw_drop', -2)
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 3)
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', -3)
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 25)
	cmds.sound( offset=i, file=file_names_list[19])
		

def j_key(i):
	#print 'J keys on joints', '::',i
	
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i, 'mid_low_ctrl','translateY', -0.8)	
	setKeys(i, 'mid_low_ctrl','translateZ', 1.2)	
	
	setKeys(i, 'right_lip_low_ctrl','translateY', -0.3)
	setKeys(i, 'right_lip_low_ctrl',	'translateZ', 1.5)
	setKeys(i, 'right_lip_low_ctrl',	'rotateX', 20)
	setKeys(i, 'right_lip_low_ctrl',	'rotateY', -10)
	setKeys(i, 'right_lip_low_ctrl',	'rotateZ', 3)
	
	setKeys(i, 'left_lip_low_ctrl','translateY', -0.3)
	setKeys(i, 'left_lip_low_ctrl',	'translateZ', 1.5)
	setKeys(i, 'left_lip_low_ctrl',	'rotateX', 20)
	setKeys(i, 'left_lip_low_ctrl',	'rotateY', -10)
	setKeys(i, 'left_lip_low_ctrl',	'rotateZ', -3)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 2.6)		
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', 0.5)
	setKeys(i, 'right_up_lid_1_ctrl', 'rotateX', -30)
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 2.6)		
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', 0.5)
	setKeys(i, 'left_up_lid_1_ctrl', 'rotateX', -30)
	
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', 3.5)		
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', 0.5)
	setKeys(i, 'center_up_lid_1_ctrl', 'rotateX', -30)
	
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 20)		
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', -25)		
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 33)		

	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	cmds.sound( offset=i, file=file_names_list[9])
	clear_lips(after)	
	
def k_key(i):
	#k
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	
	setKeys(i, 'left_lip_low_ctrl', 'translateY', -1.2)
	setKeys(i, 'right_lip_low_ctrl', 'translateY', -1.2)
	setKeys(i, 'mid_low_ctrl', 'translateY', -1.2)
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', -0.3)
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', -0.3)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', -0.3)
	
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 0)		
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', 0)		
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 0)	
	cmds.sound( offset=i, file=file_names_list[22])
	clear_lips(after)

def l_key(i):
	#l
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	cmds.sound( offset=i, file=file_names_list[23])
	
	clear_lips(after)
	
def l_short_key(i):
	setKeys(i,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	cmds.sound( offset=i, file=file_names_list[23])
	
def m_key(i):  #m==b
	#m
	before=i-3
	after=i+3
	
	clear_lips(before)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateY',2.6)
	setKeys(i, 'right_lip_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'right_lip_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'left_lip_low_ctrl', 'translateY',2.6)
	setKeys(i, 'left_lip_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'mid_low_ctrl', 'translateY',2.4)
	setKeys(i, 'mid_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'mid_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY',-1.6)
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'right_up_lid_1_ctrl', 'rotateX',-3)
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY',-1.6)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'left_up_lid_1_ctrl', 'rotateX',-3)
	
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY',-3)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'center_up_lid_1_ctrl', 'rotateX',15)
	
	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	
	cmds.sound( offset=i, file=file_names_list[24])
	clear_lips(after)
	
def n_key(i): 
	#n
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	
	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	
	cmds.sound( offset=i, file=file_names_list[25])
	clear_lips(after)
	
def o_key(i):
	#print 'o_key', '::',i
	
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i,'left_up_lid_1_ctrl','translateX',-1.5)
	setKeys(i,'left_up_lid_1_ctrl','translateY',0)
	setKeys(i,'left_up_lid_1_ctrl','translateZ',1)
	
	setKeys(i,'center_up_lid_1_ctrl','translateX',0)
	setKeys(i,'center_up_lid_1_ctrl','translateY',0)
	setKeys(i,'center_up_lid_1_ctrl','translateZ',0)
	
	setKeys(i,'mid_low_ctrl','translateX',0)
	setKeys(i,'mid_low_ctrl','translateY',0)
	setKeys(i,'mid_low_ctrl','translateZ',0)
	
	setKeys(i,'right_up_lid_1_ctrl','translateX',1.5)
	setKeys(i,'right_up_lid_1_ctrl','translateY',0)
	setKeys(i,'right_up_lid_1_ctrl','translateZ',1)
	
	setKeys(i,'right_up_lid_2_ctrl','translateX',4)
	setKeys(i,'right_up_lid_2_ctrl','translateY',-2)
	setKeys(i,'right_up_lid_2_ctrl','translateZ',-1)
	
	setKeys(i,'left_up_lid_2_ctrl','translateX',-4)
	setKeys(i,'left_up_lid_2_ctrl','translateY',-2)
	setKeys(i,'left_up_lid_2_ctrl','translateZ',-1)
	
	setKeys(i,'left_lip_low_ctrl','translateX',-1.8)
	setKeys(i,'left_lip_low_ctrl','translateY',0)
	setKeys(i,'left_lip_low_ctrl','translateZ',0)
	
	setKeys(i,'right_lip_low_ctrl','translateX',1.8)
	setKeys(i,'right_lip_low_ctrl','translateY',0)
	setKeys(i,'right_lip_low_ctrl','translateZ',0)
	setKeys(i, 'jaw_drop', 'jaw_drop', -8)
	
	setKeys(i,'left_lip_1_ctrl','translateX',-2)
	setKeys(i,'right_lip_1_ctrl','translateX',2)
	setKeys(i,'left_chin_2_ctrl','translateX',-1)
	setKeys(i,'right_chin_2_ctrl','translateX',1)

	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 0)		
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', 0)		
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 0)		
	cmds.sound( offset=i, file=file_names_list[28])

	clear_lips(after)

	
def p_key(i):  ##p==b
	#p
	before=i-3
	after=i+3
	
	clear_lips(before)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateY',2.6)
	setKeys(i, 'right_lip_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'right_lip_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'left_lip_low_ctrl', 'translateY',2.6)
	setKeys(i, 'left_lip_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'mid_low_ctrl', 'translateY',2.4)
	setKeys(i, 'mid_low_ctrl', 'translateZ',-0.7)
	setKeys(i, 'mid_low_ctrl', 'rotateX',-15)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY',-1.6)
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'right_up_lid_1_ctrl', 'rotateX',-3)
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY',-1.6)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'left_up_lid_1_ctrl', 'rotateX',-3)
	
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY',-3)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ',-0.7)
	setKeys(i, 'center_up_lid_1_ctrl', 'rotateX',15)
	
	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	
	cmds.sound( offset=i, file=file_names_list[31])
	clear_lips(after)
	
def q_key(i): ## u
	#print 'q key', '::',i
	
	before=i-3
	after=i+3
	clear_lips(before)
	cmds.sound( offset=i-1, file=file_names_list[22])#k
	
	setKeys(i, 'mid_low_ctrl', 'translateX', 0)
	setKeys(i, 'mid_low_ctrl', 'translateY', -2)
	setKeys(i, 'mid_low_ctrl', 'translateZ', 1)
	setKeys(i, 'mid_low_ctrl', 'rotateX', 10)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateX', 2)
	setKeys(i, 'right_lip_low_ctrl', 'translateY', -2.8)
	setKeys(i, 'right_lip_low_ctrl', 'translateZ', 1.6)
	setKeys(i, 'right_lip_low_ctrl', 'rotateX', 30)
	
	setKeys(i, 'left_lip_low_ctrl', 'translateX', -2)
	setKeys(i, 'left_lip_low_ctrl', 'translateY', -2.8)
	setKeys(i, 'left_lip_low_ctrl', 'translateZ', 1.6)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX', 30)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateX', 0)
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 0)
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', 0)
	setKeys(i, 'right_up_lid_1_ctrl', 'rotateX', -15)
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateX', 0)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 0)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', 0)
	setKeys(i, 'left_up_lid_1_ctrl', 'rotateX', -15)
	
	setKeys(i, 'center_up_lid_1_ctrl', 'translateX', 0)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', 4)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', 0)
	setKeys(i, 'center_up_lid_1_ctrl', 'rotateX', -28)

	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	
	cmds.sound( offset=i+1, file=file_names_list[38])#u
	clear_lips(after)
		
	
def r_key(i):
	#r
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	
	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	
	cmds.sound( offset=i, file=file_names_list[32])
	clear_lips(after)
	
def s_key(i,t_list):
	#s
	before=i-3
	after=i+3
	
	clear_lips(before)
	
	for t in t_list:
		setKeys(before, t, 'rotateZ', 0)

	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 6)
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', -6)
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 12)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 1)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY',2)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 1)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'mid_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'left_lip_low_ctrl', 'translateY', -0.8)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', 0.8)
	
	setKeys(i, 'right_lip_low_ctrl', 'rotateX', 0)
	setKeys(i, 'mid_low_ctrl', 'rotateX',0)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX', 0)
	
	cmds.sound( offset=i, file=file_names_list[34])

	for t in t_list:
		setKeys(after, t, 'rotateZ', 0)
	clear_lips(after)
	
	
def t_key(i):
	#t
	#set the time 
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	
	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	
	cmds.sound( offset=i, file=file_names_list[35])
	clear_lips(after)
	

def u_key(i):
	#u

	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i,'left_up_lid_1_ctrl','translateX',-1.5)
	setKeys(i,'left_up_lid_1_ctrl','translateY',0)
	setKeys(i,'left_up_lid_1_ctrl','translateZ',1)
	
	setKeys(i,'center_up_lid_1_ctrl','translateX',0)
	setKeys(i,'center_up_lid_1_ctrl','translateY',0)
	setKeys(i,'center_up_lid_1_ctrl','translateZ',0)
	
	setKeys(i,'mid_low_ctrl','translateX',0)
	setKeys(i,'mid_low_ctrl','translateY',0)
	setKeys(i,'mid_low_ctrl','translateZ',0)
	
	setKeys(i,'right_up_lid_1_ctrl','translateX',1.5)
	setKeys(i,'right_up_lid_1_ctrl','translateY',0)
	setKeys(i,'right_up_lid_1_ctrl','translateZ',1)
	
	setKeys(i,'right_up_lid_2_ctrl','translateX',4)
	setKeys(i,'right_up_lid_2_ctrl','translateY',-2)
	setKeys(i,'right_up_lid_2_ctrl','translateZ',-1)
	
	setKeys(i,'left_up_lid_2_ctrl','translateX',-4)
	setKeys(i,'left_up_lid_2_ctrl','translateY',-2)
	setKeys(i,'left_up_lid_2_ctrl','translateZ',-1)
	
	setKeys(i,'left_lip_low_ctrl','translateX',-1.8)
	setKeys(i,'left_lip_low_ctrl','translateY',0)
	setKeys(i,'left_lip_low_ctrl','translateZ',0)
	
	setKeys(i,'right_lip_low_ctrl','translateX',1.8)
	setKeys(i,'right_lip_low_ctrl','translateY',0)
	setKeys(i,'right_lip_low_ctrl','translateZ',0)
	setKeys(i, 'jaw_drop', 'jaw_drop', -8)
	
	setKeys(i,'left_lip_1_ctrl','translateX',-2)
	setKeys(i,'right_lip_1_ctrl','translateX',2)
	setKeys(i,'left_chin_2_ctrl','translateX',-1)
	setKeys(i,'right_chin_2_ctrl','translateX',1)

	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 0)		
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', 0)		
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 0)		
	cmds.sound( offset=i, file=file_names_list[39])

	clear_lips(after)
	
def u_short_key(i):
	#print 'u key', '::',i
	setKeys(i, 'mid_low_ctrl', 'translateX', 0)
	setKeys(i, 'mid_low_ctrl', 'translateY', -2)
	setKeys(i, 'mid_low_ctrl', 'translateZ', 1)
	setKeys(i, 'mid_low_ctrl', 'rotateX', 10)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateX', 2)
	setKeys(i, 'right_lip_low_ctrl', 'translateY', -2.8)
	setKeys(i, 'right_lip_low_ctrl', 'translateZ', 1.6)
	setKeys(i, 'right_lip_low_ctrl', 'rotateX', 30)
	
	setKeys(i, 'left_lip_low_ctrl', 'translateX', -2)
	setKeys(i, 'left_lip_low_ctrl', 'translateY', -2.8)
	setKeys(i, 'left_lip_low_ctrl', 'translateZ', 1.6)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX', 30)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateX', 0)
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 0)
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', 0)
	setKeys(i, 'right_up_lid_1_ctrl', 'rotateX', -15)
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateX', 0)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 0)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', 0)
	setKeys(i, 'left_up_lid_1_ctrl', 'rotateX', -15)
	
	setKeys(i, 'center_up_lid_1_ctrl', 'translateX', 0)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', 4)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', 0)
	setKeys(i, 'center_up_lid_1_ctrl', 'rotateX', -28)
	setKeys(i, 'right_up_lid_1_ctrl', 'rotateZ', 20)
	setKeys(i, 'left_up_lid_1_ctrl', 'rotateZ', -20)
	cmds.sound( offset=i, file=file_names_list[38])
	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	
def ur_key(i):
	u_short_key(i-1)
	setKeys(i,'center_up_lid_1_ctrl', 'rotateX', 0)
	r_key(i+1)
	
def ar_key(i):
	a_short_key(i-1,t_list)
	r_key(i+1)
	
def or_key(i):
	o_long_key(i-1)
	r_key(i+1)
	
			
def v_key(i):
	#print 'v key', '::',i
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i,"jaw_drop","jaw_drop",0)
	setKeys(i,"left_lip_low_ctrl","translateZ",-1.5)
	setKeys(i,"mid_low_ctrl","translateZ", -1.5)
	setKeys(i,"right_lip_low_ctrl","translateZ", -1.5)
	
	setKeys(i,"left_lip_low_ctrl","translateX", 0)
	setKeys(i,"mid_low_ctrl","translateX", 0)
	setKeys(i,"right_lip_low_ctrl","translateX",0)

	setKeys(i,"left_lip_low_ctrl","translateY", 1)
	setKeys(i,"mid_low_ctrl","translateY", 1)
	setKeys(i,"right_lip_low_ctrl","translateY",1)

	setKeys(i,"left_up_lid_1_ctrl","translateY", 0.5)
	setKeys(i,"center_up_lid_1_ctrl","translateY", 0.5)
	setKeys(i,"right_up_lid_1_ctrl","translateY",0.5)
	cmds.sound( offset=i, file=file_names_list[40])
	clear_lips(after)	


def w_key(i):
	#w
	#l
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i,'tongue_3_jnt_FK','rotateZ',-30)
	setKeys(i,'tongue_1_jnt_FK','rotateZ',0)
	setKeys(i,'tongue_2_jnt_FK','rotateZ',33)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', 1.8)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 1.8)
	cmds.sound( offset=i, file=file_names_list[41])
	
	clear_lips(after)
	
def x_key(i):
	#x
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	
	setKeys(i, 'left_lip_low_ctrl', 'translateY', -1.2)
	setKeys(i, 'right_lip_low_ctrl', 'translateY', -1.2)
	setKeys(i, 'mid_low_ctrl', 'translateY', -1.2)
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', -0.3)
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', -0.3)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', -0.3)
	
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 0)		
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', 0)		
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 0)	
	cmds.sound( offset=i, file=file_names_list[18])
	clear_lips(after)

	
def y_key(i): #why
	#q
	before=i-3
	after=i+3
	clear_lips(before)
	
	setKeys(i, 'mid_low_ctrl', 'translateX', 0)
	setKeys(i, 'mid_low_ctrl', 'translateY', -2)
	setKeys(i, 'mid_low_ctrl', 'translateZ', 1)
	setKeys(i, 'mid_low_ctrl', 'rotateX', 10)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateX', 2)
	setKeys(i, 'right_lip_low_ctrl', 'translateY', -2.8)
	setKeys(i, 'right_lip_low_ctrl', 'translateZ', 1.6)
	setKeys(i, 'right_lip_low_ctrl', 'rotateX', 30)
	
	setKeys(i, 'left_lip_low_ctrl', 'translateX', -2)
	setKeys(i, 'left_lip_low_ctrl', 'translateY', -2.8)
	setKeys(i, 'left_lip_low_ctrl', 'translateZ', 1.6)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX', 30)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateX', 0)
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 0)
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', 0)
	setKeys(i, 'right_up_lid_1_ctrl', 'rotateX', -15)
	
	setKeys(i, 'left_up_lid_1_ctrl', 'translateX', 0)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 0)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', 0)
	setKeys(i, 'left_up_lid_1_ctrl', 'rotateX', -15)
	
	setKeys(i, 'center_up_lid_1_ctrl', 'translateX', 0)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY', 4)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', 0)
	setKeys(i, 'center_up_lid_1_ctrl', 'rotateX', -28)

	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	cmds.sound( offset=i, file=file_names_list[42])#k

	clear_lips(after)

def z_key(i):
	#z
	before=i-3
	after=i+3
	
	clear_lips(before)
	
	for t in t_list:
		setKeys(before, t, 'rotateZ', 0)

	setKeys(i, 'jaw_drop', 'jaw_drop', 0)
	setKeys(i, 'tongue_1_jnt_FK', 'rotateZ', 6)
	setKeys(i, 'tongue_2_jnt_FK', 'rotateZ', -6)
	setKeys(i, 'tongue_3_jnt_FK', 'rotateZ', 12)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateY', 1)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateY',2)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateY', 1)
	
	setKeys(i, 'right_lip_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'mid_low_ctrl', 'translateY', -0.8)
	setKeys(i, 'left_lip_low_ctrl', 'translateY', -0.8)
	
	setKeys(i, 'right_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'center_up_lid_1_ctrl', 'translateZ', 0.8)
	setKeys(i, 'left_up_lid_1_ctrl', 'translateZ', 0.8)
	
	setKeys(i, 'right_lip_low_ctrl', 'rotateX', 0)
	setKeys(i, 'mid_low_ctrl', 'rotateX',0)
	setKeys(i, 'left_lip_low_ctrl', 'rotateX', 0)
	
	cmds.sound( offset=i, file=file_names_list[44])

	for t in t_list:
		setKeys(after, t, 'rotateZ', 0)
	clear_lips(after)
	
		
def clean_ctrls(*args):
	
	ctrl_UP=['center_eyebrow_ctrl', 'center_nose_ctrl','r_eye_ctrl','l_eye_ctrl','neck_head_ctrl',
			'center_fh_1_ctrl', 'left_fh_1_ctrl', 'left_fh_2_ctrl', 'right_fh_1_ctrl', 
			'right_fh_2_ctrl', 'left_cheecks_1_ctrl', 'left_cheecks_2_ctrl', 'left_cheecks_3_ctrl', 
			'left_cheecks_4_ctrl', 'left_eyelid_1_ctrl', 'left_eyelid_2_ctrl', 'left_eyelid_3_ctrl', 
			'left_eyelid_4_ctrl', 'left_eyelid_5_ctrl', 'left_eyelid_6_ctrl', 
			'left_lip_1_ctrl', 'left_lip_2_ctrl', 'left_lip_3_ctrl',
			'left_e_1_ctrl', 'left_e_2_ctrl', 'left_e_3_ctrl', 'left_e_4_ctrl', 'left_e_5_ctrl', 
			'left_nose_ctrl', 'center_nose_1_ctrl', 'right_cheecks_1_ctrl', 'right_cheecks_2_ctrl', 
			'right_cheecks_3_ctrl', 'right_cheecks_4_ctrl', 'right_eyelid_1_ctrl', 'right_eyelid_2_ctrl', 
			'right_eyelid_3_ctrl', 'right_eyelid_4_ctrl', 'right_eyelid_5_ctrl', 'right_eyelid_6_ctrl', 
			'right_lip_1_ctrl', 'right_lip_2_ctrl', 'right_lip_3_ctrl', 'right_e_1_ctrl', 'right_e_2_ctrl', 
			'right_e_3_ctrl', 'right_e_4_ctrl', 'right_e_5_ctrl', 'right_nose_ctrl', 'center_up_lid_1_ctrl', 
			'left_up_lid_1_ctrl', 'left_up_lid_2_ctrl', 'right_up_lid_1_ctrl', 'right_up_lid_2_ctrl',
			'left_chin_2_ctrl','right_chin_2_ctrl','left_lip_low_ctrl','right_lip_low_ctrl','mid_low_ctrl']

	all_ctrl=ctrl_UP+ctrlsAllL
	for i in all_ctrl:
		for j in reset_list:
			cmds.setAttr(i+'.'+j,0)
			
	rot=['.rx','.ry','.rz']
	for i in t_list:
		for j in rot:
			cmds.setAttr(i+j,0)
			
	cmds.setAttr('jaw_drop.jaw_drop',0)
	
def setKeys(timeS, obj, attr, value):
	cmds.currentTime( timeS, edit=True )
	cmds.setAttr(obj+'.'+attr,value)
	cmds.setKeyframe( obj, attribute=attr)# t=['0sec','1sec'] ) #str(startF)+'sec',str(endFrame)+'sec'
	
def count_letter(word, char):
    n_count = 0
    for i in word:
        if i == char:
            n_count += 1
    return n_count
	
def split_words(text):
	punctuation_end=['.','!','?']	
	
	words_array=[]
	sentence_array=text.split(punctuation_end[0])
	for i in sentence_array:
		words_array.append(i.split())
		
	return words_array

def deleteAnim(*args):
	cmds.delete( all=True, c=True )

	for i in file_names_list:
		cmds.sound( offset=0, file=i)

def speechToolGUI(*args):
	'''
	gui 
	'''
	windowID = 'speech_tool_gui'
	if cmds.window(windowID, exists=True):
		cmds.deleteUI(windowID)
	
	#creates the window
	window = cmds.window(windowID,title="Speech Tool UI", w=300,h=400, sizeable=True)
	form=cmds.formLayout(numberOfDivisions=100)
	tabs=cmds.tabLayout(innerMarginWidth=0, innerMarginHeight=0)
	cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )
	
	 
	child1=cmds.columnLayout()
	#create the rig before animation
	cmds.text(l=" --- create the rig ---") 	
	cmds.button(l = " mirror behaviour locators", align = "center",command =	mirrorBehaviourLoc)
	cmds.button(l = " create joints", align = "center",command =checkLocExist)
	cmds.button(l = " mirror behaviour nurbs", align = "center",command =	mirrorBehaviourNURBS)
	
	#set the start frame of animation
	
	cmds.text(l=" --- start frame /equally keyframed letters/---") 
	startFrame=cmds.intField(ed=True, value=5 )
	
	#set the end frame of animation
	cmds.text(l=" --- end frame /equally keyframed letters/---") 
	endFrame= cmds.intField( value=75, ed=True )
	
	#define the frames between the words
	cmds.text(l=" --- frames per space / non-euqlly /---") 
	pauseFrame= cmds.intField( value=25, ed=True )
	
	#writes the text
	cmds.text(l=" --- write your text . ! ?---")
	text = cmds.textField("textIN", w = 200)
	
	cmds.text(l=" --- set the emotion . ! ?---")
	#define the emotion
	cmds.checkBox( label='Happy ',onc=setEmotionHappy, ofc=clean_ctrls )
	cmds.checkBox( label='Sad',onc=setEmotionSad, ofc=clean_ctrls )
	cmds.checkBox( label='Angry',onc=setEmotionAngry, ofc=clean_ctrls )
	cmds.checkBox( label='Surprised',onc=setEmotionSurprised, ofc=clean_ctrls )
	cmds.checkBox( label='Fear ',onc=setEmotionFear, ofc=clean_ctrls )
	cmds.checkBox( label='Disgust',onc=setEmotionDisgust, ofc=clean_ctrls )
	cmds.checkBox( label='Undefined',onc=setEmotionRandom, ofc=clean_ctrls )
	
	cmds.button(l = "a) create the animation /equally keyframed letters/", align = "center",command = lambda *args:readText(text, cmds.intField(startFrame, query = True, value = True),cmds.intField(endFrame, query = True, value = True),cmds.intField(pauseFrame, query = True, value = True),'yes'))
	cmds.button(l = "b) create the animation /non-euqlly including pause/", align = "center",command = lambda *args:readText(text, cmds.intField(startFrame, query = True, value = True),cmds.intField(endFrame, query = True, value = True),cmds.intField(pauseFrame, query = True, value = True),'no'))
	cmds.button(l = "c) delete the animations", align = "center",command =deleteAnim )
	cmds.button(l = "d) set ctrls to 0", align = "center",command =clean_ctrls )
	cmds.button(l = "e) say the letters", align = "center",command =sayText )
	
	cmds.setParent( '..' )
	
	#cmds.columnLayout()
	child2 = cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 100), (2, 100), (3, 100)] )
	cmds.text(l=" ---  keyframe . ! ?---")
	text_2 = cmds.intField( value=0 )
	cmds.button( l = "-----------")
	
	cmds.text(l='18 consonant sounds')
	cmds.button(l = "-----------")
	cmds.button(l = "-----------")
	cmds.button(l = "1- b -bad-",align = "center",command=lambda *args:b_key( cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "2- c/k -cat/kick-",align = "center",command=lambda *args:c_key(cmds.intField(text_2, query = True, value = True),t_list)) 
	cmds.button(l = "3- d -dog-",align = "center",command=lambda *args:d_key( cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "4- f -fog- -",align = "center",command=lambda *args:f_key( cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "5- g -got-",align = "center",command=lambda *args:g_short_key(cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "6- h -has-",align = "center",command=lambda *args:h_key(cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "7- j -job-",align = "center",command=lambda *args:j_key(cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "8- l -lid-",align = "center",command=lambda *args:l_key(cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "9- m -mop-",align = "center",command=lambda *args:m_key( cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "10- n -not-",align = "center",command=lambda *args:n_key( cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "11- p -pan-",align = "center",command=lambda *args:p_key( cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "12- r -run-",align = "center",command=lambda *args:r_key(cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "13- s -sit-",align = "center",command=lambda *args:s_key( cmds.intField(text_2, query = True, value = True),t_list)) 
	cmds.button(l = "14- t -to-",align = "center",command=lambda *args:t_key( cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "15- v -van-",align = "center",command=lambda *args:v_key( cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "16- w -web-",align = "center",command=lambda *args:w_key( cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "17- y -yet-",align = "center",command=lambda *args:y_key( cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "18- z -zoo-",align = "center",command=lambda *args:z_key( cmds.intField(text_2, query = True, value = True)))
	
	cmds.text(l=" 5 short vowels ")
	cmds.button(l = "-----------")
	cmds.button(l = "-----------")
	cmds.button(l = "1- a -after-",align = "center",command=lambda *args:a_short_key( cmds.intField(text_2, query = True, value = True),t_list))
	cmds.button(l = "2- e -pen-",align = "center",command=lambda *args:e_key( cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "3- i -tie-",align = "center",command=lambda *args:i_short_key(cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "4- o -coat-",align = "center",command=lambda *args:o_key( cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "5- u -cup-",align = "center",command=lambda *args:u_short_key( cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "-----------")
	
	cmds.text(l=" 6 long vowels ")
	cmds.button(l = "-----------")
	cmds.button(l = "-----------")
	cmds.button(l = "1- a make-",align = "center",command=lambda *args:a_long_key(cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "2- e -feet-",align = "center",command=lambda *args:e_long_key( cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "3- i -tie-",align = "center",command=lambda *args:i_key( t_list,cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "4- o -coat-",align = "center",command=lambda *args:o_key( cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "5- u -rule-",align = "center",command=lambda *args:u_key( cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "6- oo -blue-",align = "center",command=lambda *args:u_key( cmds.intField(text_2, query = True, value = True)))
	
	cmds.text(l=" r vowel sounds ")
	cmds.button(l = "-----------")
	cmds.button(l = "-----------")
	cmds.button(l = "1- ur -her-",align = "center",command=lambda *args:ur_key( cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "2- ar -dark-",align = "center",command=lambda *args:ar_key( cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "3- or -fork-",align = "center",command=lambda *args:or_key( cmds.intField(text_2, query = True, value = True)))
	cmds.setParent( '..' )
	
	child4 = cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[(1, 100), (2, 100), (3, 100)] )
	cmds.text(l=" the blends ")
	text_3 = cmds.intField( value=0 )
	cmds.text(l=" ---  keyframe . ! ?---")

	cmds.button(l = "1- bl -blue-",align = "center",command=lambda *args:bl_key(cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "2- cl -clap-",align = "center",command=lambda *args:cl_key( cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "3- fl -fly-",align = "center",command=lambda *args:fl_key(cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "4- gl -glue-",align = "center",command=lambda *args:kl_key( cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "5- pl -play-",align = "center",command=lambda *args:pl_key( cmds.intField(text_3, query = True, value = True))) ###
	cmds.button(l = "6- br -break-",align = "center",command=lambda *args:br_key( cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "7- cr -cry-",align = "center",command=lambda *args:cr_key(cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "8- dr -dry-",align = "center",command=lambda *args:dr_key(cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "9- fr -fry-",align = "center",command=lambda *args:fr_key( t_list,cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "10- gr -great-",align = "center",command=lambda *args:cr_key(cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "11- pr -prize-",align = "center",command=lambda *args:pr_key(cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "12- tr -tree-",align = "center",command=lambda *args:tr_key(cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "13- sk -skate-",align = "center",command=lambda *args:sk_key( cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "14- sl -slip-",align = "center",command=lambda *args:sl_key( cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "15- sp -spot-",align = "center",command=lambda *args:sp_key( cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "16- st -stop-",align = "center",command=lambda *args:st_key( cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "17- sw -sweet-",align = "center",command=lambda *args:sw_key(cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "18- spr -spring-",align = "center",command=lambda *args:pr_key( cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "19- str -string-",align = "center",command=lambda *args:tr_key( cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "-----------")
	cmds.button(l = "-----------")
	
	cmds.text(l=" 7 digraph sounds ")
	cmds.button(l = "-----------")
	cmds.button(l = "-----------")
	cmds.button(l = "1- ch -chin-",align = "center",command=lambda *args:g_key(t_list,reset_list, lips_list, cmds.intField(text_2, query = True, value = True)))
	cmds.button(l = "2- sh -ship-",align = "center",command=lambda *args:g_key( cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "3- thing -",align = "center",command=lambda *args:t_key(cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "4- this -",align = "center",command=lambda *args:d_key(cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "5- wh -",align = "center",command=lambda *args:y_key( cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "6- ng -",align = "center",command=lambda *args:n_key( cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "7- nk -",align = "center",command=lambda *args:n_key( cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "-----------")
	cmds.button(l = "-----------")
	
	cmds.text(l=" 7 special sounds ")
	cmds.button(l = "-----------")
	cmds.button(l = "-----------")
	cmds.button(l = "1- oi -",align = "center",command=lambda *args:oi_key(t_list,reset_list, lips_list, cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "2- ow -",align = "center",command=lambda *args:ow_key( cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "3- short oo -",align = "center",command=lambda *args:o_key(cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "4- aw -",align = "center",command=lambda *args:aw_key(cmds.intField(text_3, query = True, value = True)))
	cmds.button(l = "5- zh -",align = "center",command=lambda *args:g_key( cmds.intField(text_3, query = True, value = True)))
	cmds.setParent( '..' )

	cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Automatic'), (child2, 'Sounds Type 1'), (child4, 'Sounds Type 3') ))
	cmds.showWindow() 

if __name__ == "__main__":
	speechToolGUI()
