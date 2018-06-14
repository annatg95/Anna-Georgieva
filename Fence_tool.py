import maya.cmds as cmds
import maya.mel as mel

def createFenceShape(hh,ww):
	if(not cmds.objExists('pCube1')):
		cmds.polyCube(h=hh,w=ww)
		cmds.select('pCube1.e[6:7]','pCube1.e[10:11]')
		cmds.polySplitRing( sma=180, wt=0.4)
		cmds.select('pCube1.e[10:12]', 'pCube1.e[17]')
		cmds.polySplitRing( sma=180, wt=0.6)
		cmds.select('pCube1.vtx[11]','pCube1.vtx[13:14]', 'pCube1.vtx[8]')
		cmds.move(0.0,0.18,0.0,r=True)
	else: 
		print("fuck off")
		
	

def followTheCurve(hh,ww):
	if(not cmds.objExists('curve1')):
		print("create a curve first, and insert maximum knots")
	else:
		selCVs=cmds.ls(sl=True, fl=True)
		selSize_CV=len(selCVs)

		for cvs in range(0,selSize_CV,1):
			findCV_X=cmds.getAttr(selCVs[cvs]+'.xValue')
			findCV_Y=cmds.getAttr(selCVs[cvs]+'.yValue')
			findCV_Z=cmds.getAttr(selCVs[cvs]+'.zValue')
			findCVRot_Y=cmds.get
			
			#m_yaw = atan2(m_velo.m_x,m_velo.m_z)*180/PI+180;//y
			#m_pitch = atan2(m_velo.m_y,sqrt(m_velo.m_x*m_velo.m_x+m_velo.m_z*m_velo.m_z))*180/PI;//x
			#m_rot.set(m_pitch,m_yaw,0);
			
			cmds.select(cl=True)
			
			mkJnt=cmds.polyCube()#createFenceShape(hh,ww)
			cmds.setAttr(mkJnt[0] + '.tx', findCV_X)
			cmds.setAttr(mkJnt[0] + '.ty', findCV_Y)
			cmds.setAttr(mkJnt[0] + '.tz', findCV_Z)	
	
def circularDistribution(radius,number,yVal,moveX ):
	
	cmds.select('pCube1')
	cmds.setAttr('pCube1.rotateY',-90)
	cmds.move(0,0,-radius,r=True)
	cmds.move(0, 0, radius, 'pCube1.scalePivot' ,'pCube1.rotatePivot',r=True,)
	cmds.select('pCube1')
	cmds.duplicate(rr=True)
	cmds.rotate(0,yVal,0,r=True)
	cmds.move(-moveX,0,0,r=True)
	for i in range(1,number):
		cmds.duplicate(rr=True,st=True)
	
def degree(degrees,moveN):
	deg=degrees
	fDegree=str(deg)
	
	selected = cmds.ls(sl=True)
	print len(selected)
	for i in range(1,len(selected)+1):
		if(cmds.objExists('pCube'+str(i))):
			cmds.rotate( 0, i*degrees,0 , 'pCube'+str(i), os=True)
			cmds.move(0,0,i*(moveN/1.5),'pCube'+str(i))
				
	
def createMany(number):
	if(not cmds.objExists('pCube1')):
		print("Create a fence first")
	else:
		print number
		for i in range(2,number):
			cmds.duplicate('pCube1',n='pCube'+str(i))
			cmds.move(0, 0, i*2, 'pCube'+str(i),a=True, ws=True)

	
def fenceGUI():

	windowID = 'fence gen'
	if cmds.window(windowID, exists=True):
		cmds.deleteUI(windowID)
	
	#cmds.file(force=True, new=True)	
	myWin=cmds.window(windowID,title="Fence Generator", w=300, h=200,mxb=True,mnb=True)
	cmds.columnLayout( adjustableColumn=True )
	
	#create a single straight fence
	cmds.text(align='center',label="Straight fence:")
	cmds.text(align='left',label="height: 1<2<45")
	h=cmds.intField(ed=True,minValue=1, maxValue=45, value=2 )
	cmds.text(align='left',label="width: 1<2<45")
	w=cmds.intField(ed=True,minValue=1, maxValue=45, value=2 )
	cmds.text(align='left',label="sx: 0.0<def<4.0")
	
	moveCtrl=cmds.intField(ed=True,minValue=1, maxValue=6, value=3 )
	cmds.text(align='left',label="Change the degree,10< values <45")
	degreeCtrl=cmds.intField(ed=True,minValue=10, maxValue=45, value=30 )	
	cmds.button(l="create a fence", command =lambda *args:createFenceShape(cmds.intField(h, query = True, value = True),cmds.intField(w, query = True, value = True)))
	cmds.button(l="Change degree and distance", command = lambda *args:degree(cmds.intField(degreeCtrl, query = True, value = True),cmds.intField(moveCtrl, query = True, value = True)))
	
	#how many fences along a curve 
	#calculate the rotation of the fence
	cmds.text(align='left',label="enter a number:")
	number=cmds.intField(ed=True,minValue=10, maxValue=45, value=30 )
	cmds.button(l="Create many fances ", command = lambda *args:createMany(cmds.intField(number, query = True, value = True)))
	
	cmds.text(align='center',label="Circular fences:")
	cmds.text(align='left',label="enter a radius:")
	radius=cmds.intField(ed=True,minValue=1, maxValue=45, value=5 )
	cmds.text(align='left',label="angle Y of rotation")
	yVal=cmds.intField(ed=True,minValue=1, maxValue=45, value=5 )
	cmds.text(align='left',label="x of translation")
	xVal=cmds.intField(ed=True,minValue=0, maxValue=45, value=0)
	cmds.button(l="Create Circular Fence ", command = lambda *args:circularDistribution(cmds.intField(radius, query = True, value = True),cmds.intField(number, query = True, value = True),cmds.intField(yVal, query = True, value = True),cmds.intField(xVal, query = True, value = True)))
	
	#fence following a curve
	cmds.text(align='center',label="Follow a curve: ")
	cmds.button(l="Follow me ", command = lambda *args: followTheCurve(cmds.intField(h, query = True, value = True),cmds.intField(w, query = True, value = True)))
	cmds.showWindow(myWin)
	
	
if __name__ == "__main__":
	fenceGUI()
