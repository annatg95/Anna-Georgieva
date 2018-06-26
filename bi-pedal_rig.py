# Automatic Rigging script written by Anna Georgieva for bi-pedal
#1.1 ver modification for the major project
#using the autodesk tutorials for a comprehensive rig

import maya.cmds as cmds 
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
rightVar="right_"
length_l=len(leftVar)
length_r=len(rightVar)

for lineJnt in LeftLegJnt:
	if lineJnt.startswith("left_"):
		RightLegJnt.append('right_'+lineJnt[length_l:]) 

for lineJnt in feetLeftJnt:
	if lineJnt.startswith("left_"):
		feetRightJnt.append('right_'+lineJnt[length_l:]) 

rThumbJnts=[]	
rIndexJnts=[]
rMiddleJnts=[]
rRingJnts=[]
rPinkyJnts=[]

lThumbJnts=[]	
lIndexJnts=[]
lMiddleJnts=[]
lRingJnts=[]
lPinkyJnts=[]


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

for item,item2,item3,item4,item5, item6 in zip(rThumbJnts,rIndexJnts,rMiddleJnts,rRingJnts,rPinkyJnts,RightArmJnt) :
	if item.startswith("right_"):
		lThumbJnts.append('left_'+item[length_r:]) 
	if item2.startswith("right_"):
		lIndexJnts.append('left_'+item2[length_r:]) 
	if item3.startswith("right_"):
		lMiddleJnts.append('left_'+item3[length_r:]) 
	if item4.startswith("right_"):
		lRingJnts.append('left_'+item4[length_r:]) 
	if item5.startswith("right_"):
		lPinkyJnts.append('left_'+item5[length_r:]) 
				
	if item6.startswith("right_"):
		LeftArmJnt.append('left_'+item6[length_r:]) 		

			
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

leftArmIK=[]  #checkLocExist
leftArmFK=[]	#checkLocExist

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
			cmds.joint(i,n=str(i)+'_jnt',rad=0.1)
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
				leftArmIK.append(LeftArmJnt[i]+'_IK')
				
			else:	
				cmds.duplicate(RightArmJnt[i],n=RightArmJnt[i]+'_FK')
				rightArmFK.append(RightArmJnt[i]+'_FK')	
				leftArmFK.append(LeftArmJnt[i]+'_FK')
				
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
			rightLegIK.append('right_'+lineIK[length_l:])	
		if lineFK.startswith("left_"):
			rightLegFK.append('right_'+lineFK[length_l:])	
			
	for lineFK,lineIK in zip(leftFeetIK,leftFeetFK):
		if lineFK.startswith("left_"):
			rightFeetFK.append('right_'+lineFK[length_l:]) 
		if lineIK.startswith("left_"):
			rightFeetIK.append('right_'+lineIK[length_l:]) 		
			
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
	#legs mirror right
	cmds.mirrorJoint('left_start_leg_jnt',mirrorYZ=True,mirrorBehavior=True,searchReplace=('left_', 'right_') )
	cmds.mirrorJoint('left_start_leg_jnt_FK',mirrorYZ=True,mirrorBehavior=True,searchReplace=('left_', 'right_') )
	cmds.mirrorJoint('left_start_leg_jnt_IK',mirrorYZ=True,mirrorBehavior=True,searchReplace=('left_', 'right_') )

	#arms mirror left
	cmds.mirrorJoint('right_start_arm_jnt',mirrorYZ=True,mirrorBehavior=True,searchReplace=('right_','left_') )
	cmds.mirrorJoint('right_start_arm_jnt_FK',mirrorYZ=True,mirrorBehavior=True,searchReplace=('right_','left_') )
	cmds.mirrorJoint('right_start_arm_jnt_IK',mirrorYZ=True,mirrorBehavior=True,searchReplace=('right_','left_') )

	##fingers mirror left
	cmds.mirrorJoint('right_thumb_start_jnt',mirrorYZ=True,mirrorBehavior=True,searchReplace=('right_','left_') )
	cmds.mirrorJoint('right_index_start_jnt',mirrorYZ=True,mirrorBehavior=True,searchReplace=('right_','left_') )
	cmds.mirrorJoint('right_middle_start_jnt',mirrorYZ=True,mirrorBehavior=True,searchReplace=('right_','left_') )
	cmds.mirrorJoint('right_ring_start_jnt',mirrorYZ=True,mirrorBehavior=True,searchReplace=('right_','left_') )
	cmds.mirrorJoint('right_pinky_start_jnt',mirrorYZ=True,mirrorBehavior=True,searchReplace=('right_','left_') )


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
	cmds.setAttr('Hip_ctrl.s',6,6,6)
	cmds.setAttr('Sh_ctrl.s',6,6,6)
	
	posHip=[cmds.getAttr('start_spine.translateX'),cmds.getAttr('start_spine.translateY'),cmds.getAttr('start_spine.translateZ')]
	cmds.setAttr('Hip_ctrl.translate',posHip[0]+0.5,posHip[1]-1,posHip[2]-0.5)
	posSh=[cmds.getAttr('end_spine.translateX'),cmds.getAttr('end_spine.translateY'),cmds.getAttr('end_spine.translateZ')]
	cmds.setAttr('Sh_ctrl.translate',posSh[0]+0.5,posSh[1]-1,posSh[2]-0.5)
		
	cmds.setAttr("Sh_ctrlShape.overrideEnabled", 1)
	cmds.setAttr("Sh_ctrlShape.overrideColor", 16)

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
		cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=5.5,d=3,ut=0,tol=0.01,s=8,ch=1, n=item+'ctrl')
		
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
		cmds.scale(3,3,3,item+'ctrlShape.cv[0:7]',p=position,r=True)	
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
	cmds.setAttr('body_Ctrl.s',6,6,6)
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
	pos1=[cmds.getAttr('mid_spine3.tx'),cmds.getAttr('mid_spine3.ty'),cmds.getAttr('mid_spine3.tz')]
	pos2=[cmds.getAttr('mid_spine2.tx'),cmds.getAttr('mid_spine2.ty'),cmds.getAttr('mid_spine2.tz')]
	cmds.joint(p=(pos1[0],pos1[1],pos1[2]),rad=1,n='breathe_ik_1')
	cmds.select(clear=True)
	cmds.joint(p=(pos2[0],pos2[1],pos2[2]),rad=1,n='breathe_ik_2')
	cmds.select(clear=True)
	cmds.select('breathe_ik_1','breathe_ik_2','spine_curve_ik_handle')
	mel.eval('skinClusterInfluence 1 "-ug -dr 4 -ps 0 -ns 10";')
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=4,d=3,ut=0,tol=0.01,s=8,ch=1, n='breathe_ctrl_1')
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=4,d=3,ut=0,tol=0.01,s=8,ch=1, n='breathe_ctrl_2')
	cmds.xform('breathe_ctrl_1Shape.cv[0:7]', ro=(90,0,0))
	cmds.xform('breathe_ctrl_2Shape.cv[0:7]', ro=(90,0,0))
	
	cmds.parent('breathe_ctrl_1Shape','breathe_ik_1',r=True,s=True)
	cmds.parent('breathe_ctrl_2Shape','breathe_ik_2',r=True,s=True)
	cmds.parent('breathe_ik_1','breathe_ik_2', 'torso_GRP')
	cmds.setAttr("breathe_ctrl_1Shape.overrideEnabled", 1)
	cmds.setAttr("breathe_ctrl_1Shape.overrideColor", 17)
	cmds.setAttr("breathe_ctrl_2Shape.overrideEnabled", 1)
	cmds.setAttr("breathe_ctrl_2Shape.overrideColor", 17)
	
	cmds.move(0,0,-15,'breathe_ik_2.cv[0:7]', 'breathe_ik_1.cv[0:7]', r=True )
	cmds.delete(' breathe_ctrl_2', 'breathe_ctrl_1')
	###squash and stretch settings on off
	
	cmds.distanceDimension(sp=(0,2,0),ep=(0,1,0))
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
	cmds.xform('pirate_root_ctrlShape.cv[0:7]', s=(15,15,15))
	cmds.xform('pirate_root_ctrlShape.cv[0:7]', t=(0,-10,0))
	##move 0 -12 0
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
	#creates the leg left or right
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
	cmds.xform(newName+'_Leg_settingsCTRL',s=(4,4,4))
	
	######### colour it
	giveColour(newName,'_Leg_settingsCTRL') 	
	cmds.setAttr(newName+'_Leg_settingsCTRL.translate',anklePos[0],anklePos[1],anklePos[2]-10)
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
		cmds.xform(x+'ctrlShape.cv[0:15]', s=(6,6,6) )
		#cmds.xform( x+'ctrlShape.cv[0:4]', x+'ctrlShape.cv[7]', x+'ctrlShape.cv[10]', x+'ctrlShape.cv[13]',r=True,t=(0, -50, 0))
	
	
	#for the feet one only
	cmds.curve(d=1, p=[(-3, 0, -1),(-3, 0, 2),(2, 0, 2),(2, 0, -1), (-3, 0, -1), (-3, 2, -1),(-3, 2, 2 ), (-3, 0, 2 ),(-3, 2, 2), (2, 2, 2), (2,0,2), (2, 2, 2), (2,2,-1), (2,0,-1), (2,2,-1),(-3,2,-1) ], 
						k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 ],n=newName+'_feet_start_jnt_FK'+'ctrl')
	cmds.pickWalk(newName+'_feet_start_jnt_FKctrl',d='down')
	cmds.rename('curveShape1',newName+'_feet_start_jnt_FK'+'ctrlShape')
	cmds.makeIdentity(newName+'_feet_start_jnt_FK',apply=True,t=1,r=6,s=1,n=0,pn=1)
	###colour
	giveColour(newName,'_feet_start_jnt_FK') 
		
	cmds.parent(newName+'_feet_start_jnt_FKctrlShape', newName+'_feet_start_jnt_FK',r=True,s=True)
	cmds.xform(newName+'_feet_start_jnt_FKctrlShape.cv[0:15]', s=(4,3,6) )
	cmds.xform(newName+'_feet_start_jnt_FKctrlShape.cv[0:4]', newName+'_feet_start_jnt_FKctrlShape.cv[7]', newName+'_feet_start_jnt_FKctrlShape.cv[10]', newName+'_feet_start_jnt_FKctrlShape.cv[13]',r=True,t=(0, -5, 0))
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
	cmds.setAttr(newName+'Foot_Ctrl.translate', anklePos[0],anklePos[1]-5,anklePos[2])
	cmds.setAttr(newName+'Foot_Ctrl.s', 6,6,6)
	
	if newName=='left': #for left red
		cmds.setAttr(newName+"Foot_Ctrl.overrideEnabled", 1)
		cmds.setAttr(newName+"Foot_Ctrl.overrideColor", 4)
	if newName=='right': #for right blue
		cmds.setAttr(newName+"Foot_Ctrl.overrideEnabled", 1)
		cmds.setAttr(newName+"Foot_Ctrl.overrideColor", 6)
	
	cmds.xform(newName+'Foot_Ctrl.cv[3:7]',t=(0 ,0 ,2), r=True) 
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
		
		### OPRAVIII
		
		#mel.eval('selectKey -add -k -f 124.397377 right_mid_leg_jnt_IK_translateX ;')
		#cmds.setInfinity(poi='linear')
		
		cmds.keyTangent('right_end_leg_jnt_IK',e=True,itt='spline',ott='spline', animation='objects')
		
		### OPRAVIII
		
		#mel.eval('selectKey -add -k -f 124.397377 right_end_leg_jnt_IK_translateX ;')
		#cmds.setInfinity(poi='linear')
	
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
		
		### OPRAVIII
		
		#mel.eval('selectKey -add -k -f 124.397377 left_mid_leg_jnt_IK_translateX ;')
		cmds.setInfinity(poi='linear')
		
		cmds.keyTangent('left_end_leg_jnt_IK',e=True,itt='spline',ott='spline', animation='objects')
		
		### OPRAVIII za full stretch sq samo 2
		#mel.eval('selectKey -add -k -f 124.397377 left_end_leg_jnt_IK_translateX ;')
		#cmds.setInfinity(poi='linear')
	
	#knee ctrl
	cmds.spaceLocator(n=newName+'Knee_ctrl',p=(PosKnee[0], PosKnee[1], PosKnee[2]+15))
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
	cmds.setAttr(newName+'_knee_ctrl.scale', 1,1,1)
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
	cmds.setAttr(newName+'_thigh_toKnee_end_loc.translate',PosKnee[0],PosKnee[1],PosKnee[2]+15)
	
	mel.eval('distanceDimension -sp 12.108383 85.415562 18.40254 -ep 12.108383 8.333226 2.893481 ;')
	cmds.rename('locator1',newName+'_kneeToFoot_start_loc')
	cmds.rename('locator2',newName+'_kneeToFoot_end_loc')
	cmds.setAttr(newName+'_kneeToFoot_start_loc.translate',PosKnee[0],PosKnee[1],PosKnee[2]+15)
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
		cmds.xform(newName+'heel_loc',cp=1, t=(0,-1.258,-0.919))
	if newName=='right':
		cmds.xform(newName+'heel_loc',cp=1, t=(0,-1.258,-0.919))  #right
	
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
		cmds.spaceLocator(n=newName+'inner_foot_loc',p=[1,0,1.5])
		cmds.xform(newName+'inner_foot_loc',cp=1)
		cmds.spaceLocator(n=newName+'outer_foot_loc',p=[2.191,0,1.5])
		cmds.xform(newName+'outer_foot_loc',cp=1)
	if newName=='right':
		cmds.spaceLocator(n=newName+'inner_foot_loc',p=[-1,0,1.5])
		cmds.xform(newName+'inner_foot_loc',cp=1)
		cmds.spaceLocator(n=newName+'outer_foot_loc',p=[-2.191,0,1.5])
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
		a=30
		
	if newName=='right':
		a=-30
		
	cmds.setDrivenKeyframe(newName+'outer_foot_loc.rotateZ', cd=newName+'Foot_Ctrl.tilt_out')
	cmds.setAttr(newName+"Foot_Ctrl.tilt_out", 10)
	cmds.setAttr(newName+"outer_foot_loc.rotateZ", a)
	cmds.setDrivenKeyframe(newName+'outer_foot_loc.rotateZ', cd=newName+'Foot_Ctrl.tilt_out')
	cmds.setAttr(newName+"Foot_Ctrl.tilt_out", 0)
	
	'''	
	### tilt in fix
	if newName=="right":
		cmds.setAttr(newName+'Foot_Ctrl.tilt_in',0)
		cmds.setDrivenKeyframe(newName+'inner_foot_loc.rotateZ', cd=newName+'Foot_Ctrl.tilt_in')
		cmds.setAttr(newName+'Foot_Ctrl.tilt_in',10)
		cmds.setAttr(newName+"inner_foot_loc.rotateZ", -30)
		cmds.setDrivenKeyframe(newName+'inner_foot_loc.rotateZ', cd=newName+'Foot_Ctrl.tilt_in')
		cmds.setAttr(newName+"Foot_Ctrl.tilt_in", 0)
	
	if newName=="left":
		###doesnt work
		cmds.setAttr(newName+"Foot_Ctrl.tilt_in", 0)
		cmds.setDrivenKeyframe(newName+'inner_foot_loc.rotateZ',cd=newName+'Foot_Ctrl.tilt_in')
		cmds.setAttr(newName+"inner_foot_loc.rotateZ",30)
		cmds.setAttr(newName+"Foot_Ctrl.tilt_in", 10)
		cmds.setDrivenKeyframe(newName+'inner_foot_loc.rotateZ',cd=newName+'Foot_Ctrl.tilt_in')
		cmds.setAttr(newName+"Foot_Ctrl.tilt_in", 0)
	'''
	
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
	cmds.move( 0, 0, -0.614271, newName+'wiggle_grp.scalePivot', newName+'wiggle_grp.rotatePivot',r=True)
	#tomorrow last part legs
	
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
	
	##hide locators and lock values
	kneeLoc=[newName+'_kneeToFoot_start_loc',newName+'_thigh_toKnee_end_loc',newName+'Knee_pv']
	for i in kneeLoc:
		cmds.setAttr(i+'.v',0)


	
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
	
	##right arm end
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
	
	###ik to fk !!!!!!!!!!!!!!!
	'''
	#left
	$rl_hand= `xform -query -worldSpace -rotation leftArm_IK_snap`;
	xform -worldSpace -rotation $rl_hand[0] $rl_hand[1] $rl_hand[2] leftArm_ctrl;
	matchTransform -pos leftArm_ctrl left_end_arm_jnt_FK;
	
	#right 
	$rr_hand= `xform -query -worldSpace -rotation rightArm_IK_snap`;
	xform -worldSpace -rotation $rr_hand[0] $rr_hand[1] $rr_hand[2] rightArm_ctrl;
	matchTransform -pos rightArm_ctrl right_end_arm_jnt_FK;
	
	'''
	cmds.duplicate('leftArm_ctrl', n='leftArm_IK_snap')
	cmds.delete('leftArm_IK_snap|lefthand_hdl', 'leftArm_IK_snap|leftArm_hdl', 'leftArm_IK_snap|leftArm_IK_end', 'leftArm_IK_snap|left_elbowToWrist_end')
	cmds.parent('leftArm_IK_snap','left_end_arm_jnt')
	
	
	cmds.duplicate('rightArm_ctrl', n='rightArm_IK_snap')
	cmds.delete('rightArm_IK_snap|righthand_hdl', 'rightArm_IK_snap|rightArm_hdl', 'rightArm_IK_snap|rightArm_IK_end', 'rightArm_IK_snap|right_elbowToWrist_end')
	cmds.parent('rightArm_IK_snap','right_end_arm_jnt')
	
	##elbow ik to fk 
	'''
	#left
	$tl_elbow= `xform -query -worldSpace -translation left_mid_arm_jnt`;
	$tl_elbow[1]*=-1;
	xform -worldSpace -translation $tl_elbow[0] $tl_elbow[1] $tl_elbow[2] leftelbow_Ctrl;
	
	#right
	$tr_elbow= `xform -query -worldSpace -translation right_mid_arm_jnt`;
	$tr_elbow[1]*=-1;
	xform -worldSpace -translation $tr_elbow[0] $tr_elbow[1] $tr_elbow[2] rightelbow_Ctrl;
	'''
	
	#legs ik to fk
	
	cmds.duplicate('leftFoot_Ctrl', n='leftFoot_IK_SNAP')
	cmds.delete('leftFoot_IK_SNAP|leftheel_loc')
	cmds.parent('leftFoot_IK_SNAP','left_end_leg_jnt')
		
	cmds.duplicate('rightFoot_Ctrl', n='rightFoot_IK_SNAP')
	cmds.delete('rightFoot_IK_SNAP|rightheel_loc')
	cmds.parent('rightFoot_IK_SNAP','right_end_leg_jnt')
	'''
	$rl_leg= `xform -query -worldSpace -rotation leftFoot_IK_SNAP`;
	xform -worldSpace -rotation $rl_leg[0] $rl_leg[1] $rl_leg[2] leftFoot_Ctrl;
	matchTransform -pos leftFoot_Ctrl left_end_leg_jnt_FK;
	'''
	
	''' dont use it
	$tl_knee= `xform -query -worldSpace -translation left_mid_leg_jnt`;
	$tl_knee[1]*=-1;
	xform -worldSpace -translation $tl_knee[0] $tl_knee[1] $tl_knee[2] left_knee_ctrl;
	'''
	
	'''
	$rr_leg= `xform -query -worldSpace -rotation rightFoot_IK_SNAP`;
	xform -worldSpace -rotation $rr_leg[0] $rr_leg[1] $rr_leg[2] rightFoot_Ctrl;
	matchTransform -pos rightFoot_Ctrl right_end_leg_jnt_FK;
	'''
	
	##left arm upper
	cmds.duplicate('left_start_arm_jnt_FK', n='left_start_arm_jnt_FK_SNAP')
	cmds.setAttr('left_start_arm_jnt_FK_SNAP.tx',l=False)
	cmds.setAttr('left_start_arm_jnt_FK_SNAP.ty',l=False)
	cmds.setAttr('left_start_arm_jnt_FK_SNAP.tz',l=False)
	cmds.delete('left_start_arm_jnt_FK_SNAP|left_mid_arm_jnt_FK','left_start_arm_jnt_FK_SNAP|left_start_arm_jntctrlShape')
	cmds.parent('left_start_arm_jnt_FK_SNAP','left_start_arm_jnt')
	###
	#$r_upperArm= `xform -query -worldSpace -rotation left_start_arm_jnt_FK_SNAP`;
	#xform -worldSpace -rotation $r_upperArm[0] $r_upperArm[1] $r_upperArm[2] left_start_arm_jnt_FK
	
	##left arm mid
	cmds.duplicate('left_mid_arm_jnt_FK', n='left_mid_arm_jnt_FK_SNAP')
	cmds.setAttr('left_mid_arm_jnt_FK_SNAP.tx',l=False)
	cmds.setAttr('left_mid_arm_jnt_FK_SNAP.ty',l=False)
	cmds.setAttr('left_mid_arm_jnt_FK_SNAP.tz',l=False)
	cmds.delete('left_mid_arm_jnt_FK_SNAP|left_end_arm_jnt_FK', 'left_mid_arm_jnt_FK_SNAP|left_mid_arm_jntctrlShape')
	cmds.parent('left_mid_arm_jnt_FK_SNAP','left_mid_arm_jnt')
	###
	#$r_midArm= `xform -query -worldSpace -rotation left_mid_arm_jnt_FK_SNAP`;
	#xform -worldSpace -rotation $r_midArm[0] $r_midArm[1] $r_midArm[2] left_mid_arm_jnt_FK
	
	##left arm mid
	cmds.duplicate('left_end_arm_jnt_FK', n='left_end_arm_jnt_FK_SNAP')
	cmds.setAttr('left_end_arm_jnt_FK_SNAP.tx',l=False)
	cmds.setAttr('left_end_arm_jnt_FK_SNAP.ty',l=False)
	cmds.setAttr('left_end_arm_jnt_FK_SNAP.tz',l=False)
	cmds.delete('left_end_arm_jnt_FK_SNAP|left_hand_jnt_FK', 'left_end_arm_jnt_FK_SNAP|left_end_arm_jntctrlShape')
	cmds.parent('left_end_arm_jnt_FK_SNAP','left_end_arm_jnt')
	###
	#$r_endArm= `xform -query -worldSpace -rotation left_end_arm_jnt_FK_SNAP`;
	#xform -worldSpace -rotation $r_endArm[0] $r_endArm[1] $r_endArm[2] left_end_arm_jnt_FK
	
	#marking menu
	'''
	$l_upperArm= `xform -query -worldSpace -rotation left_start_arm_jnt_FK_SNAP`;
	xform -worldSpace -rotation $l_upperArm[0] $l_upperArm[1] $l_upperArm[2] left_start_arm_jnt_FK;
	$l_midArm= `xform -query -worldSpace -rotation left_mid_arm_jnt_FK_SNAP`;
	xform -worldSpace -rotation $l_midArm[0] $l_midArm[1] $l_midArm[2] left_mid_arm_jnt_FK;
	$l_endArm= `xform -query -worldSpace -rotation left_end_arm_jnt_FK_SNAP`;
	xform -worldSpace -rotation $l_endArm[0] $l_endArm[1] $l_endArm[2] left_end_arm_jnt_FK;
	'''
	
	###ik to fk
	'''
	matchTransform -pos leftArm_ctrl left_end_arm_jnt_FK;
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
		
###
###
###

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
		dictionary={'LeftArmJnt':LeftArmJnt,'leftArmIK':leftArmIK,'leftArmFK':leftArmFK }
	if(newName=='right'):
		dictionary={'RightArmJnt':RightArmJnt, 'rightArmIK':rightArmIK,'rightArmFK':rightArmFK}
	
	#create all the ik fk blenNodes for the switch
	armOriginal=dictionary[newName.title()+'ArmJnt']

	for item in armOriginal: 
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
		cmds.xform(y+'.cv[0:7]',s=(8, 8, 8),r=True) ####scale
		cmds.xform(y+'.cv[0:7]',ro=(90, 90, 0),r=True)
		
		if newName=='right':
			cmds.setAttr(y+".overrideEnabled", 1)
			cmds.setAttr(y+".overrideColor", 6)	
		if newName=='left':
			cmds.setAttr(y+".overrideEnabled", 1)
			cmds.setAttr(y+".overrideColor", 4)	
		
	cmds.delete(newName+'_start_arm_jntctrl',newName+'_mid_arm_jntctrl',newName+'_end_arm_jntctrl',newName+'_hand_jntctrl')
	cmds.delete(newName+'_end_arm_jnt_FK|'+newName+'_hand_jnt_FK|'+newName+'_hand_jntctrlShape' )	
	
	ArmJnt=dictionary[newName.title()+'ArmJnt']
	ArmFK=dictionary[newName+'ArmFK']
	ArmIK=dictionary[newName+'ArmIK']
	
	##orient the arm before the mirroring
	cmds.joint(newName+'_start_arm_jnt', newName+'_start_arm_jnt_FK', newName+'_start_arm_jnt_IK',e=True,oj='xyz',sao='ydown',ch=True,zso=True)

	#cmds.setAttr(newName+"_mid_arm_jnt_FK.rotateOrder",3)  #WRONG 
	#cmds.setAttr(newName+"_end_arm_jnt_FK.rotateOrder", 5)	###MAKES THE ARM GO SOMEWHERE ELSE
	
	#fk controls
	mel.eval('curve -d 1 -p 0 0 -2 -p 0 0 2 -p -2 0 0 -p 2 0 0 -p 0 0 2 -p -2 0 0 -p 0 0 -2 -p 2 0 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 ;')
	cmds.rename('curve1', newName+'_Arm_settingsCTRL')
	
	if newName=='right':
		cmds.setAttr(newName+'_Arm_settingsCTRL.translate',endArm[0]-25,endArm[1],endArm[2])
		cmds.setAttr(newName+'_Arm_settingsCTRL'+".overrideEnabled", 1)
		cmds.setAttr(newName+'_Arm_settingsCTRL'+".overrideColor", 6)	
		
	if newName=='left':
		cmds.setAttr(newName+'_Arm_settingsCTRL.translate',endArm[0]+25,endArm[1],endArm[2])
		cmds.setAttr(newName+'_Arm_settingsCTRL'+".overrideEnabled", 1)
		cmds.setAttr(newName+'_Arm_settingsCTRL'+".overrideColor", 4)	
		
	cmds.setAttr(newName+'_Arm_settingsCTRL.scale',2,2,2)
	cmds.parentConstraint(newName+'_end_arm_jnt',newName+'_Arm_settingsCTRL',mo=True, w=1)
	cmds.group(newName+'_Arm_settingsCTRL', n=newName+'A_settings_GRP')
	
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
	splitJoints(newName+'_start_arm_jnt1',newName+'_mid_arm_jnt1',1,newName)
	if(cmds.objExists('new_jnt1')):
		cmds.rename('new_jnt1',MidTwist[0]) 
		
	splitJoints(newName+'_start_arm_jnt1',MidTwist[0],1,newName)
	if(cmds.objExists('new_jnt1')):
		cmds.rename('new_jnt1',MidTwist[1]) 
		
	splitJoints(MidTwist[0],newName+'_mid_arm_jnt1',1,newName)
	if(cmds.objExists('new_jnt1')):
		cmds.rename('new_jnt1',MidTwist[2]) 
	
	splitJoints(MidTwist[2],newName+'_mid_arm_jnt1',1,newName)
	if(cmds.objExists('new_jnt1')):
		cmds.rename('new_jnt1',MidTwist[3]) 

	cmds.move(midArm[0], midArm[1], midArm[2], MidTwist[3],rpr=True)
	cmds.move(midArm[0], midArm[1], midArm[2], newName+'_mid_arm_jnt1', rpr=True)	
	cmds.parent(newName+'_mid_arm_jnt1',w=True)
####
	splitJoints(newName+'_mid_arm_jnt1',newName+'_end_arm_jnt1',1,newName)
	if(cmds.objExists('new_jnt1')):
		cmds.rename('new_jnt1',MidTwist[4]) 
		
	splitJoints(newName+'_mid_arm_jnt1',MidTwist[4],1,newName)
	if(cmds.objExists('new_jnt1')):
		cmds.rename('new_jnt1',MidTwist[5]) 
		
	splitJoints(MidTwist[4],newName+'_end_arm_jnt1',1,newName)
	if(cmds.objExists('new_jnt1')):
		cmds.rename('new_jnt1',MidTwist[6]) 
	
	splitJoints(MidTwist[6],newName+'_end_arm_jnt1',1,newName)
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
	if newName=='right':
		a=-1
		b=4
	if newName=='left':
		a=1	
		b=3 
		
	cmds.setAttr(newName+"upperArm_handle.dTwistControlEnable",1)
	cmds.setAttr(newName+"upperArm_handle.dWorldUpType",4)
	cmds.setAttr(newName+"upperArm_handle.dWorldUpAxis",b)
	cmds.setAttr(newName+"upperArm_handle.dWorldUpVectorY",0)
	cmds.setAttr(newName+"upperArm_handle.dWorldUpVectorZ",a)  ##different for elft +1
	cmds.setAttr(newName+"upperArm_handle.dWorldUpVectorEndY",0)
	cmds.setAttr(newName+"upperArm_handle.dWorldUpVectorEndZ",a)##+1
	
	cmds.connectAttr(newName+'_upperArmStart_bindJnt.worldMatrix[0]',newName+'upperArm_handle.dWorldUpMatrix', f=True)
	cmds.connectAttr(newName+'_upperArmMid_bindJnt.worldMatrix[0]', newName+'upperArm_handle.dWorldUpMatrixEnd',f=True)
	
	
### OPTIMIZE
	pointsDown= [[midArm[0], midArm[1], midArm[2]],
          [endArm[0], endArm[1],endArm[2]]]
	cmds.curve(ep=pointsDown, d=1) ##d=1 for 2cv points only
	cmds.rename('curve1', newName+'lowerArm_Curve')
	cmds.ikHandle(n=newName+'lowerArm_handle',sj=newName+'_mid_arm_jnt1',ee=newName+'_end_arm_jnt1',sol='ikSplineSolver',ccv=False,c=newName+'lowerArm_Curve')
	
	
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
	cmds.setAttr(newName+"lowerArm_handle.dWorldUpAxis", b)
	cmds.setAttr(newName+"lowerArm_handle.dWorldUpVectorY", 0)
	cmds.setAttr(newName+"lowerArm_handle.dWorldUpVectorEndY", 0)
	cmds.setAttr(newName+"lowerArm_handle.dWorldUpVectorZ",a)
	cmds.setAttr(newName+"lowerArm_handle.dWorldUpVectorEndZ", a)
	
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
	##########
###squash and stretch for the segmented joints
	cmds.shadingNode('curveInfo',au=True ,n=newName+'_upperArm_length')
	cmds.shadingNode('multiplyDivide', au=True, n=newName+'_upperArmNormDiv')
	cmds.connectAttr(newName+'upperArm_Curve.worldSpace[0]', newName+'_upperArm_length.inputCurve', f=True)
	cmds.connectAttr(newName+'_upperArm_length.arcLength', newName+'_upperArmNormDiv.input1X')
	cmds.setAttr(newName+"_upperArmNormDiv.operation", 2)
	cmds.setAttr(newName+"_upperArmNormDiv.input2X", cmds.getAttr(newName+'_upperArmNormDiv.input1X'))
	if newName=='right':
		upperArmJnts=[newName+'_start_arm_jnt1','r_b_midTwist','r_a_midTwist','r_c_midTwist']
	if newName=='left':
		upperArmJnts=[newName+'_start_arm_jnt1','l_b_midTwist','l_a_midTwist','l_c_midTwist']
	for i in upperArmJnts:
		cmds.connectAttr(newName+'_upperArmNormDiv.outputX',i+'.scaleX',f=True)
		
	cmds.shadingNode('curveInfo',au=True ,n=newName+'_lowerArm_length')
	cmds.shadingNode('multiplyDivide', au=True, n=newName+'_lowerArmNormDiv')
	cmds.connectAttr(newName+'lowerArm_Curve.worldSpace[0]', newName+'_lowerArm_length.inputCurve', f=True)
	cmds.connectAttr(newName+'_lowerArm_length.arcLength', newName+'_lowerArmNormDiv.input1X')
	cmds.setAttr(newName+"_lowerArmNormDiv.operation", 2)
	cmds.setAttr(newName+"_lowerArmNormDiv.input2X", cmds.getAttr(newName+'_lowerArmNormDiv.input1X'))	
	if newName=='right':
		lowerArmJnts=['right_mid_arm_jnt1', 'r_f_midTwist','r_e_midTwist','r_g_midTwist','r_h_midTwist']
	if newName=='left':
		lowerArmJnts=['left_mid_arm_jnt1', 'l_f_midTwist','l_e_midTwist','l_g_midTwist','l_h_midTwist']
	for i in lowerArmJnts:
		cmds.connectAttr(newName+'_lowerArmNormDiv.outputX',i+'.scaleX',f=True)

###fk squash and stretch
	addFKlength=[newName+'_start_arm_jnt_FK', newName+'_mid_arm_jnt_FK ']
	for i in addFKlength:
		cmds.addAttr(i,ln="length", at='double', min=0, max=5, dv=1 )
		cmds.setAttr(i+'.length',e=True,keyable=True)
	cmds.setDrivenKeyframe(newName+'_mid_arm_jnt_FK.translateX', cd=newName+'_start_arm_jnt_FK.length')
	cmds.setDrivenKeyframe(newName+'_end_arm_jnt_FK.translateX', cd=newName+'_mid_arm_jnt_FK.length')
	cmds.setAttr(newName+'_start_arm_jnt_FK.length',0)
	cmds.setAttr(newName+'_mid_arm_jnt_FK.translateX',0)
	cmds.setDrivenKeyframe(newName+'_mid_arm_jnt_FK.translateX', cd=newName+'_start_arm_jnt_FK.length')
	cmds.setAttr(newName+'_mid_arm_jnt_FK.length',0)
	cmds.setAttr(newName+'_end_arm_jnt_FK.translateX',0)
	cmds.setDrivenKeyframe(newName+'_end_arm_jnt_FK.translateX', cd=newName+'_mid_arm_jnt_FK.length')
	
	cmds.setAttr(newName+'_start_arm_jnt_FK.length',1)
	cmds.setAttr(newName+'_mid_arm_jnt_FK.length',1)
	###
##for ik	
	mel.eval('curve -d 1 -p -2.955302 0 -0.985101 -p -3 0 2 -p 2 0 2 -p 2 0 -1 -p -3 0 -1 -p -3 2 -1 -p -3 2 2 -p -3 0 2 -p -3 2 2 -p 2 2 2 -p 2 0 2 -p 2 2 2 -p 2 2 -1 -p 2 0 -1 -p 2 2 -1 -p -3 2 -1 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 ;')
	cmds.rename('curve1', newName+'Arm_ctrl')
	cmds.xform(newName+'Arm_ctrl', cp=1)
	cmds.parentConstraint(newName+'_end_arm_jnt_IK',newName+'Arm_ctrl',mo=False, w=1)
	cmds.delete(newName+'Arm_ctrl_parentConstraint1')
	cmds.xform(newName+'Arm_ctrl',s=(0.5,0.5,0.5))   ###
	if newName=='right':
		cmds.setAttr(newName+'Arm_ctrl'+".overrideEnabled", 1)
		cmds.setAttr(newName+'Arm_ctrl'+".overrideColor", 6)	
		
	if newName=='left':
		cmds.setAttr(newName+'Arm_ctrl'+".overrideEnabled", 1)
		cmds.setAttr(newName+'Arm_ctrl'+".overrideColor", 4)	
		
	cmds.makeIdentity(newName+'Arm_ctrl',apply=True,t=1,r=1,s=0,n=0,pn=1)
	
	if newName=='right':
		cmds.setAttr(newName+'_mid_arm_jnt_IK.rotateY',-10)
	if newName=='left':
		cmds.setAttr(newName+'_mid_arm_jnt_IK.rotateY',10)
	cmds.joint(newName+'_mid_arm_jnt_IK',e=True,spa=True)
	cmds.setAttr(newName+'_mid_arm_jnt_IK.rotateY',0)	
	cmds.ikHandle(n=newName+'Arm_hdl',sj=newName+'_start_arm_jnt_IK',ee=newName+'_end_arm_jnt_IK',sol='ikRPsolver')
	cmds.ikHandle(n=newName+'hand_hdl',sj=newName+'_end_arm_jnt_IK',ee=newName+'_hand_jnt_IK',sol='ikSCsolver')
	
	#ik rotate is not moving the fk one responsible for the forearm twist!!
	cmds.parent(newName+'hand_hdl',newName+'Arm_hdl',newName+'Arm_ctrl')
	
##expression  
	mel.eval('distanceDimension -sp -2 0 0 -ep -1 0 0 ;')
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
	if newName=='left':
		mel.eval('selectKey -add -k -f 13 left_mid_arm_jnt_IK_translateX ;')
	
	if newName=='right':
		mel.eval('selectKey -add -k -f 13 right_mid_arm_jnt_IK_translateX ;')
	cmds.setInfinity(poi='linear')
	
	cmds.keyTangent(newName+'_end_arm_jnt_IK',e=True,itt='spline',ott='spline', animation='objects')
	if newName=='right':
		mel.eval('selectKey -add -k -f 13 right_end_arm_jnt_IK_translateX ;')
	if newName=='left':
		mel.eval('selectKey -add -k -f 13 left_end_arm_jnt_IK_translateX ;')
	cmds.setInfinity(poi='linear')
	
	###snappable 
	cmds.spaceLocator(n=newName+'_elbow_loc',p=(midArm[0], midArm[1], midArm[2]-2))
			
	cmds.select(newName+'_elbow_loc')
	cmds.makeIdentity(apply=True,t=1,r=1,s=0,n=0,pn=1)
	cmds.xform(newName+'_elbow_loc', cp=1)
	cmds.poleVectorConstraint(newName+'_elbow_loc',newName+'Arm_hdl' )
	###
	mel.eval('curve -d 1 -p -3 0 0 -p 3 0 0 -p 0 0 5 -p -3 0 0 -k 0 -k 1 -k 2 -k 3 ;')
	cmds.rename('curve1', newName+'elbow_Ctrl')	
	cmds.setAttr(newName+'elbow_Ctrl.translate',midArm[0], midArm[1], midArm[2]-2)
	
	if newName=='right':
		cmds.setAttr(newName+'elbow_Ctrl'+".overrideEnabled", 1)
		cmds.setAttr(newName+'elbow_Ctrl'+".overrideColor", 6)	
	if newName=='left':
		cmds.setAttr(newName+'elbow_Ctrl'+".overrideEnabled", 1)
		cmds.setAttr(newName+'elbow_Ctrl'+".overrideColor", 4)	
		
	cmds.xform(newName+'elbow_Ctrl',s=(0.2,0.2,0.2))
	cmds.makeIdentity(apply=True,t=1,r=1,s=0,n=0,pn=1)
	cmds.xform(newName+'elbow_Ctrl', cp=1)
	cmds.parent(newName+'_elbow_loc',newName+'elbow_Ctrl')	
	
	##snappable elbow
	cmds.distanceDimension(sp=(0,2,0),ep=(0,1,0))
	cmds.rename('locator1',newName+'_shoulderToElbow_start')
	cmds.rename('locator2',newName+'_shoulderToElbow_end')
	cmds.setAttr(newName+'_shoulderToElbow_start.translate',stArm[0],stArm[1],stArm[2])
	cmds.setAttr(newName+'_shoulderToElbow_end.translate',midArm[0],midArm[1],midArm[2]-2)
	cmds.rename('distanceDimension1',newName+'_upperArm_length')
	
	cmds.distanceDimension(sp=(0,2,0),ep=(0,1,0))
	cmds.rename('locator1',newName+'_elbowToWrist_start')
	cmds.rename('locator2',newName+'_elbowToWrist_end')
	cmds.setAttr(newName+'_elbowToWrist_start.translate',midArm[0],midArm[1],midArm[2]-2)
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
	pos3=[cmds.getAttr('right_start_arm.ty'),cmds.getAttr('right_start_arm.tz')]
	if newName=='right':
		a=-6
	if newName=='left':
		a=6
	cmds.joint(p=(a,pos3[0]-1,pos3[1]),rad=0.1,n=newName+'_sh_jnt_Start')
	cmds.joint(p=(stArm[0], stArm[1],stArm[2]),rad=0.1,n=newName+'_sh_jnt_End')
	cmds.joint(newName+'_sh_jnt_Start',e=True,oj='xyz',sao='yup',ch=True,zso=True)
	cmds.ikHandle(n=newName+'_IK_sh_handle',sj=newName+'_sh_jnt_Start',ee=newName+'_sh_jnt_End',sol='ikSCsolver')

	
	cmds.spaceLocator(n=newName+'_sh_loc')	
	cmds.setAttr(newName+'_sh_loc.translate',stArm[0], stArm[1], stArm[2])
	cmds.makeIdentity(newName+'_sh_loc',apply=True,t=1,r=1,s=0,n=0,pn=1)
	cmds.xform(newName+'_sh_loc', cp=1)
	cmds.parent(newName+'_IK_sh_handle',newName+'_sh_loc')
	
	cmds.distanceDimension(sp=(0,2,0),ep=(0,1,0))
	cmds.rename('locator1',newName+'_sh_start')
	cmds.rename('locator2',newName+'_sh_end')
	cmds.setAttr(newName+'_sh_start.translate',a,pos3[0]-1,pos3[1])
	cmds.setAttr(newName+'_sh_end.translate',stArm[0],stArm[1],stArm[2])	
	cmds.rename('distanceDimension1',newName+'_sh_length')
	cmds.parent(newName+'_sh_end',newName+'_sh_loc')
	
	###
	###expression 
	naturalLength=cmds.getAttr(newName+'_sh_jnt_End.translateX')
	cmds.setDrivenKeyframe(newName+'_sh_jnt_End', cd=newName+"_sh_lengthShape.distance",dv=naturalLength, at='translateX', v=naturalLength)
	cmds.setDrivenKeyframe(newName+'_sh_jnt_End', cd=newName+"_sh_lengthShape.distance",dv=naturalLength*2, at='translateX', v=naturalLength*2)
	
	cmds.keyTangent(newName+'_sh_jnt_End',e=True,itt='spline',ott='spline', animation='objects')
	if newName=='left':
		mel.eval('selectKey -add -k -f 2.416995 left_sh_jnt_End_translateX ;')
	if newName=='right':
		mel.eval('selectKey -add -k -f 2.416995 right_sh_jnt_End_translateX ;')
	cmds.setInfinity(poi='linear')
	
	###
	mel.eval('circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 1 -d 3 -ut 0 -tol 0.01 -s 8 -ch 1;')
	cmds.rename('nurbsCircle1', newName+'_shoulder_ctrl')	
	cmds.setAttr(newName+'_shoulder_ctrl.translate', stArm[0],stArm[1]+2,stArm[2])
	cmds.setAttr(newName+'_shoulder_ctrl.scale', 0.5,0.5,0.5)
	if newName=='right':
		cmds.setAttr(newName+'_shoulder_ctrl.rotate', 0,0,20)
	if newName=='left':
		cmds.setAttr(newName+'_shoulder_ctrl.rotate', 0,0,-20)	
	cmds.makeIdentity(newName+'_shoulder_ctrl',apply=True,t=1,r=1,s=0,n=0,pn=1)
	cmds.xform(newName+'_shoulder_ctrl', cp=1)
	#mel.eval('move -r 0 -20 0 right_shoulder_ctrl.scalePivot right_shoulder_ctrl.rotatePivot ;')
	cmds.parent(newName+'_sh_loc',newName+'_shoulder_ctrl') 
	
	if newName=='right':
		cmds.setAttr(newName+'_shoulder_ctrl'+".overrideEnabled", 1)
		cmds.setAttr(newName+'_shoulder_ctrl'+".overrideColor", 6)	
	
	if newName=='left':
		cmds.setAttr(newName+'_shoulder_ctrl'+".overrideEnabled", 1)
		cmds.setAttr(newName+'_shoulder_ctrl'+".overrideColor", 4)	
	
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
	#mel.eval('move -rpr 0 223 7 right_shoulder_grp.scalePivot right_shoulder_grp.rotatePivot;')

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
	if newName=='right':
		mel.eval('move -rpr -2.7 6 -2.2 rightArmBase_IkConst_Grp.scalePivot rightArmBase_IkConst_Grp.rotatePivot ;') 
	if newName=='left':
		mel.eval('move -rpr 2.7 6 -2.2 leftArmBase_IkConst_Grp.scalePivot leftArmBase_IkConst_Grp.rotatePivot ;')
	
	cmds.spaceLocator(n=newName+'_shoulderSpace_locator',p=(stArm[0], stArm[1], stArm[2]))
	cmds.makeIdentity(newName+'_shoulderSpace_locator',apply=True,t=1,r=1,s=0,n=0,pn=1)
	cmds.xform(newName+'_shoulderSpace_locator',cp=True)
	
	cmds.parent(newName+'_shoulderSpace_locator',newName+'_sh_jnt_End')
	cmds.pointConstraint(newName+'_shoulderSpace_locator', newName+'ArmBase_IkConst_Grp' ,mo=True, weight=1)
	
	cmds.group(newName+'_start_arm_jnt', n=newName+'Arm_resultConst_GRP')
	if newName=='right':
		mel.eval('move -rpr -2.7 6 -2.2 rightArm_resultConst_GRP.scalePivot rightArm_resultConst_GRP.rotatePivot ;') 
	if newName=='left':
		mel.eval('move -rpr 2.7 6 -2.2 leftArm_resultConst_GRP.scalePivot leftArm_resultConst_GRP.rotatePivot ;') 
	
	
	cmds.pointConstraint(newName+'_shoulderSpace_locator', newName+'Arm_resultConst_GRP' ,mo=True, weight=1)
	##point constrain the new grps to the locators
	
	cmds.setAttr(newName+"_Arm_settingsCTRL.FK_IK_blend",0)
	cmds.setAttr(newName+"elbow_Ctrl.Elbow_Snap", 0)
	#cmds.setAttr(newName+"elbow_Ctrl.right_elbow_blend",0)
	#cmds.setAttr(newName+"elbow_Ctrl.foreArm_Fk_visibility",0)

	###
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1,n=newName+'_gimbalOne')
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1,n=newName+'_gimbalTwo')
	cmds.setAttr(newName+'_gimbalTwo.scale',0.4,0.4,0.4)
	cmds.xform(newName+'_gimbalTwo', t=(0,0,-1))
	cmds.makeIdentity(newName+'_gimbalOne',newName+'_gimbalTwo',apply=True,t=1,r=1,s=0,n=0,pn=1)
	cmds.parent(newName+'_gimbalTwo', newName+'_gimbalOne',r=True, s=True)
	cmds.rename(newName+'_gimbalOne', newName+'Arm_gimbal_Corr_Ctrl')
	cmds.setAttr(newName+'Arm_gimbal_Corr_Ctrl.translate',stArm[0],stArm[1], stArm[2])
	cmds.setAttr(newName+'Arm_gimbal_Corr_Ctrl.scale',1,1,1)
	cmds.setAttr(newName+'Arm_gimbal_Corr_Ctrl.rotate',90,90,0)
	cmds.makeIdentity(newName+'Arm_gimbal_Corr_Ctrl',apply=True,t=1,r=1,s=0,n=0,pn=1)
	
	cmds.parent(newName+'Arm_gimbal_Corr_Ctrl', newName+'_Arm_GRP')
	cmds.parent(newName+'_start_arm_jnt_FK',newName+'Arm_gimbal_Corr_Ctrl')
	cmds.select(newName+'_start_arm_jnt')
	mel.eval('doGroup 0 0 1;')
	cmds.rename('group1',newName+'Arm_resultGimbal_GRP')
	
	if newName=='right':
		mel.eval('move -rpr -2.7 6 -2.2  rightArm_resultGimbal_GRP.scalePivot rightArm_resultGimbal_GRP.rotatePivot ;')
	if newName=='left':
		mel.eval('move -rpr 2.7 6 -2.2  leftArm_resultGimbal_GRP.scalePivot leftArm_resultGimbal_GRP.rotatePivot ;')
	
	cmds.shadingNode('blendColors',au=True ,n=newName+'Arm_gimbalCorrToggle')
	cmds.connectAttr(newName+'Arm_gimbal_Corr_Ctrl.rotate', newName+'Arm_gimbalCorrToggle.color2',f=True)
	cmds.setAttr(newName+"Arm_gimbalCorrToggle.color1R", 0)
	cmds.connectAttr(newName+'Arm_gimbalCorrToggle.output', newName+'Arm_resultGimbal_GRP.rotate',f=True )
	cmds.connectAttr(newName+'_Arm_settingsCTRL.FK_IK_blend', newName+'Arm_gimbalCorrToggle.blender', f=True)
	cmds.connectAttr(newName+'_Arm_settingsCTRL.FK_visibility', newName+'Arm_gimbal_Corr_Ctrl.visibility', f=True)
	cmds.group(newName+'Arm_gimbal_Corr_Ctrl', n=newName+'Arm_FKConst_GRP')
	
	if newName=='right':
		mel.eval('move -rpr -2.7 6 -2.2 rightArm_FKConst_GRP.scalePivot rightArm_FKConst_GRP.rotatePivot ;')
	if newName=='left':
		mel.eval('move -rpr -2.7 6 -2.2 leftArm_FKConst_GRP.scalePivot leftArm_FKConst_GRP.rotatePivot ;')
	
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
	if newName=='right':
		mel.eval('addAttr -ln "FK_rotationSpace"  -at "enum" -en "shoulder:upperBody:root:"  |rightA_settings_GRP|right_Arm_settingsCTRL;')
		mel.eval('setAttr -e-keyable true |rightA_settings_GRP|right_Arm_settingsCTRL.FK_rotationSpace;')

	if newName=='left':
		mel.eval('addAttr -ln "FK_rotationSpace"  -at "enum" -en "shoulder:upperBody:root:"  |leftA_settings_GRP|left_Arm_settingsCTRL;')
		mel.eval('setAttr -e-keyable true |leftA_settings_GRP|left_Arm_settingsCTRL.FK_rotationSpace;')

		
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
	cmds.setDrivenKeyframe(newName+'Arm_FKConst_GRP_orientConstraint1.'+newName+'_shoulderSpace_locatorW2', cd=newName+'_Arm_settingsCTRL.FK_rotationSpace' )
	cmds.setDrivenKeyframe(newName+'Arm_resultConst_GRP_orientConstraint1.'+newName+'_shoulderSpace_locatorW2', cd=newName+'_Arm_settingsCTRL.FK_rotationSpace' )
	cmds.setDrivenKeyframe(newName+'Arm_FKConst_GRP_orientConstraint1.'+newName+'_ArmBodySpace_locatorW0', cd=newName+'_Arm_settingsCTRL.FK_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Arm_resultConst_GRP_orientConstraint1.'+newName+'_ArmBodySpace_locatorW0', cd=newName+'_Arm_settingsCTRL.FK_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Arm_FKConst_GRP_orientConstraint1.'+newName+'_ArmRootSpace_locatorW1',cd=newName+'_Arm_settingsCTRL.FK_rotationSpace' )
	cmds.setDrivenKeyframe(newName+'Arm_resultConst_GRP_orientConstraint1.'+newName+'_ArmRootSpace_locatorW1', cd=newName+'_Arm_settingsCTRL.FK_rotationSpace')
	
	cmds.setAttr(newName+"_Arm_settingsCTRL.FK_rotationSpace",1)
	cmds.setAttr(listOrient[0]+'.'+newName+'_shoulderSpace_locatorW2',0)
	cmds.setAttr(listOrient[0]+'.'+newName+'_ArmBodySpace_locatorW0',1)
	cmds.setAttr(listOrient[0]+'.'+newName+'_ArmRootSpace_locatorW1',0)
	cmds.setAttr(listOrient[1]+'.'+newName+'_shoulderSpace_locatorW2',0)
	cmds.setAttr(listOrient[1]+'.'+newName+'_ArmBodySpace_locatorW0',1)
	cmds.setAttr(listOrient[1]+'.'+newName+'_ArmRootSpace_locatorW1',0)
	
	cmds.setDrivenKeyframe(newName+'Arm_FKConst_GRP_orientConstraint1.'+newName+'_shoulderSpace_locatorW2', cd=newName+'_Arm_settingsCTRL.FK_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Arm_resultConst_GRP_orientConstraint1.'+newName+'_shoulderSpace_locatorW2', cd=newName+'_Arm_settingsCTRL.FK_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Arm_FKConst_GRP_orientConstraint1.'+newName+'_ArmBodySpace_locatorW0', cd=newName+'_Arm_settingsCTRL.FK_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Arm_resultConst_GRP_orientConstraint1.'+newName+'_ArmBodySpace_locatorW0',cd=newName+'_Arm_settingsCTRL.FK_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Arm_FKConst_GRP_orientConstraint1.'+newName+'_ArmRootSpace_locatorW1', cd=newName+'_Arm_settingsCTRL.FK_rotationSpace' )
	cmds.setDrivenKeyframe(newName+'Arm_resultConst_GRP_orientConstraint1.'+newName+'_ArmRootSpace_locatorW1', cd=newName+'_Arm_settingsCTRL.FK_rotationSpace' )

	cmds.setAttr(newName+"_Arm_settingsCTRL.FK_rotationSpace",2)
	cmds.setAttr(listOrient[0]+'.'+newName+'_shoulderSpace_locatorW2',0)
	cmds.setAttr(listOrient[0]+'.'+newName+'_ArmBodySpace_locatorW0',0)
	cmds.setAttr(listOrient[0]+'.'+newName+'_ArmRootSpace_locatorW1',0)
	cmds.setAttr(listOrient[1]+'.'+newName+'_shoulderSpace_locatorW2',0)
	cmds.setAttr(listOrient[1]+'.'+newName+'_ArmBodySpace_locatorW0',0)
	cmds.setAttr(listOrient[1]+'.'+newName+'_ArmRootSpace_locatorW1',1)

	#change to cmds
	cmds.setDrivenKeyframe(newName+'Arm_FKConst_GRP_orientConstraint1.'+newName+'_shoulderSpace_locatorW2',cd=newName+'_Arm_settingsCTRL.FK_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Arm_resultConst_GRP_orientConstraint1.'+newName+'_shoulderSpace_locatorW2',cd=newName+'_Arm_settingsCTRL.FK_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Arm_FKConst_GRP_orientConstraint1.'+newName+'_ArmBodySpace_locatorW0', cd=newName+'_Arm_settingsCTRL.FK_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Arm_resultConst_GRP_orientConstraint1.'+newName+'_ArmBodySpace_locatorW0',cd=newName+'_Arm_settingsCTRL.FK_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Arm_FKConst_GRP_orientConstraint1.'+newName+'_ArmRootSpace_locatorW1', cd=newName+'_Arm_settingsCTRL.FK_rotationSpace')
	cmds.setDrivenKeyframe(newName+'Arm_resultConst_GRP_orientConstraint1.'+newName+'_ArmRootSpace_locatorW1', cd=newName+'_Arm_settingsCTRL.FK_rotationSpace' )
	
	
	###check connections
	cmds.setAttr(newName+"upperArm_Curve.inheritsTransform", 0)
	cmds.setAttr(newName+"lowerArm_Curve.inheritsTransform", 0)
	###
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
	cmds.connectAttr( newName+'_IK_armLengthShape.distance',newName+'_globalScale_rightArm_normalize_DIV.input1X', f=True)
	cmds.connectAttr( newName+'_sh_lengthShape.distance', newName+'_globalScale_rightShoulder_normalize_DIV.input1X',f=True)

	cmds.setAttr(newName+"_globalScale_rightArm_normalize_DIV.operation",2)
	cmds.setAttr(newName+"_globalScale_rightShoulder_normalize_DIV.operation",2)

	cmds.connectAttr( newName+'_globalScale_rightArm_normalize_DIV.outputX', newName+'_end_arm_jnt_IK_translateX.input',f=True)
	cmds.connectAttr( newName+'_globalScale_rightArm_normalize_DIV.outputX', newName+'_mid_arm_jnt_IK_translateX.input',f=True)
	cmds.connectAttr( newName+'_globalScale_rightShoulder_normalize_DIV.outputX', newName+'_sh_jnt_End_translateX.input', f=True)

	#do the same for the snap elbow jnts and segmented joints 
	
	cmds.shadingNode('multiplyDivide',au=True ,n=newName+'_globalScale_rightElbow_to_hand_normalize_DIV')
	cmds.setAttr(newName+"_globalScale_rightElbow_to_hand_normalize_DIV.operation", 2)
	cmds.connectAttr(newName+'_lowerArm_length1.distance', newName+'_globalScale_rightElbow_to_hand_normalize_DIV.input1X', f=True)
	cmds.connectAttr('pirate_Root_Transform.scaleY', newName+'_globalScale_rightElbow_to_hand_normalize_DIV.input2X',f=True)
	cmds.connectAttr(newName+'_globalScale_rightElbow_to_hand_normalize_DIV.outputX', newName+'LowerArm_stretch_Choice.color1R', f=True)

	cmds.shadingNode('multiplyDivide',au=True ,n=newName+'_globalScale_rightUpperArm_to_elbow_normalize_DIV')
	cmds.setAttr(newName+"_globalScale_rightUpperArm_to_elbow_normalize_DIV.operation", 2)
	cmds.connectAttr(newName+'_upperArm_length1.distance', newName+'_globalScale_rightUpperArm_to_elbow_normalize_DIV.input1X', f=True)
	cmds.connectAttr('pirate_Root_Transform.scaleY', newName+'_globalScale_rightUpperArm_to_elbow_normalize_DIV.input2X',f=True)
	cmds.connectAttr(newName+'_globalScale_rightUpperArm_to_elbow_normalize_DIV.outputX', newName+'UpperArm_stretch_Choice.color1R', f=True)
	
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
	
	cmds.delete(newName+'_end_arm_jnt1')
	if newName=='right':
		cmds.connectAttr(newName+'_globalScale_rightLowerArm_normalize_DIV.outputX', newName+'_mid_arm_jnt1.scaleX', f=True)
		cmds.connectAttr(newName+'_globalScale_rightLowerArm_normalize_DIV.outputX', 'r_f_midTwist.scaleX', f=True)
		cmds.connectAttr(newName+'_globalScale_rightLowerArm_normalize_DIV.outputX', 'r_e_midTwist.scaleX', f=True)
		cmds.connectAttr(newName+'_globalScale_rightLowerArm_normalize_DIV.outputX', 'r_g_midTwist.scaleX', f=True)
		cmds.connectAttr(newName+'_globalScale_rightLowerArm_normalize_DIV.outputX', 'r_h_midTwist.scaleX', f=True)
		
		cmds.connectAttr(newName+'_globalScale_rightForeArm_normalize_DIV.outputX', newName+'_start_arm_jnt1.scaleX', f=True)
		cmds.connectAttr(newName+'_globalScale_rightForeArm_normalize_DIV.outputX', 'r_b_midTwist.scaleX', f=True)
		cmds.connectAttr(newName+'_globalScale_rightForeArm_normalize_DIV.outputX', 'r_a_midTwist.scaleX', f=True)
		cmds.connectAttr(newName+'_globalScale_rightForeArm_normalize_DIV.outputX', 'r_c_midTwist.scaleX', f=True)
		cmds.connectAttr(newName+'_globalScale_rightForeArm_normalize_DIV.outputX', 'r_d_midTwist.scaleX', f=True)
	if newName=='left':
		cmds.connectAttr(newName+'_globalScale_rightLowerArm_normalize_DIV.outputX', newName+'_mid_arm_jnt1.scaleX', f=True)
		cmds.connectAttr(newName+'_globalScale_rightLowerArm_normalize_DIV.outputX', 'l_f_midTwist.scaleX', f=True)
		cmds.connectAttr(newName+'_globalScale_rightLowerArm_normalize_DIV.outputX', 'l_e_midTwist.scaleX', f=True)
		cmds.connectAttr(newName+'_globalScale_rightLowerArm_normalize_DIV.outputX', 'l_g_midTwist.scaleX', f=True)
		cmds.connectAttr(newName+'_globalScale_rightLowerArm_normalize_DIV.outputX', 'l_h_midTwist.scaleX', f=True)
		
		cmds.connectAttr(newName+'_globalScale_rightForeArm_normalize_DIV.outputX', newName+'_start_arm_jnt1.scaleX', f=True)
		cmds.connectAttr(newName+'_globalScale_rightForeArm_normalize_DIV.outputX', 'l_b_midTwist.scaleX', f=True)
		cmds.connectAttr(newName+'_globalScale_rightForeArm_normalize_DIV.outputX', 'l_a_midTwist.scaleX', f=True)
		cmds.connectAttr(newName+'_globalScale_rightForeArm_normalize_DIV.outputX', 'l_c_midTwist.scaleX', f=True)
		cmds.connectAttr(newName+'_globalScale_rightForeArm_normalize_DIV.outputX', 'l_d_midTwist.scaleX', f=True)
	
	cmds.parent(newName+'Arm_ctrl', newName+'_Arm_GRP')
	cmds.parent(newName+'_upperArm_length1',newName+'_lowerArm_length1',newName+'_Arm_GRP')
	
	attrRot=['.tx','.ty','.tz','.sx','.sy','.sz','.v']
	attrS=['.sx','.sy','.sz','.v']
	for i in attrRot:
		for k in armFK:
			cmds.setAttr(k+i, l=True)
	for i in attrS:
		cmds.setAttr(newName+'Arm_ctrl'+i, l=True)
		
	cmds.select(clear=True)
	fingers(newName,endArm)

	###
def fingers(newName,endAPos):
	'''
	finger creation
	'''
	
	cmds.joint(p=(endAPos[0],endAPos[1],endAPos[2]),n=newName+'_handBase_jnt')
	cmds.setAttr(newName+"_handBase_jnt.radius", 0.1)
	cmds.select(clear=True)
	
	if(newName=='right'):
		listFingers=[rThumbJnts[0],rIndexJnts[0],rMiddleJnts[0], rRingJnts[0], rPinkyJnts[0]]
	if(newName=='left'):
		listFingers=[lThumbJnts[0],lIndexJnts[0],lMiddleJnts[0], lRingJnts[0], lPinkyJnts[0]]
	
	for i in range(0,len(listFingers)):
		cmds.parent(listFingers[i], newName+'_handBase_jnt')
	cmds.joint(newName+'_handBase_jnt',e=True,oj='xyz', sao='ydown',ch=True, zso=True)
	cmds.select(clear=True)
	
	cmds.duplicate(listFingers[0],n=newName+'_thumb_Orbit_jnt')
	cmds.select(newName+'_thumb_Orbit_jnt')
	cmds.pickWalk(d='down')
	cmds.delete()
	
	cmds.parent(newName+'_thumb_Orbit_jnt',listFingers[0]) 
	cmds.parent(newName+'_thumb_Orbit_jnt',w=True)
	cmds.parent(newName+'_thumb_start_jnt',newName+'_thumb_Orbit_jnt')
	cmds.parent(newName+'_thumb_Orbit_jnt',newName+'_handBase_jnt')
	
	if(newName=='right'):
		#cmds.setAttr('right_thumb_Orbit_jnt.rotateX',-50)
		#rotate the other joints so that it matches the thumb, then freeze rotations
		cmds.select('right_thumb_Orbit_jnt')
		mel.eval('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;')
	if(newName=='left'):
		#cmds.setAttr('left_thumb_Orbit_jnt.rotateX',50)
		#rotate the other joints so that it matches the thumb, then freeze rotations
		cmds.select('left_thumb_Orbit_jnt')
		mel.eval('makeIdentity -apply true -t 1 -r 1 -s 1 -n 0 -pn 1;')
	
	if newName=='right':
		for item,item2,item3,item4,item5 in zip(rThumbJnts, rIndexJnts,rMiddleJnts,rRingJnts,rPinkyJnts):
			cmds.setAttr(item+".rotateOrder", 5)
			cmds.setAttr(item1+".rotateOrder", 5)
			cmds.setAttr(item2+".rotateOrder", 5)
			cmds.setAttr(item3+".rotateOrder", 5)
			cmds.setAttr(item4+".rotateOrder", 5)
			cmds.setAttr(item5+".rotateOrder", 5)
	if newName=='left':
		for item,item2,item3,item4,item5 in zip(lThumbJnts, lIndexJnts,lMiddleJnts,lRingJnts,lPinkyJnts):
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
	###
	for i in range(0,len(replaceNames)):
		cmds.rename(newName+str(replaceNames[i])+'start_jnt_orient|'+newName+str(replaceNames[i])+'mid_jnt',newName+str(replaceNames[i])+'mid_jnt_orient') 
		cmds.rename(newName+str(replaceNames[i])+'start_jnt_orient|'+newName+str(replaceNames[i])+'mid_jnt_orient|'+newName+str(replaceNames[i])+'mid2_jnt',newName+str(replaceNames[i])+'mid2_jnt_orient') 
		cmds.delete(newName+str(replaceNames[i])+'start_jnt_orient|'+newName+str(replaceNames[i])+'mid_jnt_orient|'+newName+str(replaceNames[i])+'mid2_jnt_orient|'+newName+str(replaceNames[i])+'end_jnt')
		#each jnt is under the orient jnt
		cmds.parent(newName+str(replaceNames[i])+'start_jnt',newName+str(replaceNames[i])+'start_jnt_orient')
		cmds.parent(newName+str(replaceNames[i])+'mid_jnt',newName+str(replaceNames[i])+'mid_jnt_orient')
		cmds.parent(newName+str(replaceNames[i])+'mid2_jnt',newName+str(replaceNames[i])+'mid2_jnt_orient')
		
		cmds.rename(newName+str(replaceNames[i])+'end_jnt',newName+str(replaceNames[i])+'end_jnt_orient')
		for k in range(0, len(replacePart)-1):
			cmds.parent(newName+replaceNames[i]+replacePart[k]+'_jnt_orient',newName+replaceNames[i]+replacePart[k+1]+'_jnt')
		###fixed
	
	jointResult=cmds.duplicate(newName+'_handBase_jnt')
	jointAsciiResult=map(lambda x: x.encode('ascii'), jointResult)
	
	cmds.select(clear=True)

###optimize
	if newName=='right':
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
	
	if newName=='left':
		mel.eval('select -add left_handBase_jnt1|left_thumb_Orbit_jnt|left_thumb_start_jnt_orient|left_thumb_start_jnt ;')
		mel.eval('select -add left_handBase_jnt1|left_thumb_Orbit_jnt|left_thumb_start_jnt_orient|left_thumb_start_jnt|left_thumb_mid_jnt_orient|left_thumb_mid_jnt ;')
		mel.eval('select -add left_handBase_jnt1|left_thumb_Orbit_jnt|left_thumb_start_jnt_orient|left_thumb_start_jnt|left_thumb_mid_jnt_orient|left_thumb_mid_jnt|left_thumb_mid2_jnt_orient|left_thumb_mid2_jnt ;')
		mel.eval('select -add left_handBase_jnt1|left_index_start_jnt_orient|left_index_start_jnt ;')
		mel.eval('select -add left_handBase_jnt1|left_index_start_jnt_orient|left_index_start_jnt|left_index_mid_jnt_orient|left_index_mid_jnt ;')
		mel.eval('select -add left_handBase_jnt1|left_index_start_jnt_orient|left_index_start_jnt|left_index_mid_jnt_orient|left_index_mid_jnt|left_index_mid2_jnt_orient|left_index_mid2_jnt ;')
		mel.eval('select -add left_handBase_jnt1|left_middle_start_jnt_orient|left_middle_start_jnt ;')
		mel.eval('select -add left_handBase_jnt1|left_middle_start_jnt_orient|left_middle_start_jnt|left_middle_mid_jnt_orient|left_middle_mid_jnt ;')
		mel.eval('select -add left_handBase_jnt1|left_middle_start_jnt_orient|left_middle_start_jnt|left_middle_mid_jnt_orient|left_middle_mid_jnt|left_middle_mid2_jnt_orient|left_middle_mid2_jnt ;')
		mel.eval('select -add left_handBase_jnt1|left_ring_start_jnt_orient|left_ring_start_jnt ;')
		mel.eval('select -add left_handBase_jnt1|left_ring_start_jnt_orient|left_ring_start_jnt|left_ring_mid_jnt_orient|left_ring_mid_jnt ;')
		mel.eval('select -add left_handBase_jnt1|left_ring_start_jnt_orient|left_ring_start_jnt|left_ring_mid_jnt_orient|left_ring_mid_jnt|left_ring_mid2_jnt_orient|left_ring_mid2_jnt ;')
		mel.eval('select -add left_handBase_jnt1|left_pinky_start_jnt_orient|left_pinky_start_jnt ;')
		mel.eval('select -add left_handBase_jnt1|left_pinky_start_jnt_orient|left_pinky_start_jnt|left_pinky_mid_jnt_orient|left_pinky_mid_jnt ;')
		mel.eval('select -add left_handBase_jnt1|left_pinky_start_jnt_orient|left_pinky_start_jnt|left_pinky_mid_jnt_orient|left_pinky_mid_jnt|left_pinky_mid2_jnt_orient|left_pinky_mid2_jnt ;')

		mel.eval('searchReplaceNames "_jnt" "_FK_CTRL" "selected";')

		cmds.rename('left_handBase_jnt1', 'left_handBase_CTRL_JNT' )
		cmds.rename('left_handBase_CTRL_JNT|left_thumb_Orbit_jnt', 'left_thumb_Orbit_FK_CTRL' )
	
	namesWithoutThumb=replaceNames[1:]
	rot_tr=['rotate', 'translate']
	for i in range(0,len(namesWithoutThumb)):
		cmds.connectAttr(newName+'_handBase_CTRL_JNT|'+newName+str(namesWithoutThumb[i])+'start_jnt_orient.'+rot_tr[0], newName+'_handBase_jnt|'+newName+str(namesWithoutThumb[i])+'start_jnt_orient.'+rot_tr[0],f=True)
		cmds.connectAttr(newName+str(namesWithoutThumb[i])+'start_FK_CTRL.'+rot_tr[0], newName+str(namesWithoutThumb[i])+'start_jnt.'+rot_tr[0], f=True)
		for k in rot_tr:	
			cmds.connectAttr(newName+str(namesWithoutThumb[i])+'start_FK_CTRL|'+newName+str(namesWithoutThumb[i])+'mid_jnt_orient.'+k, newName+str(namesWithoutThumb[i])+'start_jnt|'+newName+str(namesWithoutThumb[i])+'mid_jnt_orient.'+k,f=True)
			cmds.connectAttr(newName+str(namesWithoutThumb[i])+'mid_FK_CTRL.'+k, newName+str(namesWithoutThumb[i])+'mid_jnt.'+k,f=True)
			cmds.connectAttr(newName+str(namesWithoutThumb[i])+'mid_FK_CTRL|'+newName+str(namesWithoutThumb[i])+'mid2_jnt_orient.'+k, newName+str(namesWithoutThumb[i])+'mid_jnt|'+newName+str(namesWithoutThumb[i])+'mid2_jnt_orient.'+k,f=True)
			cmds.connectAttr(newName+str(namesWithoutThumb[i])+'mid2_FK_CTRL.'+k, newName+str(namesWithoutThumb[i])+'mid2_jnt.'+k,f=True)
			cmds.connectAttr(newName+str(namesWithoutThumb[i])+'mid2_FK_CTRL|'+newName+str(namesWithoutThumb[i])+'end_jnt_orient.'+k, newName+str(namesWithoutThumb[i])+'mid2_jnt|'+newName+str(namesWithoutThumb[i])+'end_jnt_orient.'+k, f=True)

	
	#thumb separately
	r_thumb=['right_thumb']
	l_thumb=['right_thumb']
	##?????????? be careful
	#cmds.connectAttr('r_thumb_Orbit_FK_CTRL.'+k[0], 'r_thumb_Orbit_jnt.'+k[0],f=True)
	#cmds.connectAttr('r_thumb_Orbit_FK_CTRL|r_thumb_start_jnt_orient.'+k[0], 'r_thumb_Orbit_jnt|r_thumb_start_jnt_orient.'+k[0],f=True)
		
	#for k in rot_tr:
	cmds.connectAttr(newName+'_thumb_start_FK_CTRL.rotate', newName+'_thumb_start_jnt.'+rot_tr[0], f=True)
	cmds.connectAttr(newName+'_thumb_start_FK_CTRL|'+newName+'_thumb_mid_jnt_orient.'+rot_tr[0], newName+'_thumb_start_jnt|'+newName+'_thumb_mid_jnt_orient.'+rot_tr[0], f=True)
	cmds.connectAttr(newName+'_thumb_mid_FK_CTRL.rotate', newName+'_thumb_mid_jnt.'+rot_tr[0], f=True)
	cmds.connectAttr(newName+'_thumb_mid_FK_CTRL|'+newName+'_thumb_mid2_jnt_orient.'+rot_tr[0], newName+'_thumb_mid_jnt|'+newName+'_thumb_mid2_jnt_orient.'+rot_tr[0], f=True)
	cmds.connectAttr(newName+'_thumb_mid2_FK_CTRL.rotate', newName+'_thumb_mid2_jnt.'+rot_tr[0], f=True)
	cmds.connectAttr(newName+'_thumb_mid2_FK_CTRL|'+newName+'_thumb_end_jnt_orient.'+rot_tr[0], newName+'_thumb_mid2_jnt|'+newName+'_thumb_end_jnt_orient.'+rot_tr[0] ,f=True)
	
	####only rotate cbecause translate is not needed for squash and stretch only
	
	indexFK=[newName+'_index_start_FK_CTRL',newName+'_index_mid_FK_CTRL',newName+'_index_mid2_FK_CTRL']
	thumbFK=[newName+'_thumb_start_FK_CTRL',newName+'_thumb_mid_FK_CTRL',newName+'_thumb_mid2_FK_CTRL']
	middleFK=[newName+'_middle_start_FK_CTRL',newName+'_middle_mid_FK_CTRL',newName+'_middle_mid2_FK_CTRL']
	ringFK=[newName+'_ring_start_FK_CTRL',newName+'_ring_mid_FK_CTRL',newName+'_ring_mid2_FK_CTRL']
	pinkyFK=[newName+'_pinky_start_FK_CTRL',newName+'_pinky_mid_FK_CTRL',newName+'_pinky_mid2_FK_CTRL']
	allFKs=[indexFK,thumbFK,middleFK,ringFK,pinkyFK]
	allFK=[]
	for i in range(0,5):
		allFK.append(allFKs[i])
	
	
	for item in allFK:
		for i in item:
			cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1, n=i+'ctrl')
			
			if newName=='right':
				cmds.setAttr(i+'ctrl.rotateX',90 )
				cmds.setAttr(i+'ctrl.rotateY',-90 )
				cmds.setAttr(i+".overrideEnabled", 1)
				cmds.setAttr(i+".overrideColor", 6)	
				
			if newName=='left':
				cmds.setAttr(i+'ctrl.rotateX',-90 )
				cmds.setAttr(i+'ctrl.rotateY',90 )
				cmds.setAttr(i+".overrideEnabled", 1)
				cmds.setAttr(i+".overrideColor", 4)
					
			cmds.xform(i+'ctrlShape.cv[0:7]', s=(1.5,1.5,1.5))
			cmds.makeIdentity(apply=True,t=1,r=1,s=1,n=0,pn=1)
			cmds.parent(i+'ctrlShape', i ,r=True,s=True)
			cmds.delete(i+'ctrl')
	r_ctrls=[]

	r_ctrls_types=['fist']
	for i in range(0,4):
		cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=0.5,d=3,ut=0,tol=0.01,s=8,ch=1, n=newName+'_'+str(i)+'ctrl')
		r_ctrls.append(newName+'_'+str(i)+'ctrl')
		cmds.setAttr(newName+'_'+str(i)+'ctrl.rotateZ',90)
		if newName=='right':
			cmds.setAttr(newName+'_'+str(i)+'ctrl.translate',-65,135,-5+(1*(i+2)))
			cmds.setAttr(newName+'_'+str(i)+'ctrl'+".overrideEnabled", 1)
			cmds.setAttr(newName+'_'+str(i)+'ctrl'+".overrideColor", 6)	
			
		if newName=='left':
			cmds.setAttr(newName+'_'+str(i)+'ctrl.translate',65,135,-5+(1*(i+2)))
			cmds.setAttr(newName+'_'+str(i)+'ctrl'+".overrideEnabled", 1)
			cmds.setAttr(newName+'_'+str(i)+'ctrl'+".overrideColor", 4)	
	
	for i in r_ctrls:
		for k in r_ctrls_types:	
			cmds.addAttr('|'+i,ln=k, at='double', min=-10, max=10 ,dv=0) 
			cmds.setAttr('|'+i+'.'+k,e=True,keyable=True)
	###all fingers ctrls
	
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=0.5,d=3,ut=0,tol=0.01,s=8,ch=1, n=newName+'_'+'FINGERS'+'ctrl')
	r_ctrls.append(newName+'_'+'FINGERS'+'ctrl')
	cmds.setAttr(newName+'_'+'FINGERS'+'ctrl.rotateZ',90)
	if newName=='right':
		cmds.setAttr(newName+'_'+'FINGERS'+'ctrl.translate',-65,135,-1)
		cmds.setAttr(newName+'_'+'FINGERS'+'ctrl'+".overrideEnabled", 1)
		cmds.setAttr(newName+'_'+'FINGERS'+'ctrl'+".overrideColor", 6)	
	
	if newName=='left':
		cmds.setAttr(newName+'_'+'FINGERS'+'ctrl.translate',65,135,-1)
		cmds.setAttr(newName+'_'+'FINGERS'+'ctrl'+".overrideEnabled", 1)
		cmds.setAttr(newName+'_'+'FINGERS'+'ctrl'+".overrideColor", 4)	
	
	cmds.setAttr(newName+'_'+'FINGERS'+'ctrl.scaleZ',5)
	
	
	palmMovement=[newName+'raisePalm',newName+'innerPalmRotate', newName+'outerPalmRotate',newName+'number_3', newName+'number_2', newName+'number_1']
	for i in palmMovement:
		cmds.addAttr(newName+'_FINGERSctrl', ln=i, at='double', min=0, max=10, dv=0)
		cmds.setAttr(newName+'_FINGERSctrl.'+i,e=True,keyable=True)
		
	###plantable fingers
	for i in rot_tr:
		cmds.connectAttr(newName+'_handBase_CTRL_JNT.'+i, newName+'_handBase_jnt.'+i,f=True)
	
	nameLocatorsPalm=[newName+'middlePalm_LOC', newName+'innerPalm_LOC', newName+'outerPalm_LOC']
	for i in range(0,3):
		cmds.spaceLocator(n=nameLocatorsPalm[i] ,p=(endAPos[0], endAPos[1], endAPos[2]+i*5))
		cmds.xform(nameLocatorsPalm[i], cp=1)
		cmds.setAttr(nameLocatorsPalm[i]+'.visibility', 0)
	
	if newName=='left':
		tx_i=10.7 #outer
		tx_o=10.8 #inner
	if newName=='right':
		tx_i=-10.7 #outer
		tx_o=-10.8 #inner
		
	cmds.setAttr(newName+'innerPalm_LOC'+'.tx', tx_i)
	cmds.setAttr(newName+'outerPalm_LOC'+'.tx', tx_o)
		
		
	if newName=='right':	
		cmds.setAttr(newName+'middlePalm_LOC.translateX',cmds.getAttr('right_middle_start.translateX'))
	if newName=='left':
		cmds.setAttr(newName+'middlePalm_LOC.translateX',-cmds.getAttr('right_middle_start.translateX'))
		
		
	cmds.setAttr(newName+'middlePalm_LOC.translateY',cmds.getAttr('right_middle_start.translateY'))
	cmds.setAttr(newName+'middlePalm_LOC.translateZ',cmds.getAttr('right_middle_start.translateZ'))
	cmds.setAttr(newName+"middlePalm_LOCShape.localPositionZ",0)
	cmds.setAttr(newName+"middlePalm_LOCShape.localPositionX",0)
	cmds.setAttr(newName+"middlePalm_LOCShape.localPositionY",0)
	cmds.xform(newName+'middlePalm_LOC', cp=True)
	
	if newName=='right':
		a=-1.25
		b=-0.1
		c=-4.45
		d=-10.4
	if newName=='left':
		a=1.25
		b=-0.1
		c=-4.45
		d=-10.4
	
	cmds.setAttr(newName+'outerPalm_LOC.translateX',a)
	cmds.setAttr(newName+'outerPalm_LOC.translateY',b)
	cmds.setAttr(newName+'outerPalm_LOC.translateZ',d)
	
	cmds.setAttr(newName+'innerPalm_LOC.translateX',a)
	cmds.setAttr(newName+'innerPalm_LOC.translateY',0)
	cmds.setAttr(newName+'innerPalm_LOC.translateZ',c)
	
	cmds.parent(newName+'middlePalm_LOC',newName+'outerPalm_LOC')
	cmds.parent(newName+'outerPalm_LOC',newName+'innerPalm_LOC')
	
	cmds.duplicate(newName+'_handBase_jnt', n=newName+'_handBase_CONST_JNT')
	for i in range(0,5):
		cmds.select(newName+'_handBase_CONST_JNT')
		cmds.pickWalk(d='down')
		cmds.delete()
	
	cmds.parent(newName+'_handBase_CONST_JNT', newName+'middlePalm_LOC')
	cmds.parentConstraint(newName+'_handBase_CONST_JNT',newName+'_handBase_CTRL_JNT',mo=True, w=1)
	
	for i in namesWithoutThumb:
		cmds.duplicate(newName+'_handBase_CTRL_JNT|'+newName+i+'start_jnt_orient', n=newName+i+'start_IK')
		cmds.parent(newName+i+'start_IK|'+newName+i+'start_FK_CTRL|'+newName+i+'mid_jnt_orient|'+newName+i+'mid_FK_CTRL|'+newName+i+'mid2_jnt_orient|'+newName+i+'mid2_FK_CTRL|'+newName+i+'end_jnt_orient',newName+i+'start_IK') 
		cmds.delete(newName+i+'start_IK|'+newName+i+'start_FK_CTRL')
		cmds.ikHandle(n=newName+'_'+i+'IK_hdl',sj=newName+i+'start_IK',ee=newName+i+'start_IK|'+newName+i+'end_jnt_orient',sol='ikSCsolver')
		cmds.group(newName+'_'+i+'IK_hdl', n=newName+'_'+i+'IK_hdl_GRP')
	
	##thumb separately
	cmds.duplicate(newName+'_thumb_Orbit_FK_CTRL', n=newName+'_thumb_Orbit_start_IK')
	cmds.parent(newName+'_thumb_Orbit_start_IK|'+newName+'_thumb_start_jnt_orient|'+newName+'_thumb_start_FK_CTRL|'+newName+'_thumb_mid_jnt_orient|'+newName+'_thumb_mid_FK_CTRL|'+newName+'_thumb_mid2_jnt_orient|'+newName+'_thumb_mid2_FK_CTRL|'+newName+'_thumb_end_jnt_orient', newName+'_thumb_Orbit_start_IK') 
	cmds.delete(newName+'_thumb_Orbit_start_IK|'+newName+'_thumb_start_jnt_orient')
	cmds.ikHandle(n=newName+'_thumb_IK_hdl',sj=newName+'_thumb_Orbit_start_IK',ee=newName+'_thumb_Orbit_start_IK|'+newName+'_thumb_end_jnt_orient',sol='ikSCsolver')
	cmds.group(newName+'_thumb_IK_hdl', n=newName+'_thumb_IK_hdl_GRP')
	
	for i in namesWithoutThumb:	
		cmds.parent(newName+'_handBase_CTRL_JNT|'+newName+i+'start_jnt_orient',newName+i+'start_IK')
	#thumb separately
	cmds.parent(newName+'_thumb_Orbit_FK_CTRL',newName+'_thumb_Orbit_start_IK')
	
	cmds.xform(newName+'middlePalm_LOC', cp=1)	
	cmds.move(-8.104511, 0, 0, newName+'middlePalm_LOC.scalePivot', newName+'middlePalm_LOC.rotatePivot', r=True)
	
	#match the fingers
	for i in namesWithoutThumb:
		cmds.duplicate(newName+i+'start_IK', n=newName+i+'straight_jnt')
		for k in range(0,3):
			cmds.select(newName+i+'straight_jnt')
			cmds.pickWalk(d='down') 
			cmds.delete()
		
		cmds.parent(newName+i+'straight_jnt', newName+'_handBase_jnt')
		cmds.parent(newName+'_handBase_jnt|'+newName+i+'start_jnt_orient', newName+i+'straight_jnt')
		cmds.connectAttr(newName+i+'start_IK.rotate', newName+i+'straight_jnt.rotate', f=True)
	#thumb separately
	cmds.duplicate(newName+'_thumb_Orbit_start_IK', n=newName+'_thumb_Orbit_straight_jnt')
	for k in range(0,3):
		cmds.select(newName+'_thumb_Orbit_straight_jnt')
		cmds.pickWalk(d='down') 
		cmds.delete()
	cmds.parent(newName+'_thumb_Orbit_straight_jnt', newName+'_handBase_jnt')
	cmds.parent(newName+'_handBase_jnt|'+newName+'_thumb_Orbit_jnt', newName+'_thumb_Orbit_straight_jnt')
	cmds.connectAttr(newName+'_thumb_Orbit_start_IK.rotate', newName+'_thumb_Orbit_straight_jnt.rotate', f=True)
	
	##next bind the fingers first and then set the driven keys 
	cmds.group(newName+'_handBase_jnt', newName+'_handBase_CTRL_JNT', newName+'_0ctrl', 
				newName+'_1ctrl', newName+'_2ctrl', newName+'_3ctrl', newName+'_FINGERSctrl', 
				newName+'innerPalm_LOC', newName+'__index_IK_hdl_GRP', newName+'__middle_IK_hdl_GRP',
				newName+'__ring_IK_hdl_GRP', newName+'__pinky_IK_hdl_GRP', newName+'_thumb_IK_hdl_GRP',n=newName+'Arm_GRP' )
	cmds.parent(newName+'Arm_GRP','pirate_Root_Transform')
	
	cmds.group(newName+'_0ctrl', newName+'_1ctrl', newName+'_2ctrl', newName+'_3ctrl', newName+'_FINGERSctrl', newName+'innerPalm_LOC', n=newName+'fingers_ctrl_grp')
	####
	cmds.group(newName+'__index_IK_hdl_GRP', newName+'__middle_IK_hdl_GRP', newName+'__ring_IK_hdl_GRP', newName+'__pinky_IK_hdl_GRP', newName+'_thumb_IK_hdl_GRP',newName+'_handBase_jnt', n=newName+'doN0t_touch')
	cmds.group(newName+'innerPalm_LOC', n=newName+'Hand_Const_grp')
	if newName=='right':
		tx=-9.2
	if newName=='left':	
		tx=9.2
	cmds.move(tx, 6, 2.2, newName+'Hand_Const_grp.scalePivot', newName+'Hand_Const_grp.rotatePivot', rpr=True)
	cmds.parentConstraint(newName+'_end_arm_jnt', newName+'Hand_Const_grp',mo=True, w=1)
	cmds.group(newName+'__index_IK_hdl_GRP', newName+'__middle_IK_hdl_GRP', newName+'__ring_IK_hdl_GRP', newName+'__pinky_IK_hdl_GRP', newName+'_thumb_IK_hdl_GRP', n=newName+'_hand_IKs')
	cmds.parent(newName+'_hand_IKs', newName+'Hand_Const_grp')
	
	cmds.delete(newName+'_End_bindJnt_parentConstraint1')
	cmds.parentConstraint(newName+'_handBase_CONST_JNT', newName+'_End_bindJnt',mo=True, w=1)
	
	#works
	cmds.spaceLocator(n=newName+'fingers_ctrl_att',p=(0,0,0))
	cmds.setAttr(newName+'fingers_ctrl_att.translate',tx, 6, 2.2)
	
	cmds.parent(newName+'fingers_ctrl_att',newName+'_handBase_CTRL_JNT')
	cmds.parent(newName+'Hand_Const_grp',newName+'Arm_GRP')
	cmds.parentConstraint(newName+'fingers_ctrl_att',newName+'fingers_ctrl_grp',mo=True,w=1)
	cmds.setAttr(newName+"fingers_ctrl_att.visibility",0)
	
	cmds.setAttr(newName+"_hand_IKs.visibility",0)
	##connect inner and outter palms
	'''
	
	setting keys
	cmds.setDrivenKeyframe(newName+'outerPalm_LOC.rotateX', cd=newName+'_FINGERSctrl.innerPalmRotate')
	cmds.setDrivenKeyframe(newName+'innerPalm_LOC.rotateX', cd=newName+'_FINGERSctrl.outerPalmRotate')
	cmds.setDrivenKeyframe(newName+'middlePalm_LOC.rotateZ', cd=newName+'_FINGERSctrl.raisePalm')
	
	cmds.setAttr(newName+"_FINGERSctrl.outerPalmRotate",10)
	cmds.setAttr(newName+"_FINGERSctrl.raisePalm",10)
	cmds.setAttr(newName+"_FINGERSctrl.innerPalmRotate",10)
	cmds.setAttr(newName+"outerPalm_LOC.rotateX", 30)
	cmds.setAttr(newName+"innerPalm_LOC.rotateX", -30)
	cmds.setAttr(newName+"middlePalm_LOC.rotateZ", 15)
	
	cmds.setDrivenKeyframe(newName+'outerPalm_LOC.rotateX', cd=newName+'_FINGERSctrl.innerPalmRotate')
	cmds.setDrivenKeyframe(newName+'innerPalm_LOC.rotateX', cd=newName+'_FINGERSctrl.outerPalmRotate')
	cmds.setDrivenKeyframe(newName+'middlePalm_LOC.rotateZ', cd=newName+'_FINGERSctrl.raisePalm')
	
	cmds.setAttr(newName+"_FINGERSctrl.outerPalmRotate",0)
	cmds.setAttr(newName+"_FINGERSctrl.raisePalm",0)
	cmds.setAttr(newName+"_FINGERSctrl.innerPalmRotate",0)
	
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

	###setting number_3 #za thumb predi ne rabotishe ama sega trqbva
	cmds.connectAttr('|pirate_Root_Transform|rightArm_GRP|right_handBase_CTRL_JNT|right_thumb_Orbit_start_IK|right_thumb_Orbit_FK_CTRL|right_thumb_start_jnt_orient.translate', '|pirate_Root_Transform|rightArm_GRP|doN0t_touch|right_handBase_jnt|right_thumb_Orbit_straight_jnt|right_thumb_Orbit_jnt|right_thumb_start_jnt_orient.translate', f=True)
	cmds.connectAttr('|pirate_Root_Transform|rightArm_GRP|right_handBase_CTRL_JNT|right_thumb_Orbit_start_IK|right_thumb_Orbit_FK_CTRL|right_thumb_start_jnt_orient.rotate', '|pirate_Root_Transform|rightArm_GRP|doN0t_touch|right_handBase_jnt|right_thumb_Orbit_straight_jnt|right_thumb_Orbit_jnt|right_thumb_start_jnt_orient.rotate', f=True)
	'''
	

def setKeysFingers(finger, controlCurve, cc):
	cmds.setDrivenKeyframe('right'+finger+'start_IK|right'+finger+'start_jnt_orient.rotateZ', cd=controlCurve+'.'+cc )
	cmds.setDrivenKeyframe('right'+finger+'start_FK_CTRL|right'+finger+'mid_jnt_orient.rotateZ',cd=controlCurve+'.'+cc)
	cmds.setDrivenKeyframe('right'+finger+'mid_FK_CTRL|right'+finger+'mid2_jnt_orient.rotateZ',cd=controlCurve+'.'+cc)
	
###
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
	
def splitJoints(parent, child, number,newName):
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
		jnt=cmds.joint(p=(jointPosP[0]+i*jointVector[0],jointPosP[1]+i*jointVector[1],jointPosP[2]+i*jointVector[2]),rad=0.1,n='new_jnt'+str(i))
		if(i==1):
			if newName=='right':
				cmds.joint(parent, e=True, oj=rotOrder, sao='yup',ch=True, zso=True)
			
			if newName=='left':
				cmds.joint(parent, e=True, oj=rotOrder, sao='ydown',ch=True, zso=True)
				
			cmds.parent(jnt,parent)
		lastJntCreated=jnt
	cmds.parent(child,lastJntCreated)
	
	if newName=='right':
		cmds.joint(parent, e=True, oj=rotOrder, sao='yup' ,ch=True, zso=True)
	if newName=='left':
		cmds.joint(parent, e=True, oj=rotOrder, sao='ydown' ,ch=True, zso=True)
	
def giveColour(newName,control):
	if newName=='left':
		cmds.setAttr(newName+control+".overrideEnabled", 1)
		cmds.setAttr(newName+control+".overrideColor", 4)
	if newName=='right':	
		cmds.setAttr(newName+control+".overrideEnabled", 1)
		cmds.setAttr(newName+control+".overrideColor", 6)	

def doHead(*args):
	cmds.select(cl=True)
	posStart=[0,137,-1]
	posEnd=[0,149.277,1.834]
	
	for i in range(0,4):
		cmds.joint(p=(posStart[0],posStart[1],posStart[2]),rad=1,n='neck_result_jnt'+str(i))
	for i in range(1,4):
		cmds.setAttr('neck_result_jnt'+str(i)+'.translateY',4.2)
		
	cmds.setAttr("neck_result_jnt0.rotateX",13)
	cmds.makeIdentity('neck_result_jnt0', apply=True,t=1,r=1,s=1,n=0,pn=1)
	cmds.joint('neck_result_jnt0',e=True,oj='xzy',sao='xup',ch=True,zso=True)
	
	cmds.ikHandle(n='neck_hdl',sj='neck_result_jnt0',ee='neck_result_jnt3',sol='ikSplineSolver')
	cmds.rename('curve1', 'neck_curve_ik_handle')
	cmds.duplicate('neck_result_jnt0')
	
	cmds.duplicate('neck_result_jnt0',n='neck_start_FK')
	cmds.parent('neck_start_FK|neck_result_jnt1|neck_result_jnt2|neck_result_jnt3', w=True)
	cmds.delete('neck_start_FK|neck_result_jnt1')
	cmds.rename('|neck_result_jnt3', 'neck_end_FK')
	cmds.parent('neck_end_FK','neck_start_FK')
	
	cmds.parent('neck_result_jnt4|neck_result_jnt1|neck_result_jnt2|neck_result_jnt3',w=True)
	cmds.delete('neck_result_jnt4|neck_result_jnt1')
	cmds.rename('neck_result_jnt4','start_neck_bind')
	cmds.rename('|neck_result_jnt3','end_neck_bind')
	cmds.skinCluster('start_neck_bind','end_neck_bind','neck_curve_ik_handle',mi=2)
	
	cmds.setAttr("neck_hdl.dTwistControlEnable",1)
	cmds.setAttr("neck_hdl.dWorldUpType",4)
	cmds.setAttr("neck_hdl.dWorldUpAxis",1)
	cmds.setAttr("neck_hdl.dWorldUpVectorY",-1)
	cmds.setAttr("neck_hdl.dWorldUpVectorEndY",0)
	cmds.setAttr("neck_hdl.dWorldUpVectorEndZ",-1)
	
	cmds.connectAttr('start_neck_bind.worldMatrix[0]', 'neck_hdl.dWorldUpMatrix',f=True)
	cmds.connectAttr('end_neck_bind.worldMatrix[0]',  'neck_hdl.dWorldUpMatrixEnd', f=True)
	
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1,n='head_Ctrl')
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=1,d=3,ut=0,tol=0.01,s=8,ch=1,n='neck_Ctrl')
	cmds.setAttr('head_Ctrl'+".rotateOrder", 2)
	cmds.setAttr('head_Ctrl.tx',cmds.getAttr('end_neck_bind.tx') )
	cmds.setAttr('head_Ctrl.ty',cmds.getAttr('end_neck_bind.ty') )
	cmds.setAttr('head_Ctrl.tz',cmds.getAttr('end_neck_bind.tz') )
	cmds.setAttr('neck_Ctrl.tx',cmds.getAttr('start_neck_bind.tx') )
	cmds.setAttr('neck_Ctrl.ty',cmds.getAttr('start_neck_bind.ty') )
	cmds.setAttr('neck_Ctrl.tz',cmds.getAttr('start_neck_bind.tz') )
	cmds.setAttr('head_Ctrl.s',6,6,6)
	cmds.setAttr('neck_Ctrl.s',6,6,6)
	cmds.makeIdentity('head_Ctrl','neck_Ctrl', apply=True,t=1,r=1,s=1,n=0,pn=1)
	mel.eval('move -rpr 0 149.277 1.834 mesh.scalePivot mesh.rotatePivot ;')
	
	
	cmds.joint('neck_start_FK',e=True,oj='yxz',sao='xup',ch=True,zso=True)
	cmds.setAttr("neck_start_FK.rotateOrder",1)
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=6,d=3,ut=0,tol=0.01,s=8,ch=1,n='neck_FK_Ctrl')
	cmds.circle(c=(0,0,0),nr=(0,1,0), sw=360,r=6,d=3,ut=0,tol=0.01,s=8,ch=1,n='neck_FK_Ctrl2')
	
	cmds.parent('neck_FK_CtrlShape', 'neck_start_FK',r=True, s=True)
	
	cmds.group('head_Ctrl',n='head_Ctrl_grp' )
	cmds.xform('head_Ctrl_grp', cp=1)
	#point constraint and orient constraint instead original file
	
	curveInfoNode = cmds.arclen('neck_curve_ik_handle', ch=True)
	cmds.rename(curveInfoNode, 'neck_Length')
	cmds.shadingNode('multiplyDivide',au=True,n='neck_stretchDiv')
	cmds.connectAttr('neck_Length.arcLength', 'neck_stretchDiv.input1X', f=True)
	cmds.setAttr("neck_stretchDiv.operation", 2)
	cmds.setAttr("neck_stretchDiv.input2X", cmds.getAttr('neck_stretchDiv.input1X'))
	
	###gllobal scale
	cmds.shadingNode('multiplyDivide',au=True,n='global_neckDiv')
	cmds.connectAttr('neck_Length.arcLength', 'global_neckDiv.input1X', f=True)
	cmds.connectAttr('pirate_Root_Transform.scaleY', 'global_neckDiv.input2X', f=True)
	cmds.setAttr("global_neckDiv.operation",2)
	cmds.connectAttr('global_neckDiv.outputX', 'neck_stretchDiv.input1X', f=True)
	
	for i in range (0,4):
		cmds.connectAttr('neck_stretchDiv.outputX','neck_result_jnt'+str(i)+'.scaleX')
	
	list_neck=['neck_result_jnt0', 'neck_hdl', 'neck_curve_ik_handle', 'start_neck_bind', 'neck_start_FK', 'end_neck_bind', 'neck_Ctrl', 'neck_FK_Ctrl', 'neck_FK_Ctrl2', 'head_Ctrl_grp']
	cmds.group(list_neck, n='head_neck_grp')
	cmds.parent('head_neck_grp', 'pirate_Root_Transform' )
	cmds.setAttr("neck_curve_ik_handle.inheritsTransform",0)
	
	#connecting the neck to the head
	cmds.spaceLocator(n='neck_Sh_constr_loc',p=(posEnd[0], posEnd[1], posEnd[2]))
	cmds.xform('neck_Sh_constr_loc',cp=1)
	cmds.parent('neck_Sh_constr_loc', 'sh_bind_jnt')
	cmds.group('neck_start_FK', n='neck_FK_GRP')
	mel.eval('move -rpr 0 137 -1 neck_FK_GRP.scalePivot neck_FK_GRP.rotatePivot ;')

	
	cmds.group('neck_Ctrl', n='head_grp')
	cmds.spaceLocator(n='head_neck_spaceLOC',p=(posEnd[0], posEnd[1], posEnd[2]))
	cmds.spaceLocator(n='head_sh_spaceLOC',p=(posEnd[0], posEnd[1], posEnd[2]))
	cmds.spaceLocator(n='head_body_spaceLOC',p=(posEnd[0], posEnd[1], posEnd[2]))
	cmds.spaceLocator(n='head_root_spaceLOC',p=(posEnd[0], posEnd[1], posEnd[2]))
	cmds.xform('head_neck_spaceLOC','head_sh_spaceLOC','head_body_spaceLOC','head_root_spaceLOC',cp=True)
	cmds.parent('head_neck_spaceLOC', 'neck_end_FK')
	cmds.parent('head_sh_spaceLOC', 'sh_bind_jnt')
	cmds.parent('head_body_spaceLOC', 'DO_NOT_TOUCH')
	cmds.parent('head_root_spaceLOC', 'pirate_Root_Transform')
	
	cmds.orientConstraint('head_neck_spaceLOC','head_sh_spaceLOC',
						'head_body_spaceLOC','head_root_spaceLOC',
						'head_Ctrl_grp',mo=True, w=1)
	cmds.pointConstraint('head_neck_spaceLOC','head_sh_spaceLOC',
						'head_body_spaceLOC','head_root_spaceLOC',
						'head_Ctrl_grp',mo=True, w=1)
	
	cmds.parentConstraint('head_Ctrl','end_neck_bind',mo=True, w=1)
	cmds.parentConstraint('neck_Sh_constr_loc','neck_FK_GRP',mo=True, w=1)
	cmds.parentConstraint('neck_Sh_constr_loc','start_neck_bind',mo=True, w=1)
	
	cmds.addAttr('|pirate_Root_Transform|head_neck_grp|head_Ctrl_grp|head_Ctrl',ln="pointto", at="enum",en="neck:shoulder:body:root:")
	cmds.setAttr('|pirate_Root_Transform|head_neck_grp|head_Ctrl_grp|head_Ctrl.pointto',e=True,keyable=True)
	cmds.addAttr('|pirate_Root_Transform|head_neck_grp|head_Ctrl_grp|head_Ctrl', ln="orientto", at="enum",en="neck:shoulder:body:root:")
	cmds.setAttr('|pirate_Root_Transform|head_neck_grp|head_Ctrl_grp|head_Ctrl.orientto',e=True,keyable=True)
	
	cmds.select(cl=True)
	cmds.setAttr("left_start_arm_jnt_FK.rotateZ", 58)
	cmds.setAttr("right_start_arm_jnt_FK.rotateZ", 58)
	cmds.setAttr("left_mid_arm_jnt_FK.rotateY", 4)
	cmds.setAttr("right_mid_arm_jnt_FK.rotateY", -4)
	
	cmds.setAttr("rightFoot_Ctrl.rotateY", -6)
	cmds.setAttr("leftFoot_Ctrl.rotateY", 6)
	cmds.setAttr("right_Leg_settingsCTRL.PV_blend_NO_FLIP",1)
	cmds.setAttr("left_Leg_settingsCTRL.PV_blend_NO_FLIP",1)

	
	cmds.setAttr("right_index_start_FK_CTRL.rotateY",-8)
	cmds.setAttr("right_index_mid2_FK_CTRL.rotateZ", 12)
	cmds.setAttr("right_index_start_FK_CTRL.rotateZ", 13)
	cmds.setAttr("right_index_mid_FK_CTRL.rotateZ", 12)
	
	cmds.setAttr("right_middle_start_FK_CTRL.rotateY", -2)
	cmds.setAttr("right_middle_start_FK_CTRL.rotateX",4)
	cmds.setAttr("right_middle_start_FK_CTRL.rotateZ",17)
	cmds.setAttr("right_middle_mid_FK_CTRL.rotateZ",11)
	cmds.setAttr("right_middle_mid2_FK_CTRL.rotateZ",3)
	
	cmds.setAttr("right_ring_start_FK_CTRL.rotateY",2)
	cmds.setAttr("right_ring_start_FK_CTRL.rotateZ",17)
	cmds.setAttr("right_ring_start_FK_CTRL.rotateX",9)
	
	cmds.setAttr("right_ring_mid2_FK_CTRL.rotateZ",10)
	cmds.setAttr("right_ring_mid_FK_CTRL.rotateZ",14)
	
	cmds.setAttr("right_pinky_start_FK_CTRL.rotateZ",26)
	cmds.setAttr("right_pinky_start_FK_CTRL.rotateX",9)
	cmds.setAttr("right_pinky_start_FK_CTRL.rotateY",6)
	
	cmds.setAttr("right_pinky_mid2_FK_CTRL.rotateZ",6)
	cmds.setAttr("right_pinky_mid_FK_CTRL.rotateZ",20)
	cmds.setAttr("right_thumb_mid_FK_CTRL.rotateY",7)
	cmds.setAttr("right_thumb_mid2_FK_CTRL.rotateY",10)
	
	###   left side done right idk
	
		
	cmds.setAttr("left_index_start_FK_CTRL.rotateY",8)
	cmds.setAttr("left_index_mid2_FK_CTRL.rotateZ", 12)
	cmds.setAttr("left_index_start_FK_CTRL.rotateZ", 13)
	cmds.setAttr("left_index_mid_FK_CTRL.rotateZ", 12)
	
	cmds.setAttr("left_middle_start_FK_CTRL.rotateY", 2)
	cmds.setAttr("left_middle_start_FK_CTRL.rotateX",-4)
	cmds.setAttr("left_middle_start_FK_CTRL.rotateZ",17)
	cmds.setAttr("left_middle_mid_FK_CTRL.rotateZ",11)
	cmds.setAttr("left_middle_mid2_FK_CTRL.rotateZ",3)
	
	cmds.setAttr("left_ring_start_FK_CTRL.rotateY",-2)
	cmds.setAttr("left_ring_start_FK_CTRL.rotateZ",17)
	cmds.setAttr("left_ring_start_FK_CTRL.rotateX",-9)
	
	cmds.setAttr("left_ring_mid2_FK_CTRL.rotateZ",10)
	cmds.setAttr("left_ring_mid_FK_CTRL.rotateZ",14)
	
	cmds.setAttr("left_pinky_start_FK_CTRL.rotateZ",26)
	cmds.setAttr("left_pinky_start_FK_CTRL.rotateX",-9)
	cmds.setAttr("left_pinky_start_FK_CTRL.rotateY",-6)
	
	cmds.setAttr("left_pinky_mid2_FK_CTRL.rotateZ",6)
	cmds.setAttr("left_pinky_mid_FK_CTRL.rotateZ",20)
	cmds.setAttr("left_thumb_mid_FK_CTRL.rotateY",-7)
	cmds.setAttr("left_thumb_mid2_FK_CTRL.rotateY",-10)


	
def autoRigGUI():
	'''
	ui creating with buttons
	'''
	windowID = 'auto_Pirate_rig_gui'
	if cmds.window(windowID, exists=True):
		cmds.deleteUI(windowID)
	
	#cmds.file(force=True, new=True)	
	#creates the window
	window = cmds.window(windowID,title="Auto Chef Rig UI", w=200,h=200, sizeable=False)
	cmds.columnLayout( adjustableColumn=True )
	
	cmds.text( l='Automatic Rigging Tool for a human')
	
	cmds.button( l='1. Rig it!', command=checkLocExist)
	cmds.button( l='a) create the spine', command=spineDO)
	
	cmds.text(l=" --- write l or r ---")
	legField = cmds.textField("legField", w = 200)
	cmds.button(l = "b) create a leg", align = "center",command = lambda *args:legDo(legField))
	armField = cmds.textField("armField", w = 200)
	cmds.button(l = 'c) create the arm', align = "center", command=lambda *args:armDo(armField))
	cmds.button(l = 'd) create the head', align = "center", command=doHead)
	
	cmds.button( l='2.Close', command=('cmds.deleteUI(\"' + window + '\", window=True)') )
	cmds.setParent( '..' )
	cmds.showWindow() 

if __name__ == "__main__":
	autoRigGUI()
