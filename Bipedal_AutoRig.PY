# Automatic Rigging script written by Anna Georgieva for Pirate LockJaw MasterClass
#using the autodesk tutorials for a comprehensive rig

import maya.cmds as cmds 
import random as random
import maya.mel as mel


###remove all selects and move if not needed
'''
##ALL the names of locators and joints
'''
#locators names 
namesLegLeft=['left_start_leg','left_mid_leg','left_end_leg']#3
namesArmRight=['right_start_arm','right_mid_arm','right_end_arm','right_hand']#4
spineALL=['start_spine', 'mid_spine1', 'mid_spine2', 'mid_spine3','mid_spine4','mid_spine5', 'end_spine']#7
namesFeetLeft=['left_feet_start','left_feet_end']#2

namesFingersRightThumb=['right_thumb_start','right_thumb_mid','right_thumb_mid2','right_thumb_end']#4
namesFingersRightIndex=['right_index_start','right_index_mid','right_index_mid2','right_index_end']#4
namesFingersRightMiddle=['right_middle_start','right_middle_mid','right_middle_mid2','right_middle_end']#4
namesFingersRightRing=['right_ring_start','right_ring_mid','right_ring_mid2','right_ring_end']#4
namesFingersRightPinky=['right_pinky_start','right_pinky_mid','right_pinky_mid2','right_pinky_end']#4

#7
spineJnt=[]
for item in spineALL:
	spineJnt.append(item+str('_jnt'))
	
#left and right side joint names
LeftLegJnt=[]
RightLegJnt=[]

feetLeftJnt=[]
feetRightJnt=[]
for item in namesFeetLeft: #2
	feetLeftJnt.append(item+str('_jnt'))
	
for item in namesLegLeft:#3
	LeftLegJnt.append(item+str('_jnt'))

leftVar="left_"
length=len(leftVar)

for lineJnt in LeftLegJnt:
	if lineJnt.startswith("left_"):
		RightLegJnt.append('right_'+lineJnt[length:]) 

for lineJnt in feetLeftJnt:
	if lineJnt.startswith("left_"):
		feetRightJnt.append('right_'+lineJnt[length:]) 

rThumbJnts=[]	
rIndexJnts=[]
rMiddleJnts=[]
rRingJnts=[]
rPinkyJnts=[]

RightArmJnt=[]
LeftArmJnt=[]
#4
for item1,item2,item3,item4,item5,item6 in zip(namesFingersRightThumb,namesFingersRightIndex,namesFingersRightMiddle,namesFingersRightRing,namesFingersRightPinky, namesArmRight):
	rThumbJnts.append(item1+str('_jnt'))
	rIndexJnts.append(item2+str('_jnt'))
	rMiddleJnts.append(item3+str('_jnt'))
	rRingJnts.append(item4+str('_jnt'))
	rPinkyJnts.append(item5+str('_jnt'))
	
	RightArmJnt.append(item6+str('_jnt'))
	
for lineArm in RightArmJnt:
	if lineArm.startswith('right_'):
		LeftArmJnt.append('left'+lineArm[length:]) 
			
					###FK IK Original Order jnts for parenting #optimize
handRightArmJnts=['right_hand_jnt_FK','right_hand_jnt_IK','right_hand_jnt', ]					
endRightArmJnts=['right_end_arm_jnt_FK','right_end_arm_jnt_IK','right_end_arm_jnt']
midRightArmJnts=['right_mid_arm_jnt_FK','right_mid_arm_jnt_IK','right_mid_arm_jnt']

startRightArmJnts=['right_start_arm_jnt_FK','right_start_arm_jnt_IK','right_start_arm_jnt']

endLeftLeg=['left_end_leg_jnt_FK','left_end_leg_jnt_IK','left_end_leg_jnt']
midLeftLeg=['left_mid_leg_jnt_FK','left_mid_leg_jnt_IK','left_mid_leg_jnt']
startLeftLeg=['left_start_leg_jnt_FK','left_start_leg_jnt_IK','left_start_leg_jnt']

startLeftFeet=['left_feet_start_jnt_FK','left_feet_start_jnt_IK','left_feet_start_jnt']
endLeftFeet=['left_feet_end_jnt_FK','left_feet_end_jnt_IK','left_feet_end_jnt']

spineIK=[] #is not used as the original jnt chain is used as fk
spineFK=[] ##checkLocExist

leftLegIK=[] ##checkLocExist
leftLegFK=[] ##checkLocExist

rightLegIK=[] ##checkLocExist
rightLegFK=[] ##checkLocExist

rightArmIK=[] ##checkLocExist
rightArmFK=[] ##checkLocExist

rightFeetFK=[] ##checkLocExist
rightFeetIK=[]  ##checkLocExist

leftFeetFK=[] ##checkLocExist
leftFeetIK=[]  ##checkLocExist


def checkFound(found, nameOfJnts):
	'''
	checks if the locators are named appropriately and creates the joints
	'''
	if len(found) == len(nameOfJnts):
		print('all '+str(nameOfJnts)+' exist')
		for i in nameOfJnts:
			cmds.joint(i,n=str(i)+'_jnt')
	else:
		print( str(nameOfJnts)+'is not named properly')				

def checkLocExist(*args):
	'''
	checks if the locators exist and creates FK IK and results joints 
	'''
	arrayBody=[cmds.ls(namesLegLeft,r=True), cmds.ls(namesArmRight,r=True), cmds.ls(spineALL,r=True), cmds.ls(namesFeetLeft,r=True)]
	funcBody=[namesLegLeft,namesArmRight,spineALL,namesFeetLeft]
	for i in range(0,len(arrayBody)):
		checkFound(arrayBody[i],funcBody[i])
		
	arrayFinger=[cmds.ls(namesFingersRightThumb), cmds.ls(namesFingersRightIndex), cmds.ls(namesFingersRightMiddle),cmds.ls(namesFingersRightRing),cmds.ls(namesFingersRightPinky)]
	funcFinger=[namesFingersRightThumb,namesFingersRightIndex,namesFingersRightMiddle,namesFingersRightRing,namesFingersRightPinky]
	for i in range(0,len(arrayFinger)):
		checkFound(arrayFinger[i],funcFinger[i])
	
	#duplicate joints for FK/IK
	for i in range(0,3): 
		for j in range(0,2): #create two types joints for IK and FK controllers
			if(j==0):#IK=0
				cmds.duplicate(LeftLegJnt[i],n=LeftLegJnt[i]+'_IK')
				leftLegIK.append(LeftLegJnt[i]+'_IK')
			else:#FK=1
				cmds.duplicate(LeftLegJnt[i],n=LeftLegJnt[i]+'_FK')
				leftLegFK.append(LeftLegJnt[i]+'_FK')
				
	for i in range(0,4):
		for j in range(0,2):
			if(j==0):#ik
				cmds.duplicate(RightArmJnt[i],n=RightArmJnt[i]+'_IK')	
				rightArmIK.append(RightArmJnt[i]+'_IK')	
				#leftArmIK	
			else:	
				cmds.duplicate(RightArmJnt[i],n=RightArmJnt[i]+'_FK')
				rightArmFK.append(RightArmJnt[i]+'_FK')	
				#leftArmFK
	###
	#print rightArmFK
	####			
	for i in range(0,len(spineJnt)): #if we had 3 joint hierarcies fk ik and original but we have original and fk
		'''for j in range(0,2):
			if(j==0):#IK=0
				#cmds.duplicate(spineJnt[i],n=spineJnt[i]+'_IK')
				#spineIK.append(spineJnt[i]+'_IK')
			else:#FK=1'''
		cmds.duplicate(spineJnt[i],n=spineJnt[i]+'_FK')	
		spineFK.append(spineJnt[i]+'_FK')
					
	for i in range(0,len(feetLeftJnt)):
		for j in range(0,2):
			if(j==0):#IK=0			
				cmds.duplicate(feetLeftJnt[i],n=feetLeftJnt[i]+'_IK')
				leftFeetIK.append(feetLeftJnt[i]+'_IK')
			else:
				cmds.duplicate(feetLeftJnt[i],n=feetLeftJnt[i]+'_FK')
				leftFeetFK.append(feetLeftJnt[i]+'_FK')
	
	#creates a layer for the locators, adds them and changes the colour to white
	locators = cmds.ls(type=('locator'),l=True)
	cmds.createDisplayLayer(locators,n="Locators",num=1,nr=True) 
	cmds.setAttr('Locators.color', 16) 
	cmds.setAttr('Locators.overrideColorRGB', 0, 0, 0) 
	cmds.setAttr('Locators.overrideRGBColors', 0) 

	
	cmds.createDisplayLayer('mesh',n="Mesh",num=1,nr=True) 
	cmds.setAttr('Mesh.color', 5) 
	cmds.setAttr('Mesh.overrideColorRGB', 0, 0, 0) 
	cmds.setAttr('Mesh.overrideRGBColors', 0) 
	
	#fill in the right lists strings
	for lineIK,lineFK in zip(leftLegIK,leftLegFK):
		if lineIK.startswith("left_"):
			rightLegIK.append('right_'+lineIK[length:])	
		if lineFK.startswith("left_"):
			rightLegFK.append('right_'+lineFK[length:])	
			
	for lineFK,lineIK in zip(leftFeetIK,leftFeetFK):
		if lineFK.startswith("left_"):
			rightFeetFK.append('right_'+lineFK[length:]) 
		if lineIK.startswith("left_"):
			rightFeetIK.append('right_'+lineIK[length:]) 		
			
	cmds.select(clear=True)		
	parentJoints()
#parent all the joints to the appropriate hierarchies	
def parentJoints():
	'''
	parents all the joints creates the hierarchies
	''' 
	for i in range(0,len(LeftLegJnt)):
		cmds.parent(handRightArmJnts[i],endRightArmJnts[i])
		cmds.parent(endRightArmJnts[i],midRightArmJnts[i])
		cmds.parent(midRightArmJnts[i],startRightArmJnts[i])
		cmds.parent(endLeftFeet[i],startLeftFeet[i])
		cmds.parent(startLeftFeet[i], endLeftLeg[i])
		cmds.parent(endLeftLeg[i], midLeftLeg[i])
		cmds.parent(midLeftLeg[i], startLeftLeg[i])
	
	cmds.select(clear=True)		
	
	count=len(spineJnt)-1
	
	while(count!=0):
		cmds.parent(spineJnt[count],spineJnt[count-1]) #original doing the ik
		cmds.parent(spineFK[count],spineFK[count-1])	#fk chain
		#cmds.parent(spineIK[count],spineIK[count-1]) #no ik spine now
		count-=1
		
	cmds.select(clear=True)		
	count2=len(rIndexJnts)-1
	
	while(count2!=0):
		cmds.parent(rThumbJnts[count2],rThumbJnts[count2-1])
		cmds.parent(rIndexJnts[count2],rIndexJnts[count2-1])
		cmds.parent(rMiddleJnts[count2],rMiddleJnts[count2-1])
		cmds.parent(rRingJnts[count2],rRingJnts[count2-1])
		cmds.parent(rPinkyJnts[count2],rPinkyJnts[count2-1])
		count2-=1
	
	#unparent all the start joints from the locators		
	cmds.parent(spineJnt[0],spineFK[0],RightArmJnt[0],rightArmFK[0],rightArmIK[0],	
				LeftLegJnt[0],leftLegFK[0],leftLegIK[0],
				rThumbJnts[0],rIndexJnts[0],rMiddleJnts[0],rRingJnts[0],rPinkyJnts[0],w=True) #spineIK[0]

	cmds.mirrorJoint('left_start_leg_jnt',mirrorYZ=True,mirrorBehavior=True,searchReplace=('left_', 'right_') )
	cmds.mirrorJoint('left_start_leg_jnt_FK',mirrorYZ=True,mirrorBehavior=True,searchReplace=('left_', 'right_') )
	cmds.mirrorJoint('left_start_leg_jnt_IK',mirrorYZ=True,mirrorBehavior=True,searchReplace=('left_', 'right_') )

	cmds.select(clear=True)		
#create the spine	
def spineDO(*args):	
	'''
	creates squash and stretch spine, adds controllers and a root ctrl
	'''
	cmds.joint(spineJnt[0],e=True,oj='xzy',sao='xup',ch=True,zso=True)
	cmds.ikHandle(n='spine_hdl',sj=spineJnt[0],ee=spineJnt[len(spineJnt)-1],sol='ikSplineSolver')
	cmds.rename('curve1', 'spine_curve_ik_handle')
	cmds.rename('effector1', 'spine_effector')
	
	cmds.duplicate(spineJnt[0])
	cmds.rename('start_spine_jnt1','hip_bind_jnt')
	cmds.pickWalk('hip_bind_jnt',d='down')
	cmds.parent(w=True)
	for i in range(0,6):
		cmds.pickWalk(d='down')
	cmds.parent(w=True)
	cmds.rename('|end_spine_jnt','sh_bind_jnt')
	cmds.delete('|mid_spine1_jnt')
	cmds.skinCluster('hip_bind_jnt','sh_bind_jnt','spine_curve_ik_handle',mi=2)
	
	#square controller
	mel.eval('curve -d 1 -p -3 0 -1 -p -3 0 2 -p 2 0 2 -p 2 0 -1 -p -3 0 -1 -p -3 2 -1 -p -3 2 2 -p -3 0 2 -p -3 2 2 -p 2 2 2 -p 2 0 2 -p 2 2 2 -p 2 2 -1 -p 2 0 -1 -p 2 2 -1 -p -3 2 -1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 ;')
	
	cmds.rename('curve1', 'Hip_ctrl')
	cmds.duplicate('Hip_ctrl', n='Sh_ctrl')
	cmds.xform('Hip_ctrl', cp=1)
	cmds.xform('Sh_ctrl',cp=1)
	
	posHip=[cmds.getAttr('start_spine.translateX'),cmds.getAttr('start_spine.translateY'),cmds.getAttr('start_spine.translateZ')]
	cmds.setAttr('Hip_ctrl.translate',posHip[0]+0.5,posHip[1]-1,posHip[2]-0.5)
	posSh=[cmds.getAttr('end_spine.translateX'),cmds.getAttr('end_spine.translateY'),cmds.getAttr('end_spine.translateZ')]
	cmds.setAttr('Sh_ctrl.translate',posSh[0]+0.5,posSh[1]-1,posSh[2]-0.5)
	
	cmds.scale(1, 1, 18,'Sh_ctrl.cv[0:15]', r=True, p=(posSh[0], posSh[1], posSh[2]))
	cmds.scale(12, 1, 1, 'Sh_ctrl.cv[0:15]',r=True, p=(posSh[0], posSh[1], posSh[2]))
	cmds.xform ('Sh_ctrl.cv[0:4]', 'Sh_ctrl.cv[7]', 'Sh_ctrl.cv[10]', 'Sh_ctrl.cv[13]',t=(0, -5, 0), r=True)
	cmds.xform ('Sh_ctrl.cv[0:15]',t=(0, 20, 0), r=True)
	cmds.setAttr("Sh_ctrlShape.overrideEnabled", 1)
	cmds.setAttr("Sh_ctrlShape.overrideColor", 16)

	cmds.scale(1, 1, 18,'Hip_ctrl.cv[0:15]',r=True, p=(posHip[0], posHip[1], posHip[2]))
	cmds.scale(12, 1, 1,'Hip_ctrl.cv[0:15]', r=True, p=(posHip[0], posHip[1], posHip[2]))
	cmds.xform('Hip_ctrl.cv[0:4]', 'Hip_ctrl.cv[7]' ,'Hip_ctrl.cv[10]', 'Hip_ctrl.cv[13]', t=(0, -5, 0), r=True)
	cmds.setAttr("Hip_ctrl.overrideEnabled", 1)
	cmds.setAttr("Hip_ctrl.overrideColor", 16)
	
	cmds.makeIdentity('Hip_ctrl','Sh_ctrl', apply=True,t=1,r=1,s=1,n=0,pn=1)
	
	rotOrder=['Hip_ctrl','Sh_ctrl','hip_bind_jnt','sh_bind_jnt']
	for item in rotOrder:
		cmds.setAttr(item+".rotateOrder", 2)
	
	cmds.parentConstraint('Hip_ctrl','hip_bind_jnt',mo=True, w=1)
	cmds.parentConstraint('Sh_ctrl','sh_bind_jnt',mo=True, w=1)
	
	cmds.setAttr("spine_hdl.dTwistControlEnable",1)
	cmds.setAttr("spine_hdl.dWorldUpType",4)
	cmds.setAttr("spine_hdl.dWorldUpAxis",1)
	cmds.setAttr("spine_hdl.dWorldUpVectorY",-1)
	cmds.setAttr("spine_hdl.dWorldUpVectorEndY",0)
	cmds.setAttr("spine_hdl.dWorldUpVectorEndZ",-1)
	
	cmds.connectAttr('hip_bind_jnt.worldMatrix[0]', 'spine_hdl.dWorldUpMatrix',f=True)
	cmds.connectAttr('sh_bind_jnt.worldMatrix[0]',  'spine_hdl.dWorldUpMatrixEnd', f=True)
	
	###twist ik 
	cmds.rename('start_spine_jnt_FK','hip_FK_jnt')
	cmds.rename('end_spine_jnt_FK','sh_FK_jnt')
	cmds.joint('hip_FK_jnt',e=True,oj='yxz', sao='xup', ch=True,zso=True)

	midSpineFK= spineFK[1:-1]
	for item in midSpineFK:
		cmds.setAttr(item+".rotateOrder",1) #yzx 
		cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n=item+'ctrl')
		
	cmds.group( 'Sh_ctrl', n='Sh_FKConst_Grp' )
	cmds.group( 'Hip_ctrl', n='Hip_FKConst_Grp' )
	cmds.parentConstraint('hip_FK_jnt','Hip_FKConst_Grp',mo=True, w=1)
	cmds.parentConstraint('sh_FK_jnt','Sh_FKConst_Grp',mo=True, w=1)
	
	for item in midSpineFK:
		cmds.parent(item+'ctrlShape', item,r=True, s=True)
		
	posMidLoc=[]
	posMidSpine=spineALL[1:-1]
	for item in posMidSpine:
		posMidLoc.append(cmds.getAttr(item+'.translate'))	
	flat_list = [item for sublist in posMidLoc for item in sublist]
	for item, position in zip(midSpineFK, flat_list):
		cmds.scale(30,30,30,item+'ctrlShape.cv[0:7]',p=position,r=True)	
		cmds.setAttr(item+".overrideEnabled", 1)
		cmds.setAttr(item+".overrideColor", 17)
	
	cmds.select(clear=True)
	cmds.delete('mid_spine1_jnt_FKctrl','mid_spine2_jnt_FKctrl','mid_spine3_jnt_FKctrl','mid_spine4_jnt_FKctrl','mid_spine5_jnt_FKctrl')
	###fk controls 
	
	curveInfoNode = cmds.arclen('spine_curve_ik_handle', ch=True)
	cmds.rename(curveInfoNode, 'spine_Length')
	cmds.shadingNode('multiplyDivide',au=True,n='spine_stretchDiv')
	cmds.connectAttr('spine_Length.arcLength', 'spine_stretchDiv.input1X', f=True)
	cmds.setAttr("spine_stretchDiv.operation", 2)
	cmds.setAttr("spine_stretchDiv.input2X", cmds.getAttr('spine_stretchDiv.input1X'))
	 
	spineFK_withoutLastJnt=spineJnt[0:len(spineJnt)-1]
	for item in spineFK_withoutLastJnt:
		cmds.connectAttr('spine_stretchDiv.outputX', item+'.scaleX' ,f=True) 
	
	###stretch 
	cmds.shadingNode('multiplyDivide',au=True,n='spine_squarePow')
	cmds.connectAttr('spine_stretchDiv.outputX', 'spine_squarePow.input1X' )
	cmds.setAttr("spine_squarePow.operation", 3)
	cmds.setAttr('spine_squarePow.input2X', 0.5)
	
	cmds.shadingNode('multiplyDivide',au=True,n='spine_stretch_invDiv')
	cmds.connectAttr('spine_squarePow.outputX', 'spine_stretch_invDiv.input2X' )
	cmds.setAttr("spine_stretch_invDiv.operation", 2)
	cmds.setAttr('spine_stretch_invDiv.input1X',1)
	
	for item in spineJnt:
		cmds.connectAttr('spine_stretch_invDiv.outputX', item+'.scaleY' ,f=True) 
		cmds.connectAttr('spine_stretch_invDiv.outputX', item+'.scaleZ' ,f=True) 
		
	###squash 
	###translate control square
	mel.eval('curve -d 1 -p -1 0 -3 -p -3 0 -1 -p -4 0 -1 -p -4 0 -2 -p -6 0 0 -p -4 0 2 -p -4 0 1 -p -3 0 1 -p -1 0 3 -p -1 0 4 -p -2 0 4 -p 0 0 6 -p 2 0 4 -p 1 0 4 -p 1 0 3 -p 3 0 1 -p 4 0 1 -p 4 0 2 -p 6 0 0 -p 4 0 -2 -p 4 0 -1 -p 3 0 -1 -p 1 0 -3 -p 1 0 -4 -p 2 0 -4 -p 0 0 -6 -p -2 0 -4 -p -1 0 -4 -p -1 0 -3 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 -k 17 -k 18 -k 19 -k 20 -k 21 -k 22 -k 23 -k 24 -k 25 -k 26 -k 27 -k 28 ;')
	cmds.setAttr('curve1.translate',posHip[0],posHip[1],posHip[2])
	cmds.xform('curve1',cp=1)
	cmds.rename('curve1','body_Ctrl')
	cmds.setAttr("body_Ctrl.scale", 10, 10, 10)
	cmds.makeIdentity('body_Ctrl', apply=True,t=1,r=1,s=1,n=0,pn=1)
	cmds.setAttr('body_Ctrl.rotateOrder', 2)
	cmds.setAttr('body_Ctrl'+".overrideEnabled", 1)
	cmds.setAttr('body_Ctrl'+".overrideColor", 17)	
	cmds.group('start_spine_jnt','hip_FK_jnt', 'spine_hdl',
				'spine_curve_ik_handle', 'hip_bind_jnt','sh_bind_jnt',
				'Sh_FKConst_Grp','Hip_FKConst_Grp', n='torso_GRP')
				
	cmds.parentConstraint('body_Ctrl','torso_GRP',mo=True, w=1)
	cmds.setAttr("spine_curve_ik_handle.inheritsTransform",0)
	cmds.group('start_spine_jnt', 'spine_hdl','spine_curve_ik_handle', 
				'hip_bind_jnt','sh_bind_jnt',n='DO_NOT_TOUCH')		
	
	#clean-up and lock attr
	allTorsoCtrls=['Sh_ctrl','Hip_ctrl', 'body_Ctrl',
					'mid_spine1_jnt_FK', 'mid_spine2_jnt_FK', 
					'mid_spine3_jnt_FK', 'mid_spine4_jnt_FK', 
					'mid_spine5_jnt_FK']
	
	cmds.group('body_Ctrl', 'torso_GRP',n="pirate_Root_Transform")
	cmds.setAttr("pirate_Root_Transform.rotateOrder",2)

	cmds.shadingNode('multiplyDivide',au=True,n='global_scale_spine')
	cmds.connectAttr('spine_Length.arcLength', 'global_scale_spine.input1X', f=True)
	cmds.connectAttr('pirate_Root_Transform.scaleY', 'global_scale_spine.input2X', f=True)
	cmds.setAttr("global_scale_spine.operation",2)
	cmds.connectAttr('global_scale_spine.outputX', 'spine_stretchDiv.input1X', f=True)
	
	###optimize
	namesLegRight=['right_start_leg', 'right_mid_leg', 'right_end_leg']
	for i,k in zip(namesLegLeft,namesLegRight):	
		cmds.duplicate(i,n=k)
		cmds.setAttr(k+'.translateX',-cmds.getAttr(i+'.translateX'))
	
	
	###scaling factors
	controls=["stretch_on_off","squash_on_off","manual_stretch","clamp"]
	maxValue=[1,1,1,10]
	defaultValue=[1,1,0,1]
	for i,k,l in zip(controls,maxValue, defaultValue):
		cmds.addAttr( '|pirate_Root_Transform|torso_GRP|Sh_FKConst_Grp|Sh_ctrl',ln=i, at='double', min=0,max=k,dv=l)
		cmds.setAttr( '|pirate_Root_Transform|torso_GRP|Sh_FKConst_Grp|Sh_ctrl.'+i,e=True,keyable=True)
	
	#breathe in/out joints
	cmds.joint(p=(0,180,5),n='breathe_ik_1')
	cmds.select(clear=True)
	cmds.joint(p=(0,175,5),n='breathe_ik_2')
	cmds.select(clear=True)
	cmds.select('breathe_ik_1','breathe_ik_2','spine_curve_ik_handle')
	mel.eval('skinClusterInfluence 1 "-ug -dr 4 -ps 0 -ns 10";')
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n='breathe_ctrl_1')
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n='breathe_ctrl_2')
	cmds.xform('breathe_ctrl_1Shape.cv[0:7]', s=(2,2,2))
	cmds.xform('breathe_ctrl_1Shape.cv[0:7]', ro=(90,0,0))
	cmds.xform('breathe_ctrl_2Shape.cv[0:7]', s=(2,2,2))
	cmds.xform('breathe_ctrl_2Shape.cv[0:7]', ro=(90,0,0))
	
	cmds.parent('breathe_ctrl_1Shape','breathe_ik_1',r=True,s=True)
	cmds.parent('breathe_ctrl_2Shape','breathe_ik_2',r=True,s=True)
	cmds.parent('breathe_ik_1','breathe_ik_2', 'torso_GRP')
	cmds.setAttr("breathe_ctrl_1Shape.overrideEnabled", 1)
	cmds.setAttr("breathe_ctrl_1Shape.overrideColor", 17)
	cmds.setAttr("breathe_ctrl_2Shape.overrideEnabled", 1)
	cmds.setAttr("breathe_ctrl_2Shape.overrideColor", 17)
	
	cmds.move(0,0,-35,'breathe_ik_2.cv[0:7]', 'breathe_ik_1.cv[0:7]', r=True )
	cmds.delete(' breathe_ctrl_2', 'breathe_ctrl_1')
	###squash and stretch settings on off
	cmds.distanceDimension(sp=(0,0,0),ep=(0,1,0))
	cmds.rename('locator1', 'start_spine_loc')
	cmds.rename('locator2', 'end_spine_loc')
	cmds.setAttr('start_spine_loc.translate',cmds.getAttr('start_spine.translateX'), cmds.getAttr('start_spine.translateY'),cmds.getAttr('start_spine.translateZ'))
	cmds.setAttr('end_spine_loc.translate',cmds.getAttr('end_spine.translateX'),cmds.getAttr('end_spine.translateY'),cmds.getAttr('end_spine.translateZ'))
	cmds.rename('distanceDimension1', 'spine_IK_length' )
	cmds.parent('start_spine_loc','Hip_ctrl')
	cmds.parent('end_spine_loc','Sh_ctrl')
	cmds.connectAttr('spine_IK_length.distance','global_scale_spine.input1X',f=True)
	cmds.shadingNode('condition', au=True, n='if_switch')
	cmds.shadingNode('condition', au=True, n='if_filter')
	cmds.connectAttr('spine_stretchDiv.outputX','if_switch.colorIfTrue.colorIfTrueR',f=True)
	cmds.connectAttr( 'Sh_ctrl.stretch_on_off', 'if_switch.firstTerm',f=True)
	cmds.setAttr("if_switch.secondTerm",1)
	cmds.connectAttr( ' if_switch.outColor.outColorR', 'if_filter.colorIfTrue.colorIfTrueR',f=True)
	cmds.connectAttr( ' spine_stretchDiv.output.outputX', 'if_filter.firstTerm',f=True)
	cmds.setAttr("if_filter.operation",3)
	for item in spineFK_withoutLastJnt:
		cmds.connectAttr('if_filter.outColor.outColorR', item+'.scale.scaleX' ,f=True) 
	
	cmds.shadingNode('unitConversion',au=True,n='squash_number')
	cmds.connectAttr('Sh_ctrl.squash_on_off', 'squash_number.input',f=True)
	cmds.connectAttr('squash_number.output', 'spine_stretch_invDiv.operation',f=True)
	cmds.setAttr("squash_number.conversionFactor", 2)
	
	### manual stretch and clamp
	cmds.shadingNode('plusMinusAverage',au=True,n='pm_manualStretch')
	cmds.addAttr('pm_manualStretch',ln="offset",at='double',dv=1)
	cmds.setAttr('pm_manualStretch.offset',e=True,keyable=True)
	cmds.connectAttr('pm_manualStretch.offset','pm_manualStretch.input1D[0]',f=True)
	cmds.connectAttr('Sh_ctrl.manual_stretch','pm_manualStretch.input1D[1]',f=True)
	cmds.connectAttr('pm_manualStretch.output1D', 'if_switch.colorIfTrue.colorIfTrueG' ,f=True)
	cmds.connectAttr('if_switch.outColor.outColorG', 'if_filter.colorIfFalse.colorIfFalseR', f=True)
	cmds.connectAttr('if_switch.outColor.outColorG', 'if_filter.secondTerm', f=True)
	

	cmds.shadingNode('clamp',au=True,n='cl_clampStretch')
	cmds.connectAttr('spine_stretchDiv.output.outputX', 'cl_clampStretch.input.inputR', f=True)
	cmds.connectAttr('Sh_ctrl.clamp','cl_clampStretch.max.maxR', f=True)
	cmds.connectAttr(' cl_clampStretch.output.outputR', 'if_switch.colorIfTrue.colorIfTrueR', f=True)
	
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n='pirate_root_ctrl')
	cmds.xform('pirate_root_ctrlShape.cv[0:7]', s=(80,80,80))
	cmds.setAttr('pirate_root_ctrlShape'+".overrideEnabled", 1)
	cmds.setAttr('pirate_root_ctrlShape'+".overrideColor", 16)	
	cmds.parent('pirate_root_ctrlShape','pirate_Root_Transform',r=True,s=True)
	cmds.delete('pirate_root_ctrl')	
	
	#cleaning
	scaleList=['.sx','.sy','.sz']
	translateList=['.tx','.ty','.tz']
	rotateList=['.rx','.ry','.rz']
	
	for item in allTorsoCtrls:
		for sc in scaleList:
			cmds.setAttr(item+sc,l=True)
		cmds.setAttr(item+'.v',l=True)
		
	for item in midSpineFK:
		for tr in translateList:
			cmds.setAttr(item+tr,l=True)
		cmds.setAttr(item+'.v',l=True)
		cmds.setAttr(item+".radi",l=True)
	
	for i, k in zip(scaleList, rotateList):
		cmds.setAttr('breathe_ik_2'+i, l=True)
		cmds.setAttr('breathe_ik_2'+k, l=True)
		cmds.setAttr('breathe_ik_1'+i, l=True)
		cmds.setAttr('breathe_ik_1'+k, l=True)
		
	cmds.setAttr('spine_IK_length.v',0)
	####cleanup ends here
	cmds.select(clear=True)	
		
#left/ right leg input for optimization	
def legDo(legField):
	'''
	creates the leg left or right
	'''
	newName = str(cmds.textField(legField, query=True, text=True))
	print newName

	cmds.joint(newName+'_start_leg_jnt',newName+'_start_leg_jnt_FK',newName+'_start_leg_jnt_IK',e=True,oj='xyz',sao='xup',ch=True,zso=True)
	#orienting the leg joints the same way 
	
	if newName=='left':
		anklePos=[cmds.getAttr('left_end_leg.translateX'),cmds.getAttr('left_end_leg.translateY'),cmds.getAttr('left_end_leg.translateZ')]
		PosKnee=[cmds.getAttr('left_mid_leg.translateX'),cmds.getAttr('left_mid_leg.translateY'),cmds.getAttr('left_mid_leg.translateZ')]		
		hipPos=[cmds.getAttr('left_start_leg.translateX'),cmds.getAttr('left_start_leg.translateY'),cmds.getAttr('left_start_leg.translateZ')]
	if newName=='right':
		hipPos=[cmds.getAttr('right_start_leg.translateX'),cmds.getAttr('right_start_leg.translateY'),cmds.getAttr('right_start_leg.translateZ')]
		anklePos=[cmds.getAttr('right_end_leg.translateX'),cmds.getAttr('right_end_leg.translateY'),cmds.getAttr('right_end_leg.translateZ')]
		PosKnee=[cmds.getAttr('right_mid_leg.translateX'),cmds.getAttr('right_mid_leg.translateY'),cmds.getAttr('right_mid_leg.translateZ')]	
	
	blendNodesRot=[]
	blendNodesTr=[] 
	
	leftThighLength=[]
	leftShinLength=[]
	
	rightThighLength=[]
	rightShinLength=[]
	
	side_NoFlip_Leg=[newName+'_start_NO_FLIP_leg_jnt_IK ', newName+'_mid_NO_FLIP_leg_jnt_IK', newName+'_end_NO_FLIP_leg_jnt_IK']
	side_PV_Leg=[ newName+'_start_PV_leg_jnt_IK1',newName+'_mid_PV_leg_jnt_IK1',newName+'_end_PV_leg_jnt_IK1']
	choiceROTblendNodes=[]
	choiceTRblendNodes=[]

	if(newName=='left'):
		dictionary={'LeftLegJnt':LeftLegJnt,'feetLeftJnt':feetLeftJnt,
					'leftLegIK':leftLegIK, 'leftLegFK':leftLegFK,
					'leftFeetIK':leftFeetIK, 'leftFeetFK':leftFeetFK,
					'leftThighLength':leftThighLength,
					'leftShinLength':leftShinLength}
			
	if(newName=='right'):
		dictionary={'RightLegJnt':RightLegJnt,'feetRightJnt':feetRightJnt,
					'rightLegIK':rightLegIK, 'rightLegFK':rightLegFK,
					'rightFeetIK':rightFeetIK, 'rightFeetFK':rightFeetFK,
					'rightThighLength':rightThighLength,
					'rightShinLength':rightShinLength}
	
	#LeftLegJnt or RightLegJnt
	LegJnts=dictionary[newName.title()+'LegJnt']
	for item in LegJnts:
		cmds.shadingNode('blendColors',au=True,n=item+str(newName.title())+'rot_IK_FK')
		cmds.shadingNode('blendColors',au=True,n=item+str(newName.title())+'tr_IK_FK')
		#stores all the blendNodes 
		#fisrt 20 goes left (next 20 right) 10 each tr and rot 40 in total
		blendNodesRot.append(item+str(newName.title())+'rot_IK_FK')
		blendNodesTr.append(item+str(newName.title())+'tr_IK_FK')
	
    #feetLeftJnt or feetRightJnt
	fJnts=dictionary['feet'+newName.title()+'Jnt']
	for item in fJnts:
		cmds.shadingNode('blendColors',au=True,n=item+str(newName.title())+'rot_IK_FK')
		cmds.shadingNode('blendColors',au=True,n=item+str(newName.title())+'tr_IK_FK')
		blendNodesRot.append(item+str(newName.title())+'rot_IK_FK')
		blendNodesTr.append(item+str(newName.title())+'tr_IK_FK')
	
	#x in leftLegIK , y in leftLegFK or right....
	#z in blendNodesRot, z1 in blendNodesTr or right...
	#o in LeftLegJnt or Right...
	legIK=dictionary[newName+'LegIK']
	legFK=dictionary[newName+'LegFK']
	
	for x, y, z, z1, o in zip(legIK, legFK, blendNodesRot, blendNodesTr, LegJnts):
		cmds.connectAttr(x+'.rotate', z+'.color1', f=True)
		cmds.connectAttr(y+'.rotate', z+'.color2', f=True)
		cmds.connectAttr(z+'.output', o+'.rotate', f=True)
	
		cmds.connectAttr(x+'.translate', z1+'.color1', f=True)
		cmds.connectAttr(y+'.translate', z1+'.color2', f=True)
		cmds.connectAttr(z1+'.output', o+'.translate', f=True)
	
	blendFeetRot=blendNodesRot[-2:] 
	blendFeetTr=blendNodesTr[-2:] 

	#x in leftFeetIK, y in leftFeetFK or right...
	#z in blendFeetRot, z1 in blendFeetTr or right...
	#o in feetLeftJnt or Right...
	feetIK=dictionary[newName+'FeetIK']
	feetFK=dictionary[newName+'FeetFK']
	
	for x, y, z, z1, o in zip(feetIK,feetFK, blendFeetRot, blendFeetTr,fJnts):
		cmds.connectAttr(x+'.rotate', z+'.color1', f=True)
		cmds.connectAttr(y+'.rotate', z+'.color2', f=True)
		cmds.connectAttr(z+'.output', o+'.rotate', f=True)
		
		cmds.connectAttr(x+'.translate', z1+'.color1', f=True)
		cmds.connectAttr(y+'.translate', z1+'.color2', f=True)
		cmds.connectAttr(z1+'.output', o+'.translate', f=True)
	###ik/fk switch controller
	mel.eval('curve -d 1 -p 0 0 -2 -p 0 0 2 -p -2 0 0 -p 2 0 0 -p 0 0 2 -p -2 0 0 -p 0 0 -2 -p 2 0 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 ;')
	cmds.rename('curve1', newName+'_Leg_settingsCTRL')
	cmds.xform(newName+'_Leg_settingsCTRL',s=(5,5,5))
	
	######### colour it
	giveColour(newName,'_Leg_settingsCTRL') 	
	
	cmds.setAttr(newName+'_Leg_settingsCTRL.translate',anklePos[0],anklePos[1],anklePos[2]-20)
	cmds.rotate( 0, 0, 90, newName+'_Leg_settingsCTRL', r=True, os=True, fo=True )
	cmds.parentConstraint(newName+'_end_leg_jnt',newName+'_Leg_settingsCTRL',mo=True, w=1)
	cmds.group(newName+'_Leg_settingsCTRL', n=newName+'_settings_GRP')
	
	#fk controls	
	cmds.addAttr(newName+'_Leg_settingsCTRL',ln="FK_IK_blend", nn="FK/IK_blend", at='double', min=0, max=1, dv=0 )
	cmds.setAttr(newName+'_Leg_settingsCTRL.FK_IK_blend',e=True,keyable=True)

	for item,item1 in zip(blendNodesRot,blendNodesTr):
		cmds.connectAttr(newName+'_Leg_settingsCTRL.FK_IK_blend',item+'.blender',f=True)
		cmds.connectAttr(newName+'_Leg_settingsCTRL.FK_IK_blend',item1+'.blender',f=True)
	
	for x,y in zip(LegJnts,legFK):
		cmds.curve(d=1, p=[(-3, 0, -1),(-3, 0, 2),(2, 0, 2),(2, 0, -1), (-3, 0, -1), (-3, 2, -1),(-3, 2, 2 ), (-3, 0, 2 ),(-3, 2, 2), (2, 2, 2), (2,0,2), (2, 2, 2), (2,2,-1), (2,0,-1), (2,2,-1),(-3,2,-1) ], 
						k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 ],n=x+'ctrl')
		cmds.pickWalk(x+'ctrl',d='down')
		cmds.rename('curveShape1',x+'ctrlShape')
		cmds.makeIdentity(apply=True,t=1,r=1,s=1,n=0,pn=1)
		##colour
		if newName=='left':
			cmds.setAttr(x+"ctrlShape.overrideEnabled", 1)
			cmds.setAttr(x+"ctrlShape.overrideColor", 4)
		if newName=='right':
			cmds.setAttr(x+"ctrlShape.overrideEnabled", 1)
			cmds.setAttr(x+"ctrlShape.overrideColor", 6)
		
		cmds.parent(x+'ctrlShape', y,r=True,s=True)
		cmds.xform(x+'ctrlShape.cv[0:15]', s=(6,6,8) )
		cmds.xform( x+'ctrlShape.cv[0:4]', x+'ctrlShape.cv[7]', x+'ctrlShape.cv[10]', x+'ctrlShape.cv[13]',r=True,t=(0, -10, 0))
	
	
	#for the feet one only
	cmds.curve(d=1, p=[(-3, 0, -1),(-3, 0, 2),(2, 0, 2),(2, 0, -1), (-3, 0, -1), (-3, 2, -1),(-3, 2, 2 ), (-3, 0, 2 ),(-3, 2, 2), (2, 2, 2), (2,0,2), (2, 2, 2), (2,2,-1), (2,0,-1), (2,2,-1),(-3,2,-1) ], 
						k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 ],n=newName+'_feet_start_jnt_FK'+'ctrl')
	cmds.pickWalk(newName+'_feet_start_jnt_FKctrl',d='down')
	cmds.rename('curveShape1',newName+'_feet_start_jnt_FK'+'ctrlShape')
	cmds.makeIdentity(newName+'_feet_start_jnt_FK',apply=True,t=1,r=1,s=1,n=0,pn=1)
	###colour
	giveColour(newName,'_feet_start_jnt_FK') 
		
	cmds.parent(newName+'_feet_start_jnt_FKctrlShape', newName+'_feet_start_jnt_FK',r=True,s=True)
	cmds.xform(newName+'_feet_start_jnt_FKctrlShape.cv[0:15]', s=(6,6,8) )
	cmds.xform(newName+'_feet_start_jnt_FKctrlShape.cv[0:4]', newName+'_feet_start_jnt_FKctrlShape.cv[7]', newName+'_feet_start_jnt_FKctrlShape.cv[10]', newName+'_feet_start_jnt_FKctrlShape.cv[13]',r=True,t=(0, -10, 0))
	cmds.delete(newName+'_start_leg_jntctrl', newName+'_mid_leg_jntctrl', newName+'_end_leg_jntctrl', newName+'_feet_start_jnt_FKctrl')	
	
	for i in range(0, len(leftLegFK)):
		cmds.setAttr(legFK[i]+".rotateOrder", 3) 
		cmds.setAttr(legIK[i]+".rotateOrder", 3) 
		cmds.setAttr(LegJnts[i]+".rotateOrder", 3)
	cmds.setAttr(feetFK[0]+".rotateOrder", 3)
	cmds.setAttr(feetIK[0]+".rotateOrder", 3)
	cmds.setAttr(fJnts[0]+".rotateOrder", 3)


	 ###for a proxy rig! 
	#fk stretch translateX
	cmds.addAttr(newName+'_start_leg_jnt_FK',ln="length", at='double', min=0,  dv=1 )
	cmds.setAttr(newName+'_start_leg_jnt_FK.length',e=True,keyable=True)
	
	cmds.setDrivenKeyframe(newName+'_mid_leg_jnt_FK.translateX',cd=newName+'_start_leg_jnt_FK.length')
	cmds.setAttr(newName+"_start_leg_jnt_FK.length",0)
	cmds.setAttr(newName+"_mid_leg_jnt_FK.translateX", 0)
	cmds.setDrivenKeyframe(newName+'_mid_leg_jnt_FK.translateX',cd=newName+'_start_leg_jnt_FK.length')
	
	cmds.keyTangent(newName+'_mid_leg_jnt_FK',e=True,itt='spline',ott='spline', animation='objects')
	cmds.selectKey( newName+'_mid_leg_jnt_FK_translateX', add=True, k=True)
	cmds.setInfinity(poi='linear')
	
	#add length attr for stretching the leg.2
	cmds.addAttr(newName+'_mid_leg_jnt_FK',ln="length", at='double', min=0,  dv=1 )
	cmds.setAttr( newName+'_mid_leg_jnt_FK.length',e=True,keyable=True)
	
	cmds.setDrivenKeyframe(newName+'_end_leg_jnt_FK.translateX',cd=newName+'_mid_leg_jnt_FK.length')
	cmds.setAttr(newName+"_mid_leg_jnt_FK.length",0)
	cmds.setAttr(newName+"_end_leg_jnt_FK.translateX", 0)
	cmds.setDrivenKeyframe(newName+'_end_leg_jnt_FK.translateX',cd=newName+'_mid_leg_jnt_FK.length')
	
	cmds.keyTangent(newName+'_end_leg_jnt_FK',e=True,itt='spline',ott='spline', animation='objects')
	cmds.selectKey( newName+'_end_leg_jnt_FK_translateX', add=True, k=True)
	cmds.setInfinity(poi='linear')
	
	cmds.setAttr(newName+"_start_leg_jnt_FK.length",1)
	cmds.setAttr(newName+"_mid_leg_jnt_FK.length", 1)
	
	#for ik handles
	cmds.setAttr(newName+"_Leg_settingsCTRL.FK_IK_blend", 1)
	cmds.ikHandle(n=newName+'Foot_hdl',sj=legIK[0],
					ee=legIK[2],sol='ikRPsolver')
	cmds.rename('effector1', newName+'Leg_Eff')
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n=newName+'Foot_Ctrl')
	cmds.setAttr(newName+'Foot_Ctrl.translate', anklePos[0],0,anklePos[2])
	
	if newName=='left': #for left red
		cmds.setAttr(newName+"Foot_Ctrl.overrideEnabled", 1)
		cmds.setAttr(newName+"Foot_Ctrl.overrideColor", 4)
	if newName=='right': #for right blue
		cmds.setAttr(newName+"Foot_Ctrl.overrideEnabled", 1)
		cmds.setAttr(newName+"Foot_Ctrl.overrideColor", 6)
	
	cmds.xform(newName+'Foot_Ctrl.cv[4:6]',t=(0 ,0 ,1), r=True) 
	cmds.xform(newName+'Foot_Ctrl.cv[0:7]',s=(10 ,10 ,25), r=True) 
	cmds.xform(newName+'Foot_CtrlShape.cv[3]',newName+'Foot_CtrlShape.cv[7]',t=(0, 0, 1),r=True)
	cmds.move(anklePos[0], anklePos[1], anklePos[2] ,newName+'Foot_Ctrl.scalePivot', newName+'Foot_Ctrl.rotatePivot' ,rpr=True)
	
	cmds.makeIdentity(newName+'Foot_Ctrl',apply=True, t=1 ,r=1 ,s=1, n=0 ,pn=1)
	cmds.setAttr(newName+"Foot_Ctrl.rotateOrder", 2)
	cmds.parent(newName+'Foot_hdl', newName+'Foot_Ctrl')
	
	cmds.ikHandle(n=newName+'Ball_hdl',sj=newName+'_end_leg_jnt_IK',ee=newName+'_feet_start_jnt_IK',sol='ikRPsolver')
	cmds.rename('effector1', newName+'_Ball_Eff')
	cmds.ikHandle(n=newName+'Toe_hdl',sj=newName+'_feet_start_jnt_IK',ee=newName+'_feet_end_jnt_IK',sol='ikRPsolver')
	cmds.parent(newName+'Ball_hdl',newName+'Toe_hdl', newName+'Foot_Ctrl')
	cmds.rename('effector1', newName+'_Toe_Eff')
	
	cmds.parent(newName+'_end_leg',newName+'Foot_Ctrl')
	
	#cleanup and visibility
	cmds.addAttr('|'+newName+'_settings_GRP|'+newName+'_Leg_settingsCTRL',ln="FK_visibility",at='bool')
	cmds.setAttr('|'+newName+'_settings_GRP|'+newName+'_Leg_settingsCTRL.FK_visibility',e=True,keyable=True)
	cmds.addAttr('|'+newName+'_settings_GRP|'+newName+'_Leg_settingsCTRL',ln="IK_visibility", at='bool')
	cmds.setAttr('|'+newName+'_settings_GRP|'+newName+'_Leg_settingsCTRL.IK_visibility',e=True,keyable=True)
	cmds.addAttr('|'+newName+'_settings_GRP|'+newName+'_Leg_settingsCTRL',ln="Knee_visibility",at='bool')
	cmds.setAttr('|'+newName+'_settings_GRP|'+newName+'_Leg_settingsCTRL.Knee_visibility',e=True,keyable=True)
	
	#fk ON
	cmds.setAttr(newName+"_Leg_settingsCTRL.FK_IK_blend",0)
	cmds.setAttr(newName+"_Leg_settingsCTRL.FK_visibility",1)
	cmds.setAttr(newName+"_Leg_settingsCTRL.IK_visibility",0)
	cmds.setAttr(newName+"_start_leg_jnt_IK.visibility",0)
	cmds.setDrivenKeyframe(newName+'_Leg_settingsCTRL.FK_visibility', currentDriver=newName+'_Leg_settingsCTRL.FK_IK_blend')
	cmds.setDrivenKeyframe(newName+'_Leg_settingsCTRL.IK_visibility', currentDriver=newName+'_Leg_settingsCTRL.FK_IK_blend')
	cmds.setDrivenKeyframe(newName+'_Leg_settingsCTRL.IK_visibility', currentDriver=newName+'_Leg_settingsCTRL.FK_IK_blend')
	#cmds.setDrivenKeyframe(newName+'_Leg_settingsCTRL.IK_visibility', currentDriver=newName+'_Leg_settingsCTRL.FK_IK_blend')
	
	#ik ON
	cmds.setAttr(newName+"_Leg_settingsCTRL.FK_IK_blend",1)
	cmds.setAttr(newName+"_Leg_settingsCTRL.FK_visibility",0)
	cmds.setAttr(newName+"_Leg_settingsCTRL.IK_visibility",1)
	cmds.setDrivenKeyframe(newName+'_Leg_settingsCTRL.IK_visibility',currentDriver=newName+'_Leg_settingsCTRL.FK_IK_blend')
	cmds.setDrivenKeyframe(newName+'_Leg_settingsCTRL.FK_visibility',currentDriver=newName+'_Leg_settingsCTRL.FK_IK_blend')
	
	#for squash and stretch measure tool
	cmds.distanceDimension(sp=(cmds.getAttr(newName+'_start_leg.translateX'),cmds.getAttr(newName+'_start_leg.translateY'),cmds.getAttr(newName+'_start_leg.translateZ'))
							,ep=(cmds.getAttr(newName+'_end_leg.translateX'),cmds.getAttr(newName+'_end_leg.translateY'),cmds.getAttr(newName+'_end_leg.translateZ')))
	cmds.rename('distanceDimension1', newName+'Foot_IK_length' )
	if(newName=='right'):
		driver="rightFoot_IK_lengthShape.distance"
		rightThighLength=cmds.getAttr('right_mid_leg_jnt_IK.translateX')
		rightShinLength=cmds.getAttr('right_end_leg_jnt_IK.translateX')
		sumLengthR= rightThighLength+rightShinLength
		cmds.setDrivenKeyframe('right_mid_leg_jnt_IK', cd=driver,dv=sumLengthR, at='translateX', v=rightThighLength)
		cmds.setDrivenKeyframe('right_mid_leg_jnt_IK', cd=driver,dv=sumLengthR*2, at='translateX', v=rightThighLength*2)
		cmds.setDrivenKeyframe('right_end_leg_jnt_IK', cd=driver,dv=sumLengthR, at='translateX', v=rightShinLength)
		cmds.setDrivenKeyframe('right_end_leg_jnt_IK', cd=driver,dv=sumLengthR*2, at='translateX', v=rightShinLength*2)
		
		cmds.keyTangent('right_mid_leg_jnt_IK',e=True,itt='spline',ott='spline', animation='objects')
		mel.eval('selectKey -add -k -f 124.397377 right_mid_leg_jnt_IK_translateX ;')
		cmds.setInfinity(poi='linear')
		
		cmds.keyTangent('right_end_leg_jnt_IK',e=True,itt='spline',ott='spline', animation='objects')
		mel.eval('selectKey -add -k -f 124.397377 right_end_leg_jnt_IK_translateX ;')
		cmds.setInfinity(poi='linear')
	
	if(newName=='left'):
		#expression 
		driver="leftFoot_IK_lengthShape.distance"
		leftThighLength=cmds.getAttr('left_mid_leg_jnt_IK.translateX')
		leftShinLength=cmds.getAttr('left_end_leg_jnt_IK.translateX')
		sumLengthL= leftThighLength+leftShinLength
		cmds.setDrivenKeyframe('left_mid_leg_jnt_IK', cd=driver,dv=sumLengthL, at='translateX', v=leftThighLength)
		cmds.setDrivenKeyframe('left_mid_leg_jnt_IK', cd=driver,dv=sumLengthL*2, at='translateX', v=leftThighLength*2)
		cmds.setDrivenKeyframe('left_end_leg_jnt_IK', cd=driver,dv=sumLengthL, at='translateX', v=leftShinLength)
		cmds.setDrivenKeyframe('left_end_leg_jnt_IK', cd=driver,dv=sumLengthL*2, at='translateX', v=leftShinLength*2)
		
		cmds.keyTangent('left_mid_leg_jnt_IK',e=True,itt='spline',ott='spline', animation='objects')
		mel.eval('selectKey -add -k -f 124.397377 left_mid_leg_jnt_IK_translateX ;')
		cmds.setInfinity(poi='linear')
		
		cmds.keyTangent('left_end_leg_jnt_IK',e=True,itt='spline',ott='spline', animation='objects')
		mel.eval('selectKey -add -k -f 124.397377 left_end_leg_jnt_IK_translateX ;')
		cmds.setInfinity(poi='linear')
		
	#knee ctrl
	cmds.spaceLocator(n=newName+'Knee_ctrl',p=(PosKnee[0], PosKnee[1], PosKnee[2]+20))
	cmds.makeIdentity(newName+'Knee_ctrl',apply=True,t=1,r=1,s=0,n=0,pn=1)
	cmds.xform(newName+'Knee_ctrl', cp=1)
	cmds.poleVectorConstraint(newName+'Knee_ctrl',newName+'Foot_hdl' )
	
	cmds.setAttr(newName+"Foot_IK_length.visibility",0)
	
	if(newName=='left'):
		cmds.setAttr("leftKnee_ctrl.translate",1000.108,-76.577,-31.439)
		cmds.setAttr("leftFoot_hdl.twist", 90)
	if(newName=='right'):
		cmds.setAttr("rightKnee_ctrl.translate",-1000.108,-76.577,-31.439)
		cmds.setAttr("rightFoot_hdl.twist", 270)
	
	cmds.parent(newName+'Knee_ctrl',newName+'Foot_Ctrl')
	cmds.group(newName+'Knee_ctrl',n=newName+'NoFlip_knee_GRP')
	if(newName=='left'):
		mel.eval('move -r -1000.216384 0 0 leftNoFlip_knee_GRP.scalePivot leftNoFlip_knee_GRP.rotatePivot')
	if(newName=='right'):
		mel.eval('move -r 1000.216384 0 0 rightNoFlip_knee_GRP.scalePivot rightNoFlip_knee_GRP.rotatePivot')
	
	cmds.addAttr('|'+newName+'Foot_Ctrl',ln="kneeTwist",at='double',dv=0)
	cmds.setAttr('|'+newName+'Foot_Ctrl.kneeTwist',e=True,keyable=True)
	cmds.connectAttr(newName+'Foot_Ctrl.kneeTwist', newName+'NoFlip_knee_GRP.rotateY',f=True)
	
	cmds.select(newName+'_start_leg_jnt_IK', newName+'_mid_leg_jnt_IK', newName+'_end_leg_jnt_IK',
				newName+'_feet_start_jnt_IK', newName+'_feet_end_jnt_IK', newName+'_Toe_Eff', newName+'Toe_hdl', newName+'Leg_Eff',
				newName+'Foot_Ctrl', newName+'Foot_hdl', newName+'Foot_hdl_poleVectorConstraint1', newName+'_Ball_Eff',
				newName+'Ball_hdl', newName+'Toe_hdl' ,newName+'_end_leg', newName+'NoFlip_knee_GRP',
				newName+'Knee_ctrl',r=True)
	
	noFlipDuplicated=cmds.duplicate(rr=True, un=True)
	cmds.select(clear=True)
	cmds.delete(newName+'Foot_Ctrl|'+newName+'Foot_hdl',newName+'Foot_Ctrl|'+newName+'_end_leg',newName+'Foot_Ctrl|'+newName+'NoFlip_knee_GRP')
	
###optimize
	cmds.rename(newName+'_start_leg_jnt_IK1',newName+'_start_NO_FLIP_leg_jnt_IK')
	cmds.rename(newName+'_start_NO_FLIP_leg_jnt_IK|'+newName+'_mid_leg_jnt_IK',newName+'_mid_NO_FLIP_leg_jnt_IK')
	cmds.rename(newName+'_start_NO_FLIP_leg_jnt_IK|'+newName+'_mid_NO_FLIP_leg_jnt_IK|'+newName+'_end_leg_jnt_IK',newName+'_end_NO_FLIP_leg_jnt_IK')
	cmds.rename(newName+'_start_NO_FLIP_leg_jnt_IK|'+newName+'_mid_NO_FLIP_leg_jnt_IK|'+newName+'_end_NO_FLIP_leg_jnt_IK|'+newName+'_feet_start_jnt_IK',newName+'_feet_start_NO_FLIP_leg_jnt_IK')
	cmds.rename(newName+'_start_NO_FLIP_leg_jnt_IK|'+newName+'_mid_NO_FLIP_leg_jnt_IK|'+newName+'_end_NO_FLIP_leg_jnt_IK|'+newName+'_feet_start_NO_FLIP_leg_jnt_IK|'+newName+'_feet_end_jnt_IK',newName+'_feet_end_NO_FLIP_leg_jnt_IK')
	cmds.rename(newName+'_start_NO_FLIP_leg_jnt_IK|'+newName+'_mid_NO_FLIP_leg_jnt_IK|'+newName+'_end_NO_FLIP_leg_jnt_IK|'+newName+'_feet_start_NO_FLIP_leg_jnt_IK|'+newName+'_Toe_Eff', newName+'_Toe_Eff_NO_FLIP')
	cmds.rename(newName+'_start_NO_FLIP_leg_jnt_IK|'+newName+'_mid_NO_FLIP_leg_jnt_IK|'+newName+'_end_NO_FLIP_leg_jnt_IK|'+newName+'_Ball_Eff', '_Ball_Eff_NO_FLIP')
	cmds.rename(newName+'Leg_Eff',newName+'Leg_Eff_NO_FLIP')
	cmds.rename(newName+'Foot_IK_length1',newName+'Foot_IK_length_NO_FLIP')
	cmds.rename(newName+'_start_leg1',newName+'_start_leg_NO_FLIP')
	cmds.rename(newName+'Foot_Ctrl1',newName+'Foot_Ctrl_NO_FLIP')
	cmds.rename(newName+'Foot_hdl',newName+'Foot_hdl_NO_FLIP')
	cmds.rename(newName+'Foot_hdl_poleVectorConstraint1',newName+'Foot_hdl_PVconst_NO_FLIP')
	cmds.rename(newName+'_end_leg',newName+'_end_leg_NO_FLIP')			
		
	cmds.parent(newName+'Foot_hdl_NO_FLIP',newName+'_end_leg_NO_FLIP',newName+'NoFlip_knee_GRP',newName+'Foot_Ctrl')

	cmds.delete(newName+'Foot_Ctrl_NO_FLIP',newName+'_feet_end_NO_FLIP_leg_jnt_IK',newName+'_feet_start_NO_FLIP_leg_jnt_IK')
	cmds.connectAttr(newName+'Foot_Ctrl.kneeTwist', newName+'NoFlip_knee_GRP.rotateY',f=True)
	
	cmds.select(newName+'_end_leg_NO_FLIP',newName+'NoFlip_knee_GRP',newName+'_start_NO_FLIP_leg_jnt_IK', newName+'_mid_NO_FLIP_leg_jnt_IK', newName+'_end_NO_FLIP_leg_jnt_IK',
				newName+'Leg_Eff_NO_FLIP', newName+'Foot_IK_length_NO_FLIP', newName+'_start_leg_NO_FLIP')
	cmds.duplicate(rr=True, un=True)
###optimize
	cmds.rename(newName+'_start_NO_FLIP_leg_jnt_IK1',newName+'_start_PV_leg_jnt_IK1')
	cmds.rename(newName+'_start_PV_leg_jnt_IK1|'+newName+'_mid_NO_FLIP_leg_jnt_IK',newName+'_mid_PV_leg_jnt_IK1')
	cmds.rename(newName+'_start_PV_leg_jnt_IK1|'+newName+'_mid_PV_leg_jnt_IK1|'+newName+'_end_NO_FLIP_leg_jnt_IK',newName+'_end_PV_leg_jnt_IK1')
	cmds.rename(newName+'_start_PV_leg_jnt_IK1|'+newName+'_mid_PV_leg_jnt_IK1|'+newName+'Leg_Eff_NO_FLIP',newName+'Leg_Eff_PV')
	cmds.rename(newName+'Foot_IK_length_NO_FLIP1', newName+'Foot_IK_length_PV')
	cmds.rename(newName+'Foot_Ctrl1|'+newName+'Foot_hdl_NO_FLIP', newName+'Foot_hdl_PV')
	cmds.rename(newName+'Foot_Ctrl1|'+newName+'Foot_hdl_PV|'+newName+'Foot_hdl_PVconst_NO_FLIP ', newName+'Foot_hdl_PVconst_PV')
	cmds.rename(newName+'Foot_Ctrl1|'+newName+'_end_leg_NO_FLIP ', newName+'_end_leg_PV')
	cmds.rename(newName+'Foot_Ctrl1|'+newName+'NoFlip_knee_GRP ', newName+'PV_knee_GRP')
	cmds.rename(newName+'PV_knee_GRP|'+newName+'Knee_ctrl', newName+'Knee_pv')

	cmds.parent(newName+'Foot_hdl_PV',newName+'_end_leg_PV',newName+'PV_knee_GRP',newName+'Foot_Ctrl')
	
	cmds.delete(newName+'_start_leg_jnt_IK1',newName+'Foot_Ctrl1' )
	cmds.parent(newName+'Knee_pv',w=True)
	cmds.delete(newName+'PV_knee_GRP')
	
	cmds.setAttr(newName+"Foot_hdl_PV.twist",0)
	cmds.setAttr(newName+"Knee_pv.translateZ",0)
	cmds.setAttr(newName+"Knee_pv.translateX",0)
	cmds.setAttr(newName+"Knee_pv.translateY",0)

	###blend NODES for pv no_flip
	if(newName=='left'):
		three_IK_Leg=leftLegIK[:3]
	if(newName=='right'):
		three_IK_Leg=rightLegIK[:3]
	
	for item in three_IK_Leg:
		cmds.shadingNode('blendColors',au=True,n=item+'_rot_PV_NoFlip')
		choiceROTblendNodes.append(item+'_rot_PV_NoFlip')
		cmds.shadingNode('blendColors',au=True,n=item+'_tr_PV_NoFlip')
		choiceTRblendNodes.append(item+'_tr_PV_NoFlip')
	
	for x, y, z, z1, o in zip(side_NoFlip_Leg, side_PV_Leg, choiceROTblendNodes, choiceTRblendNodes, three_IK_Leg):
		cmds.connectAttr(x+'.rotate', z+'.color1', f=True)
		cmds.connectAttr(y+'.rotate', z+'.color2', f=True)
		cmds.connectAttr(z+'.output', o+'.rotate', f=True)
		cmds.connectAttr(x+'.translate', z1+'.color1', f=True)
		cmds.connectAttr(y+'.translate', z1+'.color2', f=True)
		cmds.connectAttr(z1+'.output', o+'.translate', f=True)
		
	cmds.addAttr(newName+'_Leg_settingsCTRL',ln="PV_blend_NO_FLIP", nn="PV_blend/No_Flip", at='double', min=0, max=1, dv=0 )
	cmds.setAttr(newName+'_Leg_settingsCTRL.PV_blend_NO_FLIP',e=True,keyable=True)	
	
	for item,item1 in zip(choiceROTblendNodes,choiceTRblendNodes):
			cmds.connectAttr(newName+'_Leg_settingsCTRL.PV_blend_NO_FLIP',item+'.blender',f=True)
			cmds.connectAttr(newName+'_Leg_settingsCTRL.PV_blend_NO_FLIP',item1+'.blender',f=True)
	cmds.setAttr(newName+'_start_leg_NO_FLIP.visibility',0)
	#snappable knee
	cmds.setAttr(newName+"_Leg_settingsCTRL.PV_blend_NO_FLIP",1)
	mel.eval('curve -d 1 -p -3 0 0 -p 3 0 0 -p 0 0 5 -p -3 0 0 -k 0 -k 1 -k 2 -k 3 ;')
	cmds.rename('curve1', newName+'_knee_ctrl')
	cmds.setAttr(newName+'_knee_ctrl.scale', 2,2,2)
	giveColour(newName,'_knee_ctrl') 
	###
	cmds.setAttr(newName+'_knee_ctrl.translateX',cmds.getAttr(newName+'Knee_pv.localPositionX'))
	cmds.setAttr(newName+'_knee_ctrl.translateY',cmds.getAttr(newName+'Knee_pv.localPositionY'))
	cmds.setAttr(newName+'_knee_ctrl.translateZ',cmds.getAttr(newName+'Knee_pv.localPositionZ'))
	mel.eval('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;')
	cmds.parent(newName+'Knee_pv',newName+'_knee_ctrl')
	#create random distanceDimension as we need new locators
	
	mel.eval('distanceDimension -sp 12 137 21 -ep 12 88 33 ;')
	cmds.rename('locator1',newName+'_thigh_toKnee_start_loc')
	cmds.rename('locator2',newName+'_thigh_toKnee_end_loc')
	cmds.setAttr(newName+'_thigh_toKnee_start_loc.translate',hipPos[0],hipPos[1],hipPos[2])
	cmds.setAttr(newName+'_thigh_toKnee_end_loc.translate',PosKnee[0],PosKnee[1],PosKnee[2]+20)
	
	mel.eval('distanceDimension -sp 12.108383 85.415562 18.40254 -ep 12.108383 8.333226 2.893481 ;')
	cmds.rename('locator1',newName+'_kneeToFoot_start_loc')
	cmds.rename('locator2',newName+'_kneeToFoot_end_loc')
	cmds.setAttr(newName+'_kneeToFoot_start_loc.translate',PosKnee[0],PosKnee[1],PosKnee[2]+20)
	cmds.setAttr(newName+'_kneeToFoot_end_loc.translate',anklePos[0],anklePos[1],anklePos[2])
	
	cmds.parent(newName+'_thigh_toKnee_end_loc',newName+'_kneeToFoot_start_loc',newName+'_knee_ctrl' )
	cmds.parent(newName+'_kneeToFoot_end_loc',newName+'Foot_Ctrl') 
	
	cmds.rename('distanceDimension1', newName+'ThighToKnee_dist')
	cmds.rename('distanceDimension2', newName+'KneeToFoot_dist')
	
	#side_PV_Leg
	cmds.shadingNode('blendColors',au=True,n=newName+'ThighPV_stretch_Choice')
	cmds.connectAttr(newName+'ThighToKnee_distShape.distance', newName+'ThighPV_stretch_Choice.color1R',f=True)
	cmds.connectAttr(newName+'_mid_leg_jnt_IK_translateX2.output', newName+'ThighPV_stretch_Choice.color2R', f=True)
	cmds.disconnectAttr(newName+'_mid_leg_jnt_IK_translateX2.output', newName+'_mid_PV_leg_jnt_IK1.translateX')
	cmds.connectAttr(newName+'ThighPV_stretch_Choice.outputR', newName+'_mid_PV_leg_jnt_IK1.translateX',f=True)

	cmds.shadingNode('blendColors',au=True,n=newName+'ShinPV_stretch_Choice')
	cmds.connectAttr(newName+'KneeToFoot_distShape.distance', newName+'ShinPV_stretch_Choice.color1R',f=True)
	cmds.connectAttr(newName+'_end_leg_jnt_IK_translateX2.output',newName+'ShinPV_stretch_Choice.color2R',f=True)
	cmds.disconnectAttr(newName+'_end_leg_jnt_IK_translateX2.output', newName+'_end_PV_leg_jnt_IK1.translateX')
	cmds.connectAttr(newName+'ShinPV_stretch_Choice.outputR', newName+'_end_PV_leg_jnt_IK1.translateX',f=True)

	cmds.addAttr('|'+newName+'_knee_ctrl',ln="Knee_snap",at='double',min=0,max=1,dv=0)
	cmds.setAttr('|'+newName+'_knee_ctrl.Knee_snap',e=True,keyable=True)
		
	cmds.connectAttr(newName+'_knee_ctrl.Knee_snap', newName+'ShinPV_stretch_Choice.blender',f=True)
	cmds.connectAttr(newName+'_knee_ctrl.Knee_snap', newName+'ThighPV_stretch_Choice.blender',f=True)
 
	cmds.connectAttr(newName+'_Leg_settingsCTRL.FK_visibility', newName+'_start_leg_jnt_FK.visibility',f=True)
	cmds.connectAttr(newName+'_Leg_settingsCTRL.IK_visibility', newName+'Foot_Ctrl.visibility',f=True)
	cmds.connectAttr(newName+'_Leg_settingsCTRL.Knee_visibility', newName+'_knee_ctrl.visibility',f=True)

	
	##
	cmds.setAttr(newName+"ThighToKnee_dist.visibility",0)
	cmds.setAttr(newName+"KneeToFoot_dist.visibility",0)
	
	cmds.group(newName+'_start_leg_jnt',newName+'_start_leg_jnt_FK',newName+'_start_leg_jnt_IK',
				newName+'Foot_Ctrl',newName+'_start_NO_FLIP_leg_jnt_IK',newName+'_start_leg_NO_FLIP',
				newName+'_start_leg_NO_FLIP',newName+'_start_PV_leg_jnt_IK1',newName+'Foot_IK_length_PV',
				newName+'_start_leg_NO_FLIP1',newName+'_knee_ctrl',newName+'_thigh_toKnee_start_loc',
				newName+'ThighToKnee_dist', newName+'KneeToFoot_dist', n=newName+'Leg_grp')
	
	cmds.parent(newName+'Leg_grp', 'pirate_Root_Transform')

	cmds.group(newName+'_start_leg_jnt_IK',newName+'_start_NO_FLIP_leg_jnt_IK',newName+'_start_PV_leg_jnt_IK1',
			newName+'_thigh_toKnee_start_loc',newName+'KneeToFoot_dist',newName+'ThighToKnee_dist',
			newName+'_start_leg_NO_FLIP1',newName+'Foot_IK_length_PV',newName+'_start_leg_jnt',
			newName+'_start_leg_NO_FLIP', n='DO_NOT_TOUCH_GRP')
	
	cmds.group(newName+'_start_leg_jnt_IK',newName+'_start_NO_FLIP_leg_jnt_IK', newName+'_start_PV_leg_jnt_IK1',
			newName+'_thigh_toKnee_start_loc', newName+'_start_leg_NO_FLIP1',newName+'_start_leg_NO_FLIP', n=newName+'Leg_IK_Const_GRP')
	cmds.group(newName+'_start_leg_jnt',n=newName+'Leg_result_Const_GRP')
	
	#optimize for loop attatching the legs
	cmds.move(hipPos[0],hipPos[1],hipPos[2],newName+'Leg_result_Const_GRP.scalePivot', newName+'Leg_result_Const_GRP.rotatePivot',rpr=True)
	cmds.move(hipPos[0],hipPos[1],hipPos[2],newName+'Leg_IK_Const_GRP.scalePivot', newName+'Leg_IK_Const_GRP.rotatePivot',rpr=True)
	cmds.spaceLocator(n=newName+'_Hip_space_LOC',p=(hipPos[0], hipPos[1], hipPos[2]))
	cmds.parent(newName+'_Hip_space_LOC', 'hip_bind_jnt')
	cmds.xform(newName+'_Hip_space_LOC', cp=1)
	cmds.pointConstraint(newName+'_Hip_space_LOC',newName+'Leg_IK_Const_GRP',mo=True, weight=1)
	cmds.pointConstraint(newName+'_Hip_space_LOC',newName+'Leg_result_Const_GRP',mo=True ,weight=1)
	
	cmds.group(newName+'_start_leg_jnt_FK', n=newName+'Leg_FK_Const_GRP')
	cmds.move(hipPos[0],hipPos[1],hipPos[2],newName+'Leg_FK_Const_GRP.scalePivot', newName+'Leg_FK_Const_GRP.rotatePivot',rpr=True)
	cmds.pointConstraint(newName+'_Hip_space_LOC',newName+'Leg_FK_Const_GRP',mo=True ,weight=1)
	cmds.duplicate(newName+'_Hip_space_LOC',n=newName+'_Body_space_LOC')
	cmds.duplicate(newName+'_Body_space_LOC',n=newName+'_Root_space_LOC')
	
	cmds.parent(newName+'_Root_space_LOC', 'pirate_Root_Transform')
	cmds.parent(newName+'_Body_space_LOC', 'DO_NOT_TOUCH')
	cmds.orientConstraint(newName+'_Hip_space_LOC', newName+'_Body_space_LOC',newName+'_Root_space_LOC', newName+'Leg_FK_Const_GRP',w=1)
	cmds.orientConstraint(newName+'_Hip_space_LOC', newName+'_Body_space_LOC',newName+'_Root_space_LOC', newName+'Leg_result_Const_GRP',w=1)
	
	cmds.addAttr('|'+newName+'_settings_GRP|'+newName+'_Leg_settingsCTRL', ln="Fk_rotationSpace",at="enum",en="hip:upperBody:root:")
	cmds.setAttr('|'+newName+'_settings_GRP|'+newName+'_Leg_settingsCTRL.Fk_rotationSpace' ,e=True,keyable=True)
	
	#ik scale for the root transform
	cmds.parent(newName+'Foot_IK_length_NO_FLIP', newName+'Leg_grp|DO_NOT_TOUCH_GRP')
	cmds.shadingNode('multiplyDivide',au=True ,n='globalScale'+newName+'Leg_noFlipNormDiv')
	cmds.shadingNode('multiplyDivide', au=True, n='globalScale'+newName+'Leg_pvNormDiv')
	cmds.connectAttr(newName+'KneeToFoot_distShape.distance','globalScale'+newName+'Leg_noFlipNormDiv.input1X')
	cmds.connectAttr(newName+'ThighToKnee_distShape.distance','globalScale'+newName+'Leg_pvNormDiv.input1X')
	cmds.connectAttr('pirate_Root_Transform.scaleY','globalScale'+newName+'Leg_noFlipNormDiv.input2X')
	cmds.connectAttr('pirate_Root_Transform.scaleY','globalScale'+newName+'Leg_pvNormDiv.input2X')
	cmds.setAttr("globalScale"+newName+"Leg_noFlipNormDiv.operation", 2)
	cmds.setAttr("globalScale"+newName+"Leg_pvNormDiv.operation", 2)
	cmds.connectAttr('globalScale'+newName+'Leg_noFlipNormDiv.outputX', newName+'_mid_leg_jnt_IK_translateX1.input',f=True)
	cmds.connectAttr('globalScale'+newName+'Leg_noFlipNormDiv.outputX', newName+'_end_leg_jnt_IK_translateX1.input', f=True)
	cmds.connectAttr('globalScale'+newName+'Leg_pvNormDiv.outputX', newName+'_mid_leg_jnt_IK_translateX2.input', f=True)
	cmds.connectAttr('globalScale'+newName+'Leg_pvNormDiv.outputX', newName+'_end_leg_jnt_IK_translateX2.input', f=True)

	##for the knee snap jnts
	cmds.shadingNode('multiplyDivide',au=True ,n='globalScale'+newName+'Knee_toFoot_NormDiv')
	cmds.shadingNode('multiplyDivide', au=True, n='globalScale'+newName+'Thigh_toKnee_NormDiv')
	cmds.connectAttr(newName+'KneeToFoot_distShape.distance','globalScale'+newName+'Knee_toFoot_NormDiv.input1X')
	cmds.connectAttr(newName+'ThighToKnee_distShape.distance','globalScale'+newName+'Thigh_toKnee_NormDiv.input1X')
	cmds.connectAttr('pirate_Root_Transform.scaleY','globalScale'+newName+'Knee_toFoot_NormDiv.input2X')
	cmds.connectAttr('pirate_Root_Transform.scaleY','globalScale'+newName+'Thigh_toKnee_NormDiv.input2X')
	cmds.setAttr("globalScale"+newName+"Knee_toFoot_NormDiv.operation", 2)
	cmds.setAttr("globalScale"+newName+"Thigh_toKnee_NormDiv.operation", 2)
	cmds.connectAttr('globalScale'+newName+'Knee_toFoot_NormDiv.outputX', newName+'ShinPV_stretch_Choice.color1R',f=True)
	cmds.connectAttr('globalScale'+newName+'Thigh_toKnee_NormDiv.outputX', newName+'ThighPV_stretch_Choice.color1R',f=True)
	
	#when no flip hide the pv joints
	cmds.setAttr(newName+'_Leg_settingsCTRL.PV_blend_NO_FLIP',1) 
	cmds.setAttr(newName+'_start_PV_leg_jnt_IK1.visibility',0) 
	cmds.setAttr(newName+'_Leg_settingsCTRL.Knee_visibility', 0)
	cmds.setDrivenKeyframe(newName+'_start_PV_leg_jnt_IK1.visibility', cd=newName+'_Leg_settingsCTRL.PV_blend_NO_FLIP')
	cmds.setDrivenKeyframe(newName+'_Leg_settingsCTRL.Knee_visibility', cd=newName+'_Leg_settingsCTRL.PV_blend_NO_FLIP')
	
	#and the opposite with the knee ctrl shown
	cmds.setAttr(newName+'_Leg_settingsCTRL.PV_blend_NO_FLIP',0) 
	cmds.setAttr(newName+'_start_NO_FLIP_leg_jnt_IK.visibility',0) 
	cmds.setDrivenKeyframe(newName+'_start_PV_leg_jnt_IK1.visibility', cd=newName+'_Leg_settingsCTRL.PV_blend_NO_FLIP')
	cmds.setAttr(newName+'_Leg_settingsCTRL.Knee_visibility', 1)
	cmds.setDrivenKeyframe(newName+'_Leg_settingsCTRL.Knee_visibility', cd=newName+'_Leg_settingsCTRL.PV_blend_NO_FLIP')
	
	
	#reverse foot ctrl
	cmds.spaceLocator(n=newName+'toe_loc',p=cmds.xform(feetFK[1],q=True, ws=True, t=True))
	cmds.xform(newName+'toe_loc',cp=1)
	cmds.spaceLocator(n=newName+'ball_loc',p=cmds.xform(feetFK[0],q=True, ws=True, t=True))
	cmds.xform(newName+'ball_loc',cp=1)
	cmds.spaceLocator(n=newName+'heel_loc',p=cmds.xform(legFK[2],q=True, ws=True, t=True))
	if newName=='left':
		cmds.xform(newName+'heel_loc',cp=1, t=(-1,-11.714,-9.5))
	else:
		cmds.xform(newName+'heel_loc',cp=1, t=(1,-11.714,-9.5))
	cmds.makeIdentity(newName+'heel_loc',apply=True,t=1,r=1,s=1,n=0,pn=1)
	cmds.parent(newName+'toe_loc', newName+'ball_loc', newName+'heel_loc', newName+'Foot_Ctrl')
	cmds.parent(newName+'Ball_hdl', newName+'Toe_hdl', newName+'Foot_hdl_NO_FLIP', newName+'Foot_hdl_PV',
				newName+'toe_loc', newName+'ball_loc', newName+'heel_loc')
	
	cmds.parent(newName+'Ball_hdl',newName+'Foot_hdl_NO_FLIP', newName+'Foot_hdl_PV',newName+'ball_loc')
	cmds.parent(newName+'ball_loc',newName+'toe_loc')
	cmds.parent(newName+'NoFlip_knee_GRP',newName+'_end_leg_NO_FLIP', newName+'_end_leg_PV', newName+'_kneeToFoot_end_loc',newName+'ball_loc')
	
	###custom attr for the walk cycle
	walkAttr=['roll','bendLimitAngle','toeStraightAngle']
	angle=[0,45,70]
	for i,k in zip(walkAttr,angle):
		cmds.addAttr('|pirate_Root_Transform|'+newName+'Leg_grp|'+newName+'Foot_Ctrl', ln=i, at='double', dv=k)
		cmds.setAttr('|pirate_Root_Transform|'+newName+'Leg_grp|'+newName+'Foot_Ctrl.'+i, e=True,keyable=True)

	cmds.shadingNode('clamp', au=True,n=newName+'heel_rot_clamp')
	cmds.connectAttr(newName+'Foot_Ctrl.roll', newName+'heel_rot_clamp.input.inputR.', f=True)
	cmds.setAttr(newName+'heel_rot_clamp.minR', -90)
	cmds.connectAttr(newName+'heel_rot_clamp.outputR', newName+'heel_loc.rotateX', f=True)
	
	cmds.shadingNode('clamp', au=True,n=newName+'ball_ZeroToBend_clamp')
	cmds.connectAttr(newName+'Foot_Ctrl.roll', newName+'ball_ZeroToBend_clamp.input.inputR.', f=True)

	cmds.connectAttr(newName+'Foot_Ctrl.bendLimitAngle', newName+'ball_ZeroToBend_clamp.maxR', f=True)
	cmds.shadingNode('setRange', au=True,n=newName+'ball_ZeroToBend_Percent')
	cmds.connectAttr(newName+'ball_ZeroToBend_clamp.min.minR', newName+'ball_ZeroToBend_Percent.oldMin.oldMinX.', f=True)
	cmds.connectAttr(newName+'ball_ZeroToBend_clamp.max.maxR', newName+'ball_ZeroToBend_Percent.oldMax.oldMaxX.', f=True)
	cmds.setAttr( newName+'ball_ZeroToBend_Percent.maxX',1)
	cmds.connectAttr(newName+'ball_ZeroToBend_clamp.input.inputR', newName+'ball_ZeroToBend_Percent.value.valueX.', f=True)
	cmds.shadingNode('plusMinusAverage', au=True,n=newName+'foot_Invert_Percentage')
	cmds.setAttr(newName+'foot_Invert_Percentage.input1D[0]', 1)
	cmds.setAttr(newName+'foot_Invert_Percentage.input1D[1]', 1)
	##fixed
	cmds.shadingNode('clamp', au=True,n=newName+'foot_bend_StraightClamp')
	cmds.connectAttr(newName+'Foot_Ctrl.bendLimitAngle', newName+'foot_bend_StraightClamp.min.minR.', f=True)
	cmds.connectAttr(newName+'Foot_Ctrl.toeStraightAngle', newName+'foot_bend_StraightClamp.max.maxR.', f=True)
	cmds.connectAttr(newName+'Foot_Ctrl.roll', newName+'foot_bend_StraightClamp.input.inputR.', f=True)
	
	cmds.shadingNode('setRange', au=True,n=newName+'foot_bend_toStraightPercent')
	cmds.connectAttr(newName+'foot_bend_StraightClamp.min.minR', newName+'foot_bend_toStraightPercent.oldMin.oldMinX.', f=True)
	cmds.connectAttr(newName+'foot_bend_StraightClamp.max.maxR', newName+'foot_bend_toStraightPercent.oldMax.oldMaxX.', f=True)
	cmds.setAttr( newName+'foot_bend_toStraightPercent.maxX',1)
	cmds.connectAttr(newName+'foot_bend_StraightClamp.input.inputR', newName+'foot_bend_toStraightPercent.value.valueX.', f=True)
	
	cmds.shadingNode('multiplyDivide', au=True,n=newName+'foot_roll_mult')
	cmds.connectAttr(newName+'foot_bend_toStraightPercent.outValue.outValueX.',newName+'foot_roll_mult.input1.input1X',f=True)
	cmds.connectAttr(newName+'foot_bend_StraightClamp.inputR.',newName+'foot_roll_mult.input2X',f=True)
	cmds.connectAttr(newName+'foot_roll_mult.output.outputX.',newName+'toe_loc.rotate.rotateX',f=True)
	###over-rotation
	cmds.connectAttr(newName+'foot_bend_toStraightPercent.outValueX', newName+'foot_Invert_Percentage.input1D[1]', f=True)
	cmds.setAttr(newName+"foot_Invert_Percentage.operation", 2)
	cmds.shadingNode('multiplyDivide', au=True,n=newName+'ball_percent_mult')
	cmds.connectAttr(newName+'ball_ZeroToBend_Percent.outValueX',  newName+'ball_percent_mult.input1X', f=True)
	cmds.connectAttr(newName+'foot_Invert_Percentage.output1D', newName+'ball_percent_mult.input2X',f=True)
	cmds.shadingNode('multiplyDivide', au=True,n=newName+'ball_roll_mult')
	cmds.connectAttr( newName+'ball_percent_mult.outputX', newName+'ball_roll_mult.input1X', f=True)
	cmds.connectAttr(newName+'Foot_Ctrl.roll', newName+'ball_roll_mult.input2X', f=True)
	cmds.connectAttr(newName+'ball_roll_mult.outputX', newName+'ball_loc.rotateX', f=True)

	#set limit of the roll works for the left foot only
	#complementary foot controls
	if newName=='left':
		cmds.spaceLocator(n=newName+'inner_foot_loc',p=[23.611,3.29,24.699])
		cmds.xform(newName+'inner_foot_loc',cp=1)
		cmds.spaceLocator(n=newName+'outer_foot_loc',p=[5.752,0.807,25.009])
		cmds.xform(newName+'outer_foot_loc',cp=1)
	if newName=='right':
		cmds.spaceLocator(n=newName+'inner_foot_loc',p=[-23.611,3.29,24.699])
		cmds.xform(newName+'inner_foot_loc',cp=1)
		cmds.spaceLocator(n=newName+'outer_foot_loc',p=[-5.752,0.807,25.009])
		cmds.xform(newName+'outer_foot_loc',cp=1)

	cmds.parent(newName+'inner_foot_loc',newName+'outer_foot_loc')
	cmds.parent(newName+'outer_foot_loc',newName+'heel_loc')
	cmds.parent(newName+'Toe_hdl', newName+'toe_loc',newName+'inner_foot_loc')
	cmds.addAttr('|pirate_Root_Transform|'+newName+'Leg_grp|'+newName+'Foot_Ctrl', ln='tilt_in', at='double', dv=0,min=0,max=10)
	cmds.setAttr('|pirate_Root_Transform|'+newName+'Leg_grp|'+newName+'Foot_Ctrl.tilt_in', e=True,keyable=True)
	cmds.addAttr('|pirate_Root_Transform|'+newName+'Leg_grp|'+newName+'Foot_Ctrl', ln='tilt_out', at='double', dv=0,min=0,max=10)
	cmds.setAttr('|pirate_Root_Transform|'+newName+'Leg_grp|'+newName+'Foot_Ctrl.tilt_out', e=True,keyable=True)
	
	###check it
	if newName=="left":
		cmds.setDrivenKeyframe(newName+'inner_foot_loc.rotateZ', cd=newName+'Foot_Ctrl.tilt_out')
		cmds.setAttr(newName+"Foot_Ctrl.tilt_out", 10)
		cmds.setAttr(newName+"inner_foot_loc.rotateZ", -30)
		cmds.setDrivenKeyframe(newName+'inner_foot_loc.rotateZ', cd=newName+'Foot_Ctrl.tilt_out')
		cmds.setAttr(newName+"Foot_Ctrl.tilt_out", 0)
		
		
	if newName=="right":
		cmds.setDrivenKeyframe(newName+'inner_foot_loc.rotateZ', cd=newName+'Foot_Ctrl.tilt_out')
		cmds.setAttr(newName+"Foot_Ctrl.tilt_out", 10)
		cmds.setAttr(newName+"inner_foot_loc.rotateZ", 30)
		cmds.setDrivenKeyframe(newName+'inner_foot_loc.rotateZ', cd=newName+'Foot_Ctrl.tilt_out')
		cmds.setAttr(newName+"Foot_Ctrl.tilt_out", 0)
		

	
	### tilt in fix
	if newName=="right":
		cmds.setAttr(newName+'Foot_Ctrl.tilt_in',0)
		cmds.setDrivenKeyframe(newName+'outer_foot_loc.rotateZ', cd=newName+'Foot_Ctrl.tilt_in')
		cmds.setAttr(newName+'Foot_Ctrl.tilt_in',10)
		cmds.setAttr("rightouter_foot_loc.rotateZ", -30)
		cmds.setDrivenKeyframe(newName+'outer_foot_loc.rotateZ', cd=newName+'Foot_Ctrl.tilt_in')
		cmds.setAttr(newName+"Foot_Ctrl.tilt_in", 0)
	
	if newName=="left":
		###doesnt work
		cmds.setAttr("leftFoot_Ctrl.tilt_in", 0)
		cmds.setDrivenKeyframe('leftouter_foot_loc.rotateZ',cd='leftFoot_Ctrl.tilt_in')
		cmds.setAttr("leftouter_foot_loc.rotateZ",30)
		cmds.setAttr("leftFoot_Ctrl.tilt_in", 10)
		cmds.setDrivenKeyframe('leftouter_foot_loc.rotateZ',cd='leftFoot_Ctrl.tilt_in')
		cmds.setAttr("leftFoot_Ctrl.tilt_in", 0)
	
	
	###
	cmds.addAttr('|pirate_Root_Transform|'+newName+'Leg_grp|'+newName+'Foot_Ctrl', ln='lean', at='double', dv=0)
	cmds.setAttr('|pirate_Root_Transform|'+newName+'Leg_grp|'+newName+'Foot_Ctrl.lean', e=True,keyable=True)
	
	cmds.addAttr('|pirate_Root_Transform|'+newName+'Leg_grp|'+newName+'Foot_Ctrl', ln='toe_spin', at='double', dv=0)
	cmds.setAttr('|pirate_Root_Transform|'+newName+'Leg_grp|'+newName+'Foot_Ctrl.toe_spin', e=True,keyable=True)
	
	cmds.addAttr('|pirate_Root_Transform|'+newName+'Leg_grp|'+newName+'Foot_Ctrl', ln='toeWiggle', at='double', dv=0)
	cmds.setAttr('|pirate_Root_Transform|'+newName+'Leg_grp|'+newName+'Foot_Ctrl.toeWiggle', e=True,keyable=True)
	
	cmds.connectAttr(newName+'Foot_Ctrl.lean',newName+'ball_loc.rotate.rotateZ', )
	cmds.connectAttr(newName+'Foot_Ctrl.toe_spin',newName+'toe_loc.rotate.rotateY' )
	cmds.group(newName+'Toe_hdl', n=newName+'wiggle_grp')
		#cmds.move -rpr 12 4.00646e-006 33.473797 wiggle.scalePivot wiggle.rotatePivot ;
	#tomorrow last part legs

	###skin the legs 
	if(newName=='left'):
		cmds.setAttr(newName+"_Leg_settingsCTRL.PV_blend_NO_FLIP" ,1)
		cmds.setAttr(newName+'Foot_Ctrl.translateX',6)
		cmds.setAttr(newName+'Foot_Ctrl.rotateY',46)
	if(newName=='right'):
		cmds.setAttr(newName+"_Leg_settingsCTRL.PV_blend_NO_FLIP", 1)
		cmds.setAttr(newName+'Foot_Ctrl.translateX',-6)
		cmds.setAttr(newName+'Foot_Ctrl.rotateY',-46)
#skin when everything is created
	
	###set spaces OPTIMIZEE
	
	cmds.setAttr(newName+"_Leg_settingsCTRL.Fk_rotationSpace" ,0)
	
	cmds.setAttr(newName+"Leg_FK_Const_GRP_orientConstraint1."+newName+"_Hip_space_LOCW0",1)
	cmds.setAttr(newName+"Leg_result_Const_GRP_orientConstraint1."+newName+"_Hip_space_LOCW0", 1)
	cmds.setAttr(newName+"Leg_result_Const_GRP_orientConstraint1."+newName+"_Root_space_LOCW2",0)
	cmds.setAttr(newName+"Leg_result_Const_GRP_orientConstraint1."+newName+"_Body_space_LOCW1", 0)
	cmds.setAttr(newName+"Leg_FK_Const_GRP_orientConstraint1."+newName+"_Body_space_LOCW1", 0)
	cmds.setAttr(newName+"Leg_FK_Const_GRP_orientConstraint1."+newName+"_Root_space_LOCW2", 0)
	
	cmds.setDrivenKeyframe(newName+'Leg_FK_Const_GRP_orientConstraint1.'+newName+'_Hip_space_LOCW0',cd=newName+'_Leg_settingsCTRL.Fk_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Leg_FK_Const_GRP_orientConstraint1.'+newName+'_Body_space_LOCW1',cd=newName+'_Leg_settingsCTRL.Fk_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Leg_FK_Const_GRP_orientConstraint1.'+newName+'_Root_space_LOCW2', cd=newName+'_Leg_settingsCTRL.Fk_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Leg_result_Const_GRP_orientConstraint1.'+newName+'_Hip_space_LOCW0',cd=newName+'_Leg_settingsCTRL.Fk_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Leg_result_Const_GRP_orientConstraint1.'+newName+'_Body_space_LOCW1',cd=newName+'_Leg_settingsCTRL.Fk_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Leg_result_Const_GRP_orientConstraint1.'+newName+'_Root_space_LOCW2',cd=newName+'_Leg_settingsCTRL.Fk_rotationSpace')

	cmds.setAttr(newName+"_Leg_settingsCTRL.Fk_rotationSpace",1)
	
	cmds.setAttr(newName+"Leg_result_Const_GRP_orientConstraint1."+newName+"_Hip_space_LOCW0",0)
	cmds.setAttr(newName+"Leg_FK_Const_GRP_orientConstraint1."+newName+"_Hip_space_LOCW0",0)
	cmds.setAttr(newName+"Leg_result_Const_GRP_orientConstraint1."+newName+"_Body_space_LOCW1",1)
	cmds.setAttr(newName+"Leg_FK_Const_GRP_orientConstraint1."+newName+"_Body_space_LOCW1",1)
	cmds.setAttr(newName+"Leg_result_Const_GRP_orientConstraint1."+newName+"_Root_space_LOCW2",0)
	cmds.setAttr(newName+"Leg_FK_Const_GRP_orientConstraint1."+newName+"_Root_space_LOCW2", 0)
	
	cmds.setDrivenKeyframe(newName+'Leg_FK_Const_GRP_orientConstraint1.'+newName+'_Hip_space_LOCW0', cd=newName+'_Leg_settingsCTRL.Fk_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Leg_FK_Const_GRP_orientConstraint1.'+newName+'_Body_space_LOCW1',cd=newName+'_Leg_settingsCTRL.Fk_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Leg_FK_Const_GRP_orientConstraint1.'+newName+'_Root_space_LOCW2', cd=newName+'_Leg_settingsCTRL.Fk_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Leg_result_Const_GRP_orientConstraint1.'+newName+'_Hip_space_LOCW0',cd=newName+'_Leg_settingsCTRL.Fk_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Leg_result_Const_GRP_orientConstraint1.'+newName+'_Body_space_LOCW1',cd=newName+'_Leg_settingsCTRL.Fk_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Leg_result_Const_GRP_orientConstraint1.'+newName+'_Root_space_LOCW2',cd=newName+'_Leg_settingsCTRL.Fk_rotationSpace')

	
	cmds.setAttr(newName+"_Leg_settingsCTRL.Fk_rotationSpace", 2)
	cmds.setAttr(newName+"Leg_result_Const_GRP_orientConstraint1."+newName+"_Body_space_LOCW1",0)
	cmds.setAttr(newName+"Leg_FK_Const_GRP_orientConstraint1."+newName+"_Body_space_LOCW1",0)
	cmds.setAttr(newName+"Leg_result_Const_GRP_orientConstraint1."+newName+"_Root_space_LOCW2",1)
	cmds.setAttr(newName+"Leg_FK_Const_GRP_orientConstraint1."+newName+"_Root_space_LOCW2",1)
	cmds.setAttr(newName+"Leg_result_Const_GRP_orientConstraint1."+newName+"_Hip_space_LOCW0",0)
	cmds.setAttr(newName+"Leg_FK_Const_GRP_orientConstraint1."+newName+"_Hip_space_LOCW0",0)
	
	cmds.setDrivenKeyframe(newName+'Leg_FK_Const_GRP_orientConstraint1.'+newName+'_Hip_space_LOCW0', cd=newName+'_Leg_settingsCTRL.Fk_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Leg_FK_Const_GRP_orientConstraint1.'+newName+'_Body_space_LOCW1' ,cd=newName+'_Leg_settingsCTRL.Fk_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Leg_FK_Const_GRP_orientConstraint1.'+newName+'_Root_space_LOCW2', cd=newName+'_Leg_settingsCTRL.Fk_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Leg_result_Const_GRP_orientConstraint1.'+newName+'_Hip_space_LOCW0',cd=newName+'_Leg_settingsCTRL.Fk_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Leg_result_Const_GRP_orientConstraint1.'+newName+'_Body_space_LOCW1',cd=newName+'_Leg_settingsCTRL.Fk_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Leg_result_Const_GRP_orientConstraint1.'+newName+'_Root_space_LOCW2',cd=newName+'_Leg_settingsCTRL.Fk_rotationSpace')
	
	cmds.select(clear=True) 
	
	#match ik fk rotation hip space 
	cmds.shadingNode('blendColors',au=True,n=newName+'Leg_resultOrientChoice')
	cmds.connectAttr(newName+'Leg_result_Const_GRP_orientConstraint1.constraintRotate', newName+'Leg_resultOrientChoice.color2', f=True)
	cmds.setAttr(newName+'Leg_resultOrientChoice.color1R', 0)
	cmds.connectAttr(newName+'_Leg_settingsCTRL.FK_IK_blend', newName+'Leg_resultOrientChoice.blender', f=True)
	cmds.connectAttr(newName+'Leg_resultOrientChoice.output', newName+'Leg_result_Const_GRP.rotate', f=True)
	cmds.disconnectAttr(newName+'Leg_result_Const_GRP_orientConstraint1.constraintRotateX', newName+'Leg_result_Const_GRP.rotateX')
	cmds.disconnectAttr(newName+'Leg_result_Const_GRP_orientConstraint1.constraintRotateY', newName+'Leg_result_Const_GRP.rotateY')
	cmds.disconnectAttr(newName+'Leg_result_Const_GRP_orientConstraint1.constraintRotateZ', newName+'Leg_result_Const_GRP.rotateZ')

	#fixing error for the right connections of the start toe
	if newName=='right':
		cmds.connectAttr('right_feet_start_jnt_FK.rotate', 'right_feet_start_jntRightrot_IK_FK.color2',f=True)
		cmds.connectAttr('right_feet_start_jnt_IK.rotate', 'right_feet_start_jntRightrot_IK_FK.color1', f=True)
		
	cmds.connectAttr(newName+'Foot_Ctrl.toeWiggle', newName+'wiggle_grp.rotateX',f=True)

	'''
	if(newName=='right'):
		driver="rightFoot_IK_length_NO_FLIPShape.distance"
		rightThighLength=cmds.getAttr('right_mid_leg_jnt_IK.translateX')
		rightShinLength=cmds.getAttr('right_end_leg_jnt_IK.translateX')
		sumLengthR= rightThighLength+rightShinLength
		cmds.setDrivenKeyframe('right_mid_leg_jnt_IK', cd=driver,dv=sumLengthR, at='translateX', v=rightThighLength)
		cmds.setDrivenKeyframe('right_mid_leg_jnt_IK', cd=driver,dv=sumLengthR*2, at='translateX', v=rightThighLength*2)
		cmds.setDrivenKeyframe('right_end_leg_jnt_IK', cd=driver,dv=sumLengthR, at='translateX', v=rightShinLength)
		cmds.setDrivenKeyframe('right_end_leg_jnt_IK', cd=driver,dv=sumLengthR*2, at='translateX', v=rightShinLength*2)
		
		cmds.keyTangent('right_mid_leg_jnt_IK',e=True,itt='spline',ott='spline', animation='objects')
		mel.eval('selectKey -add -k -f 124.397377 right_mid_leg_jnt_IK_translateX ;')
		cmds.setInfinity(poi='linear')
		
		cmds.keyTangent('right_end_leg_jnt_IK',e=True,itt='spline',ott='spline', animation='objects')
		mel.eval('selectKey -add -k -f 124.397377 right_end_leg_jnt_IK_translateX ;')
		cmds.setInfinity(poi='linear')
	
	if(newName=='left'):
		#expression 
		driver="leftFoot_IK_length_NO_FLIPShape.distance"
		leftThighLength=cmds.getAttr('left_mid_leg_jnt_IK.translateX')
		leftShinLength=cmds.getAttr('left_end_leg_jnt_IK.translateX')
		sumLengthL= leftThighLength+leftShinLength
		cmds.setDrivenKeyframe('left_mid_leg_jnt_IK', cd=driver,dv=sumLengthL, at='translateX', v=leftThighLength)
		cmds.setDrivenKeyframe('left_mid_leg_jnt_IK', cd=driver,dv=sumLengthL*2, at='translateX', v=leftThighLength*2)
		cmds.setDrivenKeyframe('left_end_leg_jnt_IK', cd=driver,dv=sumLengthL, at='translateX', v=leftShinLength)
		cmds.setDrivenKeyframe('left_end_leg_jnt_IK', cd=driver,dv=sumLengthL*2, at='translateX', v=leftShinLength*2)
		
		cmds.keyTangent('left_mid_leg_jnt_IK',e=True,itt='spline',ott='spline', animation='objects')
		mel.eval('selectKey -add -k -f 124.397377 left_mid_leg_jnt_IK_translateX ;')
		cmds.setInfinity(poi='linear')
		
		cmds.keyTangent('left_end_leg_jnt_IK',e=True,itt='spline',ott='spline', animation='objects')
		mel.eval('selectKey -add -k -f 124.397377 left_end_leg_jnt_IK_translateX ;')
		cmds.setInfinity(poi='linear')
	'''
	#lock attr
	attr=['.tx','.ty','.tz','.rx','.ry','.rz','.sx','.sy','.sz','.v']
	scaleXYZ=['.sx','.sy','.sz','.v']
	for i in attr:
		cmds.setAttr(newName+'_settings_GRP'+i,l=True)
	
	cmds.setAttr(newName+'Ball_hdl.v',0)
	cmds.setAttr(newName+'Foot_hdl_NO_FLIP.v',0) 
	cmds.setAttr(newName+'Foot_hdl_PV.v',0) 

	for i in scaleXYZ:
		cmds.setAttr(newName+"_Leg_settingsCTRL"+i,l=True)
		cmds.setAttr(newName+'Foot_Ctrl'+i,l=True)
		
	attrWithout=attr[3:]
	attrWithout2=attr[:3]+attr[6:]
	for i in attr:
		cmds.setAttr(newName+'_Leg_settingsCTRL'+i,l=True, k=False)
		
	for i in attrWithout:
		cmds.setAttr(newName+'_knee_ctrl'+i,l=True,k=False)
	for i in attrWithout2:
		cmds.setAttr(feetFK[0]+i,l=True,k=False)
		for k in legFK:
			cmds.setAttr(k+i,l=True,k=False)
			
	cmds.setAttr(newName+"outer_foot_loc.visibility",0)
	cmds.setAttr(newName+"inner_foot_loc.visibility",0)
	
	#fix toe spin
	cmds.parent(newName+'wiggle_grp',newName+'toe_loc')
	
def doClothes(*args):
	'''
	coat joints and names
	boots and gloves joints and names 
	pistol and cutlass joints and names
	'''
	clothesJntsPos=[[2.395,128.191,-17.104],[2.551,109.472,-20.523],[2.735,87.446,-24.547],[2.857,72.797,-27.223],
					[21.292,126.721,21.775],[20.465,112.999,23.657],[19.389,95.178,26.102],[18.727,84.203,27.607],
					[-15.528,132.706,25.535],[-17.074,117.531,25.349], [-19.218,96.498,25.091],[-20.489,84.023,24.938],
					[28.115,125.583,3.267],[32.5,109.997,2.405], [37.59,91.901,1.404], [41.568,77.762,0.622],
					[-24.728,137.269,5.663],[-31.03,113.961,5.822],[-36.447,93.929,5.958],[-40.793,77.856,6.068]]
	clothesNames=['back_coat_1','back_coat_2','back_coat_3','back_coat_4', 
				'side_left_coat_1','side_left_coat_2','side_left_coat_3','side_left_coat_4', 
				'side_right_coat_1','side_right_coat_2','side_right_coat_3','side_right_coat_4', 
				'side_1_3_left_coat_1','side_1_3_left_coat_2','side_1_3_left_coat_3','side_1_3_left_coat_4',	
				'side_1_3_right_coat_1','side_1_3_right_coat_2','side_1_3_right_coat_3','side_1_3_right_coat_4']	
	
	for x, y in zip(clothesJntsPos, clothesNames):
		cmds.joint(p=x,n=y)
		
	cmds.joint('side_left_coat_1','side_right_coat_1','side_1_3_left_coat_1','side_1_3_right_coat_1','back_coat_1',e=True,oj='xyz',sao='yup',ch=True,zso=True)	
	withoutLast=['back_coat_1','back_coat_2','back_coat_3', 
				'side_left_coat_1','side_left_coat_2','side_left_coat_3',
				'side_right_coat_1','side_right_coat_2','side_right_coat_3', 
				'side_1_3_left_coat_1','side_1_3_left_coat_2','side_1_3_left_coat_3',	
				'side_1_3_right_coat_1','side_1_3_right_coat_2','side_1_3_right_coat_3']	
	for y in withoutLast:
		cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n=y+'ctrl')
		cmds.setAttr(y+'ctrl.scale',5,5,5)
		cmds.xform(y+'ctrlShape.cv[0:7]',ro=(0,0,90))
		cmds.makeIdentity(y+'ctrl', apply=True,t=1,r=1,s=1,n=0,pn=1)
		cmds.parent(y+'ctrlShape', y, s=True, r=True)
		cmds.delete(y+'ctrl')
	for y in clothesNames:
		cmds.setAttr(y+".drawStyle",2)	
		
	clothesL=clothesNames[4:8]+clothesNames[12:16]
	clothesR=clothesNames[8:12]+clothesNames[16:18]
	for y in clothesL:
		cmds.setAttr(y+".overrideEnabled", 1)
		cmds.setAttr(y+".overrideColor", 4)
	for y in clothesR:
		cmds.setAttr(y+".overrideEnabled", 1)
		cmds.setAttr(y+".overrideColor", 6)
	clothesM=clothesNames[0:4]
	for y in clothesM:
		cmds.setAttr(y+".overrideEnabled", 1)
		cmds.setAttr(y+".overrideColor", 16)
	
	cmds.parent('side_left_coat_1','side_right_coat_1','side_1_3_left_coat_1','side_1_3_right_coat_1',w=True)	
	##cleanup
	attr=['.tx','.ty','.tz','.sx','.sy','.sz','.v']
	for i in clothesNames:
		for k in attr:
			cmds.setAttr(i+k,l=True)
	cmds.select(clear=True)
	doBoots()
	doGloves()
	
def doGloves():
	gloveJntsPos=[[-52.529,121.096,18.14],[-46.315,133.32,17.018],[-39.206,147.301,15.734],[-58.789,120.768,15.541],
					[-56.052,135.883,11.382], [-53.269,151.25,7.154], [-55.958,119.46,9.389],[-51.939,131.575,1.716],
					[-47.601,144.655,-6.567],[-51.461,118.596,13.546],[-42.206,130.852,5.931],[-34.867,140.57,-0.107]]
	gloveJntNames=['glove_1','glove_2','glove_3','glove_4','glove_5','glove_6','glove_7','glove_8',
					'glove_9', 'glove_10', 'glove_11', 'glove_12']	
	for x, y in zip(gloveJntsPos, gloveJntNames):
		cmds.joint(p=x,n=y)

	cmds.joint('glove_1','glove_4','glove_10','glove_7',e=True,oj='xyz',sao='yup',ch=True,zso=True)	
	withoutLast=['glove_1','glove_2','glove_4','glove_5','glove_7','glove_8',
					 'glove_10', 'glove_11']	
	for y in withoutLast:
		cmds.group(y,n=y+'_GRP')
		cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n=y+'ctrl')
		cmds.setAttr(y+'ctrl.scale',5,5,5)
		cmds.xform(y+'ctrlShape.cv[0:7]', ro=(0,0,90))
		cmds.makeIdentity(y+'ctrl', apply=True,t=1,r=1,s=1,n=0,pn=1)
		cmds.parent(y+'ctrlShape', y, s=True, r=True)
		cmds.delete(y+'ctrl')
		cmds.setAttr(y+".overrideEnabled", 1)
		cmds.setAttr(y+".overrideColor", 6)
	
	for y in gloveJntNames:
		cmds.setAttr(y+".drawStyle",2)	
		
	cmds.parent('glove_1','glove_4','glove_10','glove_7','glove_7_GRP','glove_10_GRP','glove_4_GRP',w=True)
	cmds.parent('glove_1','glove_1_GRP')
	cmds.parent('glove_4','glove_4_GRP')
	cmds.parent('glove_7','glove_7_GRP')
	cmds.parent('glove_10','glove_10_GRP')
	cmds.group('glove_1_GRP','glove_4_GRP','glove_10_GRP','glove_7_GRP',n='gloves_ctrl_ALL_grp')
	
	###
	cmds.setAttr("right_start_arm_jnt_FK.rotateZ", 69)
	cmds.setAttr("right_start_arm_jnt_FK.rotateY", 5)
	cmds.setAttr("right_mid_arm_jnt_FK.rotateY", -22.8)
	cmds.setAttr("right_mid_arm_jnt_FK.rotateZ", -2)
	###
	
	cmds.spaceLocator(n='right_glovesAtt',p=(0,0,0))
	cmds.setAttr('right_glovesAtt.translate',-50.641,130.549,9.087)
	cmds.parent('right_glovesAtt','r_g_midTwist')
	cmds.parentConstraint('right_glovesAtt','gloves_ctrl_ALL_grp',mo=True, w=1)
	cmds.parent('gloves_ctrl_ALL_grp','pirate_Root_Transform')
	
	attr=['.tx','.ty','.tz','.sx','.sy','.sz','.v']
	for i in gloveJntNames:
		for k in attr:
			cmds.setAttr(i+k,l=True)
	cmds.select(clear=True)
	
def doBoots():
	bootsJntsPos=[[-29.688,65.571,12.231],[-29.744,53.844,11.985],[-31.195,43.478,12.253],[-34.811,33.955,14.519],
					[-27.194,65.964,-6.186], [-27.417,54.007,-6.347], [-28.29,44.437,-6.753],[-29.019,33.501,-8.963],
					[-10.745,64.9,-7.173],[-10.154,55.206,-8.499],[-9.573,44.973,-9.621],[-8.225,35.148,-11.508],
					[-6.966,61.094,12.561],[-6.578,51.225,13.21],[-8.383,42.261,15.796],[-11.069,34.586,19.357]]
	bootsJntNames=['right_boots_1','right_boots_2','right_boots_3','right_boots_4','side_right_boots_5',
					'side_right_boots_6','side_right_boots_7','side_right_boots_8','side_right_boots_9',
					'side_right_boots_10','side_right_boots_11','side_right_boots_12',
					'right_in_boots_1','right_in_boots_2','right_in_boots_3','right_in_boots_4']
	for x, y in zip(bootsJntsPos, bootsJntNames):
		cmds.joint(p=x,n=y)
		
	cmds.joint('right_boots_1','right_in_boots_1','side_right_boots_5','side_right_boots_9',e=True,oj='xyz',sao='yup',ch=True,zso=True)	
	withoutLastBR=['right_boots_1','right_boots_2','right_boots_3','side_right_boots_5',
					'side_right_boots_6','side_right_boots_7','side_right_boots_9',
					'side_right_boots_10','side_right_boots_11',
					'right_in_boots_1','right_in_boots_2','right_in_boots_3']	
	for y in withoutLastBR:
		#cmds.group(y,n=y+'_GRP')
		#cmds.xform( y+'_GRP.scalePivot', y+'_GRP.rotatePivot',t=(cmds.getAttr(y+'.translateX'),cmds.getAttr(y+'.translateY'),cmds.getAttr(y+'.translateZ')))
		#cmds.makeIdentity(y+'_GRP', apply=True,t=1,r=1,s=1,n=0,pn=1)
		cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n=y+'ctrl')
		cmds.setAttr(y+'ctrl.scale',5,5,5)
		cmds.xform(y+'ctrlShape.cv[0:7]', ro=(0,0,90))
		cmds.makeIdentity(y+'ctrl', apply=True,t=1,r=1,s=1,n=0,pn=1)
		cmds.parent(y+'ctrlShape', y, s=True, r=True)
		cmds.delete(y+'ctrl')
		cmds.setAttr(y+".overrideEnabled", 1)
		cmds.setAttr(y+".overrideColor", 6)
	for i in bootsJntNames:
		cmds.setAttr(i+".drawStyle",2)	
		
	cmds.parent('side_right_boots_5','side_right_boots_9','right_in_boots_1',w=True)	
	leftBoots=cmds.mirrorJoint('right_boots_1',mirrorYZ=True,mirrorBehavior=True,searchReplace=('right_', 'left_') )
	leftBoots0=cmds.mirrorJoint('side_right_boots_5',mirrorYZ=True,mirrorBehavior=True,searchReplace=('right_', 'left_') )
	leftBoots1=cmds.mirrorJoint('side_right_boots_9',mirrorYZ=True,mirrorBehavior=True,searchReplace=('right_', 'left_') )
	leftBoots2=cmds.mirrorJoint('right_in_boots_1',mirrorYZ=True,mirrorBehavior=True,searchReplace=('right_', 'left_') )
	
	
	for i,k,l,m in zip(leftBoots,leftBoots0,leftBoots1,leftBoots2):
		cmds.setAttr(i+".overrideEnabled", 1)
		cmds.setAttr(i+".overrideColor", 4)
		cmds.setAttr(k+".overrideEnabled", 1)
		cmds.setAttr(k+".overrideColor", 4)
		cmds.setAttr(l+".overrideEnabled", 1)
		cmds.setAttr(l+".overrideColor", 4)
		cmds.setAttr(m+".overrideEnabled", 1)
		cmds.setAttr(m+".overrideColor", 4)
	
	
	cmds.group('right_boots_1', 'side_right_boots_5', 'side_right_boots_9', 'right_in_boots_1', n='right_boots_jnts_ctrl')
	cmds.group('left_boots_1', 'side_left_boots_5', 'side_left_boots_9', 'left_in_boots_1', n='left_boots_jnts_ctrl')
	cmds.group('back_coat_1', 'side_left_coat_1', 'side_right_coat_1', 'side_1_3_left_coat_1', 'side_1_3_right_coat_1', n='coat_grp')
	
	cmds.spaceLocator(n='left_knee_loc',p=(14.705,80.172,6.393))
	cmds.parent('left_knee_loc','left_mid_leg_jnt')
	cmds.spaceLocator(n='right_knee_loc',p=(-14.705,80.172,6.393))
	cmds.parent('right_knee_loc','right_mid_leg_jnt')
	
	cmds.parentConstraint('left_knee_loc','left_boots_jnts_ctrl',mo=True, w=1)
	cmds.parentConstraint('right_knee_loc','right_boots_jnts_ctrl',mo=True, w=1)
	
	cmds.spaceLocator(n='spine_coat_loc',p=(0,150,5))
	cmds.parent('spine_coat_loc','Hip_ctrl')
	cmds.parentConstraint('start_spine_loc','coat_grp',mo=True, w=1)
	cmds.parent('right_boots_jnts_ctrl','left_boots_jnts_ctrl','coat_grp','pirate_Root_Transform')		
	
	attr=['.tx','.ty','.tz','.sx','.sy','.sz','.v']
	for i in bootsJntNames:
		for k in attr:
			cmds.setAttr(i+k,l=True)
	bootsJntNamesLeft=['left_boots_1','left_boots_2','left_boots_3','left_boots_4','side_left_boots_5',
					'side_left_boots_6','side_left_boots_7','side_left_boots_8','side_left_boots_9',
					'side_left_boots_10','side_left_boots_11','side_left_boots_12',
					'left_in_boots_1','left_in_boots_2','left_in_boots_3','left_in_boots_4']
			
	for i in bootsJntNamesLeft:
		for k in attr:
			cmds.setAttr(i+k,l=True)
	
	cmds.select(clear=True)

def ik_fk_match():
	###fk to ik
	cmds.setAttr('left'+'Foot_Ctrl.translateX',0)
	cmds.setAttr('left'+'Foot_Ctrl.rotateY',0)
	cmds.setAttr('right'+'Foot_Ctrl.translateX',0)
	cmds.setAttr('right'+'Foot_Ctrl.rotateY',0)
		
	cmds.setAttr("right_start_arm_jnt_FK.rotateZ", 0)
	cmds.setAttr("right_start_arm_jnt_FK.rotateY", 0)
	cmds.setAttr("right_mid_arm_jnt_FK.rotateY", 0)
	cmds.setAttr("right_mid_arm_jnt_FK.rotateZ", 0)
	
	##right arm upper
	cmds.duplicate('right_start_arm_jnt_FK', n='right_start_arm_jnt_FK_SNAP')
	cmds.setAttr('right_start_arm_jnt_FK_SNAP.tx',l=False)
	cmds.setAttr('right_start_arm_jnt_FK_SNAP.ty',l=False)
	cmds.setAttr('right_start_arm_jnt_FK_SNAP.tz',l=False)
	cmds.delete('right_start_arm_jnt_FK_SNAP|right_mid_arm_jnt_FK','right_start_arm_jnt_FK_SNAP|right_start_arm_jntctrlShape')
	cmds.parent('right_start_arm_jnt_FK_SNAP','right_start_arm_jnt')
	###
	#$r_upperArm= `xform -query -worldSpace -rotation right_start_arm_jnt_FK_SNAP`;
	#xform -worldSpace -rotation $r_upperArm[0] $r_upperArm[1] $r_upperArm[2] right_start_arm_jnt_FK
	
	##right arm mid
	cmds.duplicate('right_mid_arm_jnt_FK', n='right_mid_arm_jnt_FK_SNAP')
	cmds.setAttr('right_mid_arm_jnt_FK_SNAP.tx',l=False)
	cmds.setAttr('right_mid_arm_jnt_FK_SNAP.ty',l=False)
	cmds.setAttr('right_mid_arm_jnt_FK_SNAP.tz',l=False)
	cmds.delete('right_mid_arm_jnt_FK_SNAP|right_end_arm_jnt_FK', 'right_mid_arm_jnt_FK_SNAP|right_mid_arm_jntctrlShape')
	cmds.parent('right_mid_arm_jnt_FK_SNAP','right_mid_arm_jnt')
	###
	#$r_midArm= `xform -query -worldSpace -rotation right_mid_arm_jnt_FK_SNAP`;
	#xform -worldSpace -rotation $r_midArm[0] $r_midArm[1] $r_midArm[2] right_mid_arm_jnt_FK
	
	##right arm mid
	cmds.duplicate('right_end_arm_jnt_FK', n='right_end_arm_jnt_FK_SNAP')
	cmds.setAttr('right_end_arm_jnt_FK_SNAP.tx',l=False)
	cmds.setAttr('right_end_arm_jnt_FK_SNAP.ty',l=False)
	cmds.setAttr('right_end_arm_jnt_FK_SNAP.tz',l=False)
	cmds.delete('right_end_arm_jnt_FK_SNAP|right_hand_jnt_FK', 'right_end_arm_jnt_FK_SNAP|right_end_arm_jntctrlShape')
	cmds.parent('right_end_arm_jnt_FK_SNAP','right_end_arm_jnt')
	###
	#$r_endArm= `xform -query -worldSpace -rotation right_end_arm_jnt_FK_SNAP`;
	#xform -worldSpace -rotation $r_endArm[0] $r_endArm[1] $r_endArm[2] right_end_arm_jnt_FK
	
	#marking menu
	'''
	$r_upperArm= `xform -query -worldSpace -rotation right_start_arm_jnt_FK_SNAP`;
	xform -worldSpace -rotation $r_upperArm[0] $r_upperArm[1] $r_upperArm[2] right_start_arm_jnt_FK;
	$r_midArm= `xform -query -worldSpace -rotation right_mid_arm_jnt_FK_SNAP`;
	xform -worldSpace -rotation $r_midArm[0] $r_midArm[1] $r_midArm[2] right_mid_arm_jnt_FK;
	$r_endArm= `xform -query -worldSpace -rotation right_end_arm_jnt_FK_SNAP`;
	xform -worldSpace -rotation $r_endArm[0] $r_endArm[1] $r_endArm[2] right_end_arm_jnt_FK;
	'''
	
	###ik to fk
	'''
	matchTransform -pos rightArm_ctrl right_end_arm_jnt_FK;
	'''
	
	###legs  left leg
	###fk to ik
	cmds.duplicate('left_start_leg_jnt_FK', n='left_start_leg_jnt_FK_SNAP')
	cmds.setAttr('left_start_leg_jnt_FK_SNAP.tx',l=False)
	cmds.setAttr('left_start_leg_jnt_FK_SNAP.ty',l=False)
	cmds.setAttr('left_start_leg_jnt_FK_SNAP.tz',l=False)
	cmds.delete('left_start_leg_jnt_FK_SNAP|left_mid_leg_jnt_FK', 'left_start_leg_jnt_FK_SNAP|left_start_leg_jntctrlShape')
	cmds.parent('left_start_leg_jnt_FK_SNAP','left_start_leg_jnt')
	###
	#$r_upperArm= `xform -query -worldSpace -rotation right_start_arm_jnt_FK_SNAP`;
	#xform -worldSpace -rotation $r_upperArm[0] $r_upperArm[1] $r_upperArm[2] right_start_arm_jnt_FK
	
	cmds.duplicate('left_mid_leg_jnt_FK', n='left_mid_leg_jnt_FK_SNAP')
	cmds.setAttr('left_mid_leg_jnt_FK_SNAP.tx',l=False)
	cmds.setAttr('left_mid_leg_jnt_FK_SNAP.ty',l=False)
	cmds.setAttr('left_mid_leg_jnt_FK_SNAP.tz',l=False)
	cmds.delete('left_mid_leg_jnt_FK_SNAP|left_end_leg_jnt_FK', 'left_mid_leg_jnt_FK_SNAP|left_mid_leg_jntctrlShape')
	cmds.parent('left_mid_leg_jnt_FK_SNAP','left_mid_leg_jnt')
	###
	#$r_midArm= `xform -query -worldSpace -rotation right_mid_arm_jnt_FK_SNAP`;
	#xform -worldSpace -rotation $r_midArm[0] $r_midArm[1] $r_midArm[2] right_mid_arm_jnt_FK
	
	cmds.duplicate('left_end_leg_jnt_FK', n='left_end_leg_jnt_FK_SNAP')
	cmds.setAttr('left_end_leg_jnt_FK_SNAP.tx',l=False)
	cmds.setAttr('left_end_leg_jnt_FK_SNAP.ty',l=False)
	cmds.setAttr('left_end_leg_jnt_FK_SNAP.tz',l=False)
	cmds.delete('left_end_leg_jnt_FK_SNAP|left_feet_start_jnt_FK', 'left_end_leg_jnt_FK_SNAP|left_end_leg_jntctrlShape')
	cmds.parent('left_end_leg_jnt_FK_SNAP','left_end_leg_jnt')
	###
	#$r_endArm= `xform -query -worldSpace -rotation right_end_arm_jnt_FK_SNAP`;
	#xform -worldSpace -rotation $r_endArm[0] $r_endArm[1] $r_endArm[2] right_end_arm_jnt_FK

	'''
	$l_upperLeg= `xform -query -worldSpace -rotation left_start_leg_jnt_FK_SNAP`;
	xform -worldSpace -rotation $l_upperLeg[0] $l_upperLeg[1] $l_upperLeg[2] left_start_leg_jnt_FK;
	$l_midLeg= `xform -query -worldSpace -rotation left_mid_leg_jnt_FK_SNAP`;
	xform -worldSpace -rotation $l_midLeg[0] $l_midLeg[1] $l_midLeg[2] left_mid_leg_jnt_FK;
	$l_endLeg= `xform -query -worldSpace -rotation left_end_leg_jnt_FK_SNAP`;
	xform -worldSpace -rotation $l_endLeg[0] $l_endLeg[1] $l_endLeg[2] left_end_leg_jnt_FK;
	'''
	
	###legs right leg
	###fk to ik
	cmds.duplicate('right_start_leg_jnt_FK', n='right_start_leg_jnt_FK_SNAP')
	cmds.setAttr('right_start_leg_jnt_FK_SNAP.tx',l=False)
	cmds.setAttr('right_start_leg_jnt_FK_SNAP.ty',l=False)
	cmds.setAttr('right_start_leg_jnt_FK_SNAP.tz',l=False)
	cmds.delete('right_start_leg_jnt_FK_SNAP|right_mid_leg_jnt_FK', 'right_start_leg_jnt_FK_SNAP|right_start_leg_jntctrlShape')
	cmds.parent('right_start_leg_jnt_FK_SNAP','right_start_leg_jnt')
	###
	#$r_upperArm= `xform -query -worldSpace -rotation right_start_arm_jnt_FK_SNAP`;
	#xform -worldSpace -rotation $r_upperArm[0] $r_upperArm[1] $r_upperArm[2] right_start_arm_jnt_FK
	
	cmds.duplicate('right_mid_leg_jnt_FK', n='right_mid_leg_jnt_FK_SNAP')
	cmds.setAttr('right_mid_leg_jnt_FK_SNAP.tx',l=False)
	cmds.setAttr('right_mid_leg_jnt_FK_SNAP.ty',l=False)
	cmds.setAttr('right_mid_leg_jnt_FK_SNAP.tz',l=False)
	cmds.delete('right_mid_leg_jnt_FK_SNAP|right_end_leg_jnt_FK', 'right_mid_leg_jnt_FK_SNAP|right_mid_leg_jntctrlShape')
	cmds.parent('right_mid_leg_jnt_FK_SNAP','right_mid_leg_jnt')
	###
	#$r_midArm= `xform -query -worldSpace -rotation right_mid_arm_jnt_FK_SNAP`;
	#xform -worldSpace -rotation $r_midArm[0] $r_midArm[1] $r_midArm[2] right_mid_arm_jnt_FK
	
	cmds.duplicate('right_end_leg_jnt_FK', n='right_end_leg_jnt_FK_SNAP')
	cmds.setAttr('right_end_leg_jnt_FK_SNAP.tx',l=False)
	cmds.setAttr('right_end_leg_jnt_FK_SNAP.ty',l=False)
	cmds.setAttr('right_end_leg_jnt_FK_SNAP.tz',l=False)
	cmds.delete('right_end_leg_jnt_FK_SNAP|right_feet_start_jnt_FK', 'right_end_leg_jnt_FK_SNAP|right_end_leg_jntctrlShape')
	cmds.parent('right_end_leg_jnt_FK_SNAP','right_end_leg_jnt')
	###
	#$r_endArm= `xform -query -worldSpace -rotation right_end_arm_jnt_FK_SNAP`;
	#xform -worldSpace -rotation $r_endArm[0] $r_endArm[1] $r_endArm[2] right_end_arm_jnt_FK

	'''
	$r_upperLeg= `xform -query -worldSpace -rotation right_start_leg_jnt_FK_SNAP`;
	xform -worldSpace -rotation $r_upperLeg[0] $r_upperLeg[1] $r_upperLeg[2] right_start_leg_jnt_FK;
	$r_midLeg= `xform -query -worldSpace -rotation right_mid_leg_jnt_FK_SNAP`;
	xform -worldSpace -rotation $r_midLeg[0] $r_midLeg[1] $r_midLeg[2] right_mid_leg_jnt_FK;
	$r_endLeg= `xform -query -worldSpace -rotation right_end_leg_jnt_FK_SNAP`;
	xform -worldSpace -rotation $r_endLeg[0] $r_endLeg[1] $r_endLeg[2] right_end_leg_jnt_FK;
	'''
	
def separatelyRun():
	cmds.select('start_spine_jnt', 'mid_spine1_jnt', 'mid_spine2_jnt', 'mid_spine3_jnt', 'mid_spine4_jnt', 'mid_spine5_jnt', 'end_spine_jnt',
					'left_start_leg_jnt', 'left_mid_leg_jnt', 'left_end_leg_jnt', 'left_feet_start_jnt', 'left_feet_end_jnt',
					'right_start_leg_jnt', 'right_mid_leg_jnt', 'right_end_leg_jnt', 'right_feet_start_jnt', 'right_feet_end_jnt',
					'right_sh_jnt_Start','right_sh_jnt_End','right_start_arm_jnt', 'right_mid_arm_jnt', 'right_end_arm_jnt', 'right_end_arm_jnt|right_hand_jnt',
					'right_handBase_jnt', 'right_index_straight_jnt', 'right_index_straight_jnt|right_index_start_jnt_orient', 'right_index_start_jnt', 'right_index_start_jnt|right_index_mid_jnt_orient',
					'right_index_mid_jnt', 'right_index_mid_jnt|right_index_mid2_jnt_orient', 'right_index_mid2_jnt', 'right_index_mid2_jnt|right_index_end_jnt_orient', 'right_middle_straight_jnt',
					'right_middle_straight_jnt|right_middle_start_jnt_orient','right_middle_start_jnt', 'right_middle_start_jnt|right_middle_mid_jnt_orient', 'right_middle_mid_jnt',
					'right_middle_mid_jnt|right_middle_mid2_jnt_orient', 'right_middle_mid2_jnt', 'right_middle_mid2_jnt|right_middle_end_jnt_orient', 'right_ring_straight_jnt', 
					'right_ring_straight_jnt|right_ring_start_jnt_orient', 'right_ring_start_jnt', 'right_ring_start_jnt|right_ring_mid_jnt_orient','right_ring_mid_jnt', 
					'right_ring_mid_jnt|right_ring_mid2_jnt_orient', 'right_ring_mid2_jnt', 'right_ring_mid2_jnt|right_ring_end_jnt_orient', 'right_pinky_straight_jnt',
					'right_pinky_straight_jnt|right_pinky_start_jnt_orient', 'right_pinky_start_jnt', 'right_pinky_start_jnt|right_pinky_mid_jnt_orient', 'right_pinky_mid_jnt', 
					'right_pinky_mid_jnt|right_pinky_mid2_jnt_orient','right_pinky_mid2_jnt', 'right_pinky_mid2_jnt|right_pinky_end_jnt_orient', 'right_thumb_Orbit_straight_jnt',
					'right_thumb_Orbit_jnt', 'right_thumb_Orbit_jnt|right_thumb_start_jnt_orient', 'right_thumb_start_jnt', 'right_thumb_start_jnt|right_thumb_mid_jnt_orient',
					'right_thumb_mid_jnt', 'right_thumb_mid_jnt|right_thumb_mid2_jnt_orient', 'right_thumb_mid2_jnt','right_thumb_mid2_jnt|right_thumb_end_jnt_orient',
					'jnt_tentacle1_1_Result','jnt_tentacle1_2_Result','jnt_tentacle1_3_Result','jnt_tentacle1_4_Result','jnt_tentacle1_5_Result','jnt_tentacle1_6_Result','jnt_tentacle1_7_Result','jnt_tentacle1_8_Result','jnt_tentacle1_9_Result','jnt_tentacle1_10_Result',
					'jnt_tentacle1_11_Result','jnt_tentacle1_12_Result','jnt_tentacle1_13_Result','left_sh_jnt_Start', 'left_sh_jnt_End','neck_2', 'neck_1',
					'right_boots_1', 'right_boots_2', 'right_boots_3', 'right_boots_4', 'side_right_boots_5', 'side_right_boots_6', 'side_right_boots_7', 'side_right_boots_8', 'side_right_boots_9',
					'side_right_boots_10', 'side_right_boots_11', 'side_right_boots_12', 'right_in_boots_1', 'right_in_boots_2', 'right_in_boots_3', 'right_in_boots_4' ,
					'left_boots_1', 'left_boots_2', 'left_boots_3', 'left_boots_4', 'side_left_boots_5', 'side_left_boots_6', 'side_left_boots_7', 'side_left_boots_8', 
					'side_left_boots_9', 'side_left_boots_10', 'side_left_boots_11', 'side_left_boots_12', 'left_in_boots_1','left_in_boots_2', 'left_in_boots_3', 'left_in_boots_4',
					'back_coat_1','back_coat_2','back_coat_3','back_coat_4', 
					'side_left_coat_1','side_left_coat_2','side_left_coat_3','side_left_coat_4', 
					'side_right_coat_1','side_right_coat_2','side_right_coat_3','side_right_coat_4', 
					'side_1_3_left_coat_1','side_1_3_left_coat_2','side_1_3_left_coat_3','side_1_3_left_coat_4',	
					'side_1_3_right_coat_1','side_1_3_right_coat_2','side_1_3_right_coat_3','side_1_3_right_coat_4',
					'glove_1','glove_2','glove_3','glove_4','glove_5','glove_6','glove_7','glove_8',
					'glove_9', 'glove_10', 'glove_11', 'glove_12')#'PirateKing_Legs_L1','PirateKing_Body_L1','Tentacle',tsb=True,mi=5)

	cmds.select('PirateKing_Body_L1','PirateKing_Legs_L1','Tentacle',add=True)
	
	
	
def skinEverything(*args):
	'''
	skin to the geometry
	'''
	
	cmds.skinCluster( 'jnt_tentacle1_1_ctrlJnts', 'jnt_tentacle1_5_ctrlJnts','jnt_tentacle1_7_ctrlJnts', 'jnt_tentacle1_10_ctrlJnts' , 'jnt_tentacle1_13_ctrlJnts','tentacle1', mi=5)
	cmds.skinCluster('hat_jnt_1','left_edge_hat_jnt1','right_edge_hat_jnt1', 
					'right_nose_1_jnt', 'right_eye_7_jnt',  'right_eye_3_jnt', 'right_eyebrow_end_jnt','right_eyebrow_mid_jnt',
					 'right_eyebrow_start_jnt', 'nose_top_jnt','left_nose_1_jnt', 'left_eye_7_jnt', 'left_eye_3_jnt', 'left_eyebrow_end_jnt',
					  'left_eyebrow_mid_jnt', 'left_eyebrow_start_jnt', 'base_mst_jnt','PirateKing_Head_L1',mi=5)
					
	cmds.skinCluster('left_top_move_bindJnt','left_top_move_Sq_str','left_bot_move_bindJnt','left_screw',
						'right_top_move_bindJnt','right_top_move_Sq_str','right_bot_move_bindJnt','right_screw','PirateKing_Jaw_L1',mi=5)
	cmds.skinCluster('left_eye','polySurface1')		  
	cmds.skinCluster('right_eye','polySurface2')	
	
	####set all the driven keys
	###set hat
	hatJnts=['right_edge_hat_jnt3','right_edge_hat_jnt2','right_edge_hat_jnt1','left_edge_hat_jnt3','left_edge_hat_jnt2','left_edge_hat_jnt1']
	rotXYZ=['.rotateX','.rotateY','.rotateZ']
	trXYZ=['.translateX','.translateY','.translateZ']
	for i in hatJnts:#-9.5
		cmds.setDrivenKeyframe(i+rotXYZ[2],cd='hatBox_ctrl.translateY')
		
	cmds.setAttr("hatBox_ctrl.translateY",0)
	for i in hatJnts:#0
		cmds.setAttr(i+rotXYZ[2], 15)
	for i in hatJnts:
		cmds.setDrivenKeyframe(i+rotXYZ[2],cd='hatBox_ctrl.translateY')
	
	cmds.setAttr("hatBox_ctrl.translateY",-19)
	for i in hatJnts:#-19
		cmds.setAttr(i+rotXYZ[2], -15)
	for i in hatJnts:
		cmds.setDrivenKeyframe(i+rotXYZ[2],cd='hatBox_ctrl.translateY')
	
	#setEyebrows LEFT
	eyeBrowJointsL=['left_eyebrow_start_jnt','left_eyebrow_mid_jnt','left_eyebrow_end_jnt']
	eyeBrowJointsR=['right_eyebrow_start_jnt','right_eyebrow_mid_jnt','right_eyebrow_end_jnt']
	
	cmds.setAttr('left_eyebrow_start_jnt.translateY',240.972)
	cmds.setAttr('left_eyebrow_mid_jnt.translateY',241.651)
	cmds.setAttr('left_eyebrow_end_jnt.translateY',241.885)
	for i in eyeBrowJointsL:#-9.5
		cmds.setDrivenKeyframe(i+trXYZ[1],cd='eyebrowsLBox_ctrl.translateY')
	
	cmds.setAttr("eyebrowsLBox_ctrl.translateY",0)
	cmds.setAttr('left_eyebrow_start_jnt.translateY',244)
	cmds.setAttr('left_eyebrow_mid_jnt.translateY',242)
	cmds.setAttr('left_eyebrow_end_jnt.translateY',240)
	
	for i in eyeBrowJointsL:#-0
		cmds.setDrivenKeyframe(i+trXYZ[1],cd='eyebrowsLBox_ctrl.translateY')
	
	cmds.setAttr("eyebrowsLBox_ctrl.translateY",-19)
	cmds.setAttr('left_eyebrow_start_jnt.translateY',238)
	cmds.setAttr('left_eyebrow_mid_jnt.translateY',239)
	cmds.setAttr('left_eyebrow_end_jnt.translateY',240)
	for i in eyeBrowJointsL:#-19
		cmds.setDrivenKeyframe(i+trXYZ[1],cd='eyebrowsLBox_ctrl.translateY')
	#setEyebrows Right
	
	cmds.setAttr('right_eyebrow_start_jnt.translateY',240.972)
	cmds.setAttr('right_eyebrow_mid_jnt.translateY',241.651)
	cmds.setAttr('right_eyebrow_end_jnt.translateY',241.885)
	for i in eyeBrowJointsR:#-9.5
		cmds.setDrivenKeyframe(i+trXYZ[1],cd='eyebrowsRBox_ctrl.translateY')
	
	cmds.setAttr("eyebrowsRBox_ctrl.translateY",0)
	cmds.setAttr('right_eyebrow_start_jnt.translateY',244)
	cmds.setAttr('right_eyebrow_mid_jnt.translateY',242)
	cmds.setAttr('right_eyebrow_end_jnt.translateY',240)
	
	for i in eyeBrowJointsR:#-0
		cmds.setDrivenKeyframe(i+trXYZ[1],cd='eyebrowsRBox_ctrl.translateY')
	
	cmds.setAttr("eyebrowsRBox_ctrl.translateY",-19)
	cmds.setAttr('right_eyebrow_start_jnt.translateY',238)
	cmds.setAttr('right_eyebrow_mid_jnt.translateY',239)
	cmds.setAttr('right_eyebrow_end_jnt.translateY',240)
	for i in eyeBrowJointsR:#-19
		cmds.setDrivenKeyframe(i+trXYZ[1],cd='eyebrowsRBox_ctrl.translateY')
	
	#set Nose sniff
	noseJnts=['nose_top_jnt','left_nose_1_jnt','right_nose_1_jnt']
	for i in noseJnts:#-9.5
		cmds.setDrivenKeyframe(i+trXYZ[1],cd='noseBox_ctrl.translateY')
	
	cmds.setAttr("noseBox_ctrl.translateY",-19)
	cmds.setAttr('nose_top_jnt.translateY',237)
	cmds.setAttr('left_nose_1_jnt.translateY',236)
	cmds.setAttr('right_nose_1_jnt.translateY',236)
	
	for i in noseJnts:#-19
		cmds.setDrivenKeyframe(i+trXYZ[1],cd='noseBox_ctrl.translateY')
		
	###
	eyesBlink=['right_eye_3_jnt','right_eye_7_jnt','left_eye_3_jnt','left_eye_7_jnt']
	for i in eyesBlink:#-9.5
		cmds.setDrivenKeyframe(i+trXYZ[1],cd='blinkBox_ctrl.translateY')
		cmds.setDrivenKeyframe(i+trXYZ[2],cd='blinkBox_ctrl.translateY')
		
		
	cmds.setAttr("blinkBox_ctrl.translateY",-19)
	cmds.setAttr("left_eye_7_jnt.translateY",238)
	cmds.setAttr("left_eye_7_jnt.translateZ",20.5)
	cmds.setAttr("left_eye_3_jnt.translateY",238)
	cmds.setAttr("left_eye_3_jnt.translateZ",20.5)
	cmds.setAttr("right_eye_7_jnt.translateY",238)
	cmds.setAttr("right_eye_7_jnt.translateZ",20.5)
	cmds.setAttr("right_eye_3_jnt.translateY",238)
	cmds.setAttr("right_eye_3_jnt.translateZ",20.5)
	
	for i in eyesBlink:#19
		cmds.setDrivenKeyframe(i+trXYZ[1],cd='blinkBox_ctrl.translateY')
		cmds.setDrivenKeyframe(i+trXYZ[2],cd='blinkBox_ctrl.translateY')
	
	###
	moustacheJ=['left_mst_7','left_mst_8','left_mst_9','left_mst_10','left_mst_2','left_mst_3','left_mst_4','left_mst_5']
	for i in moustacheJ: #-9.5
		cmds.setDrivenKeyframe(i+rotXYZ[2],cd='moustacheBox_ctrl.translateY')
	
	cmds.setAttr("moustacheBox_ctrl.translateY",-19)
	for i in moustacheJ:
		cmds.setAttr(i+rotXYZ[2],-50)
	for i in moustacheJ: #-19
		cmds.setDrivenKeyframe(i+rotXYZ[2],cd='moustacheBox_ctrl.translateY')
		
	cmds.setAttr("moustacheBox_ctrl.translateY",0)
	for i in moustacheJ:#0
		cmds.setAttr(i+rotXYZ[2],50)
	for i in moustacheJ: #-19
		cmds.setDrivenKeyframe(i+rotXYZ[2],cd='moustacheBox_ctrl.translateY')
	###
	###fix the fingers
	cmds.setAttr("right_thumb_start_FK_CTRL.rotateZ", 0)
	cmds.setAttr("right_thumb_mid2_FK_CTRL.rotateZ",0)
	
	cmds.setAttr("right_index_start_FK_CTRL.rotateY",0)
	cmds.setAttr("right_index_start_FK_CTRL.rotateZ",0)
	cmds.setAttr("right_index_start_FK_CTRL.rotateX",0)
	cmds.setAttr("right_index_mid_FK_CTRL.rotateZ", 0)
	
	cmds.setAttr("right_middle_start_FK_CTRL.rotateX", 0)
	cmds.setAttr("right_middle_start_FK_CTRL.rotateY", 0)
	cmds.setAttr("right_middle_start_FK_CTRL.rotateZ", 0)
	
	cmds.setAttr("right_middle_mid_FK_CTRL.rotateX", 0)
	cmds.setAttr("right_middle_mid_FK_CTRL.rotateY", 0)
	cmds.setAttr("right_middle_mid_FK_CTRL.rotateZ", 0)
	
	cmds.setAttr("right_ring_start_FK_CTRL.rotateX",0)
	cmds.setAttr("right_ring_start_FK_CTRL.rotateY",0)
	cmds.setAttr("right_ring_start_FK_CTRL.rotateZ",0)
	
	cmds.setAttr("right_ring_mid_FK_CTRL.rotateZ",0)
	
	cmds.setAttr("right_pinky_start_FK_CTRL.rotateZ", 0)
	cmds.setAttr("right_pinky_start_FK_CTRL.rotateY", 0)
	
	cmds.setAttr("right_pinky_mid_FK_CTRL.rotateZ",0)
		
	boxCtrl=['blinkBox_ctrl','moustacheBox_ctrl', 'eyebrowsLBox_ctrl','eyebrowsRBox_ctrl', 'noseBox_ctrl', 'hatBox_ctrl']
	for i in boxCtrl:
		cmds.setAttr(i+'.translateY',-9.5) #change to 0 later
	
	###
	cmds.group('left_tentacle_GRP_parentConstraint1','jnt_tentacle1_1_IK_grp','jnt_tentacle1_1_Result_grp','tentalce_hdl','tentacle_distance', 'tentacle1',n='doNOTtouch')
	cmds.setAttr("tentacle1.visibility",0)
	cmds.setAttr("tentalce_hdl.visibility",0)
	cmds.setAttr("tentacle_distance.visibility",0)
	
	###add aditional attributes for the pistol and cutlass
	attributes=['cutlass','pistol','world']
	for i in attributes:
		cmds.addAttr('right_Arm_settingsCTRL',ln=i, at='double', min=0, max=5, dv=1 )
		cmds.setAttr('right_Arm_settingsCTRL.'+i,e=True,keyable=True)
		
	### pistol and cutlass connection
	'''
	cmds.spaceLocator(p=(-104, 192, 5),n='pistol_loc')
	cmds.parent('PirateKing_Pistol_L1','pistol_loc')
	cmds.group('pistol_loc',n='pistol_loc_grp')
	cmds.xform('pistol_loc','pistol_loc_grp',cp=True)
	cmds.parentConstraint('right_handBase_CTRL_JNT', 'pistol_loc_grp', mo=1, w=1)
	
	cmds.spaceLocator(p=(15.274, 160.668, 29.083),n='cutlass_loc')
	cmds.parent('PirateKing_Cutlass_L1','cutlass_loc')
	cmds.group('cutlass_loc',n='cutlass_loc_grp')
	cmds.xform('cutlass_loc','cutlass_loc_grp',cp=True)
	cmds.parentConstraint('right_handBase_CTRL_JNT', 'cutlass_loc_grp', mo=1, w=1)
	'''
	
	##number 3
	rotXYZ=['.rotateX','.rotateY','.rotateZ']
	for i in rotXYZ:
		cmds.setDrivenKeyframe('right_thumb_Orbit_FK_CTRL|right_thumb_start_jnt_orient'+i,cd='right_FINGERSctrl.number_3')
		cmds.setDrivenKeyframe('right_thumb_start_FK_CTRL|right_thumb_mid_jnt_orient'+i,cd='right_FINGERSctrl.number_3')
		cmds.setDrivenKeyframe('right_thumb_mid_FK_CTRL|right_thumb_mid2_jnt_orient'+i, cd='right_FINGERSctrl.number_3')
		
		cmds.setDrivenKeyframe('right_pinky_start_IK|right_pinky_start_jnt_orient'+i,cd='right_FINGERSctrl.number_3')
		cmds.setDrivenKeyframe('right_pinky_start_FK_CTRL|right_pinky_mid_jnt_orient'+i,cd='right_FINGERSctrl.number_3')
		cmds.setDrivenKeyframe('right_pinky_mid_FK_CTRL|right_pinky_mid2_jnt_orient'+i, cd='right_FINGERSctrl.number_3')
	
	cmds.setAttr('right_FINGERSctrl.number_3',10)
	cmds.setAttr('right'+'_pinky_'+'start_IK|right'+'_pinky_'+'start_jnt_orient.rotateZ', 70.5 )
	cmds.setAttr('right'+'_pinky_'+'start_IK|right'+'_pinky_'+'start_jnt_orient.rotateY', 13.5 )
	cmds.setAttr('right'+'_pinky_'+'start_FK_CTRL|right'+'_pinky_'+'mid_jnt_orient.rotateZ',50)
	cmds.setAttr('right'+'_pinky_'+'mid_FK_CTRL|right'+'_pinky_'+'mid2_jnt_orient.rotateZ',40)
	
	cmds.setAttr('right_thumb_Orbit_FK_CTRL|right_thumb_start_jnt_orient.rotateX', 14 )
	cmds.setAttr('right_thumb_Orbit_FK_CTRL|right_thumb_start_jnt_orient.rotateY', -35 )
	cmds.setAttr('right_thumb_Orbit_FK_CTRL|right_thumb_start_jnt_orient.rotateZ', 48 )
	cmds.setAttr('right_thumb_start_FK_CTRL|right_thumb_mid_jnt_orient.rotateZ',19.5)
	cmds.setAttr('right_thumb_mid_FK_CTRL|right_thumb_mid2_jnt_orient.rotateZ',50)
	
	for i in rotXYZ:
		cmds.setDrivenKeyframe('right_thumb_Orbit_FK_CTRL|right_thumb_start_jnt_orient'+i,cd='right_FINGERSctrl.number_3')
		cmds.setDrivenKeyframe('right_thumb_start_FK_CTRL|right_thumb_mid_jnt_orient'+i,cd='right_FINGERSctrl.number_3')
		cmds.setDrivenKeyframe('right_thumb_mid_FK_CTRL|right_thumb_mid2_jnt_orient'+i, cd='right_FINGERSctrl.number_3')
		
		cmds.setDrivenKeyframe('right_pinky_start_IK|right_pinky_start_jnt_orient'+i,cd='right_FINGERSctrl.number_3')
		cmds.setDrivenKeyframe('right_pinky_start_FK_CTRL|right_pinky_mid_jnt_orient'+i,cd='right_FINGERSctrl.number_3')
		cmds.setDrivenKeyframe('right_pinky_mid_FK_CTRL|right_pinky_mid2_jnt_orient'+i, cd='right_FINGERSctrl.number_3')
		
	cmds.setAttr('right_FINGERSctrl.number_3',0)
	##end setting number 3
	rotXYZ=['.rotateX','.rotateY','.rotateZ']
	for i in rotXYZ:
		cmds.setDrivenKeyframe('right_thumb_Orbit_FK_CTRL|right_thumb_start_jnt_orient'+i,cd='right_FINGERSctrl.number_2')
		cmds.setDrivenKeyframe('right_thumb_start_FK_CTRL|right_thumb_mid_jnt_orient'+i,cd='right_FINGERSctrl.number_2')
		cmds.setDrivenKeyframe('right_thumb_mid_FK_CTRL|right_thumb_mid2_jnt_orient'+i, cd='right_FINGERSctrl.number_2')
		
		cmds.setDrivenKeyframe('right_pinky_start_IK|right_pinky_start_jnt_orient'+i,cd='right_FINGERSctrl.number_2')
		cmds.setDrivenKeyframe('right_pinky_start_FK_CTRL|right_pinky_mid_jnt_orient'+i,cd='right_FINGERSctrl.number_2')
		cmds.setDrivenKeyframe('right_pinky_mid_FK_CTRL|right_pinky_mid2_jnt_orient'+i, cd='right_FINGERSctrl.number_2')
		
		cmds.setDrivenKeyframe('right_ring_start_IK|right_ring_start_jnt_orient'+i,cd='right_FINGERSctrl.number_2')
		cmds.setDrivenKeyframe('right_ring_start_FK_CTRL|right_ring_mid_jnt_orient'+i,cd='right_FINGERSctrl.number_2')
		cmds.setDrivenKeyframe('right_ring_mid_FK_CTRL|right_ring_mid2_jnt_orient'+i, cd='right_FINGERSctrl.number_2')
	
	cmds.setAttr('right_FINGERSctrl.number_2',10)
	cmds.setAttr('right'+'_pinky_'+'start_IK|right'+'_pinky_'+'start_jnt_orient.rotateZ', 70.5 )
	cmds.setAttr('right'+'_pinky_'+'start_IK|right'+'_pinky_'+'start_jnt_orient.rotateY', 13.5 )
	cmds.setAttr('right'+'_pinky_'+'start_FK_CTRL|right'+'_pinky_'+'mid_jnt_orient.rotateZ',50)
	cmds.setAttr('right'+'_pinky_'+'mid_FK_CTRL|right'+'_pinky_'+'mid2_jnt_orient.rotateZ',40)
	
	cmds.setAttr('right_thumb_Orbit_FK_CTRL|right_thumb_start_jnt_orient.rotateX', 14 )
	cmds.setAttr('right_thumb_Orbit_FK_CTRL|right_thumb_start_jnt_orient.rotateY', -35 )
	cmds.setAttr('right_thumb_Orbit_FK_CTRL|right_thumb_start_jnt_orient.rotateZ', 48 )
	cmds.setAttr('right_thumb_start_FK_CTRL|right_thumb_mid_jnt_orient.rotateZ',19.5)
	cmds.setAttr('right_thumb_mid_FK_CTRL|right_thumb_mid2_jnt_orient.rotateZ',50)
	
	cmds.setAttr("right_ring_start_IK|right_ring_start_jnt_orient.rotateX",5)
	cmds.setAttr("right_ring_start_IK|right_ring_start_jnt_orient.rotateZ",60)
	cmds.setAttr("right_ring_start_FK_CTRL|right_ring_mid_jnt_orient.rotateZ",60)
	cmds.setAttr("right_ring_mid_FK_CTRL|right_ring_mid2_jnt_orient.rotateZ",60)
	
	for i in rotXYZ:
		cmds.setDrivenKeyframe('right_thumb_Orbit_FK_CTRL|right_thumb_start_jnt_orient'+i,cd='right_FINGERSctrl.number_2')
		cmds.setDrivenKeyframe('right_thumb_start_FK_CTRL|right_thumb_mid_jnt_orient'+i,cd='right_FINGERSctrl.number_2')
		cmds.setDrivenKeyframe('right_thumb_mid_FK_CTRL|right_thumb_mid2_jnt_orient'+i, cd='right_FINGERSctrl.number_2')
		
		cmds.setDrivenKeyframe('right_pinky_start_IK|right_pinky_start_jnt_orient'+i,cd='right_FINGERSctrl.number_2')
		cmds.setDrivenKeyframe('right_pinky_start_FK_CTRL|right_pinky_mid_jnt_orient'+i,cd='right_FINGERSctrl.number_2')
		cmds.setDrivenKeyframe('right_pinky_mid_FK_CTRL|right_pinky_mid2_jnt_orient'+i, cd='right_FINGERSctrl.number_2')
		
		cmds.setDrivenKeyframe('right_ring_start_IK|right_ring_start_jnt_orient'+i,cd='right_FINGERSctrl.number_2')
		cmds.setDrivenKeyframe('right_ring_start_FK_CTRL|right_ring_mid_jnt_orient'+i,cd='right_FINGERSctrl.number_2')
		cmds.setDrivenKeyframe('right_ring_mid_FK_CTRL|right_ring_mid2_jnt_orient'+i, cd='right_FINGERSctrl.number_2')
	###end setting up number 2
	cmds.setAttr('right_FINGERSctrl.number_2',0)
	
	###start  setting number 1
	
	rotXYZ=['.rotateX','.rotateY','.rotateZ']
	for i in rotXYZ:
		cmds.setDrivenKeyframe('right_thumb_Orbit_FK_CTRL|right_thumb_start_jnt_orient'+i,cd='right_FINGERSctrl.number_1')
		cmds.setDrivenKeyframe('right_thumb_start_FK_CTRL|right_thumb_mid_jnt_orient'+i,cd='right_FINGERSctrl.number_1')
		cmds.setDrivenKeyframe('right_thumb_mid_FK_CTRL|right_thumb_mid2_jnt_orient'+i, cd='right_FINGERSctrl.number_1')
		
		cmds.setDrivenKeyframe('right_pinky_start_IK|right_pinky_start_jnt_orient'+i,cd='right_FINGERSctrl.number_1')
		cmds.setDrivenKeyframe('right_pinky_start_FK_CTRL|right_pinky_mid_jnt_orient'+i,cd='right_FINGERSctrl.number_1')
		cmds.setDrivenKeyframe('right_pinky_mid_FK_CTRL|right_pinky_mid2_jnt_orient'+i, cd='right_FINGERSctrl.number_1')
		
		cmds.setDrivenKeyframe('right_ring_start_IK|right_ring_start_jnt_orient'+i,cd='right_FINGERSctrl.number_1')
		cmds.setDrivenKeyframe('right_ring_start_FK_CTRL|right_ring_mid_jnt_orient'+i,cd='right_FINGERSctrl.number_1')
		cmds.setDrivenKeyframe('right_ring_mid_FK_CTRL|right_ring_mid2_jnt_orient'+i, cd='right_FINGERSctrl.number_1')
		
		cmds.setDrivenKeyframe('right_middle_start_IK|right_middle_start_jnt_orient'+i,cd='right_FINGERSctrl.number_1')
		cmds.setDrivenKeyframe('right_middle_start_FK_CTRL|right_middle_mid_jnt_orient'+i,cd='right_FINGERSctrl.number_1')
		cmds.setDrivenKeyframe('right_middle_mid_FK_CTRL|right_middle_mid2_jnt_orient'+i, cd='right_FINGERSctrl.number_1')
	
	cmds.setAttr('right_FINGERSctrl.number_1',10)
	cmds.setAttr('right'+'_pinky_'+'start_IK|right'+'_pinky_'+'start_jnt_orient.rotateZ', 70.5 )
	cmds.setAttr('right'+'_pinky_'+'start_IK|right'+'_pinky_'+'start_jnt_orient.rotateY', 13.5 )
	cmds.setAttr('right'+'_pinky_'+'start_FK_CTRL|right'+'_pinky_'+'mid_jnt_orient.rotateZ',50)
	cmds.setAttr('right'+'_pinky_'+'mid_FK_CTRL|right'+'_pinky_'+'mid2_jnt_orient.rotateZ',40)
	
	cmds.setAttr('right_thumb_Orbit_FK_CTRL|right_thumb_start_jnt_orient.rotateX', 14 )
	cmds.setAttr('right_thumb_Orbit_FK_CTRL|right_thumb_start_jnt_orient.rotateY', -35 )
	cmds.setAttr('right_thumb_Orbit_FK_CTRL|right_thumb_start_jnt_orient.rotateZ', 48 )
	cmds.setAttr('right_thumb_start_FK_CTRL|right_thumb_mid_jnt_orient.rotateZ',19.5)
	cmds.setAttr('right_thumb_mid_FK_CTRL|right_thumb_mid2_jnt_orient.rotateZ',50)
	
	cmds.setAttr("right_ring_start_IK|right_ring_start_jnt_orient.rotateX",5)
	cmds.setAttr("right_ring_start_IK|right_ring_start_jnt_orient.rotateZ",60)
	cmds.setAttr("right_ring_start_FK_CTRL|right_ring_mid_jnt_orient.rotateZ",60)
	cmds.setAttr("right_ring_mid_FK_CTRL|right_ring_mid2_jnt_orient.rotateZ",60)
	
	cmds.setAttr("right_middle_start_IK|right_middle_start_jnt_orient.rotateZ",50)
	cmds.setAttr("right_middle_start_FK_CTRL|right_middle_mid_jnt_orient.rotateZ",70)
	cmds.setAttr("right_middle_mid_FK_CTRL|right_middle_mid2_jnt_orient.rotateZ",50)
	
	for i in rotXYZ:
		cmds.setDrivenKeyframe('right_thumb_Orbit_FK_CTRL|right_thumb_start_jnt_orient'+i,cd='right_FINGERSctrl.number_1')
		cmds.setDrivenKeyframe('right_thumb_start_FK_CTRL|right_thumb_mid_jnt_orient'+i,cd='right_FINGERSctrl.number_1')
		cmds.setDrivenKeyframe('right_thumb_mid_FK_CTRL|right_thumb_mid2_jnt_orient'+i, cd='right_FINGERSctrl.number_1')
		
		cmds.setDrivenKeyframe('right_pinky_start_IK|right_pinky_start_jnt_orient'+i,cd='right_FINGERSctrl.number_1')
		cmds.setDrivenKeyframe('right_pinky_start_FK_CTRL|right_pinky_mid_jnt_orient'+i,cd='right_FINGERSctrl.number_1')
		cmds.setDrivenKeyframe('right_pinky_mid_FK_CTRL|right_pinky_mid2_jnt_orient'+i, cd='right_FINGERSctrl.number_1')
		
		cmds.setDrivenKeyframe('right_ring_start_IK|right_ring_start_jnt_orient'+i,cd='right_FINGERSctrl.number_1')
		cmds.setDrivenKeyframe('right_ring_start_FK_CTRL|right_ring_mid_jnt_orient'+i,cd='right_FINGERSctrl.number_1')
		cmds.setDrivenKeyframe('right_ring_mid_FK_CTRL|right_ring_mid2_jnt_orient'+i, cd='right_FINGERSctrl.number_1')	
		
		cmds.setDrivenKeyframe('right_middle_start_IK|right_middle_start_jnt_orient'+i,cd='right_FINGERSctrl.number_1')
		cmds.setDrivenKeyframe('right_middle_start_FK_CTRL|right_middle_mid_jnt_orient'+i,cd='right_FINGERSctrl.number_1')
		cmds.setDrivenKeyframe('right_middle_mid_FK_CTRL|right_middle_mid2_jnt_orient'+i, cd='right_FINGERSctrl.number_1')
	
	cmds.setAttr('right_FINGERSctrl.number_1',0)
	cmds.setAttr("faceJnts.visibility",0)

	cmds.parent('eye_main_ctrl','head_ALL_grp')
	cmds.parent('spine_IK_length','torso_GRP')
	cmds.parent('left_settings_GRP', 'right_settings_GRP', 'rightA_settings_GRP', 'T_settings_GRP', 'face_box_grp','pirate_Root_Transform')
	
	ik_fk_match()

	###end
	
	#creates a layer for the locators, adds them and changes the colour to white
	'''
	joints = cmds.ls(type=('joint'),l=True)
	for i in joints:
		cmds.setAttr(i+'.drawStyle',2)
		
	joints = cmds.ls(type=('joint'),l=True)
	for i in joints:
		cmds.setAttr(i+'.drawStyle',0)
	'''
	cmds.select(clear=True)
	
		
def armDo(armField):	
	'''
	creates the right arm for now, finish for the left arm 
	'''
	newName = cmds.textField(armField, query=True, text=True)
	print newName
	
	if(newName=='right'):
		stArm=[cmds.getAttr('right_start_arm.translateX'), cmds.getAttr('right_start_arm.translateY'), cmds.getAttr('right_start_arm.translateZ')]			
		midArm=[cmds.getAttr('right_mid_arm.translateX'), cmds.getAttr('right_mid_arm.translateY'), cmds.getAttr('right_mid_arm.translateZ')]			
		endArm=[cmds.getAttr('right_end_arm.translateX'), cmds.getAttr('right_end_arm.translateY'), cmds.getAttr('right_end_arm.translateZ')]			
	if(newName=='left'):
		stArm=[-cmds.getAttr('right_start_arm.translateX'), cmds.getAttr('right_start_arm.translateY'), cmds.getAttr('right_start_arm.translateZ')]			
		midArm=[-cmds.getAttr('right_mid_arm.translateX'), cmds.getAttr('right_mid_arm.translateY'), cmds.getAttr('right_mid_arm.translateZ')]			
		endArm=[-cmds.getAttr('right_end_arm.translateX'), cmds.getAttr('right_end_arm.translateY'), cmds.getAttr('right_end_arm.translateZ')]			
	
	blendNodesRot=[]
	blendNodesTr=[]
	if(newName=='left'):
		dictionary={'LeftArmJnt':leftArmJnt,'leftArmIK':leftArmIK,'leftArmFK':leftArmFK }
	if(newName=='right'):
		dictionary={'RightArmJnt':RightArmJnt, 'rightArmIK':rightArmIK,'rightArmFK':rightArmFK}
	
	#create all the ik fk blenNodes for the switch
	armOriginal=dictionary[newName.title()+'ArmJnt']
	for item in (armOriginal): 
		cmds.shadingNode('blendColors',au=True,n=item+'rot_IK_FK')
		cmds.shadingNode('blendColors',au=True,n=item+'tr_IK_FK')
		
		blendNodesRot.append(item+'rot_IK_FK')
		blendNodesTr.append(item+'tr_IK_FK')
		
	armIK=dictionary[newName+'ArmIK']
	armFK=dictionary[newName+'ArmFK']
	
	#make one function that takes all these stuff in legdo 2 times usage and here one total 3
	for x, y, z, z1, o in zip(armIK, armFK, blendNodesRot, blendNodesTr,armOriginal ):
		cmds.connectAttr(x+'.rotate', z+'.color1', f=True)
		cmds.connectAttr(y+'.rotate', z+'.color2', f=True)
		cmds.connectAttr(z+'.output', o+'.rotate', f=True)
	
		cmds.connectAttr(x+'.translate', z1+'.color1', f=True)
		cmds.connectAttr(y+'.translate', z1+'.color2', f=True)
		cmds.connectAttr(z1+'.output', o+'.translate', f=True)
		
	#fk controllers for the fk joints create 3 times for fk legs and arm!!!
	for x,y in zip(armOriginal,armFK):
		cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n=x+'ctrl')
		cmds.makeIdentity(apply=True,t=1,r=1,s=1,n=0,pn=1)
		cmds.parent(x+'ctrlShape', y,r=True,s=True)
		cmds.xform(y+'.cv[0:7]',s=(20, 20, 20),r=True)
		cmds.xform(y+'.cv[0:7]',ro=(90, 90, 0),r=True)
		cmds.setAttr(y+".overrideEnabled", 1)
		cmds.setAttr(y+".overrideColor", 6)	
		
	cmds.delete(newName+'_start_arm_jntctrl',newName+'_mid_arm_jntctrl',newName+'_end_arm_jntctrl',newName+'_hand_jntctrl')
	cmds.delete(newName+'_end_arm_jnt_FK|'+newName+'_hand_jnt_FK|'+newName+'_hand_jntctrlShape' )	
	
	ArmJnt=dictionary[newName.title()+'ArmJnt']
	ArmFK=dictionary[newName+'ArmFK']
	ArmIK=dictionary[newName+'ArmIK']
	cmds.joint(ArmJnt, ArmFK, ArmIK,e=True,oj='xyz',sao='ydown',ch=True,zso=True)
	#cmds.setAttr(newName+"_mid_arm_jnt_FK.rotateOrder",3)  #WRONG 
	#cmds.setAttr(newName+"_end_arm_jnt_FK.rotateOrder", 5)	###MAKES THE ARM GO SOMEWHERE ELSE
	
	#fk controls
	mel.eval('curve -d 1 -p 0 0 -2 -p 0 0 2 -p -2 0 0 -p 2 0 0 -p 0 0 2 -p -2 0 0 -p 0 0 -2 -p 2 0 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 ;')
	cmds.rename('curve1', newName+'_Arm_settingsCTRL')
	cmds.setAttr(newName+'_Arm_settingsCTRL.translate',endArm[0]-40,endArm[1],endArm[2])
	cmds.setAttr(newName+'_Arm_settingsCTRL.scale',5,5,5)
	cmds.parentConstraint(newName+'_end_arm_jnt',newName+'_Arm_settingsCTRL',mo=True, w=1)
	cmds.group(newName+'_Arm_settingsCTRL', n=newName+'A_settings_GRP')
	cmds.setAttr(newName+'_Arm_settingsCTRL'+".overrideEnabled", 1)
	cmds.setAttr(newName+'_Arm_settingsCTRL'+".overrideColor", 6)	
	
	#lock attr
	cmds.setAttr(newName+"_Arm_settingsCTRL.sx",l=True)
	cmds.setAttr(newName+"_Arm_settingsCTRL.sy",l=True)
	cmds.setAttr(newName+"_Arm_settingsCTRL.sz",l=True)

	attr=['.tx','.ty','.tz','.rx','.ry','.rz','.sx','.sy','.sz','.v']
	for i in attr:
		cmds.setAttr(newName+'A_settings_GRP'+i,l=True)
		cmds.setAttr(newName+'_Arm_settingsCTRL'+i,l=True)
	cmds.addAttr(newName+'_Arm_settingsCTRL',ln="FK_IK_blend", nn="FK/IK_blend", at='double', min=0, max=1, dv=0 )
	cmds.setAttr(newName+'_Arm_settingsCTRL.FK_IK_blend',e=True,keyable=True)
	for item,item1 in zip(blendNodesRot,blendNodesTr):
		cmds.connectAttr(newName+'_Arm_settingsCTRL.FK_IK_blend',item+'.blender',f=True)
		cmds.connectAttr(newName+'_Arm_settingsCTRL.FK_IK_blend',item1+'.blender',f=True)
		
	SplitFirst=cmds.duplicate(newName+'_start_arm_jnt')
	cmds.rename(newName+'_start_arm_jnt1|'+newName+'_mid_arm_jnt', newName+'_mid_arm_jnt1')
	cmds.rename(newName+'_mid_arm_jnt1|'+newName+'_end_arm_jnt', newName+'_end_arm_jnt1')
	if(newName=='left'):
		MidTwist=['l_a_midTwist','l_b_midTwist','l_c_midTwist','l_d_midTwist','l_e_midTwist','l_f_midTwist','l_g_midTwist','l_h_midTwist']
	if(newName=='right'):
		MidTwist=['r_a_midTwist','r_b_midTwist','r_c_midTwist','r_d_midTwist','r_e_midTwist','r_f_midTwist','r_g_midTwist','r_h_midTwist']
	
	###split joints
	splitJoints(newName+'_start_arm_jnt1',newName+'_mid_arm_jnt1',1)
	if(cmds.objExists('new_jnt1')):
		cmds.rename('new_jnt1',MidTwist[0]) 
		
	splitJoints(newName+'_start_arm_jnt1',MidTwist[0],1)
	if(cmds.objExists('new_jnt1')):
		cmds.rename('new_jnt1',MidTwist[1]) 
		
	splitJoints(MidTwist[0],newName+'_mid_arm_jnt1',1)
	if(cmds.objExists('new_jnt1')):
		cmds.rename('new_jnt1',MidTwist[2]) 
	
	splitJoints(MidTwist[2],newName+'_mid_arm_jnt1',1)
	if(cmds.objExists('new_jnt1')):
		cmds.rename('new_jnt1',MidTwist[3]) 

	cmds.move(midArm[0], midArm[1], midArm[2], MidTwist[3],rpr=True)
	cmds.move(midArm[0], midArm[1], midArm[2], newName+'_mid_arm_jnt1', rpr=True)	
	cmds.parent(newName+'_mid_arm_jnt1',w=True)
####
	splitJoints(newName+'_mid_arm_jnt1',newName+'_end_arm_jnt1',1)
	if(cmds.objExists('new_jnt1')):
		cmds.rename('new_jnt1',MidTwist[4]) 
		
	splitJoints(newName+'_mid_arm_jnt1',MidTwist[4],1)
	if(cmds.objExists('new_jnt1')):
		cmds.rename('new_jnt1',MidTwist[5]) 
		
	splitJoints(MidTwist[4],newName+'_end_arm_jnt1',1)
	if(cmds.objExists('new_jnt1')):
		cmds.rename('new_jnt1',MidTwist[6]) 
	
	splitJoints(MidTwist[6],newName+'_end_arm_jnt1',1)
	if(cmds.objExists('new_jnt1')):
		cmds.rename('new_jnt1',MidTwist[7]) 
	
	cmds.move(endArm[0], endArm[1], endArm[2],MidTwist[7], rpr=True)
	cmds.move(endArm[0], endArm[1], endArm[2],newName+'_end_arm_jnt1',rpr=True)	

### twisting the forearm and the upperarm
	pointsUp = [[stArm[0], stArm[1], stArm[2]],
          [midArm[0], midArm[1],midArm[2]]]
	cmds.curve(ep=pointsUp, d=1)  ##d=1 for 2cv points only
	cmds.rename('curve1', newName+'upperArm_Curve')
	cmds.ikHandle(n= newName+'upperArm_handle',sj= newName+'_start_arm_jnt1',ee=MidTwist[3],sol='ikSplineSolver',ccv=False,c= newName+'upperArm_Curve')
	cmds.rename('effector1',  newName+'upperArm_effector')
	
	cmds.duplicate( newName+'_start_arm_jnt',n= newName+'_upperArmStart_bindJnt')
	cmds.select( newName+'_upperArmStart_bindJnt')
	cmds.pickWalk(d='down')
	cmds.parent(w=True)
	cmds.delete('|'+newName+'_mid_arm_jnt|'+newName+'_end_arm_jnt')
	cmds.rename('|'+newName+'_mid_arm_jnt',newName+'_upperArmMid_bindJnt')
	
	cmds.select(newName+'_upperArmStart_bindJnt',newName+'_upperArmMid_bindJnt')
	cmds.select(newName+'upperArm_Curve',add=True)
	cmds.skinCluster(mi=2)
	
	#different z axis for right and left
	cmds.setAttr(newName+"upperArm_handle.dTwistControlEnable",1)
	cmds.setAttr(newName+"upperArm_handle.dWorldUpType",4)
	cmds.setAttr(newName+"upperArm_handle.dWorldUpAxis",4)
	cmds.setAttr(newName+"upperArm_handle.dWorldUpVectorY",0)
	cmds.setAttr(newName+"upperArm_handle.dWorldUpVectorZ",-1)  ##different for elft +1
	cmds.setAttr(newName+"upperArm_handle.dWorldUpVectorEndY",0)
	cmds.setAttr(newName+"upperArm_handle.dWorldUpVectorEndZ",-1)##+1
	
	cmds.connectAttr(newName+'_upperArmStart_bindJnt.worldMatrix[0]',newName+'upperArm_handle.dWorldUpMatrix', f=True)
	cmds.connectAttr(newName+'_upperArmMid_bindJnt.worldMatrix[0]', newName+'upperArm_handle.dWorldUpMatrixEnd',f=True)
	
### OPTIMIZE
	pointsDown= [[midArm[0], midArm[1], midArm[2]],
          [endArm[0], endArm[1],endArm[2]]]
	cmds.curve(ep=pointsDown, d=1) ##d=1 for 2cv points only
	cmds.rename('curve1', newName+'lowerArm_Curve')
	cmds.ikHandle(n=newName+'lowerArm_handle',sj=newName+'_mid_arm_jnt1',ee=newName+'_end_arm_jnt1',sol='ikSplineSolver',ccv=False,c=newName+'lowerArm_Curve')
	cmds.rename('effector1', newName+'lowerArm_effector')
	
	cmds.duplicate(newName+'_start_arm_jnt',n=newName+'_lowerArmStart_bindJnt')
	cmds.select(newName+'_lowerArmStart_bindJnt')
	cmds.pickWalk(d='down')
	cmds.parent(w=True)
	cmds.rename('|'+newName+'_mid_arm_jnt',newName+'_lowerArmMid_bindJnt')
	cmds.select(newName+'_lowerArmMid_bindJnt')
	cmds.pickWalk(d='down')
	cmds.rename(newName+'_lowerArmMid_bindJnt|'+newName+'_end_arm_jnt', newName+'_lowerArmEnd_bindJnt')
	cmds.parent(newName+'_lowerArmEnd_bindJnt',w=True)
	
	cmds.delete(newName+'_lowerArmStart_bindJnt',newName+'_lowerArmMid_bindJnt')
	cmds.select(newName+'_upperArmMid_bindJnt',newName+'_lowerArmEnd_bindJnt')
	cmds.select(newName+'lowerArm_Curve',add=True)
	cmds.skinCluster(mi=2)
	
	cmds.setAttr(newName+"lowerArm_handle.dTwistControlEnable", 1)
	cmds.setAttr(newName+"lowerArm_handle.dWorldUpType", 4)
	cmds.setAttr(newName+"lowerArm_handle.dWorldUpAxis", 4)
	cmds.setAttr(newName+"lowerArm_handle.dWorldUpVectorY", 0)
	cmds.setAttr(newName+"lowerArm_handle.dWorldUpVectorEndY", 0)
	cmds.setAttr(newName+"lowerArm_handle.dWorldUpVectorZ", -1)
	cmds.setAttr(newName+"lowerArm_handle.dWorldUpVectorEndZ", -1)
	
	cmds.connectAttr(newName+'_upperArmMid_bindJnt.worldMatrix[0]', newName+'lowerArm_handle.dWorldUpMatrix',f=True)
	cmds.connectAttr(newName+'_lowerArmEnd_bindJnt.worldMatrix[0]', newName+'lowerArm_handle.dWorldUpMatrixEnd', f=True)

	cmds.rename(newName+'_upperArmStart_bindJnt',newName+'_Start_bindJnt')
	cmds.rename(newName+'_upperArmMid_bindJnt',newName+'_Middle_bindJnt')
	cmds.rename(newName+'_lowerArmEnd_bindJnt',newName+'_End_bindJnt')

	cmds.parentConstraint(newName+'_end_arm_jnt',newName+'_End_bindJnt',mo=False, w=1)
	cmds.parentConstraint(newName+'_mid_arm_jnt',newName+'_Middle_bindJnt',mo=False, w=1)
	cmds.parentConstraint(newName+'_start_arm_jnt',newName+'_Start_bindJnt',mo=False, w=1)
	
	cmds.group(newName+'lowerArm_Curve',newName+'upperArm_Curve',newName+'lowerArm_handle',newName+'upperArm_handle',n=newName+'_arm_TwistGRP' )
	cmds.setAttr(newName+'_arm_TwistGRP.visibility',0)
	
###squash and stretch for the segmented joints
	cmds.shadingNode('curveInfo',au=True ,n='right_upperArm_length')
	cmds.shadingNode('multiplyDivide', au=True, n='right_upperArmNormDiv')
	cmds.connectAttr('rightupperArm_Curve.worldSpace[0]', 'right_upperArm_length.inputCurve', f=True)
	cmds.connectAttr('right_upperArm_length.arcLength', 'right_upperArmNormDiv.input1X')
	cmds.setAttr("right_upperArmNormDiv.operation", 2)
	cmds.setAttr("right_upperArmNormDiv.input2X", cmds.getAttr('right_upperArmNormDiv.input1X'))
	upperArmJnts=['right_start_arm_jnt1','r_b_midTwist','r_a_midTwist','r_c_midTwist']
	for i in upperArmJnts:
		cmds.connectAttr('right_upperArmNormDiv.outputX',i+'.scaleX',f=True)
		
	cmds.shadingNode('curveInfo',au=True ,n='right_lowerArm_length')
	cmds.shadingNode('multiplyDivide', au=True, n='right_lowerArmNormDiv')
	cmds.connectAttr('rightlowerArm_Curve.worldSpace[0]', 'right_lowerArm_length.inputCurve', f=True)
	cmds.connectAttr('right_lowerArm_length.arcLength', 'right_lowerArmNormDiv.input1X')
	cmds.setAttr("right_lowerArmNormDiv.operation", 2)
	cmds.setAttr("right_lowerArmNormDiv.input2X", cmds.getAttr('right_lowerArmNormDiv.input1X'))	
	lowerArmJnts=['right_mid_arm_jnt1', 'r_f_midTwist','r_e_midTwist','r_g_midTwist','r_h_midTwist']
	for i in lowerArmJnts:
		cmds.connectAttr('right_lowerArmNormDiv.outputX',i+'.scaleX',f=True)
	
###fk squash and stretch
	addFKlength=['right_start_arm_jnt_FK', 'right_mid_arm_jnt_FK ']
	for i in addFKlength:
		cmds.addAttr(i,ln="length", at='double', min=0, max=5, dv=1 )
		cmds.setAttr(i+'.length',e=True,keyable=True)
	cmds.setDrivenKeyframe('right_mid_arm_jnt_FK.translateX', cd='right_start_arm_jnt_FK.length')
	cmds.setDrivenKeyframe('right_end_arm_jnt_FK.translateX', cd='right_mid_arm_jnt_FK.length')
	cmds.setAttr('right_start_arm_jnt_FK.length',0)
	cmds.setAttr('right_mid_arm_jnt_FK.translateX',0)
	cmds.setDrivenKeyframe('right_mid_arm_jnt_FK.translateX', cd='right_start_arm_jnt_FK.length')
	cmds.setAttr('right_mid_arm_jnt_FK.length',0)
	cmds.setAttr('right_end_arm_jnt_FK.translateX',0)
	cmds.setDrivenKeyframe('right_end_arm_jnt_FK.translateX', cd='right_mid_arm_jnt_FK.length')
	
	cmds.setAttr('right_start_arm_jnt_FK.length',1)
	cmds.setAttr('right_mid_arm_jnt_FK.length',1)

##for ik	
	mel.eval('curve -d 1 -p -2.955302 0 -0.985101 -p -3 0 2 -p 2 0 2 -p 2 0 -1 -p -3 0 -1 -p -3 2 -1 -p -3 2 2 -p -3 0 2 -p -3 2 2 -p 2 2 2 -p 2 0 2 -p 2 2 2 -p 2 2 -1 -p 2 0 -1 -p 2 2 -1 -p -3 2 -1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 ;')
	cmds.rename('curve1', newName+'Arm_ctrl')
	cmds.xform(newName+'Arm_ctrl', cp=1)
	cmds.parentConstraint(newName+'_end_arm_jnt_IK',newName+'Arm_ctrl',mo=False, w=1)
	cmds.delete(newName+'Arm_ctrl_parentConstraint1')
	cmds.xform(newName+'Arm_ctrl',s=(5,5,5))
	cmds.setAttr(newName+'Arm_ctrl'+".overrideEnabled", 1)
	cmds.setAttr(newName+'Arm_ctrl'+".overrideColor", 6)	
	cmds.makeIdentity(newName+'Arm_ctrl',apply=True,t=1,r=1,s=0,n=0,pn=1)
	
	cmds.setAttr(newName+'_mid_arm_jnt_IK.rotateY',-10)
	cmds.joint(newName+'_mid_arm_jnt_IK',e=True,spa=True)
	cmds.setAttr(newName+'_mid_arm_jnt_IK.rotateY',0)	
	cmds.ikHandle(n=newName+'Arm_hdl',sj=newName+'_start_arm_jnt_IK',ee=newName+'_end_arm_jnt_IK',sol='ikRPsolver')
	cmds.ikHandle(n=newName+'hand_hdl',sj=newName+'_end_arm_jnt_IK',ee=newName+'_hand_jnt_IK',sol='ikSCsolver')
	
	#ik rotate is not moving the fk one responsible for the forearm twist!!
	cmds.parent(newName+'hand_hdl',newName+'Arm_hdl',newName+'Arm_ctrl')
	
##expression  
	mel.eval('distanceDimension -sp -1 0 0 -ep -0 0 0 ;')
	cmds.rename('locator1',newName+'Arm_IK_start')
	cmds.rename('locator2',newName+'Arm_IK_end')
	cmds.setAttr(newName+'Arm_IK_start.translate',stArm[0],stArm[1],stArm[2])
	cmds.setAttr(newName+'Arm_IK_end.translate',endArm[0],endArm[1],endArm[2])
	cmds.rename('distanceDimension1',newName+'_IK_armLength')
	cmds.parent(newName+'Arm_IK_end',newName+'Arm_ctrl')
	
	driver=newName+"_IK_armLengthShape.distance"
	rightUpperArmLength=cmds.getAttr(newName+'_mid_arm_jnt_IK.translateX')
	rightLowerArmLength=cmds.getAttr(newName+'_end_arm_jnt_IK.translateX')
	sumLengthR= rightUpperArmLength+rightLowerArmLength
	cmds.setDrivenKeyframe(newName+'_mid_arm_jnt_IK', cd=driver,dv=sumLengthR, at='translateX', v=rightUpperArmLength)
	cmds.setDrivenKeyframe(newName+'_mid_arm_jnt_IK', cd=driver,dv=sumLengthR*2, at='translateX', v=rightUpperArmLength*2)
	cmds.setDrivenKeyframe(newName+'_end_arm_jnt_IK', cd=driver,dv=sumLengthR, at='translateX', v=rightLowerArmLength)
	cmds.setDrivenKeyframe(newName+'_end_arm_jnt_IK', cd=driver,dv=sumLengthR*2, at='translateX', v=rightLowerArmLength*2)
	
	cmds.keyTangent(newName+'_mid_arm_jnt_IK',e=True,itt='spline',ott='spline', animation='objects')
	mel.eval('selectKey -add -k -f 150.782776 right_mid_arm_jnt_IK_translateX ;')
	cmds.setInfinity(poi='linear')
	
	cmds.keyTangent(newName+'_end_arm_jnt_IK',e=True,itt='spline',ott='spline', animation='objects')
	mel.eval('selectKey -add -k -f 150.782776 right_end_arm_jnt_IK_translateX ;')
	cmds.setInfinity(poi='linear')
	
	###snappable 
	cmds.spaceLocator(n=newName+'_elbow_loc',p=(midArm[0], midArm[1], midArm[2]-20))
	cmds.select(newName+'_elbow_loc')
	cmds.makeIdentity(apply=True,t=1,r=1,s=0,n=0,pn=1)
	cmds.xform(newName+'_elbow_loc', cp=1)
	cmds.poleVectorConstraint(newName+'_elbow_loc',newName+'Arm_hdl' )
	###
	mel.eval('curve -d 1 -p -3 0 0 -p 3 0 0 -p 0 0 5 -p -3 0 0 -k 0 -k 1 -k 2 -k 3 ;')
	cmds.rename('curve1', newName+'elbow_Ctrl')	
	cmds.setAttr(newName+'elbow_Ctrl.translate',midArm[0], midArm[1], midArm[2]-20)
	cmds.setAttr(newName+'elbow_Ctrl'+".overrideEnabled", 1)
	cmds.setAttr(newName+'elbow_Ctrl'+".overrideColor", 6)	
	cmds.xform(newName+'elbow_Ctrl',s=(2,2,2))
	cmds.makeIdentity(apply=True,t=1,r=1,s=0,n=0,pn=1)
	cmds.xform(newName+'elbow_Ctrl', cp=1)
	cmds.parent(newName+'_elbow_loc',newName+'elbow_Ctrl')	
	
	##snappable elbow
	mel.eval('distanceDimension -sp -1 0 0 -ep 0 0 0;')
	cmds.rename('locator1',newName+'_shoulderToElbow_start')
	cmds.rename('locator2',newName+'_shoulderToElbow_end')
	cmds.setAttr(newName+'_shoulderToElbow_start.translate',stArm[0],stArm[1],stArm[2])
	cmds.setAttr(newName+'_shoulderToElbow_end.translate',midArm[0],midArm[1],midArm[2]-20)
	cmds.rename('distanceDimension1',newName+'_upperArm_length')
	
	mel.eval('distanceDimension -sp -1 0 0 -ep 0 0 0;')
	cmds.rename('locator1',newName+'_elbowToWrist_start')
	cmds.rename('locator2',newName+'_elbowToWrist_end')
	cmds.setAttr(newName+'_elbowToWrist_start.translate',midArm[0],midArm[1],midArm[2]-20)
	cmds.setAttr(newName+'_elbowToWrist_end.translate',endArm[0],endArm[1],endArm[2])	
	cmds.rename('distanceDimension1',newName+'_lowerArm_length')
	
	cmds.parent(newName+'_shoulderToElbow_end',newName+'_elbowToWrist_start', newName+'elbow_Ctrl')	
	cmds.parent(newName+'_elbowToWrist_end',newName+'Arm_ctrl')
		
	cmds.addAttr(newName+'elbow_Ctrl',ln="Elbow_Snap", at='double', min=0, max=1, dv=0 )
	cmds.setAttr(newName+'elbow_Ctrl.Elbow_Snap',e=True,keyable=True)
	
	cmds.shadingNode('blendColors',au=True,n=newName+'UpperArm_stretch_Choice')
	cmds.shadingNode('blendColors',au=True,n=newName+'LowerArm_stretch_Choice')
	
	cmds.connectAttr(newName+'elbow_Ctrl.Elbow_Snap', newName+'UpperArm_stretch_Choice.blender',f=True)
	cmds.connectAttr(newName+'elbow_Ctrl.Elbow_Snap', newName+'LowerArm_stretch_Choice.blender',f=True)
	cmds.connectAttr(newName+'_upperArm_length1.distance', newName+'UpperArm_stretch_Choice.color1R',f=True)
	cmds.connectAttr(newName+'_mid_arm_jnt_IK_translateX.output', newName+'UpperArm_stretch_Choice.color2R', f=True)
	cmds.connectAttr(newName+'UpperArm_stretch_Choice.outputR',newName+'_mid_arm_jnt_IK.translateX',f=True)
	
	cmds.connectAttr(newName+'_lowerArm_length1.distance', newName+'LowerArm_stretch_Choice.color1R',f=True)
	cmds.connectAttr(newName+'_end_arm_jnt_IK_translateX.output',newName+'LowerArm_stretch_Choice.color2R',f=True)
	cmds.connectAttr(newName+'LowerArm_stretch_Choice.outputR', newName+'_end_arm_jnt_IK.translateX',f=True)

	#cleanup 
	cmds.addAttr(newName+'_Arm_settingsCTRL',ln="FK_visibility",at='bool')
	cmds.setAttr(newName+'_Arm_settingsCTRL.FK_visibility',e=True,keyable=True)
	cmds.addAttr(newName+'_Arm_settingsCTRL',ln="IK_visibility", at='bool')
	cmds.setAttr(newName+'_Arm_settingsCTRL.IK_visibility',e=True,keyable=True)
		
	cmds.connectAttr(newName+'_Arm_settingsCTRL.FK_visibility', newName+'_start_arm_jnt_FK.visibility',f=True)
	cmds.connectAttr(newName+'_Arm_settingsCTRL.IK_visibility', newName+'Arm_ctrl.visibility',f=True)

	#fk ON
	cmds.setAttr(newName+"_Arm_settingsCTRL.FK_IK_blend",0)
	cmds.setAttr(newName+"_Arm_settingsCTRL.FK_visibility",1)
	cmds.setAttr(newName+"_Arm_settingsCTRL.IK_visibility",0)
	cmds.setAttr(newName+"_start_arm_jnt_IK.visibility",0)
	cmds.setAttr(newName+'elbow_Ctrl.visibility',0)
	cmds.setDrivenKeyframe(newName+'_Arm_settingsCTRL.FK_visibility', currentDriver=newName+'_Arm_settingsCTRL.FK_IK_blend')
	cmds.setDrivenKeyframe(newName+'_Arm_settingsCTRL.IK_visibility', currentDriver=newName+'_Arm_settingsCTRL.FK_IK_blend')
	cmds.setDrivenKeyframe(newName+'_start_arm_jnt_IK.visibility', currentDriver=newName+'_Arm_settingsCTRL.FK_IK_blend')
	cmds.setDrivenKeyframe(newName+'elbow_Ctrl.visibility', currentDriver=newName+'_Arm_settingsCTRL.FK_IK_blend')

	#ik ON
	cmds.setAttr(newName+"_Arm_settingsCTRL.FK_IK_blend",1)
	cmds.setAttr(newName+"_Arm_settingsCTRL.FK_visibility",0)
	cmds.setAttr(newName+"_Arm_settingsCTRL.IK_visibility",1)
	cmds.setAttr(newName+"_start_arm_jnt_IK.visibility",1)
	cmds.setAttr(newName+'elbow_Ctrl.visibility',1)
	cmds.setDrivenKeyframe(newName+'_Arm_settingsCTRL.IK_visibility',currentDriver=newName+'_Arm_settingsCTRL.FK_IK_blend')
	cmds.setDrivenKeyframe(newName+'_Arm_settingsCTRL.FK_visibility',currentDriver=newName+'_Arm_settingsCTRL.FK_IK_blend')
	cmds.setDrivenKeyframe(newName+'_start_arm_jnt_IK.visibility',currentDriver=newName+'_Arm_settingsCTRL.FK_IK_blend')
	cmds.setDrivenKeyframe(newName+'elbow_Ctrl.visibility', currentDriver=newName+'_Arm_settingsCTRL.FK_IK_blend')
	##fk elbow control  if it doesnt work skip it do it later
	
	'''
	#run the code manually otherwise doesnt work
	cmds.setAttr(newName+"_Arm_settingsCTRL.FK_IK_blend", 0)
	cmds.duplicate(newName+'_mid_arm_jnt_FK',n=newName+'_mid_arm_jnt_elbowFK')
	cmds.parent(newName+'_mid_arm_jnt_elbowFK',w=True)
	cmds.rename(newName+'_mid_arm_jnt_elbowFK|'+newName+'_end_arm_jnt_FK', newName+'_end_arm_jnt_elbowFK')
	cmds.rename(newName+'_end_arm_jnt_elbowFK|'+newName+'_hand_jnt_FK', newName+'_hand_jnt_elbowFK')
	cmds.setAttr(newName+"_Arm_settingsCTRL.FK_IK_blend", 1)
	cmds.setAttr(newName+"elbow_Ctrl.Elbow_Snap", 1)
	cmds.xform(newName+'_mid_arm_jnt_elbowFK', t=(midArm[0],midArm[1],midArm[2]-20))	
	cmds.parent(newName+'_mid_arm_jnt_elbowFK',newName+'elbow_Ctrl')
	cmds.group('rightArm_IK_end','rightArm_hdl','right_elbowToWrist_end', n='rightArm_IK_constGRP')
	endArm=[cmds.getAttr('right_end_arm.translateX'), cmds.getAttr('right_end_arm.translateY'), cmds.getAttr('right_end_arm.translateZ')]			
	cmds.move(endArm[0],endArm[1],endArm[2], 'rightArm_IK_constGRP.scalePivot', 'rightArm_IK_constGRP.rotatePivot',rpr=True)
	cmds.parent('rightArm_IK_constGRP',w=True)
	cmds.parentConstraint('rightArm_ctrl','rightArm_IK_constGRP',mo=True, w=1)
	cmds.parentConstraint('right_end_arm_jnt_elbowFK','rightArm_IK_constGRP',mo=False, w=1)
	mel.eval('addAttr -ln "right_elbow_blend"  -at double  -min 0 -max 1 -dv 0 |rightelbow_Ctrl;')
	mel.eval('setAttr -e-keyable true |rightelbow_Ctrl.right_elbow_blend;')
	cmds.setAttr(newName+"Arm_IK_constGRP_parentConstraint1."+newName+"Arm_ctrlW0",1)
	cmds.setAttr(newName+"Arm_IK_constGRP_parentConstraint1."+newName+"_end_arm_jnt_elbowFKW1", 0)
	cmds.setDrivenKeyframe(newName+'Arm_IK_constGRP_parentConstraint1.'+newName+'Arm_ctrlW0',
							newName+'Arm_IK_constGRP_parentConstraint1.'+newName+'_end_arm_jnt_elbowFKW1'
							,cd=newName+'elbow_Ctrl.'+newName+'_elbow_blend')
	cmds.setAttr(newName+"elbow_Ctrl.right_elbow_blend",1)	
	cmds.setAttr(newName+"Arm_IK_constGRP_parentConstraint1."+newName+"Arm_ctrlW0",0)
	cmds.setAttr(newName+"Arm_IK_constGRP_parentConstraint1."+newName+"_end_arm_jnt_elbowFKW1", 1)
	cmds.setDrivenKeyframe(newName+'Arm_IK_constGRP_parentConstraint1.'+newName+'Arm_ctrlW0',
							newName+'Arm_IK_constGRP_parentConstraint1.'+newName+'_end_arm_jnt_elbowFKW1'
							,cd=newName+'elbow_Ctrl.'+newName+'_elbow_blend')
	mel.eval('addAttr -ln "foreArm_Fk_visibility"  -at bool |'+newName+'elbow_Ctrl;')
	mel.eval('setAttr -e-keyable true |'+newName+'elbow_Ctrl.foreArm_Fk_visibility;')
	cmds.setAttr(newName+"elbow_Ctrl.foreArm_Fk_visibility", 1)
	mel.eval('connectAttr -f rightelbow_Ctrl.foreArm_Fk_visibility right_mid_arm_jnt_elbowFK.visibility;')
	cmds.setDrivenKeyframe('rightelbow_Ctrl.foreArm_Fk_visibility',cd='rightelbow_Ctrl.right_elbow_blend')
		
	cmds.group(newName+'Arm_ctrl', n=newName+'Arm_IK_vis_grp')	
	cmds.setAttr(newName+'Arm_IK_vis_grp.visibility',1)
	cmds.connectAttr(newName+'_Arm_settingsCTRL.IK_visibility', newName+'Arm_IK_vis_grp.visibility',f=True)
	cmds.disconnectAttr(newName+'_Arm_settingsCTRL.IK_visibility', newName+'Arm_ctrl.visibility')
	#cmds.setAttr("elbow_Ctrl.right_elbow_blend", 1)
	#cmds.setAttr("rightArm_ctrl.visibility", 0)
	#cmds.setDrivenKeyframe('rightArm_ctrl.visibility', cd='elbow_Ctrl.right_elbow_blend')
	#cmds.setAttr("elbow_Ctrl.right_elbow_blend", 0)
	#cmds.setAttr("rightArm_ctrl.visibility", 1)
	#cmds.setDrivenKeyframe('rightArm_ctrl.visibility', cd='elbow_Ctrl.right_elbow_blend')
	cmds.setAttr(newName+"elbow_Ctrl."+newName+"_elbow_blend",1)
	###lock and hide
	for i in attr:
		cmds.setAttr(newName+'Arm_IK_vis_grp'+i,l=True)
	cmds.select(clear=True)
	#there is more to do...
	'''
	
	###do the clavicle  
	cmds.joint(p=(stArm[0]+10, stArm[1]-5,stArm[2]),n=newName+'_sh_jnt_Start')
	cmds.joint(p=(stArm[0], stArm[1],stArm[2]),n=newName+'_sh_jnt_End')
	cmds.joint(newName+'_sh_jnt_Start',e=True,oj='xyz',sao='yup',ch=True,zso=True)
	cmds.ikHandle(n=newName+'_IK_sh_handle',sj=newName+'_sh_jnt_Start',ee=newName+'_sh_jnt_End',sol='ikSCsolver')
	cmds.rename('effector1', newName+'_sh_eff')
	cmds.spaceLocator(n=newName+'_sh_loc')	
	cmds.setAttr(newName+'_sh_loc.translate',stArm[0], stArm[1], stArm[2])
	cmds.makeIdentity(newName+'_sh_loc',apply=True,t=1,r=1,s=0,n=0,pn=1)
	cmds.xform(newName+'_sh_loc', cp=1)
	cmds.parent(newName+'_IK_sh_handle',newName+'_sh_loc')
	
	mel.eval('distanceDimension -sp -1 0 0 -ep 0 0 0;')
	cmds.rename('locator1',newName+'_sh_start')
	cmds.rename('locator2',newName+'_sh_end')
	cmds.setAttr(newName+'_sh_start.translate',stArm[0]+10,stArm[1]-5,stArm[2])
	cmds.setAttr(newName+'_sh_end.translate',stArm[0],stArm[1],stArm[2])	
	cmds.rename('distanceDimension1',newName+'_sh_length')
	cmds.parent(newName+'_sh_end',newName+'_sh_loc')
	
	###expression 
	naturalLength=cmds.getAttr(newName+'_sh_jnt_End.translateX')
	cmds.setDrivenKeyframe(newName+'_sh_jnt_End', cd=newName+"_sh_lengthShape.distance",dv=naturalLength, at='translateX', v=naturalLength)
	cmds.setDrivenKeyframe(newName+'_sh_jnt_End', cd=newName+"_sh_lengthShape.distance",dv=naturalLength*2, at='translateX', v=naturalLength*2)
	
	cmds.keyTangent(newName+'_sh_jnt_End',e=True,itt='spline',ott='spline', animation='objects')
	mel.eval('selectKey -add -k -f 22.36068 right_sh_jnt_End_translateX ;')
	cmds.setInfinity(poi='linear')
	
	###
	mel.eval('circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 0.01 -s 8 -ch 1;')
	cmds.rename('nurbsCircle1', newName+'_shoulder_ctrl')	
	cmds.setAttr(newName+'_shoulder_ctrl.translate', stArm[0],stArm[1]+20,stArm[2])
	cmds.setAttr(newName+'_shoulder_ctrl.scale', 5,5,5)
	cmds.setAttr(newName+'_shoulder_ctrl.rotate', 0,0,20)
	cmds.makeIdentity(newName+'_shoulder_ctrl',apply=True,t=1,r=1,s=0,n=0,pn=1)
	cmds.xform(newName+'_shoulder_ctrl', cp=1)
	#mel.eval('move -r 0 -20 0 right_shoulder_ctrl.scalePivot right_shoulder_ctrl.rotatePivot ;')
	cmds.parent(newName+'_sh_loc',newName+'_shoulder_ctrl') 
	cmds.setAttr(newName+'_shoulder_ctrl'+".overrideEnabled", 1)
	cmds.setAttr(newName+'_shoulder_ctrl'+".overrideColor", 6)	
	
	##lock all the values but translate
	attr2=['.rx','.ry','.rz','.sx','.sy','.sz']
	for i in attr2:
		cmds.setAttr(newName+'_shoulder_ctrl'+i,l=True)
	
	##shoulderVisibility
	cmds.addAttr(newName+'_Arm_settingsCTRL',ln="Shoulder_visibility", at='bool' )
	cmds.setAttr(newName+'_Arm_settingsCTRL.Shoulder_visibility',e=True,keyable=True)
	cmds.connectAttr(newName+'_Arm_settingsCTRL.Shoulder_visibility', newName+'_shoulder_ctrl.visibility',f=True)
	
	##hide all stuff
	listHide=(newName+'_lowerArm_length1',newName+'_upperArm_length1',newName+'_sh_length',newName+'_shoulderToElbow_start',newName+'_IK_armLength',
				newName+'Arm_IK_start',newName+'_sh_start')
	for item in listHide:
		cmds.setAttr(item+'.v',0)
	
	cmds.group(newName+'_sh_jnt_Start', newName+'_sh_start', newName+'_sh_length', newName+'_shoulder_ctrl',n=newName+'_shoulder_grp')
	cmds.parent(newName+'_shoulder_grp','pirate_Root_Transform')
	cmds.group(newName+'_sh_start', newName+'_sh_length',newName+'_sh_jnt_Start', n=newName+'DO_NOT_GRP')
	mel.eval('move -rpr 0 223 7 right_shoulder_grp.scalePivot right_shoulder_grp.rotatePivot;')

	cmds.parentConstraint('sh_bind_jnt',newName+'_shoulder_grp',mo=True, w=1)
	cmds.group(newName+'_start_arm_jnt1', newName+'_mid_arm_jnt1', newName+'_Start_bindJnt', newName+'_Middle_bindJnt',
				newName+'_End_bindJnt', newName+'_arm_TwistGRP', newName+'Arm_IK_start', newName+'_IK_armLength', newName+'elbow_Ctrl',
				newName+'_shoulderToElbow_start', newName+'_upperArm_length', newName+'_lowerArm_length', 
				 newName+'_start_arm_jnt_IK', newName+'_start_arm_jnt_FK', newName+'_start_arm_jnt' ,
				n=newName+'_Arm_GRP') #newName+'Arm_IK_constGRP', newName+'Arm_IK_vis_grp',
	cmds.parent(newName+'_Arm_GRP','pirate_Root_Transform')
	
	cmds.group(newName+'_start_arm_jnt', newName+'_start_arm_jnt_IK',
			newName+'_lowerArm_length', newName+'_upperArm_length', newName+'_shoulderToElbow_start',
			newName+'_IK_armLength', newName+'Arm_IK_start', newName+'_arm_TwistGRP', newName+'_End_bindJnt', 
			newName+'_Middle_bindJnt', newName+'_Start_bindJnt', newName+'_mid_arm_jnt1', newName+'_start_arm_jnt1', n=newName+'DO_NOt_touch_grp')
	#newName+'Arm_IK_constGRP',
	cmds.group(newName+'_start_arm_jnt_IK', newName+'_shoulderToElbow_start', newName+'Arm_IK_start', n=newName+'ArmBase_IkConst_Grp')
	mel.eval('move -rpr -26 192 3 rightArmBase_IkConst_Grp.scalePivot rightArmBase_IkConst_Grp.rotatePivot ;')
	
	cmds.spaceLocator(n=newName+'_shoulderSpace_locator',p=(stArm[0], stArm[1], stArm[2]))
	cmds.select(newName+'_shoulderSpace_locator')
	mel.eval('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;')
	cmds.xform(newName+'_shoulderSpace_locator',cp=True)
	
	cmds.parent(newName+'_shoulderSpace_locator',newName+'_sh_jnt_End')
	cmds.pointConstraint(newName+'_shoulderSpace_locator', newName+'ArmBase_IkConst_Grp' ,mo=True, weight=1)
	
	cmds.group(newName+'_start_arm_jnt', n=newName+'Arm_resultConst_GRP')
	mel.eval('move -rpr -26 192 3 rightArm_resultConst_GRP.scalePivot rightArm_resultConst_GRP.rotatePivot ;')
	cmds.pointConstraint(newName+'_shoulderSpace_locator', newName+'Arm_resultConst_GRP' ,mo=True, weight=1)
	##point constrain the new grps to the locators
	
	
	cmds.setAttr(newName+"_Arm_settingsCTRL.FK_IK_blend",0)
	cmds.setAttr(newName+"elbow_Ctrl.Elbow_Snap", 0)
	#cmds.setAttr(newName+"elbow_Ctrl.right_elbow_blend",0)
	#cmds.setAttr(newName+"elbow_Ctrl.foreArm_Fk_visibility",0)

	
	mel.eval('circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 0.01 -s 8 -ch 1;')
	mel.eval('circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 0.01 -s 8 -ch 1;')
	mel.eval('scale -r 0.363108 0.363108 0.363108 ;')
	mel.eval('move -rpr -z -1 ;')
	cmds.select('nurbsCircle1','nurbsCircle2')
	mel.eval('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;')
	cmds.parent('nurbsCircleShape2', 'nurbsCircle1',r=True, s=True)
	cmds.delete('nurbsCircle2')
	cmds.rename('nurbsCircle1', newName+'Arm_gimbal_Corr_Ctrl')
	cmds.setAttr(newName+'Arm_gimbal_Corr_Ctrl.translate',stArm[0],stArm[1], stArm[2])
	cmds.setAttr(newName+'Arm_gimbal_Corr_Ctrl.scale',12,12,12)
	cmds.setAttr(newName+'Arm_gimbal_Corr_Ctrl.rotate',90,90,0)
	cmds.select(newName+'Arm_gimbal_Corr_Ctrl')
	mel.eval('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;')
	cmds.parent(newName+'Arm_gimbal_Corr_Ctrl', newName+'_Arm_GRP')
	cmds.parent(newName+'_start_arm_jnt_FK',newName+'Arm_gimbal_Corr_Ctrl')
	cmds.select(newName+'_start_arm_jnt')
	mel.eval('doGroup 0 0 1;')
	cmds.rename('group1',newName+'Arm_resultGimbal_GRP')
	mel.eval('move -rpr -26 192 3 rightArm_resultGimbal_GRP.scalePivot rightArm_resultGimbal_GRP.rotatePivot ;')
	cmds.shadingNode('blendColors',au=True ,n=newName+'Arm_gimbalCorrToggle')
	cmds.connectAttr(newName+'Arm_gimbal_Corr_Ctrl.rotate', newName+'Arm_gimbalCorrToggle.color2',f=True)
	cmds.setAttr(newName+"Arm_gimbalCorrToggle.color1R", 0)
	cmds.connectAttr(newName+'Arm_gimbalCorrToggle.output', newName+'Arm_resultGimbal_GRP.rotate',f=True )
	cmds.connectAttr(newName+'_Arm_settingsCTRL.FK_IK_blend', newName+'Arm_gimbalCorrToggle.blender', f=True)
	cmds.connectAttr(newName+'_Arm_settingsCTRL.FK_visibility', newName+'Arm_gimbal_Corr_Ctrl.visibility', f=True)
	cmds.group(newName+'Arm_gimbal_Corr_Ctrl', n=newName+'Arm_FKConst_GRP')
	mel.eval('move -rpr -26 192 3 rightArm_FKConst_GRP.scalePivot rightArm_FKConst_GRP.rotatePivot ;')
	cmds.pointConstraint(newName+'_shoulderSpace_locator', newName+'Arm_FKConst_GRP', mo=True, weight=1)
	cmds.duplicate(newName+'_shoulderSpace_locator', n=newName+'_ArmBodySpace_locator' )
	cmds.duplicate(newName+'_shoulderSpace_locator', n=newName+'_ArmRootSpace_locator')
	cmds.parent(newName+'_ArmBodySpace_locator', 'DO_NOT_TOUCH')
	cmds.parent(newName+'_ArmRootSpace_locator', 'pirate_Root_Transform')
	cmds.select(newName+'_ArmBodySpace_locator',newName+'_ArmRootSpace_locator', newName+'_shoulderSpace_locator', newName+'Arm_FKConst_GRP' )
	mel.eval('orientConstraint -offset 0 0 0 -weight 1;')
	cmds.select(clear=True)
	cmds.select(newName+'_ArmBodySpace_locator',newName+'_ArmRootSpace_locator', newName+'_shoulderSpace_locator', newName+'Arm_resultConst_GRP' )
	mel.eval('orientConstraint -offset 0 0 0 -weight 1;')
	mel.eval('addAttr -ln "FK_rotationSpace"  -at "enum" -en "shoulder:upperBody:root:"  |rightA_settings_GRP|right_Arm_settingsCTRL;')
	mel.eval('setAttr -e-keyable true |rightA_settings_GRP|right_Arm_settingsCTRL.FK_rotationSpace;')


	##### OPTIMIZEEE
	listOrient=[newName+'Arm_resultConst_GRP_orientConstraint1',newName+'Arm_FKConst_GRP_orientConstraint1']
	#for item in listOrient:
	cmds.setAttr(newName+"_Arm_settingsCTRL.FK_rotationSpace",0)
	cmds.setAttr(listOrient[0]+'.'+newName+'_shoulderSpace_locatorW2',1)
	cmds.setAttr(listOrient[0]+'.'+newName+'_ArmBodySpace_locatorW0',0)
	cmds.setAttr(listOrient[0]+'.'+newName+'_ArmRootSpace_locatorW1',0)
	cmds.setAttr(listOrient[1]+'.'+newName+'_shoulderSpace_locatorW2',1)
	cmds.setAttr(listOrient[1]+'.'+newName+'_ArmBodySpace_locatorW0',0)
	cmds.setAttr(listOrient[1]+'.'+newName+'_ArmRootSpace_locatorW1',0)
		
		#change to cmds
	mel.eval('setDrivenKeyframe -currentDriver right_Arm_settingsCTRL.FK_rotationSpace rightArm_FKConst_GRP_orientConstraint1.right_shoulderSpace_locatorW2;')
	mel.eval('setDrivenKeyframe -currentDriver right_Arm_settingsCTRL.FK_rotationSpace rightArm_resultConst_GRP_orientConstraint1.right_shoulderSpace_locatorW2;')
	mel.eval('setDrivenKeyframe -currentDriver right_Arm_settingsCTRL.FK_rotationSpace rightArm_FKConst_GRP_orientConstraint1.right_ArmBodySpace_locatorW0;')
	mel.eval('setDrivenKeyframe -currentDriver right_Arm_settingsCTRL.FK_rotationSpace rightArm_resultConst_GRP_orientConstraint1.right_ArmBodySpace_locatorW0;')
	mel.eval('setDrivenKeyframe -currentDriver right_Arm_settingsCTRL.FK_rotationSpace rightArm_FKConst_GRP_orientConstraint1.right_ArmRootSpace_locatorW1;')
	mel.eval('setDrivenKeyframe -currentDriver right_Arm_settingsCTRL.FK_rotationSpace rightArm_resultConst_GRP_orientConstraint1.right_ArmRootSpace_locatorW1;')
	
	cmds.setAttr("right_Arm_settingsCTRL.FK_rotationSpace",1)
	cmds.setAttr(listOrient[0]+'.'+newName+'_shoulderSpace_locatorW2',0)
	cmds.setAttr(listOrient[0]+'.'+newName+'_ArmBodySpace_locatorW0',1)
	cmds.setAttr(listOrient[0]+'.'+newName+'_ArmRootSpace_locatorW1',0)
	cmds.setAttr(listOrient[1]+'.'+newName+'_shoulderSpace_locatorW2',0)
	cmds.setAttr(listOrient[1]+'.'+newName+'_ArmBodySpace_locatorW0',1)
	cmds.setAttr(listOrient[1]+'.'+newName+'_ArmRootSpace_locatorW1',0)
	
	mel.eval('setDrivenKeyframe -currentDriver right_Arm_settingsCTRL.FK_rotationSpace rightArm_FKConst_GRP_orientConstraint1.right_shoulderSpace_locatorW2;')
	mel.eval('setDrivenKeyframe -currentDriver right_Arm_settingsCTRL.FK_rotationSpace rightArm_resultConst_GRP_orientConstraint1.right_shoulderSpace_locatorW2;')
	mel.eval('setDrivenKeyframe -currentDriver right_Arm_settingsCTRL.FK_rotationSpace rightArm_FKConst_GRP_orientConstraint1.right_ArmBodySpace_locatorW0;')
	mel.eval('setDrivenKeyframe -currentDriver right_Arm_settingsCTRL.FK_rotationSpace rightArm_resultConst_GRP_orientConstraint1.right_ArmBodySpace_locatorW0;')
	mel.eval('setDrivenKeyframe -currentDriver right_Arm_settingsCTRL.FK_rotationSpace rightArm_FKConst_GRP_orientConstraint1.right_ArmRootSpace_locatorW1;')
	mel.eval('setDrivenKeyframe -currentDriver right_Arm_settingsCTRL.FK_rotationSpace rightArm_resultConst_GRP_orientConstraint1.right_ArmRootSpace_locatorW1;')

		
		#change to cmds
	cmds.setAttr("right_Arm_settingsCTRL.FK_rotationSpace",2)
	cmds.setAttr(listOrient[0]+'.'+newName+'_shoulderSpace_locatorW2',0)
	cmds.setAttr(listOrient[0]+'.'+newName+'_ArmBodySpace_locatorW0',0)
	cmds.setAttr(listOrient[0]+'.'+newName+'_ArmRootSpace_locatorW1',0)
	cmds.setAttr(listOrient[1]+'.'+newName+'_shoulderSpace_locatorW2',0)
	cmds.setAttr(listOrient[1]+'.'+newName+'_ArmBodySpace_locatorW0',0)
	cmds.setAttr(listOrient[1]+'.'+newName+'_ArmRootSpace_locatorW1',1)

	#change to cmds
	mel.eval('setDrivenKeyframe -currentDriver right_Arm_settingsCTRL.FK_rotationSpace rightArm_FKConst_GRP_orientConstraint1.right_shoulderSpace_locatorW2;')
	mel.eval('setDrivenKeyframe -currentDriver right_Arm_settingsCTRL.FK_rotationSpace rightArm_resultConst_GRP_orientConstraint1.right_shoulderSpace_locatorW2;')
	mel.eval('setDrivenKeyframe -currentDriver right_Arm_settingsCTRL.FK_rotationSpace rightArm_FKConst_GRP_orientConstraint1.right_ArmBodySpace_locatorW0;')
	mel.eval('setDrivenKeyframe -currentDriver right_Arm_settingsCTRL.FK_rotationSpace rightArm_resultConst_GRP_orientConstraint1.right_ArmBodySpace_locatorW0;')
	mel.eval('setDrivenKeyframe -currentDriver right_Arm_settingsCTRL.FK_rotationSpace rightArm_FKConst_GRP_orientConstraint1.right_ArmRootSpace_locatorW1;')
	mel.eval('setDrivenKeyframe -currentDriver right_Arm_settingsCTRL.FK_rotationSpace rightArm_resultConst_GRP_orientConstraint1.right_ArmRootSpace_locatorW1;')
	##ne raboti 
	
	###check connections
	cmds.setAttr(newName+"upperArm_Curve.inheritsTransform", 0)
	cmds.setAttr(newName+"lowerArm_Curve.inheritsTransform", 0)
	
	mel.eval('shadingNode -asUtility blendColors;')
	cmds.rename('blendColors1',newName+'_resultArmOrientChoice')
	cmds.connectAttr(newName+'Arm_resultConst_GRP_orientConstraint1.constraintRotate', newName+'_resultArmOrientChoice.color2')
	cmds.setAttr(newName+"_resultArmOrientChoice.color1R",0)
	cmds.connectAttr(newName+'_resultArmOrientChoice.output', newName+'Arm_resultConst_GRP.rotate',f=True)
	cmds.connectAttr(newName+'_Arm_settingsCTRL.FK_IK_blend', newName+'_resultArmOrientChoice.blender',f=True)

	cmds.shadingNode('multiplyDivide',au=True ,n=newName+'_globalScale_rightArm_normalize_DIV')
	cmds.shadingNode('multiplyDivide',au=True ,n=newName+'_globalScale_rightShoulder_normalize_DIV')
	
	cmds.connectAttr( 'pirate_Root_Transform.scaleX', newName+'_globalScale_rightArm_normalize_DIV.input2X',f=True)
	cmds.connectAttr( 'pirate_Root_Transform.scaleX', newName+'_globalScale_rightShoulder_normalize_DIV.input2X',f=True)   ####
	cmds.connectAttr( 'right_IK_armLengthShape.distance',newName+'_globalScale_rightArm_normalize_DIV.input1X', f=True)
	cmds.connectAttr( 'right_sh_lengthShape.distance', newName+'_globalScale_rightShoulder_normalize_DIV.input1X',f=True)

	cmds.setAttr(newName+"_globalScale_rightArm_normalize_DIV.operation",2)
	cmds.setAttr(newName+"_globalScale_rightShoulder_normalize_DIV.operation",2)

	cmds.connectAttr( newName+'_globalScale_rightArm_normalize_DIV.outputX', newName+'_end_arm_jnt_IK_translateX.input',f=True)
	cmds.connectAttr( newName+'_globalScale_rightArm_normalize_DIV.outputX', newName+'_mid_arm_jnt_IK_translateX.input',f=True)
	cmds.connectAttr( newName+'_globalScale_rightShoulder_normalize_DIV.outputX', newName+'_sh_jnt_End_translateX.input', f=True)

	#do the same for the snap elbow jnts and segmented joints 
	
	cmds.shadingNode('multiplyDivide',au=True ,n=newName+'_globalScale_rightElbow_to_hand_normalize_DIV')
	cmds.setAttr("right_globalScale_rightElbow_to_hand_normalize_DIV.operation", 2)
	cmds.connectAttr('right_lowerArm_length1.distance', 'right_globalScale_rightElbow_to_hand_normalize_DIV.input1X', f=True)
	cmds.connectAttr('pirate_Root_Transform.scaleY', 'right_globalScale_rightElbow_to_hand_normalize_DIV.input2X',f=True)
	cmds.connectAttr('right_globalScale_rightElbow_to_hand_normalize_DIV.outputX', 'rightLowerArm_stretch_Choice.color1R', f=True)

	cmds.shadingNode('multiplyDivide',au=True ,n=newName+'_globalScale_rightUpperArm_to_elbow_normalize_DIV')
	cmds.setAttr(newName+"_globalScale_rightUpperArm_to_elbow_normalize_DIV.operation", 2)
	cmds.connectAttr('right_upperArm_length1.distance', 'right_globalScale_rightUpperArm_to_elbow_normalize_DIV.input1X', f=True)
	cmds.connectAttr('pirate_Root_Transform.scaleY', 'right_globalScale_rightUpperArm_to_elbow_normalize_DIV.input2X',f=True)
	cmds.connectAttr('right_globalScale_rightUpperArm_to_elbow_normalize_DIV.outputX', 'rightUpperArm_stretch_Choice.color1R', f=True)

### segmented joints lower arm jnts global scale
	cmds.shadingNode('multiplyDivide',au=True ,n=newName+'_globalScale_rightForeArm_normalize_DIV')
	cmds.setAttr(newName+"_globalScale_rightForeArm_normalize_DIV.operation", 2)
	
	cmds.connectAttr( newName+'_upperArmNormDiv.output', newName+"_globalScale_rightForeArm_normalize_DIV.input1", f=True)
	cmds.connectAttr( 'pirate_Root_Transform.scale', newName+"_globalScale_rightForeArm_normalize_DIV.input2", f=True)
	

### segmented joints upper arm jnts 
	cmds.shadingNode('multiplyDivide',au=True ,n=newName+'_globalScale_rightLowerArm_normalize_DIV')
	cmds.setAttr(newName+"_globalScale_rightLowerArm_normalize_DIV.operation", 2)
	
	cmds.connectAttr( newName+'_lowerArmNormDiv.output', newName+"_globalScale_rightLowerArm_normalize_DIV.input1", f=True)
	cmds.connectAttr( 'pirate_Root_Transform.scale', newName+"_globalScale_rightLowerArm_normalize_DIV.input2", f=True)
	
	cmds.delete('right_end_arm_jnt1')
	cmds.connectAttr(newName+'_globalScale_rightLowerArm_normalize_DIV.outputX', 'right_mid_arm_jnt1.scaleX', f=True)
	cmds.connectAttr(newName+'_globalScale_rightLowerArm_normalize_DIV.outputX', 'r_f_midTwist.scaleX', f=True)
	cmds.connectAttr(newName+'_globalScale_rightLowerArm_normalize_DIV.outputX', 'r_e_midTwist.scaleX', f=True)
	cmds.connectAttr(newName+'_globalScale_rightLowerArm_normalize_DIV.outputX', 'r_g_midTwist.scaleX', f=True)
	cmds.connectAttr(newName+'_globalScale_rightLowerArm_normalize_DIV.outputX', 'r_h_midTwist.scaleX', f=True)
	
	cmds.connectAttr(newName+'_globalScale_rightForeArm_normalize_DIV.outputX', 'right_start_arm_jnt1.scaleX', f=True)
	cmds.connectAttr(newName+'_globalScale_rightForeArm_normalize_DIV.outputX', 'r_b_midTwist.scaleX', f=True)
	cmds.connectAttr(newName+'_globalScale_rightForeArm_normalize_DIV.outputX', 'r_a_midTwist.scaleX', f=True)
	cmds.connectAttr(newName+'_globalScale_rightForeArm_normalize_DIV.outputX', 'r_c_midTwist.scaleX', f=True)
	cmds.connectAttr(newName+'_globalScale_rightForeArm_normalize_DIV.outputX', 'r_d_midTwist.scaleX', f=True)
	
	cmds.parent(newName+'Arm_ctrl', newName+'_Arm_GRP')
	cmds.parent(newName+'_upperArm_length1',newName+'_lowerArm_length1',newName+'_Arm_GRP')
	
	attrRot=['.tx','.ty','.tz','.sx','.sy','.sz','.v']
	attrS=['.sx','.sy','.sz','.v']
	for i in attrRot:
		for k in armFK:
			cmds.setAttr(k+i, l=True)
	for i in attrS:
		cmds.setAttr('rightArm_ctrl'+i, l=True)
		
	cmds.select(clear=True)
	fingers('right',endArm)
	
	
def leftClavicle():
	newName='left'
	cmds.joint(p=(16, 187,3),n=newName+'_sh_jnt_Start')
	cmds.joint(p=(28.747,192.73,5.126),n=newName+'_sh_jnt_End')
	cmds.joint(newName+'_sh_jnt_Start',e=True,oj='xyz',sao='yup',ch=True,zso=True)
	cmds.ikHandle(n=newName+'_IK_sh_handle',sj=newName+'_sh_jnt_Start',ee=newName+'_sh_jnt_End',sol='ikSCsolver')
	cmds.spaceLocator(n=newName+'_sh_loc')	
	cmds.setAttr(newName+'_sh_loc.translate',28.747,192.73,5.126)
	cmds.makeIdentity(newName+'_sh_loc',apply=True,t=1,r=1,s=0,n=0,pn=1)
	cmds.xform(newName+'_sh_loc', cp=1)
	cmds.parent(newName+'_IK_sh_handle',newName+'_sh_loc')
	
	mel.eval('distanceDimension -sp -1 0 0 -ep 0 0 0;')
	cmds.rename('locator1',newName+'_sh_start')
	cmds.rename('locator2',newName+'_sh_end')
	cmds.setAttr(newName+'_sh_start.translate',16, 187,3)
	cmds.setAttr(newName+'_sh_end.translate',28.747,192.73,5.126)	
	cmds.rename('distanceDimension1',newName+'_sh_length')
	cmds.parent(newName+'_sh_end',newName+'_sh_loc')
	
	###expression 
	naturalLength=cmds.getAttr(newName+'_sh_jnt_End.translateX')
	cmds.setDrivenKeyframe(newName+'_sh_jnt_End', cd=newName+"_sh_lengthShape.distance",dv=naturalLength, at='translateX', v=naturalLength)
	cmds.setDrivenKeyframe(newName+'_sh_jnt_End', cd=newName+"_sh_lengthShape.distance",dv=naturalLength*2, at='translateX', v=naturalLength*2)
	
	cmds.keyTangent(newName+'_sh_jnt_End',e=True,itt='spline',ott='spline', animation='objects')
	mel.eval('selectKey -add -k -f 14.53004 left_sh_jnt_End_translateX ;')
	cmds.setInfinity(poi='linear')

	###
	mel.eval('circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 0.01 -s 8 -ch 1;')
	cmds.rename('nurbsCircle1', newName+'_shoulder_ctrl')	
	cmds.setAttr(newName+'_shoulder_ctrl.translate', 28.747,192.73+20,5.126)
	cmds.setAttr(newName+'_shoulder_ctrl.scale', 5,5,5)
	cmds.setAttr(newName+'_shoulder_ctrl.rotate', 0,0,-20)
	cmds.makeIdentity(newName+'_shoulder_ctrl',apply=True,t=1,r=1,s=0,n=0,pn=1)
	cmds.xform(newName+'_shoulder_ctrl', cp=1)
	#mel.eval('move -r 0 -20 0 right_shoulder_ctrl.scalePivot right_shoulder_ctrl.rotatePivot ;')
	cmds.parent(newName+'_sh_loc',newName+'_shoulder_ctrl') 
	cmds.setAttr(newName+'_shoulder_ctrl'+".overrideEnabled", 1)
	cmds.setAttr(newName+'_shoulder_ctrl'+".overrideColor", 4)	
	
	##lock all the values but translate
	attr2=['.rx','.ry','.rz','.sx','.sy','.sz']
	for i in attr2:
		cmds.setAttr(newName+'_shoulder_ctrl'+i,l=True)
	
	##shoulderVisibility
	cmds.addAttr('_Tentacle_settingsCTRL',ln="Shoulder_visibility", at='bool' )
	cmds.setAttr('_Tentacle_settingsCTRL.Shoulder_visibility',e=True,keyable=True)
	cmds.connectAttr('_Tentacle_settingsCTRL.Shoulder_visibility', newName+'_shoulder_ctrl.visibility',f=True)

	##hide all stuff
	cmds.group(newName+'_sh_jnt_Start', newName+'_sh_start', newName+'_sh_length', newName+'_shoulder_ctrl',n=newName+'_shoulder_grp')
	cmds.parent(newName+'_shoulder_grp','pirate_Root_Transform')
	cmds.group(newName+'_sh_start', newName+'_sh_length',newName+'_sh_jnt_Start', n=newName+'DO_NOT_GRP')
	mel.eval('move -rpr 0 223 7 right_shoulder_grp.scalePivot right_shoulder_grp.rotatePivot;')

	cmds.parentConstraint('sh_bind_jnt',newName+'_shoulder_grp',mo=True, w=1)
	cmds.spaceLocator(n=newName+'_shoulderSpace_locator',p=(28.747,192.73,5.126))
	cmds.makeIdentity(newName+'_shoulderSpace_locator',apply=True,t=1,r=1,s=0,n=0,pn=1)
	cmds.xform(newName+'_shoulderSpace_locator',cp=True)
	
	cmds.parent(newName+'_shoulderSpace_locator',newName+'_sh_jnt_End')
	cmds.parentConstraint('sh_bind_jnt', newName+'_shoulder_grp' ,mo=True, weight=1)
	cmds.parentConstraint('left_shoulderSpace_locator', 'left_tentacle_GRP' ,mo=True, weight=1)
	
	###scaling fix
	cmds.shadingNode('multiplyDivide',au=True ,n=newName+'_globalScale_leftShoulder_normalize_DIV')
	cmds.connectAttr( 'pirate_Root_Transform.scaleX', newName+'_globalScale_leftShoulder_normalize_DIV.input2X',f=True)   ####
	cmds.connectAttr( 'left_sh_lengthShape.distance', newName+'_globalScale_leftShoulder_normalize_DIV.input1X',f=True)		### fiiixed
	cmds.setAttr(newName+"_globalScale_leftShoulder_normalize_DIV.operation",2)
	cmds.connectAttr( newName+'_globalScale_leftShoulder_normalize_DIV.outputX', newName+'_sh_jnt_End_translateX.input', f=True)
	
	cmds.select(clear=True)


def fingers(newName,endAPos):
	'''
	finger creation
	'''
	
	cmds.joint(p=(endAPos[0],endAPos[1],endAPos[2]),n='right_handBase_jnt')
	cmds.setAttr(newName+"_handBase_jnt.radius", 0.5)
	cmds.select(clear=True)
	
	if(newName=='right'):
		listFingers=[rThumbJnts[0],rIndexJnts[0],rMiddleJnts[0], rRingJnts[0], rPinkyJnts[0]]
	
	for i in range(0,len(listFingers)):
		cmds.parent(listFingers[i], newName+'_handBase_jnt')
	cmds.joint(newName+'_handBase_jnt',e=True,oj='xyz', sao='ydown',ch=True, zso=True)
	cmds.select(clear=True)
	
	cmds.duplicate(rThumbJnts[0],n='right_thumb_Orbit_jnt')
	cmds.select('right_thumb_Orbit_jnt')
	cmds.pickWalk(d='down')
	cmds.delete()
	
	cmds.parent('right_thumb_Orbit_jnt',rThumbJnts[0]) 
	cmds.parent('right_thumb_Orbit_jnt',w=True)
	cmds.parent('right_thumb_start_jnt','right_thumb_Orbit_jnt')
	cmds.parent('right_thumb_Orbit_jnt','right_handBase_jnt')
	
	if(newName=='right'):
		cmds.setAttr('right_thumb_Orbit_jnt.rotateX',-70)
		#rotate the other joints so that it matches the thumb, then freeze rotations
		cmds.select('right_thumb_Orbit_jnt')
		mel.eval('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;')
	
	for item,item2,item3,item4,item5 in zip(rThumbJnts, rIndexJnts,rMiddleJnts,rRingJnts,rPinkyJnts):
		cmds.setAttr(item+".rotateOrder", 5)
		cmds.setAttr(item1+".rotateOrder", 5)
		cmds.setAttr(item2+".rotateOrder", 5)
		cmds.setAttr(item3+".rotateOrder", 5)
		cmds.setAttr(item4+".rotateOrder", 5)
		cmds.setAttr(item5+".rotateOrder", 5)
	
	for item in listFingers:
		cmds.duplicate(item,n=item+'_orient')
	
	replaceNames=['_thumb_','_index_', '_middle_', '_ring_', '_pinky_']
	replacePart=['mid2','mid','start']
	for i in range(0,len(replaceNames)):
		cmds.rename('right'+str(replaceNames[i])+'start_jnt_orient|right'+str(replaceNames[i])+'mid_jnt','right'+str(replaceNames[i])+'mid_jnt_orient') 
		cmds.rename('right'+str(replaceNames[i])+'start_jnt_orient|right'+str(replaceNames[i])+'mid_jnt_orient|right'+str(replaceNames[i])+'mid2_jnt','right'+str(replaceNames[i])+'mid2_jnt_orient') 
		cmds.delete('right'+str(replaceNames[i])+'start_jnt_orient|right'+str(replaceNames[i])+'mid_jnt_orient|right'+str(replaceNames[i])+'mid2_jnt_orient|right'+str(replaceNames[i])+'end_jnt')
		#each jnt is under the orient jnt
		cmds.parent('right'+str(replaceNames[i])+'start_jnt','right'+str(replaceNames[i])+'start_jnt_orient')
		cmds.parent('right'+str(replaceNames[i])+'mid_jnt','right'+str(replaceNames[i])+'mid_jnt_orient')
		cmds.parent('right'+str(replaceNames[i])+'mid2_jnt','right'+str(replaceNames[i])+'mid2_jnt_orient')
		
		cmds.rename('right'+str(replaceNames[i])+'end_jnt','right'+str(replaceNames[i])+'end_jnt_orient')
		for k in range(0, len(replacePart)-1):
			cmds.parent('right'+replaceNames[i]+replacePart[k]+'_jnt_orient','right'+replaceNames[i]+replacePart[k+1]+'_jnt')
		###fixed
	
	jointResult=cmds.duplicate('right_handBase_jnt')
	jointAsciiResult=map(lambda x: x.encode('ascii'), jointResult)
	
	cmds.select(clear=True)
	
###optimize
	mel.eval('select -add right_handBase_jnt1|right_thumb_Orbit_jnt|right_thumb_start_jnt_orient|right_thumb_start_jnt ;')
	mel.eval('select -add right_handBase_jnt1|right_thumb_Orbit_jnt|right_thumb_start_jnt_orient|right_thumb_start_jnt|right_thumb_mid_jnt_orient|right_thumb_mid_jnt ;')
	mel.eval('select -add right_handBase_jnt1|right_thumb_Orbit_jnt|right_thumb_start_jnt_orient|right_thumb_start_jnt|right_thumb_mid_jnt_orient|right_thumb_mid_jnt|right_thumb_mid2_jnt_orient|right_thumb_mid2_jnt ;')
	mel.eval('select -add right_handBase_jnt1|right_index_start_jnt_orient|right_index_start_jnt ;')
	mel.eval('select -add right_handBase_jnt1|right_index_start_jnt_orient|right_index_start_jnt|right_index_mid_jnt_orient|right_index_mid_jnt ;')
	mel.eval('select -add right_handBase_jnt1|right_index_start_jnt_orient|right_index_start_jnt|right_index_mid_jnt_orient|right_index_mid_jnt|right_index_mid2_jnt_orient|right_index_mid2_jnt ;')
	mel.eval('select -add right_handBase_jnt1|right_middle_start_jnt_orient|right_middle_start_jnt ;')
	mel.eval('select -add right_handBase_jnt1|right_middle_start_jnt_orient|right_middle_start_jnt|right_middle_mid_jnt_orient|right_middle_mid_jnt ;')
	mel.eval('select -add right_handBase_jnt1|right_middle_start_jnt_orient|right_middle_start_jnt|right_middle_mid_jnt_orient|right_middle_mid_jnt|right_middle_mid2_jnt_orient|right_middle_mid2_jnt ;')
	mel.eval('select -add right_handBase_jnt1|right_ring_start_jnt_orient|right_ring_start_jnt ;')
	mel.eval('select -add right_handBase_jnt1|right_ring_start_jnt_orient|right_ring_start_jnt|right_ring_mid_jnt_orient|right_ring_mid_jnt ;')
	mel.eval('select -add right_handBase_jnt1|right_ring_start_jnt_orient|right_ring_start_jnt|right_ring_mid_jnt_orient|right_ring_mid_jnt|right_ring_mid2_jnt_orient|right_ring_mid2_jnt ;')
	mel.eval('select -add right_handBase_jnt1|right_pinky_start_jnt_orient|right_pinky_start_jnt ;')
	mel.eval('select -add right_handBase_jnt1|right_pinky_start_jnt_orient|right_pinky_start_jnt|right_pinky_mid_jnt_orient|right_pinky_mid_jnt ;')
	mel.eval('select -add right_handBase_jnt1|right_pinky_start_jnt_orient|right_pinky_start_jnt|right_pinky_mid_jnt_orient|right_pinky_mid_jnt|right_pinky_mid2_jnt_orient|right_pinky_mid2_jnt ;')

	mel.eval('searchReplaceNames "_jnt" "_FK_CTRL" "selected";')
	
	cmds.rename('right_handBase_jnt1', 'right_handBase_CTRL_JNT' )
	cmds.rename('right_handBase_CTRL_JNT|right_thumb_Orbit_jnt', 'right_thumb_Orbit_FK_CTRL' )
	
	namesWithoutThumb=replaceNames[1:]
	rot_tr=['rotate', 'translate']
	for i in range(0,len(namesWithoutThumb)):
		cmds.connectAttr('right_handBase_CTRL_JNT|right'+str(namesWithoutThumb[i])+'start_jnt_orient.'+rot_tr[0], 'right_handBase_jnt|right'+str(namesWithoutThumb[i])+'start_jnt_orient.'+rot_tr[0],f=True)
		cmds.connectAttr('right'+str(namesWithoutThumb[i])+'start_FK_CTRL.'+rot_tr[0], 'right'+str(namesWithoutThumb[i])+'start_jnt.'+rot_tr[0], f=True)
		for k in rot_tr:	
			cmds.connectAttr('right'+str(namesWithoutThumb[i])+'start_FK_CTRL|right'+str(namesWithoutThumb[i])+'mid_jnt_orient.'+k, 'right'+str(namesWithoutThumb[i])+'start_jnt|right'+str(namesWithoutThumb[i])+'mid_jnt_orient.'+k,f=True)
			cmds.connectAttr('right'+str(namesWithoutThumb[i])+'mid_FK_CTRL.'+k, 'right'+str(namesWithoutThumb[i])+'mid_jnt.'+k,f=True)
			cmds.connectAttr('right'+str(namesWithoutThumb[i])+'mid_FK_CTRL|right'+str(namesWithoutThumb[i])+'mid2_jnt_orient.'+k, 'right'+str(namesWithoutThumb[i])+'mid_jnt|right'+str(namesWithoutThumb[i])+'mid2_jnt_orient.'+k,f=True)
			cmds.connectAttr('right'+str(namesWithoutThumb[i])+'mid2_FK_CTRL.'+k, 'right'+str(namesWithoutThumb[i])+'mid2_jnt.'+k,f=True)
			cmds.connectAttr('right'+str(namesWithoutThumb[i])+'mid2_FK_CTRL|right'+str(namesWithoutThumb[i])+'end_jnt_orient.'+k, 'right'+str(namesWithoutThumb[i])+'mid2_jnt|right'+str(namesWithoutThumb[i])+'end_jnt_orient.'+k, f=True)
	
	#thumb separately
	r_thumb=['right_thumb']
	l_thumb=['right_thumb']
	##?????????? be careful
	#cmds.connectAttr('r_thumb_Orbit_FK_CTRL.'+k[0], 'r_thumb_Orbit_jnt.'+k[0],f=True)
	#cmds.connectAttr('r_thumb_Orbit_FK_CTRL|r_thumb_start_jnt_orient.'+k[0], 'r_thumb_Orbit_jnt|r_thumb_start_jnt_orient.'+k[0],f=True)
		
	#for k in rot_tr:
	cmds.connectAttr('right_thumb_start_FK_CTRL.rotate', 'right_thumb_start_jnt.'+rot_tr[0], f=True)
	cmds.connectAttr('right_thumb_start_FK_CTRL|right_thumb_mid_jnt_orient.'+rot_tr[0], 'right_thumb_start_jnt|right_thumb_mid_jnt_orient.'+rot_tr[0], f=True)
	cmds.connectAttr('right_thumb_mid_FK_CTRL.rotate', 'right_thumb_mid_jnt.'+rot_tr[0], f=True)
	cmds.connectAttr('right_thumb_mid_FK_CTRL|right_thumb_mid2_jnt_orient.'+rot_tr[0], 'right_thumb_mid_jnt|right_thumb_mid2_jnt_orient.'+rot_tr[0], f=True)
	cmds.connectAttr('right_thumb_mid2_FK_CTRL.rotate', 'right_thumb_mid2_jnt.'+rot_tr[0], f=True)
	cmds.connectAttr('right_thumb_mid2_FK_CTRL|right_thumb_end_jnt_orient.'+rot_tr[0], 'right_thumb_mid2_jnt|right_thumb_end_jnt_orient.'+rot_tr[0] ,f=True)
	
	####only rotate cbecause translate is not needed for squash and stretch only
	
	indexFK=['right_index_start_FK_CTRL','right_index_mid_FK_CTRL','right_index_mid2_FK_CTRL']
	thumbFK=['right_thumb_start_FK_CTRL','right_thumb_mid_FK_CTRL','right_thumb_mid2_FK_CTRL']
	middleFK=['right_middle_start_FK_CTRL','right_middle_mid_FK_CTRL','right_middle_mid2_FK_CTRL']
	ringFK=['right_ring_start_FK_CTRL','right_ring_mid_FK_CTRL','right_ring_mid2_FK_CTRL']
	pinkyFK=['right_pinky_start_FK_CTRL','right_pinky_mid_FK_CTRL','right_pinky_mid2_FK_CTRL']
	allFKs=[indexFK,thumbFK,middleFK,ringFK,pinkyFK]
	allFK=[]
	for i in range(0,5):
		allFK.append(allFKs[i])
	
	for item in allFK:
		for i in item:
			cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n=i+'ctrl')
			cmds.setAttr(i+'ctrl.rotateX',90 )
			cmds.setAttr(i+".overrideEnabled", 1)
			cmds.setAttr(i+".overrideColor", 6)	
			cmds.xform(i+'ctrlShape.cv[0:7]', s=(3,3,3))
			cmds.makeIdentity(apply=True,t=1,r=1,s=1,n=0,pn=1)
			cmds.parent(i+'ctrlShape', i ,r=True,s=True)
			cmds.delete(i+'ctrl')
	r_ctrls=[]
	
	r_ctrls_types=['fist']
	for i in range(0,4):
		cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n='right_'+str(i)+'ctrl')
		r_ctrls.append('right_'+str(i)+'ctrl')
		cmds.setAttr('right_'+str(i)+'ctrl.rotateZ',90)
		cmds.setAttr('right_'+str(i)+'ctrl.translate',-114,200,(0.8+i)*2)
		cmds.setAttr('right_'+str(i)+'ctrl'+".overrideEnabled", 1)
		cmds.setAttr('right_'+str(i)+'ctrl'+".overrideColor", 6)	
	
	for i in r_ctrls:
		for k in r_ctrls_types:	
			cmds.addAttr('|'+i,ln=k, at='double', min=-10, max=10 ,dv=0) 
			cmds.setAttr('|'+i+'.'+k,e=True,keyable=True)
	###all fingers ctrls
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n='right_'+'FINGERS'+'ctrl')
	r_ctrls.append('right_'+'FINGERS'+'ctrl')
	cmds.setAttr('right_'+'FINGERS'+'ctrl.rotateZ',90)
	cmds.setAttr('right_'+'FINGERS'+'ctrl.translate',-114,200,4.25)
	cmds.setAttr('right_'+'FINGERS'+'ctrl.scaleZ',5)
	cmds.setAttr('right_'+'FINGERS'+'ctrl'+".overrideEnabled", 1)
	cmds.setAttr('right_'+'FINGERS'+'ctrl'+".overrideColor", 6)	
	
	palmMovement=['raisePalm','innerPalmRotate', 'outerPalmRotate','number_3', 'number_2', 'number_1']
	for i in palmMovement:
		cmds.addAttr('right_FINGERSctrl', ln=i, at='double', min=0, max=10, dv=0)
		cmds.setAttr('right_FINGERSctrl.'+i,e=True,keyable=True)
	

	###plantable fingers
	for i in rot_tr:
		cmds.connectAttr('right_handBase_CTRL_JNT.'+i, 'right_handBase_jnt.'+i,f=True)

	nameLocatorsPalm=['middlePalm_LOC', 'innerPalm_LOC', 'outerPalm_LOC']
	for i in range(0,3):
		cmds.spaceLocator(n=nameLocatorsPalm[i] ,p=(endAPos[0], endAPos[1], endAPos[2]+i*5))
		cmds.xform(nameLocatorsPalm[i], cp=1)
		cmds.setAttr(nameLocatorsPalm[i]+'.visibility', 0)
		
	cmds.setAttr('middlePalm_LOC.translateX',cmds.getAttr('right_middle_start.translateX'))
	cmds.setAttr('middlePalm_LOC.translateY',cmds.getAttr('right_middle_start.translateY'))
	cmds.setAttr('middlePalm_LOC.translateZ',cmds.getAttr('right_middle_start.translateZ'))
	cmds.setAttr("middlePalm_LOCShape.localPositionZ",0)
	cmds.setAttr("middlePalm_LOCShape.localPositionX",0)
	cmds.setAttr("middlePalm_LOCShape.localPositionY",0)
	
	cmds.setAttr('outerPalm_LOC.translateX',-11.6)
	cmds.setAttr('outerPalm_LOC.translateY',0)
	cmds.setAttr('outerPalm_LOC.translateZ',-4)
	
	cmds.setAttr('innerPalm_LOC.translateX',-11.6)
	cmds.setAttr('innerPalm_LOC.translateY',0)
	cmds.setAttr('innerPalm_LOC.translateZ',-11.6)
	
	cmds.parent('middlePalm_LOC','outerPalm_LOC')
	cmds.parent('outerPalm_LOC','innerPalm_LOC')
	
	cmds.duplicate('right_handBase_jnt', n='right_handBase_CONST_JNT')
	for i in range(0,5):
		cmds.select('right_handBase_CONST_JNT')
		cmds.pickWalk(d='down')
		cmds.delete()
	
	cmds.parent('right_handBase_CONST_JNT', 'middlePalm_LOC')
	cmds.parentConstraint('right_handBase_CONST_JNT','right_handBase_CTRL_JNT',mo=True, w=1)
	
	for i in namesWithoutThumb:
		cmds.duplicate('right_handBase_CTRL_JNT|right'+i+'start_jnt_orient', n='right'+i+'start_IK')
		cmds.parent('right'+i+'start_IK|right'+i+'start_FK_CTRL|right'+i+'mid_jnt_orient|right'+i+'mid_FK_CTRL|right'+i+'mid2_jnt_orient|right'+i+'mid2_FK_CTRL|right'+i+'end_jnt_orient','right'+i+'start_IK') 
		cmds.delete('right'+i+'start_IK|right'+i+'start_FK_CTRL')
		cmds.ikHandle(n='right_'+i+'IK_hdl',sj='right'+i+'start_IK',ee='right'+i+'start_IK|right'+i+'end_jnt_orient',sol='ikSCsolver')
		cmds.group('right_'+i+'IK_hdl', n='right_'+i+'IK_hdl_GRP')
	cmds.rename('effector3', 'right_index_eff')
	cmds.rename('effector4', 'right_midd_eff')
	cmds.rename('effector5', 'right_ring_eff')
	cmds.rename('effector6', 'right_pinky_eff')
	##thumb separately
	cmds.duplicate('right_thumb_Orbit_FK_CTRL', n='right_thumb_Orbit_start_IK')
	cmds.parent('right_thumb_Orbit_start_IK|right_thumb_start_jnt_orient|right_thumb_start_FK_CTRL|right_thumb_mid_jnt_orient|right_thumb_mid_FK_CTRL|right_thumb_mid2_jnt_orient|right_thumb_mid2_FK_CTRL|right_thumb_end_jnt_orient' ,'right_thumb_Orbit_start_IK') 
	cmds.delete('right_thumb_Orbit_start_IK|right_thumb_start_jnt_orient')
	cmds.ikHandle(n='right_thumb_IK_hdl',sj='right_thumb_Orbit_start_IK',ee='right_thumb_Orbit_start_IK|right_thumb_end_jnt_orient',sol='ikSCsolver')
	cmds.group('right_thumb_IK_hdl', n='right_thumb_IK_hdl_GRP')
	
	for i in namesWithoutThumb:	
		cmds.parent('right_handBase_CTRL_JNT|right'+i+'start_jnt_orient','right'+i+'start_IK')
	#thumb separately
	cmds.parent('right_thumb_Orbit_FK_CTRL','right_thumb_Orbit_start_IK')
	
	cmds.xform('middlePalm_LOC', cp=1)	
	cmds.move(-8.104511, 0, 0, 'middlePalm_LOC.scalePivot', 'middlePalm_LOC.rotatePivot', r=True)

	#match the fingers
	for i in namesWithoutThumb:
		cmds.duplicate('right'+i+'start_IK', n='right'+i+'straight_jnt')
		for k in range(0,3):
			cmds.select('right'+i+'straight_jnt')
			cmds.pickWalk(d='down') 
			cmds.delete()
		
		cmds.parent('right'+i+'straight_jnt', 'right_handBase_jnt')
		cmds.parent('right_handBase_jnt|right'+i+'start_jnt_orient', 'right'+i+'straight_jnt')
		cmds.connectAttr('right'+i+'start_IK.rotate', 'right'+i+'straight_jnt.rotate', f=True)
	#thumb separately
	cmds.duplicate('right_thumb_Orbit_start_IK', n='right_thumb_Orbit_straight_jnt')
	for k in range(0,3):
		cmds.select('right_thumb_Orbit_straight_jnt')
		cmds.pickWalk(d='down') 
		cmds.delete()
	cmds.parent('right_thumb_Orbit_straight_jnt', 'right_handBase_jnt')
	cmds.parent('right_handBase_jnt|right_thumb_Orbit_jnt', 'right_thumb_Orbit_straight_jnt')
	cmds.connectAttr('right_thumb_Orbit_start_IK.rotate', 'right_thumb_Orbit_straight_jnt.rotate', f=True)
	
	##next bind the fingers first and then set the driven keys 
	cmds.group('right_handBase_jnt', 'right_handBase_CTRL_JNT', 'right_0ctrl', 
				'right_1ctrl', 'right_2ctrl', 'right_3ctrl', 'right_FINGERSctrl', 
				'innerPalm_LOC', 'right__index_IK_hdl_GRP', 'right__middle_IK_hdl_GRP',
				'right__ring_IK_hdl_GRP', 'right__pinky_IK_hdl_GRP', 'right_thumb_IK_hdl_GRP',n='rightArm_GRP' )
	cmds.parent('rightArm_GRP','pirate_Root_Transform')
	
	cmds.group('right_0ctrl', 'right_1ctrl', 'right_2ctrl', 'right_3ctrl', 'right_FINGERSctrl', 'innerPalm_LOC', n='fingers_ctrl_grp')
	####
	
	cmds.group('right__index_IK_hdl_GRP', 'right__middle_IK_hdl_GRP', 'right__ring_IK_hdl_GRP', 'right__pinky_IK_hdl_GRP', 'right_thumb_IK_hdl_GRP','right_handBase_jnt', n='doN0t_touch')
	cmds.group('innerPalm_LOC', n='rightHand_Const_grp')
	cmds.move(-102.821564, 192, 3, 'rightHand_Const_grp.scalePivot', 'rightHand_Const_grp.rotatePivot', rpr=True)
	cmds.parentConstraint('right_end_arm_jnt', 'rightHand_Const_grp',mo=True, w=1)
	cmds.group('right__index_IK_hdl_GRP', 'right__middle_IK_hdl_GRP', 'right__ring_IK_hdl_GRP', 'right__pinky_IK_hdl_GRP', 'right_thumb_IK_hdl_GRP', n='right_hand_IKs')
	cmds.parent('right_hand_IKs', 'rightHand_Const_grp')
	
	cmds.delete('right_End_bindJnt_parentConstraint1')
	cmds.parentConstraint('right_handBase_CONST_JNT', 'right_End_bindJnt',mo=True, w=1)
	
	#works
	cmds.spaceLocator(n='fingers_ctrl_att',p=(0,0,0))
	cmds.setAttr('fingers_ctrl_att.translate',-52.864,123.598,11.537)
	
	cmds.parent('fingers_ctrl_att','right_handBase_CTRL_JNT')
	cmds.parent('rightHand_Const_grp','rightArm_GRP')
	cmds.parentConstraint('fingers_ctrl_att','fingers_ctrl_grp',mo=True,w=1)
	cmds.setAttr("fingers_ctrl_att.visibility",0)
	##connect inner and outter palms
	
	
	cmds.setDrivenKeyframe('outerPalm_LOC.rotateX', cd='right_FINGERSctrl.innerPalmRotate')
	cmds.setDrivenKeyframe('innerPalm_LOC.rotateX', cd='right_FINGERSctrl.outerPalmRotate')
	cmds.setDrivenKeyframe('middlePalm_LOC.rotateZ', cd='right_FINGERSctrl.raisePalm')
	
	cmds.setAttr("right_FINGERSctrl.outerPalmRotate",10)
	cmds.setAttr("right_FINGERSctrl.raisePalm",10)
	cmds.setAttr("right_FINGERSctrl.innerPalmRotate",10)
	cmds.setAttr("outerPalm_LOC.rotateX", 30)
	cmds.setAttr("innerPalm_LOC.rotateX", -30)
	cmds.setAttr("middlePalm_LOC.rotateZ", 15)
	
	cmds.setDrivenKeyframe('outerPalm_LOC.rotateX', cd='right_FINGERSctrl.innerPalmRotate')
	cmds.setDrivenKeyframe('innerPalm_LOC.rotateX', cd='right_FINGERSctrl.outerPalmRotate')
	cmds.setDrivenKeyframe('middlePalm_LOC.rotateZ', cd='right_FINGERSctrl.raisePalm')
	
	cmds.setAttr("right_FINGERSctrl.outerPalmRotate",0)
	cmds.setAttr("right_FINGERSctrl.raisePalm",0)
	cmds.setAttr("right_FINGERSctrl.innerPalmRotate",0)
	
	####setting fist
	r_ctrls_withoutLast=r_ctrls[:-1]

	for i, k in zip(namesWithoutThumb, r_ctrls):
		setKeysFingers(i,k, 'fist')
	for i in r_ctrls_withoutLast:
		cmds.setAttr(i+'.'+r_ctrls_types[0], 10)
	
	for i in namesWithoutThumb:
		cmds.setAttr('right'+i+'start_IK|right'+i+'start_jnt_orient.rotateZ',80)
		cmds.setAttr('right'+i+'start_FK_CTRL|right'+i+'mid_jnt_orient.rotateZ',80)
		cmds.setAttr('right'+i+'mid_FK_CTRL|right'+i+'mid2_jnt_orient.rotateZ',80)
	
	for i, k in zip(namesWithoutThumb, r_ctrls):
		setKeysFingers(i,k, 'fist')
	for i in r_ctrls_withoutLast:
		cmds.setAttr(i+'.'+r_ctrls_types[0], 0)	
	
	cmds.select(clear=True)	
	###end setting fist 
	##hide all the IK joints
	cmds.setAttr('right_index_start_IK.drawStyle', 2)
	cmds.setAttr('right_middle_start_IK.drawStyle',2)
	cmds.setAttr('right_pinky_start_IK.drawStyle',2)
	cmds.setAttr('right_ring_start_IK.drawStyle',2)
	cmds.setAttr('right_thumb_Orbit_start_IK.drawStyle',2)
	
	cmds.setAttr('right_pinky_start_IK|right_pinky_end_jnt_orient.drawStyle',2)
	cmds.setAttr(' right_ring_start_IK|right_ring_end_jnt_orient .drawStyle',2)
	cmds.setAttr('right_index_start_IK|right_index_end_jnt_orient.drawStyle',2)
	cmds.setAttr('right_middle_start_IK|right_middle_end_jnt_orient.drawStyle',2)
	
	cmds.setAttr("right_hand_IKs.visibility",0)

	###setting number_3 #za thumb predi ne rabotishe ama sega trqbva
	cmds.connectAttr('|pirate_Root_Transform|rightArm_GRP|right_handBase_CTRL_JNT|right_thumb_Orbit_start_IK|right_thumb_Orbit_FK_CTRL|right_thumb_start_jnt_orient.translate', '|pirate_Root_Transform|rightArm_GRP|doN0t_touch|right_handBase_jnt|right_thumb_Orbit_straight_jnt|right_thumb_Orbit_jnt|right_thumb_start_jnt_orient.translate', f=True)
	cmds.connectAttr('|pirate_Root_Transform|rightArm_GRP|right_handBase_CTRL_JNT|right_thumb_Orbit_start_IK|right_thumb_Orbit_FK_CTRL|right_thumb_start_jnt_orient.rotate', '|pirate_Root_Transform|rightArm_GRP|doN0t_touch|right_handBase_jnt|right_thumb_Orbit_straight_jnt|right_thumb_Orbit_jnt|right_thumb_start_jnt_orient.rotate', f=True)

	
	##delete the end end of the end joint
	#cmds.delete('right_end_arm_jnt1','right_End_bindJnt|right_hand_jnt')
	###set rot of the fingers before bindSkin
	cmds.setAttr("right_thumb_start_FK_CTRL.rotateZ", 23)
	cmds.setAttr("right_thumb_mid2_FK_CTRL.rotateZ",5)
	
	cmds.setAttr("right_index_start_FK_CTRL.rotateY",2)
	cmds.setAttr("right_index_start_FK_CTRL.rotateZ",27)
	cmds.setAttr("right_index_start_FK_CTRL.rotateX",-0.5)
	cmds.setAttr("right_index_mid_FK_CTRL.rotateZ", 11)
	
	cmds.setAttr("right_middle_start_FK_CTRL.rotateX", 1)
	cmds.setAttr("right_middle_start_FK_CTRL.rotateY", 3)
	cmds.setAttr("right_middle_start_FK_CTRL.rotateZ", 10)
	
	cmds.setAttr("right_middle_mid_FK_CTRL.rotateX", -1)
	cmds.setAttr("right_middle_mid_FK_CTRL.rotateY", 4.5)
	cmds.setAttr("right_middle_mid_FK_CTRL.rotateZ", 22)
	
	cmds.setAttr("right_ring_start_FK_CTRL.rotateX",-0.5)
	cmds.setAttr("right_ring_start_FK_CTRL.rotateY",5.5)
	cmds.setAttr("right_ring_start_FK_CTRL.rotateZ",22.5)
	
	cmds.setAttr("right_ring_mid_FK_CTRL.rotateZ",9)
	
	cmds.setAttr("right_pinky_start_FK_CTRL.rotateZ", 8)
	cmds.setAttr("right_pinky_start_FK_CTRL.rotateY", 10)
	
	cmds.setAttr("right_pinky_mid_FK_CTRL.rotateZ",25)
	
	
	

def setKeysFingers(finger, controlCurve, cc):
	cmds.setDrivenKeyframe('right'+finger+'start_IK|right'+finger+'start_jnt_orient.rotateZ', cd=controlCurve+'.'+cc )
	cmds.setDrivenKeyframe('right'+finger+'start_FK_CTRL|right'+finger+'mid_jnt_orient.rotateZ',cd=controlCurve+'.'+cc)
	cmds.setDrivenKeyframe('right'+finger+'mid_FK_CTRL|right'+finger+'mid2_jnt_orient.rotateZ',cd=controlCurve+'.'+cc)
	
def tentacleDo(*args):
	'''
	#FK BETTER THAN IK 
	'''
	inputCurve='tentacle1'
	idName='tentacle1'
	numberOfCvs=cmds.getAttr('tentacle1.cp',s=1)
	Jnts=[]
	IKjnts=[]
	ctrlForIK=[]
	ResultJnts=[]
	for i in range(0, numberOfCvs):
		cmds.select( clear = True )
		currentCvPos = cmds.pointPosition('tentacle1.cv['+str(i)+']', w=1 )
		Jnt = cmds.joint( name = '_'.join( ['jnt', idName, str( i+1 )] ) )
		cmds.xform( Jnt, t = currentCvPos )
		Jnts.append( Jnt )
		cmds.duplicate(Jnt, n=Jnt+'_IK')
		IKjnts.append(Jnt+'_IK')
		cmds.duplicate(Jnt, n=Jnt+'_Result')
		ResultJnts.append(Jnt+'_Result')
		cmds.duplicate(Jnt, n=Jnt+'_ctrlJnts')
		ctrlForIK.append(Jnt+'_ctrlJnts')

	cmds.select( clear = True )
	orientation = 'xyz'
	
	cleanIK=map(lambda x: x.encode('ascii'), IKjnts)
	cleanResult=map(lambda x: x.encode('ascii'), ResultJnts)
	ctrlIK=map(lambda x: x.encode('ascii'), ctrlForIK)
	for i in reversed(xrange(12)):
		cmds.parent(Jnts[i],Jnts[i-1])
		cmds.parent(IKjnts[i], IKjnts[i-1])
		cmds.parent(ResultJnts[i], ResultJnts[i-1])
		cmds.parent(ctrlIK[i], ctrlIK[i-1])
		
	cmds.parent('jnt_tentacle1_1',w=True)
	cmds.parent('jnt_tentacle1_13','jnt_tentacle1_12')
	cmds.parent('jnt_tentacle1_1_IK','jnt_tentacle1_1_Result','jnt_tentacle1_1_ctrlJnts',w=True)
	cmds.parent('jnt_tentacle1_13_IK','jnt_tentacle1_12_IK')
	cmds.parent('jnt_tentacle1_13_Result','jnt_tentacle1_12_Result')
	cmds.parent('jnt_tentacle1_13_ctrlJnts','jnt_tentacle1_12_ctrlJnts')
	
	cmds.joint(Jnts[0],IKjnts[0],ResultJnts[0], ctrlForIK[0],e=True, oj=orientation, sao='yup', ch=True, zso=True)

	#blend between the IK and the FK and result	
	blendNodesRot=[]
	blendNodesTr=[]
	for item in Jnts:
		cmds.shadingNode('blendColors',au=True,n=item+'rot_IK_FK')
		cmds.shadingNode('blendColors',au=True,n=item+'tr_IK_FK')
		blendNodesRot.append(item+'rot_IK_FK')
		blendNodesTr.append(item+'tr_IK_FK')
	for x, y, z, z1, o in zip(cleanIK, Jnts, blendNodesRot, blendNodesTr, cleanResult):
		cmds.connectAttr(x+'.rotate', z+'.color1', f=True)
		cmds.connectAttr(y+'.rotate', z+'.color2', f=True)
		cmds.connectAttr(z+'.output', o+'.rotate', f=True)
	
		cmds.connectAttr(x+'.translate', z1+'.color1', f=True)
		cmds.connectAttr(y+'.translate', z1+'.color2', f=True)
		cmds.connectAttr(z1+'.output', o+'.translate', f=True)
	
	###settings ik/fk blend
	mel.eval('curve -d 1 -p 0 0 -2 -p 0 0 2 -p -2 0 0 -p 2 0 0 -p 0 0 2 -p -2 0 0 -p 0 0 -2 -p 2 0 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 ;')
	cmds.rename('curve1', '_Tentacle_settingsCTRL')
	cmds.xform('_Tentacle_settingsCTRL',t=(140,-16,10))
	cmds.xform('_Tentacle_settingsCTRL',s=(5,5,5))
	cmds.setAttr('_Tentacle_settingsCTRL'+".overrideEnabled", 1)
	cmds.setAttr('_Tentacle_settingsCTRL'+".overrideColor", 4)
	
	cmds.rotate( 90, 0, 0, '_Tentacle_settingsCTRL', r=True, os=True, fo=True )
	cmds.parentConstraint(cleanResult[len(cleanResult)-1],'_Tentacle_settingsCTRL',mo=True, w=1)
	cmds.group('_Tentacle_settingsCTRL', n='T_settings_GRP')
	
	
	#fk controls	
	cmds.addAttr('_Tentacle_settingsCTRL',ln="FK_IK_blend", nn="FK/IK_blend", at='double', min=0, max=1, dv=0 )
	cmds.setAttr('_Tentacle_settingsCTRL.FK_IK_blend',e=True,keyable=True)
	
	cmds.addAttr('_Tentacle_settingsCTRL',ln="FK_visibility", at='double', min=0, max=1, dv=0 )
	cmds.setAttr('_Tentacle_settingsCTRL.FK_visibility',e=True,keyable=True)
	
	cmds.addAttr('_Tentacle_settingsCTRL',ln="IK_visibility", at='double', min=0, max=1, dv=0 )
	cmds.setAttr('_Tentacle_settingsCTRL.IK_visibility',e=True,keyable=True)

	for item,item1 in zip(blendNodesRot,blendNodesTr):
		cmds.connectAttr('_Tentacle_settingsCTRL.FK_IK_blend',item+'.blender',f=True)
		cmds.connectAttr('_Tentacle_settingsCTRL.FK_IK_blend',item1+'.blender',f=True)
		
	###
	#lock attr
	attr=['.tx','.ty','.tz','.rx','.ry','.rz','.sx','.sy','.sz','.v']
	attrRot=['.tx','.ty','.tz','.sx','.sy','.sz','.v']
	attrTr=['.rx','.ry','.rz','.sx','.sy','.sz','.v']
	for i in attr:
		cmds.setAttr('T_settings_GRP'+i,l=True)
		
	### create FK first
	listEnum=[12,12,12,12,12,11,11,11,11,11,7,6,5]	
	for i,k in zip(Jnts,listEnum):
		cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n=i+'ctrl')
		cmds.setAttr(i+'ctrl.rotateZ',90 )
		cmds.setAttr(i+'ctrl.scale',2*k,2*k,2*k )
		cmds.makeIdentity(apply=True,t=1,r=1,s=1,n=0,pn=1)
		cmds.parent(i+'ctrlShape', i ,r=True,s=True)
		cmds.setAttr(i+'ctrlShape'+".overrideEnabled", 1)
		cmds.setAttr(i+'ctrlShape'+".overrideColor", 4)
		cmds.delete(i+'ctrl')
		
		
	### create groups 	
	IKgrp=[]
	FKgrp=[]
	Res_grp=[]
	for i in IKjnts:
		cmds.group(i, n=i+'_grp')
		cmds.xform( i+'_grp.scalePivot', i+'_grp.rotatePivot',t=(cmds.getAttr(i+'.translateX')-17.830254,cmds.getAttr(i+'.translateY'),cmds.getAttr(i+'.translateZ')))
		IKgrp.append(i+'_grp')
	for i in ResultJnts:
		cmds.group(i, n=i+'_grp')
		cmds.xform( i+'_grp.scalePivot', i+'_grp.rotatePivot',t=(cmds.getAttr(i+'.translateX')-17.830254,cmds.getAttr(i+'.translateY'),cmds.getAttr(i+'.translateZ')))
		Res_grp.append(i+'_grp')
	for i in Jnts:
		cmds.group(i, n=i+'_grp')
		cmds.xform( i+'_grp.scalePivot', i+'_grp.rotatePivot',t=(cmds.getAttr(i+'.translateX')-17.830254,cmds.getAttr(i+'.translateY'),cmds.getAttr(i+'.translateZ')))
		FKgrp.append(i+'_grp')
		
	#17.830254
	cmds.distanceDimension(sp=(0,0,0),ep=(0,1,0))
	cmds.rename('locator1', 'start_tentacle_loc')
	cmds.rename('locator2', 'end_tentacle_loc')
	cmds.setAttr('start_tentacle_loc.translate',28.747,193.642,5.126)#cmds.getAttr(ResultJnts[0]+'.translateX'), cmds.getAttr(ResultJnts[0]+'.translateY'),cmds.getAttr(ResultJnts[0]+'.translateZ')
	cmds.setAttr('end_tentacle_loc.translate',131.79,5.197,9.277)
	cmds.rename('distanceDimension1', 'tentacle_distance' )
	
	###squash and stretch
	cmds.shadingNode('multiplyDivide', au=True, n='tentacle_mulDiv')
	cmds.setAttr("tentacle_mulDiv.operation",2)
	cmds.connectAttr('tentacle_distance.distance', 'tentacle_mulDiv.input1X', f=True)
	cmds.shadingNode('multiplyDivide', au=True, n='tentacle_result')
	cmds.setAttr("tentacle_result.operation",1)
	cmds.connectAttr('tentacle_mulDiv.output.outputX', 'tentacle_result.input1X', f=True)
	cmds.setAttr('tentacle_result.input2X', 17.835)
	cmds.setAttr("tentacle_mulDiv.input2X", 214.018)

	for i,k in zip(IKjnts[1:], Jnts[1:]):
		cmds.setAttr(i+".translateX",0)
		cmds.setAttr(k+".translateX",0)
	
	without1_FKgrp=FKgrp[1:]
	without1_IKgrp=IKgrp[1:]
	without1_ResGrp=Res_grp[1:]
	for i,k in zip(without1_IKgrp,without1_FKgrp):
		cmds.connectAttr('tentacle_result.output.outputX', i+'.translate.translateX', f=True)
	###ik controllers for sq and stch 
	cmds.parent('start_tentacle_loc','jnt_tentacle1_1_ctrlJnts')
	cmds.parent('end_tentacle_loc','jnt_tentacle1_13_ctrlJnts')
	cmds.parent('jnt_tentacle1_13_ctrlJnts', 'jnt_tentacle1_5_ctrlJnts','jnt_tentacle1_7_ctrlJnts','jnt_tentacle1_10_ctrlJnts', w=True)
	cmds.delete('jnt_tentacle1_2_ctrlJnts','jnt_tentacle1_6_ctrlJnts','jnt_tentacle1_8_ctrlJnts','jnt_tentacle1_11_ctrlJnts')
	
	###controllers for the ik controllers
	ctrlCurve=['start_ik','ik_ctrl_1','ik_ctrl_2','ik_ctrl_3','end_ik']
	ikCtrlJoints=['jnt_tentacle1_1_ctrlJnts','jnt_tentacle1_5_ctrlJnts','jnt_tentacle1_7_ctrlJnts','jnt_tentacle1_10_ctrlJnts','jnt_tentacle1_13_ctrlJnts']
	
	for x,y in zip(ctrlCurve,ikCtrlJoints):
		cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n=x)
		cmds.setAttr(x+'.translateX',cmds.getAttr(y+'.translateX'))
		cmds.setAttr(x+'.translateY',cmds.getAttr(y+'.translateY'))
		cmds.setAttr(x+'.translateZ',cmds.getAttr(y+'.translateZ'))
		cmds.setAttr(x+'.scale',23,23,23)
		cmds.setAttr(x+'.rotate',0,0,30)
	
	cmds.makeIdentity(ctrlCurve,apply=True,t=1,r=1,s=1,n=0,pn=1)
	cmds.parent('jnt_tentacle1_1_ctrlJnts','start_ik')
	cmds.parent('jnt_tentacle1_13_ctrlJnts','end_ik')
	cmds.parent('jnt_tentacle1_5_ctrlJnts','ik_ctrl_1')
	cmds.parent('jnt_tentacle1_7_ctrlJnts','ik_ctrl_2')
	cmds.parent('jnt_tentacle1_10_ctrlJnts','ik_ctrl_3')
	
	###colour change first
	for i in ctrlCurve:
		cmds.setAttr(i+".overrideEnabled", 1)
		cmds.setAttr(i+".overrideColor", 4)
	
	cmds.rebuildCurve("tentacle1",ch=1,rpo=1,rt=0,end=1,kr=0,kcp=0,kep=1,kt=0,s=2,d=3,tol=0.01 )
	cmds.ikHandle(n='tentalce_hdl',sj='jnt_tentacle1_1_IK',ee='jnt_tentacle1_13_IK',sol='ikSplineSolver',ccv=False,c='tentacle1')
	
	for x,y,z in zip(without1_IKgrp,without1_ResGrp, without1_FKgrp):
		cmds.connectAttr(x+'.translate', y+'.translate', f=True)
		cmds.connectAttr('tentacle_result.outputX', z+'.translateX', f=True)
	
	
	#create tree main controllers which control different parts of the fk's and 
	tentacleDivideList=['tentacle_part1','tentacle_part2','tentacle_part3']
	for i in range(0,3):
		mel.eval('curve -d 1 -p -2.97211 0 -0.0950481 -p -2.12202 0 -2.078591 -p -0.0676363 0 -2.928681 -p 1.986747 0 -2.078591 -p 1.986747 0 0.0112132 -p -0.0676363 0 0.082054 -p -1 0 -1 -p -3 0 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 ;')
		cmds.rename('curve1', tentacleDivideList[i])
		cmds.xform(tentacleDivideList[i],t=(50*(i+1),225,6))
		cmds.xform(tentacleDivideList[i],s=(5,5,5))
		cmds.makeIdentity(tentacleDivideList[i], apply=True,t=1,r=1,s=1,n=0,pn=1)
		cmds.setAttr(tentacleDivideList[i]+".overrideEnabled", 1)
		cmds.setAttr(tentacleDivideList[i]+".overrideColor", 4)
		
		
	###fk ik on of visibility and if possible evaluation
	cmds.setAttr("_Tentacle_settingsCTRL.FK_visibility", 1)
	for i in Jnts:
		cmds.connectAttr('_Tentacle_settingsCTRL.FK_visibility', i+'.visibility', f=True)
	for i in tentacleDivideList:
		cmds.connectAttr('_Tentacle_settingsCTRL.FK_visibility', i+'.visibility', f=True)
	for i in ctrlCurve:
		cmds.connectAttr('_Tentacle_settingsCTRL.IK_visibility', i+'.visibility', f=True)
	
	cmds.setAttr("_Tentacle_settingsCTRL.FK_visibility", 0)	
	cmds.setAttr("_Tentacle_settingsCTRL.IK_visibility", 1)	
	
	cmds.setAttr("_Tentacle_settingsCTRL.FK_IK_blend", 1)
	cmds.setAttr("_Tentacle_settingsCTRL.FK_visibility", 0)
	cmds.setAttr("_Tentacle_settingsCTRL.IK_visibility", 1)
	cmds.setAttr("jnt_tentacle1_1_IK_grp.visibility",1)
	cmds.setDrivenKeyframe('_Tentacle_settingsCTRL.FK_visibility' ,cd='_Tentacle_settingsCTRL.FK_IK_blend')
	cmds.setDrivenKeyframe('_Tentacle_settingsCTRL.IK_visibility' ,cd='_Tentacle_settingsCTRL.FK_IK_blend')
	cmds.setDrivenKeyframe('jnt_tentacle1_1_IK_grp.visibility' ,cd='_Tentacle_settingsCTRL.FK_IK_blend')
	
	cmds.setAttr("_Tentacle_settingsCTRL.FK_IK_blend", 0)
	cmds.setAttr("_Tentacle_settingsCTRL.FK_visibility", 1)
	cmds.setAttr("_Tentacle_settingsCTRL.IK_visibility", 0)
	cmds.setAttr("jnt_tentacle1_1_IK_grp.visibility",0)
	cmds.setDrivenKeyframe('_Tentacle_settingsCTRL.FK_visibility' ,cd='_Tentacle_settingsCTRL.FK_IK_blend')
	cmds.setDrivenKeyframe('_Tentacle_settingsCTRL.IK_visibility' ,cd='_Tentacle_settingsCTRL.FK_IK_blend')
	cmds.setDrivenKeyframe('jnt_tentacle1_1_IK_grp.visibility' ,cd='_Tentacle_settingsCTRL.FK_IK_blend')
	
	'''
	
	#next 
	##seamless IK FK
	
	matchTransform -pos start_ik jnt_tentacle1_1;
	matchTransform -pos ik_ctrl_1 jnt_tentacle1_5;
	matchTransform -pos ik_ctrl_2 jnt_tentacle1_7;
	matchTransform -pos ik_ctrl_3 jnt_tentacle1_10;
	matchTransform -pos end_ik jnt_tentacle1_13;
	
	matchTransform -pos jnt_tentacle1_1_IK_grp jnt_tentacle1_1_grp;
	matchTransform -pos jnt_tentacle1_2_IK_grp jnt_tentacle1_2_grp;
	matchTransform -pos jnt_tentacle1_3_IK_grp jnt_tentacle1_3_grp;
	matchTransform -pos jnt_tentacle1_4_IK_grp jnt_tentacle1_4_grp;
	matchTransform -pos jnt_tentacle1_5_IK_grp jnt_tentacle1_5_grp;
	matchTransform -pos jnt_tentacle1_6_IK_grp jnt_tentacle1_6_grp;
	matchTransform -pos jnt_tentacle1_7_IK_grp jnt_tentacle1_7_grp;
	matchTransform -pos jnt_tentacle1_8_IK_grp jnt_tentacle1_8_grp;
	matchTransform -pos jnt_tentacle1_9_IK_grp jnt_tentacle1_9_grp;
	matchTransform -pos jnt_tentacle1_10_IK_grp jnt_tentacle1_10_grp;
	matchTransform -pos jnt_tentacle1_11_IK_grp jnt_tentacle1_11_grp;
	matchTransform -pos jnt_tentacle1_12_IK_grp jnt_tentacle1_12_grp;
	matchTransform -pos jnt_tentacle1_13_IK_grp jnt_tentacle1_13_grp;
	
	'''	 
	#squash and stretch
	cmds.shadingNode('multiplyDivide', au=True, n='tentacle_sqrtStretch_pow')
	cmds.setAttr("tentacle_sqrtStretch_pow.operation", 3)
	cmds.shadingNode('multiplyDivide', au=True, n='tentacle_stretchInvert_Div')
	cmds.setAttr("tentacle_stretchInvert_Div.operation", 2)
	cmds.connectAttr('tentacle_mulDiv.output.outputX','tentacle_sqrtStretch_pow.input1.input1X')
	cmds.connectAttr('tentacle_sqrtStretch_pow.output.outputX','tentacle_stretchInvert_Div.input2.input2X')
	cmds.setAttr("tentacle_sqrtStretch_pow.input2X",0.5)
	cmds.setAttr("tentacle_stretchInvert_Div.input1X",1)
	
	for i in ResultJnts:
		cmds.connectAttr( 'tentacle_stretchInvert_Div.output.outputX', i+'.scale.scaleY', f=True) 

	cmds.group('jnt_tentacle1_1_grp', 'jnt_tentacle1_1_IK_grp', 'jnt_tentacle1_1_Result_grp', 'tentalce_hdl',
				tentacleDivideList, ctrlCurve,'tentacle_distance', 'tentacle1', n='left_tentacle_GRP' )
	cmds.parent('left_tentacle_GRP', 'pirate_Root_Transform')	
	
	#match the result joint to the fk or ik so the mesh follows
	#scale global for the tentacle	
	cmds.shadingNode('multiplyDivide', au=True, n='global_scale_tentacle')	
	cmds.setAttr("global_scale_tentacle.operation", 2)
	cmds.connectAttr('tentacle_distanceShape.distance','global_scale_tentacle.input1X',f=True )
	cmds.connectAttr('pirate_Root_Transform.scaleY','global_scale_tentacle.input2X', f=True )
	cmds.connectAttr('global_scale_tentacle.outputX','tentacle_mulDiv.input1X', f=True )
	cmds.setAttr("tentacle1.inheritsTransform",0)

	cmds.select(clear=True)
	
	###connect the three parts to the fks
	thirdPartF=FKgrp[9:13]
	secondPartF=FKgrp[5:9]
	firstPartF=FKgrp[1:5]
	thirdPartR=Res_grp[9:13]
	secondPartR=Res_grp[5:9]
	firstPartR=Res_grp[1:5]
	
	for i,k in zip(thirdPartF, thirdPartR):
		cmds.connectAttr('tentacle_part3.rotate', i+'.rotate',f=True)
		cmds.connectAttr(i+'.rotate',k+'.rotate',f=True)
	for i,k in zip(secondPartF, secondPartR):
		cmds.connectAttr('tentacle_part2.rotate', i+'.rotate',f=True)
		cmds.connectAttr(i+'.rotate',k+'.rotate',f=True)
	for i,k in zip(firstPartF, firstPartR):
		cmds.connectAttr('tentacle_part1.rotate', i+'.rotate',f=True)
		cmds.connectAttr(i+'.rotate',k+'.rotate',f=True)
	
	#skin ONCE AND FOREVER!
	#cmds.setAttr('Tentacle.rotateZ',-87)
	#cmds.makeIdentity('Tentacle', apply=True,t=1,r=1,s=1,n=0,pn=1)
	#cmds.skinCluster( 'jnt_tentacle1_1_Result', 'Tentacle', mi=5) ####2
	#cmds.setAttr("jnt_tentacle1_1.rotateZ",-60.5)
	
	#lock
	for i in Jnts:
		for z in attrRot:
			cmds.setAttr(i+z,l=True)	
	for i in tentacleDivideList:
		for k in attrRot:
			cmds.setAttr(i+k,l=True)
	for i in ctrlCurve:
		for k in attrTr:
			cmds.setAttr(i+k,l=True)
	cmds.select(clear=True)
	
	cmds.setAttr("jnt_tentacle1_13.jointOrientZ", 0)
	cmds.setAttr("jnt_tentacle1_13.jointOrientX", 0)
	cmds.setAttr("jnt_tentacle1_13.jointOrientY", 0)

	cmds.setAttr("jnt_tentacle1_13.rotateX", 0)
	cmds.setAttr("jnt_tentacle1_13.rotateY", 0)
	cmds.setAttr("jnt_tentacle1_13.rotateZ", 0)

	
	leftClavicle()
	
	
def hipCenter():
	'''
	doesnt work at the moment
	'''
	#taken from a tutorial on the internet
	cmds.shadingNode('plusMinusAverage',au=True ,n='hip_legsPlusMinAvg')
	cmds.shadingNode('multiplyDivide',au=True ,n='hip_legsMulDiv')
	cmds.connectAttr('left_Leg_settingsCTRL.translate','hip_legsPlusMinAvg.input3D[0]')
	cmds.connectAttr('right_Leg_settingsCTRL.translate','hip_legsPlusMinAvg.input3D[1]')
	cmds.connectAttr('hip_legsPlusMinAvg.output3D', 'hip_legsMulDiv.input1')
	cmds.setAttr("hip_legsMulDiv.operation", 2)
	cmds.setAttr("hip_legsMulDiv.input2X", 2)
	cmds.setAttr("hip_legsMulDiv.input2Y", 6)
	cmds.setAttr("hip_legsMulDiv.input2Z", 2)
	cmds.connectAttr('hip_legsMulDiv.output', 'body_Ctrl.translate')
	
def doHat():
	'''
	hatjoints
	'''
	
	hatJntsPos=[[7.5,263.513,8.525], [7.587,271.552,8.175], [8.037,280.887,2.627],[16.66,292.79,-1.81], [29.404,302.257,-5.62],
				[43.746,308.561,-8.438], [57.161,310.83,-9.847], [72.818,307.833,-9.583], [83.151,296.048,-6.094],
				[87.006,284.324,-2.315],[86.259,276.541,0.352]]	
	hatNames=['hat_jnt_1','hat_jnt_2','hat_jnt_3','hat_jnt_4','hat_jnt_5','hat_jnt_6','hat_jnt_7','hat_jnt_8','hat_jnt_9','hat_jnt_10','hat_jnt_11']
	
	for x, y in zip(hatJntsPos, hatNames):
		cmds.joint(p=(x),n=y)
		
	cmds.joint('hat_jnt_1',e=True,oj='xyz',sao='yup',ch=True,zso=True)	
	withoutLast=hatNames[:-1]
	for y in withoutLast:
		cmds.group(y,n=y+'_GRP')
		cmds.xform( y+'_GRP.scalePivot', y+'_GRP.rotatePivot',t=(cmds.getAttr(y+'.translateX'),cmds.getAttr(y+'.translateY'),cmds.getAttr(y+'.translateZ')))
		cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n=y+'ctrl')
		cmds.parent(y+'ctrlShape', y, s=True, r=True) 
		cmds.xform(y+'ctrlShape.cv[0:7]', s=(8,8,8))
		cmds.xform(y+'ctrlShape.cv[0:7]', ro=(0,0,90))
		cmds.delete(y+'ctrl')
		cmds.setAttr(y+".overrideEnabled", 1)
		cmds.setAttr(y+".overrideColor", 4)
	
	cmds.select(clear=True)
	cmds.curve(d=1.0, p=[(0,12,48),(0,15,46),(0,15,42),(0,12,40),(0,12,48)],k=[0,1,2,3,4], n='Hat_all_ctrl')
	cmds.setAttr('Hat_all_ctrl.translate', 35,310,0 )
	cmds.setAttr('Hat_all_ctrl.rotate',0,90,0)
	cmds.xform('Hat_all_ctrl',cp=1)
	cmds.makeIdentity('Hat_all_ctrl', apply=True,t=1,r=1,s=1,n=0,pn=1)
	
	cmds.select(clear=True)
	edgesHatL=['left_edge_hat_jnt1','left_edge_hat_jnt2','left_edge_hat_jnt3','left_edge_hat_jnt4']
	edgeHatPosL=[[12.375,250.691,6.008],[28.374,242.132,-2.759],[40.176,237.41,-8.702],[51.079,235.533,-13.438]]
	for x, y in zip(edgeHatPosL, edgesHatL):
		cmds.joint(p=(x),n=y)
		
	cmds.joint('left_edge_hat_jnt1',e=True,oj='xyz',sao='yup',ch=True,zso=True)		
	withoutLast1=edgesHatL[:-1]
	for y in withoutLast1:
		cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n=y+'ctrl')
		cmds.parent(y+'ctrlShape', y, s=True, r=True)
		cmds.xform(y+'ctrlShape.cv[0:7]', s=(5,5,5))
		cmds.xform(y+'ctrlShape.cv[0:7]', ro=(0,0,90))
		cmds.delete(y+'ctrl')
		cmds.setAttr(y+".overrideEnabled", 1)
		cmds.setAttr(y+".overrideColor", 4)
	for y in edgesHatL:
		cmds.setAttr(y+".drawStyle",2)
	
	cmds.select(clear=True)
	edgesHatR=['right_edge_hat_jnt1','right_edge_hat_jnt2','right_edge_hat_jnt3','right_edge_hat_jnt4']
	edgeHatPosR=[[-10.718,249.371,1.769],[-21.585,244.791,-1.556],[-34.071,239.346,-6.543],[-49.695,234.8,-16.474]]
	for x, y in zip(edgeHatPosR, edgesHatR):
		cmds.joint(p=(x),n=y)
		
	cmds.joint('right_edge_hat_jnt1',e=True,oj='xyz',sao='yup',ch=True,zso=True)	
	withoutLast2=edgesHatR[:-1]
	for y in withoutLast2:	
		cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n=y+'ctrl')
		cmds.parent(y+'ctrlShape', y, s=True, r=True)
		cmds.xform(y+'ctrlShape.cv[0:7]', s=(5,5,5))
		cmds.xform(y+'ctrlShape.cv[0:7]', ro=(0,0,90))
		cmds.delete(y+'ctrl')
		cmds.setAttr(y+".overrideEnabled", 1)
		cmds.setAttr(y+".overrideColor", 6)
	
	for y in edgesHatR:
		cmds.setAttr(y+".drawStyle",2)
	
	cmds.select(clear=True)
	cmds.group('Hat_all_ctrl','hat_jnt_1','left_edge_hat_jnt1','right_edge_hat_jnt1','hat_jnt_1_GRP', n='hat_grp')
	
	cmds.parent('hat_jnt_1','hat_jnt_1_GRP')
	
	for i in withoutLast:
		cmds.connectAttr('Hat_all_ctrl.rotate', i+'_GRP.rotate',f=True)	

	cmds.setAttr("Hat_all_ctrl.overrideEnabled", 1)
	cmds.setAttr("Hat_all_ctrl.overrideColor", 4)

	attrTr=['.tx','.ty','.tz','.sx','.sy','.sz','.v']
	for i in attrTr:
		cmds.setAttr('Hat_all_ctrl'+i,l=True)	
	
	
	cmds.select(clear=True)
			
def doFace(*args):
	'''
	face creation
	'''
	posJnts=[11.225, 240.295, 11.796, 227.196, 13.949, 9.494,-3.698,11.251 ]
	
	cmds.joint(p=(posJnts[0], posJnts[1],posJnts[2]),n='left_top_move_'+'Sq_str')
	cmds.joint(p=(posJnts[0], posJnts[3],posJnts[4]),n='left_bot_move_'+'Sq_str')
	
	cmds.joint('left_top_move_Sq_str','left_bot_move_Sq_str',e=True,oj='xyz',sao='yup',ch=True,zso=True)
	
	cmds.duplicate('left_top_move_Sq_str', n='left_top_move_bindJnt')	
	cmds.rename('left_top_move_bindJnt|left_bot_move_Sq_str', 'left_bot_move_bindJnt')
	cmds.parent('left_bot_move_bindJnt',w=True)
	
	cmds.setAttr('left_bot_move_bindJnt.radius',2)
	cmds.setAttr('left_top_move_bindJnt.radius',2)	
	
	cmds.mirrorJoint('left_bot_move_bindJnt',mirrorYZ=True,mirrorBehavior=True,searchReplace=('left_', 'right_') )
	cmds.mirrorJoint('left_top_move_bindJnt',mirrorYZ=True,mirrorBehavior=True,searchReplace=('left_', 'right_') )
	cmds.mirrorJoint('left_top_move_Sq_str',mirrorYZ=True,mirrorBehavior=True,searchReplace=('left_', 'right_') )
	
	cmds.select(clear=True)
	cmds.joint(p=(11.225,230.333,9.582),n='left_screw')
	cmds.mirrorJoint('left_screw',mirrorYZ=True,mirrorBehavior=True,searchReplace=('left_', 'right_'))
	
	cmds.setAttr('left_screw.radius',2)
	cmds.setAttr('right_screw.radius',2)	
	#ik splines and pull mechanis
	cmds.ikHandle(n='left_jaw_hdl',sj='left_top_move_Sq_str',ee='left_bot_move_Sq_str',sol='ikSplineSolver')
	#cmds.rename('effector3','left_jaw_eff')
	cmds.rename('curve1', 'left_jaw_curve')
	cmds.ikHandle(n='right_jaw_hdl',sj='right_top_move_Sq_str',ee='right_bot_move_Sq_str',sol='ikSplineSolver')
	#cmds.rename('effector4','right_jaw_eff')
	cmds.rename('curve1', 'right_jaw_curve')
	
	#bind joints to the spines
	cmds.skinCluster('left_top_move_bindJnt','left_bot_move_bindJnt','left_jaw_curve',mi=2)
	cmds.skinCluster('right_top_move_bindJnt','right_bot_move_bindJnt','right_jaw_curve',mi=2)
	 
	#do the stretch, since we dont squash 

	cmds.shadingNode('curveInfo',au=True, n='left_jaw_curve_length')
	cmds.shadingNode('curveInfo',au=True, n='right_jaw_curve_length')
	cmds.connectAttr('left_jaw_curveShape.worldSpace[0]', 'left_jaw_curve_length.inputCurve', f=True)
	cmds.connectAttr('right_jaw_curveShape.worldSpace[0]', 'right_jaw_curve_length.inputCurve')
	
	cmds.shadingNode('multiplyDivide',au=True,n='left_Jaw_stretchDiv')
	cmds.shadingNode('multiplyDivide',au=True,n='right_Jaw_stretchDiv')
	cmds.setAttr("left_Jaw_stretchDiv.operation", 2)
	cmds.setAttr("right_Jaw_stretchDiv.operation", 2)
	
	cmds.connectAttr('right_jaw_curve_length.arcLength', 'right_Jaw_stretchDiv.input1X')
	cmds.connectAttr('left_jaw_curve_length.arcLength', 'left_Jaw_stretchDiv.input1X')
	
	cmds.setAttr("right_Jaw_stretchDiv.input2X",13.275)
	cmds.setAttr("left_Jaw_stretchDiv.input2X",13.275)

	cmds.connectAttr('left_Jaw_stretchDiv.outputX', 'left_top_move_Sq_str.scaleX' ,f=True) 
	cmds.connectAttr('left_Jaw_stretchDiv.outputX', 'left_bot_move_Sq_str.scaleX' ,f=True) 
	cmds.connectAttr('right_Jaw_stretchDiv.outputX', 'right_top_move_Sq_str.scaleX' ,f=True) 
	cmds.connectAttr('right_Jaw_stretchDiv.outputX', 'right_bot_move_Sq_str.scaleX' ,f=True) 

	cmds.parent('left_bot_move_bindJnt','left_screw')
	cmds.parent('right_bot_move_bindJnt','right_screw')

	## select left_screw and right_screw and rotate it 
	#change the curves
	#cmds.curve(ep=points pos, d=1)  ##d=1 for 2cv points only
	
	jntFacePos=[[1.748,240.972,23.068],  [4.956,241.651,22.314],  [8.355,241.885,20.326],  
				 [3.743,239.123,20.064], [3.743,237.138,20.064],  [2.199,235.121, 21.1], 
				[0,234.213,23.992],[3.789,237.936,19.717]]
	namesFaceJntsL=['left_eyebrow_start_jnt', 'left_eyebrow_mid_jnt', 'left_eyebrow_end_jnt', 'left_eye_3_jnt', 
				'left_eye_7_jnt', 'left_nose_1_jnt', 'nose_top_jnt','left_eye']
	namesFaceJntsR=[]
	
	moustachePos=[[0,231.831,23.61],[4.792,230.246,24.126],[8.638,228.867,20.424], [12.737,228.867,16.738],[15.819,230.07,15.049], [18.296,233.097,14.75] ]
	moustacheNamesL=['base_mst_jnt','left_mst_1', 'left_mst_2', 'left_mst_3', 'left_mst_4' , 'left_mst_5', 'left_mst_6' ]
	moustacheNamesR=[]
	
	cmds.select(clear=True)
	for x, y in zip(jntFacePos, namesFaceJntsL):
		cmds.joint(p=(x),n=y)
		cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n=y+'ctrl')
		cmds.parent(y+'ctrlShape', y, s=True, r=True)
		#
		cmds.xform(y+'ctrlShape.cv[0:7]', s=(1,1,1))
		cmds.xform(y+'ctrlShape.cv[0:7]', ro=(90,0,0))
		cmds.delete(y+'ctrl')
		cmds.select(clear=True)
		cmds.setAttr(y+".overrideEnabled", 1)
		cmds.setAttr(y+".overrideColor", 4)

	for i in namesFaceJntsL:
		if i.startswith('left'):
			namesFaceJntsR.append('right_'+i[5:]) 
	for x, y in zip(namesFaceJntsL,namesFaceJntsR):
		cmds.duplicate(x,n=y)
		cmds.setAttr(y+'.translateX', -cmds.getAttr(x+'.translateX'))
		cmds.setAttr(x+".overrideEnabled", 1)
		cmds.setAttr(x+".overrideColor", 6)
	cmds.select(clear=True)	
		
	for x,y in zip(moustachePos, moustacheNamesL):
		cmds.joint(p=(x),n=y)	
		cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n=y+'ctrl')
		cmds.parent(y+'ctrlShape', y, s=True, r=True)
		cmds.xform(y+'ctrlShape.cv[0:7]', s=(2,2,2))
		cmds.xform(y+'ctrlShape.cv[0:7]', ro=(90,0,0))
		cmds.delete(y+'ctrl')
		cmds.setAttr(y+".overrideEnabled", 1)
		cmds.setAttr(y+".overrideColor", 4)
			
	
	cmds.setAttr('right_eye.translateX', -cmds.getAttr('left_eye.translateX'))	
	cmds.setAttr('right_eye.translateY', cmds.getAttr('left_eye.translateY'))	
	cmds.setAttr('right_eye.translateZ', cmds.getAttr('left_eye.translateZ'))	
	namesChange=cmds.mirrorJoint('base_mst_jnt|left_mst_1',mirrorYZ=True, mirrorBehavior=True)
	
	moustacheNamesR=['left_mst_6','left_mst_7','left_mst_8','left_mst_9','left_mst_10']
	for i in moustacheNamesR:
		cmds.setAttr(i+".overrideEnabled", 1)
		cmds.setAttr(i+".overrideColor", 6)
	
	##optimize with a foor loop
	cmds.rename('left_mst_6', moustacheNamesR[0])
	cmds.rename(moustacheNamesR[0]+'|left_mst_7', moustacheNamesR[1])
	cmds.rename('left_mst_8', moustacheNamesR[2])
	cmds.rename('left_mst_9', moustacheNamesR[3])
	cmds.rename('left_mst_10', moustacheNamesR[4])
	cmds.select(clear=True)
	
	cmds.group('left_top_move_Sq_str', 'left_top_move_bindJnt', 'right_top_move_bindJnt', 'right_top_move_Sq_str',
				'left_jaw_hdl', 'left_jaw_curve', 'right_jaw_hdl', 'right_jaw_curve', n='jaw_grp')
	cmds.parent('jaw_grp', 'pirate_Root_Transform')
	
	
	#do the Hat
	doHat()
	cmds.group( 'right_nose_1_jnt', 'right_eye_7_jnt', 'left_eye','right_eye',
				 'right_eye_3_jnt',
				'right_eyebrow_end_jnt', 'right_eyebrow_mid_jnt', 'right_eyebrow_start_jnt', 'nose_top_jnt', 
				'left_nose_1_jnt', 'left_eye_7_jnt',
				'left_eye_3_jnt', 'left_eyebrow_end_jnt',
				 'left_eyebrow_mid_jnt', 'left_eyebrow_start_jnt', n='faceJnts')
	cmds.parent('faceJnts', 'pirate_Root_Transform')
	cmds.select(clear=True)
	### do the neck
	neckJnts=[[0,210,5],[0,214,5],[0,230.355,9.576]] #[0,218.778,7.433],[0,240.298,11.812],[0,256.309,9.745],
	neckNames=['neck_2','neck_1','jaw_connect'] #,'neck_3','neck_4'
	for x, y in zip(neckJnts, neckNames): 
		cmds.joint(p=(x),n=y)
	cmds.parent('jaw_connect',w=True)
		
	cmds.parent('left_screw', 'right_screw', 'jaw_connect')
	cmds.parent('base_mst_jnt', 'faceJnts')
	cmds.group('left_top_move_bindJnt','right_top_move_bindJnt', n='jaw_grp_base')
	cmds.parentConstraint('neck_1','jaw_grp_base',mo=True, w=1)
	cmds.parentConstraint('neck_1','faceJnts',mo=True, w=1)
	cmds.group('jaw_connect', n='jaw_grp_connect')
	
	cmds.parentConstraint('neck_1','faceJnts',mo=True, w=1)
	cmds.parentConstraint('neck_1','hat_grp',mo=True, w=1)
	cmds.parentConstraint('neck_1','jaw_grp_connect',mo=True, w=1)
	cmds.parent('jaw_grp_connect','jaw_grp')
	cmds.parent('jaw_grp_connect','pirate_Root_Transform')
	cmds.parent('hat_grp', 'pirate_Root_Transform')
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n='jaw_ctrl')
	cmds.setAttr('jaw_ctrl.translateX', cmds.getAttr('end_spine.translateX'))
	cmds.setAttr('jaw_ctrl.translateY', cmds.getAttr('end_spine.translateY')+20)
	cmds.setAttr('jaw_ctrl.translateZ', cmds.getAttr('end_spine.translateZ')+20)
	cmds.setAttr('jaw_ctrl.scale',6,6,6)
	cmds.xform('jaw_ctrl.cv[4:6]',t=(0,2,0) )

	cmds.makeIdentity('jaw_ctrl', apply=True,t=1,r=1,s=1,n=0,pn=1)
	cmds.addAttr( 'jaw_ctrl',ln='jaw_drop', at='double', min=0,max=15,dv=0)
	cmds.setAttr( 'jaw_ctrl.jaw_drop',e=True,keyable=True)
	cmds.setAttr('jaw_ctrl'+".overrideEnabled", 1)
	cmds.setAttr('jaw_ctrl'+".overrideColor", 16)
	
	
	cmds.group('jaw_grp_base', 'hat_grp','faceJnts', 'jaw_grp_connect', 'jaw_grp', n='head_ALL_grp')
	#set keys is not working do it manually
	cmds.connectAttr( 'jaw_ctrl.jaw_drop', 'jaw_connect.rotateX', f=True)
	
	
	cmds.shadingNode('multiplyDivide', au=True, n='global_scale_jaw_left')	
	cmds.setAttr("global_scale_jaw_left.operation", 2)
	cmds.connectAttr('left_jaw_curve_length.arcLength','global_scale_jaw_left.input1X',f=True )
	cmds.connectAttr('pirate_Root_Transform.scaleY','global_scale_jaw_left.input2X', f=True )
	cmds.connectAttr('global_scale_jaw_left.outputX','left_Jaw_stretchDiv.input1X', f=True )
	cmds.setAttr("left_jaw_curve.inheritsTransform",0)
	
	cmds.shadingNode('multiplyDivide', au=True, n='global_scale_jaw_right')	
	cmds.setAttr("global_scale_jaw_right.operation", 2)
	cmds.connectAttr('right_jaw_curve_length.arcLength','global_scale_jaw_right.input1X',f=True )
	cmds.connectAttr('pirate_Root_Transform.scaleY','global_scale_jaw_right.input2X', f=True )
	cmds.connectAttr('global_scale_jaw_right.outputX','right_Jaw_stretchDiv.input1X', f=True )
	cmds.setAttr("right_jaw_curve.inheritsTransform",0)
	
	#connect to body 
	cmds.spaceLocator(n='neck_const_head_locator',p=(0,195,5))
	cmds.parent('neck_const_head_locator','sh_bind_jnt')
	cmds.duplicate('neck_const_head_locator', n='neck_orient_body_locator')
	cmds.parent('neck_orient_body_locator','DO_NOT_TOUCH')
	cmds.group('neck_2', n='neck_grp')
	cmds.parent('neck_grp','head_ALL_grp')
	cmds.parentConstraint('neck_const_head_locator','head_ALL_grp',mo=True, w=1)
	cmds.orientConstraint('neck_const_head_locator', 'neck_orient_body_locator','neck_grp',w=1)
	
	cmds.parent('jaw_ctrl', 'head_ALL_grp')
	
	cmds.addAttr('|pirate_Root_Transform|torso_GRP|Sh_FKConst_Grp|Sh_ctrl',ln="HeadRotation",at="enum",en="head:body:")
	cmds.setAttr('|pirate_Root_Transform|torso_GRP|Sh_FKConst_Grp|Sh_ctrl.HeadRotation', e=True,keyable=True)
	
	cmds.setAttr("Sh_ctrl.HeadRotation", 0)
	cmds.setAttr("neck_grp_orientConstraint1.neck_const_head_locatorW0",1)
	cmds.setAttr("neck_grp_orientConstraint1.neck_orient_body_locatorW1",1)
	cmds.setAttr("head_ALL_grp_parentConstraint1.neck_const_head_locatorW0",1)
	
	cmds.setDrivenKeyframe('neck_grp_orientConstraint1.neck_const_head_locatorW0',cd='Sh_ctrl.HeadRotation')
	cmds.setDrivenKeyframe('neck_grp_orientConstraint1.neck_orient_body_locatorW1',cd='Sh_ctrl.HeadRotation')
	cmds.setDrivenKeyframe('head_ALL_grp_parentConstraint1.neck_const_head_locatorW0',cd='Sh_ctrl.HeadRotation')
	
	cmds.setAttr("Sh_ctrl.HeadRotation", 1)
	cmds.setAttr("neck_grp_orientConstraint1.neck_const_head_locatorW0",0)
	cmds.setAttr("neck_grp_orientConstraint1.neck_orient_body_locatorW1",1)
	cmds.setAttr("head_ALL_grp_parentConstraint1.neck_const_head_locatorW0",0)
	
	cmds.setDrivenKeyframe('neck_grp_orientConstraint1.neck_const_head_locatorW0',cd='Sh_ctrl.HeadRotation')
	cmds.setDrivenKeyframe('neck_grp_orientConstraint1.neck_orient_body_locatorW1',cd='Sh_ctrl.HeadRotation')
	cmds.setDrivenKeyframe('head_ALL_grp_parentConstraint1.neck_const_head_locatorW0',cd='Sh_ctrl.HeadRotation')
	
	cmds.setAttr("Sh_ctrl.HeadRotation", 0)
	#facial controls
	faceCtrls=controlFace()
	#print faceCtrls
	attr=['.tx','.ty','.tz','.rx','.ry','.rz','.sx','.sy','.sz','.v']
	attrRot=['.rx','.ry','.rz','.sx','.sy','.sz','.v']
	attrTr=['.tx','.ty','.tz','.sx','.sy','.sz','.v']
	for i in attr:
		cmds.setAttr('jaw_ctrl'+i,l=True)
	for i in attrRot:
		cmds.setAttr('eye_main_ctrl'+i,l=True)
		cmds.setAttr('eye_right'+i,l=True)
		cmds.setAttr('eye_left'+i,l=True)
	for i in attrTr:
		cmds.setAttr('right_edge_hat_jnt1'+i,l=True)
		cmds.setAttr('right_edge_hat_jnt2'+i,l=True)
		cmds.setAttr('right_edge_hat_jnt3'+i,l=True)
		cmds.setAttr('left_edge_hat_jnt1'+i,l=True)
		cmds.setAttr('left_edge_hat_jnt2'+i,l=True)
		cmds.setAttr('left_edge_hat_jnt3'+i,l=True)
		
	cmds.select(clear=True)

def controlFace():
	cmds.curve(d=1.0, p=[(-92,229,0),(-92,203,0),(-40,203,0),(-40,229,0),(-92,229,0)],k=[0,1,2,3,4],n='faceBox')
	cmds.setAttr("faceBox.overrideEnabled", 1)
	cmds.setAttr("faceBox.overrideColor", 16)
	
	cmds.xform('faceBox', cp=True)
	boxNames=['blinkBox','moustacheBox', 'eyebrowsLBox','eyebrowsRBox', 'noseBox', 'hatBox']
	
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
	
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n='eye_main_ctrl')
	cmds.setAttr( 'eye_main_ctrl.translate',0,238,35 )
	cmds.setAttr( 'eye_main_ctrl.rotateX',-90 )
	cmds.setAttr( 'eye_main_ctrl.scale',10,10,4 )
	cmds.setAttr("eye_main_ctrl.overrideEnabled", 1)
	cmds.setAttr("eye_main_ctrl.overrideColor", 16)	
		
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n='eye_left')
	cmds.setAttr( 'eye_left.translate',3.789,237.936,35 )
	cmds.setAttr( 'eye_left.rotateX',-90 )
	cmds.setAttr("eye_left.overrideEnabled", 1)
	cmds.setAttr("eye_left.overrideColor", 16)

	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n='eye_right')
	cmds.setAttr( 'eye_right.translate',-3.826,237.98,35 )
	cmds.setAttr( 'eye_right.rotateX',-90 )
	cmds.setAttr("eye_right.overrideEnabled", 1)
	cmds.setAttr("eye_right.overrideColor", 16)

	cmds.makeIdentity('eye_right','eye_left', 'eye_main_ctrl', apply=True,t=1,r=1,s=1,n=0,pn=1)
	cmds.parent('eye_right','eye_left', 'eye_main_ctrl')
	
	cmds.aimConstraint('eye_right','right_eye', mo=True, w=1, aim=(1,0,0),upVector=(0,1,0),wut="vector", wu=(0,1,0))
	cmds.aimConstraint('eye_left','left_eye', mo=True, w=1, aim=(1,0,0),upVector=(0,1,0),wut="vector", wu=(0,1,0))

	mel.eval('addAttr -ln "face_Ctrls"  -at double  -min 0 -max 1 -dv 0 |pirate_Root_Transform|torso_GRP|Sh_FKConst_Grp|Sh_ctrl;')
	mel.eval('setAttr -e-keyable true |pirate_Root_Transform|torso_GRP|Sh_FKConst_Grp|Sh_ctrl.face_Ctrls;')
	
	cmds.setAttr("face_box_grp.visibility", 0)
	cmds.setDrivenKeyframe('face_box_grp.visibility',cd='|pirate_Root_Transform|torso_GRP|Sh_FKConst_Grp|Sh_ctrl.face_Ctrls')
	cmds.setAttr('|pirate_Root_Transform|torso_GRP|Sh_FKConst_Grp|Sh_ctrl.face_Ctrls',1)
	cmds.setAttr('face_box_grp.visibility',1)
	cmds.setDrivenKeyframe('face_box_grp.visibility',cd='|pirate_Root_Transform|torso_GRP|Sh_FKConst_Grp|Sh_ctrl.face_Ctrls')
	
	cmds.setAttr('|pirate_Root_Transform|torso_GRP|Sh_FKConst_Grp|Sh_ctrl.face_Ctrls',0)
	attr=['.tx','.tz','.rx','.ry','.rz','.sx','.sy','.sz','.v']
	for i in attr:
		for k in ctrlNames:
			cmds.setAttr(k+i,l=True)
			cmds.setAttr(k+'.ty',-9.5)
		for j in boxNames:
			cmds.setAttr(j+i,l=True)
		cmds.setAttr('faceBox'+i,l=True)
		cmds.setAttr('face_box_grp'+i,l=True)
	return ctrlNames
	

	#insert Joint function
def insertJoint(num_jnts):
	'''
	insert joints function equal distance from parent and child and oriented as well
	'''
	joints=cmds.ls(sl = True)
	if(len(joints)<2):
		cmds.error("select two joints!")

	else:
		parent=joints[0]
		child=joints[1]
		splitJoints(parent,child,num_jnts)
	
def splitJoints(parent, child, number):
	'''
	splits the joints
	'''

	number+=1
	cmds.select(cl=True)
	
	if((cmds.joint(ex=parent))==0 or (cmds.joint(ex=child))==0 ):
		cmds.error("doesnt exist!")

	jointPosP=cmds.joint(parent,q=True, p=True )
	jointPosC=cmds.joint(child,q=True, p=True )
	rotOrder=cmds.joint(parent, q=True, roo=True)
	cmds.parent(child, w=True)
	
	jointVector=[]
	jointVector.append((jointPosC[0]-jointPosP[0])/number)
	jointVector.append((jointPosC[1]-jointPosP[1])/number)
	jointVector.append((jointPosC[2]-jointPosP[2])/number)
		
	cmds.select(cl=True)
	lastJntCreated=parent
	for i in range(1,number):
		jnt=cmds.joint(p=(jointPosP[0]+i*jointVector[0],jointPosP[1]+i*jointVector[1],jointPosP[2]+i*jointVector[2]),n='new_jnt'+str(i))
		if(i==1):
			cmds.joint(parent, e=True, oj=rotOrder, sao='yup' ,ch=True, zso=True)
			cmds.parent(jnt,parent)
		lastJntCreated=jnt
	cmds.parent(child,lastJntCreated)
	cmds.joint(parent, e=True, oj=rotOrder, sao='yup' ,ch=True, zso=True)
	
	
	
	
def giveColour(newName,control):
	if newName=='left':
		cmds.setAttr(newName+control+".overrideEnabled", 1)
		cmds.setAttr(newName+control+".overrideColor", 4)
	if newName=='right':	
		cmds.setAttr(newName+control+".overrideEnabled", 1)
		cmds.setAttr(newName+control+".overrideColor", 6)	
	
def autoRigGUI():
	'''
	ui creating with buttons
	'''
	windowID = 'auto_Pirate_rig_gui'
	if cmds.window(windowID, exists=True):
		cmds.deleteUI(windowID)
	
	#cmds.file(force=True, new=True)	
	#creates the window
	window = cmds.window(windowID,title="Auto Pirate Rig UI", w=200,h=200, sizeable=False)
	cmds.columnLayout( adjustableColumn=True )
	
	#cmds.image( image='H:\pirate.jpe', w=295,h=307 )
	#cmds.image( image='/run/media/i7626222/POLDARK/pirate.jpe', w=295,h=307 )
	cmds.text( l='Automatic Rigging Tool for a PI-rate!')
	
	cmds.button( l='1. Rig it!', command=checkLocExist)
	cmds.button( l='a) create the spine', command=spineDO)
	
	cmds.text(l=" --- write left or right ---")
	legField = cmds.textField("legField", w = 200)
	cmds.button(l = "b) create a leg", align = "center",command = lambda *args:legDo(legField))
	armField = cmds.textField("armField", w = 200)
	cmds.button(l = 'c) create the arm', align = "center", command=lambda *args:armDo(armField))
	cmds.button(l = 'd) create the tentacle', align = "center", command=tentacleDo)
	cmds.button(l = 'e) create the face', align = "center", command=doFace)
	cmds.button(l = 'f) create the clothes', align = "center", command=doClothes)
	cmds.button(l = 'e) finalize', align = "center", command=skinEverything)
	
	cmds.button( l='2.Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') )
	cmds.setParent( '..' )
	cmds.showWindow() 

if __name__ == "__main__":
	autoRigGUI()


