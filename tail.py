
inputCurve='curve1'
idName='tail1'
numberOfCvs=11
print numberOfCvs
Jnts=[]
IKjnts=[]
ctrlForIK=[]
ResultJnts=[]
for i in range(0, numberOfCvs):
    cmds.select( clear = True )
    currentCvPos = cmds.pointPosition('curve1.cv['+str(i)+']', w=1 )
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
