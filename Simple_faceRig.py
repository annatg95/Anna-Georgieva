import maya.cmds as cmds

def yellowCon(s):
	cmds.setAttr(s+'.overrideEnabled',1)
	cmds.setAttr(s+'.overrideColor',17)	

def blueCon(s):
	cmds.setAttr(s+'.overrideEnabled',1)
	cmds.setAttr(s+'.overrideColor',6)
	
def redCon(s):
	cmds.setAttr(s+'.overrideEnabled',1)
	cmds.setAttr(s+'.overrideColor',13)
	
def whiteCon(s):
	cmds.setAttr(s+'.overrideEnabled',1)
	cmds.setAttr(s+'.overrideColor',30)

	
#create mouth module
Lme=cmds.joint(n='l_mouthEdge_JNT')
Lmee=cmds.joint(n='l_mouthEdgeEnd_JNT')
cmds.setAttr(Lmee+'.ty',.5)
cmds.setAttr(Lmee+'.visibility',0)
Lmec=cmds.circle(n='l_mouthEdge_CTRL')
Lmecg=cmds.group(n='l_mouthEdgeCtrl_GRP')
cmds.parentConstraint(Lmec,Lme,mo=True, n='myConstrL')
cmds.setAttr(Lmecg+'.tx', 5)
blueCon(Lmec[0])
cmds.select(d=True)

Rme=cmds.joint(n='r_mouthEdge_JNT')
Rmee=cmds.joint(n='r_mouthEdgeEnd_JNT')
cmds.setAttr(Rmee+'.ty',.5)
cmds.setAttr(Rmee+'.visibility',0)
Rmec=cmds.circle(n='r_mouthEdge_CTRL')
Rmecg=cmds.group(n='r_mouthEdgeCtrl_GRP')
cmds.parentConstraint(Rmec,Rme,mo=True, n='myConstrR')
cmds.setAttr(Rmecg+'.tx',-5)
redCon(Rmec[0])
cmds.select(d=True)

#upper mouth left
Lmum=cmds.joint(n='l_mouthUpperMid_JNT')
Lmume=cmds.joint(n='l_mouthUpperMidEnd_JNT')
cmds.setAttr(Lmume+'.ty', .5)
cmds.setAttr(Lmume+'.visibility', 0)
Lmumc=cmds.circle(n='l_mouthUpperMid_CTRL')
Lmumcg=cmds.group(n='l_mouthUpperMidCtrl_GRP')
cmds.parentConstraint(Lmumc,Lmum,mo=True)
cmds.setAttr(Lmumcg+'.tx',3)
cmds.setAttr(Lmumcg+'.ty',3)
cmds.setAttr(Lmumcg+'.tz',0.7)
yellowCon(Lmumc[0])
cmds.select(d=True)

#upper mouth right
Rmum=cmds.joint(n='r_mouthUpperMid_JNT')
Rmume=cmds.joint(n='r_mouthUpperMidEnd_JNT')
cmds.setAttr(Rmume+'.ty', .5)
cmds.setAttr(Rmume+'.visibility', 0)
Rmumc=cmds.circle(n='r_mouthUpperMid_CTRL')
Rmumcg=cmds.group(n='r_mouthUpperMidCtrl_GRP')
cmds.parentConstraint(Rmumc,Rmum,mo=True)
cmds.setAttr(Rmumcg+'.tx',-3)
cmds.setAttr(Rmumcg+'.ty',3)
cmds.setAttr(Rmumcg+'.tz',0.7)
yellowCon(Rmumc[0])
cmds.select(d=True)

#upper mouth center
Cmum=cmds.joint(n='c_mouthUpperMid_JNT')
Cmume=cmds.joint(n='c_mouthUpperMidEnd_JNT')
cmds.setAttr(Cmume+'.ty', .5)
cmds.setAttr(Cmume+'.visibility', 0)
Cmumc=cmds.circle(n='c_mouthUpperMid_CTRL')
Cmumcg=cmds.group(n='c_mouthUpperMidCtrl_GRP')
cmds.parentConstraint(Cmumc,Cmum,mo=True)
cmds.setAttr(Cmumcg+'.ty',4)
cmds.setAttr(Cmumcg+'.tz',1)
yellowCon(Cmumc[0])
cmds.select(d=True)

#lower mouth center
Lcmum=cmds.joint(n='c_mouthLowerMid_JNT')
Lcmume=cmds.joint(n='c_mouthLowerMidEnd_JNT')
cmds.setAttr(Lcmume+'.ty', .5)
cmds.setAttr(Lcmume+'.visibility', 0)
Lcmumc=cmds.circle(n='c_mouthLowerMid_CTRL')
Lcmumcg=cmds.group(n='c_mouthLowerMidCtrl_GRP')
cmds.parentConstraint(Lcmumc,Lcmum,mo=True)
cmds.setAttr(Lcmumcg+'.ty',-4)
cmds.setAttr(Lcmumcg+'.tz',1)
whiteCon(Lcmumc[0])
cmds.select(d=True)

#lower mouth right
Lrmum=cmds.joint(n='r_mouthLowerMid_JNT')
Lrmume=cmds.joint(n='r_mouthLowerMidEnd_JNT')
cmds.setAttr(Lrmume+'.ty', .5)
cmds.setAttr(Lrmume+'.visibility', 0)
Lrmumc=cmds.circle(n='r_mouthLowerMid_CTRL')
Lrmumcg=cmds.group(n='r_mouthLowerMidCtrl_GRP')
cmds.parentConstraint(Lrmumc,Lrmum,mo=True)
cmds.setAttr(Lrmumcg+'.tx',-3)
cmds.setAttr(Lrmumcg+'.ty',-3)
cmds.setAttr(Lrmumcg+'.tz',0.7)
whiteCon(Lrmumc[0])
cmds.select(d=True)

#lower mouth left
Llmum=cmds.joint(n='l_mouthLowerMid_JNT')
Llmume=cmds.joint(n='l_mouthLowerMidEnd_JNT')
cmds.setAttr(Llmume+'.ty', .5)
cmds.setAttr(Llmume+'.visibility', 0)
Llmumc=cmds.circle(n='l_mouthLowerMid_CTRL')
Llmumcg=cmds.group(n='l_mouthLowerMidCtrl_GRP')
cmds.parentConstraint(Llmumc,Llmum,mo=True)
cmds.setAttr(Llmumcg+'.tx',3)
cmds.setAttr(Llmumcg+'.ty',-3)
cmds.setAttr(Llmumcg+'.tz',0.7)
whiteCon(Llmumc[0])
cmds.select(d=True)

#group selection
ctrlGrp=cmds.group(Llmumcg,Lrmumcg,Lcmumcg,Cmumcg,Lmecg,Rmecg,Lmumcg,Rmumcg, n='all_ctr')
jntGrp=cmds.group(Llmum,Lrmum,Lcmum,Cmum,Rmum,Lmum,Lme,Rme,n='all_jnt')
