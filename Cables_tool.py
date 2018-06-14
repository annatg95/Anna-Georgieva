#extruding faces along a curve making cables

import maya.cmds as cmds
import maya.mel as mel
	
def deleteAll(self):
	cmds.file(force=True, new=True)
	
def selectAllDelHis(number):
	cmds.select(all=True)
	if(number!=1):
		cmds.polyUnite( n='combined')
		
	cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0 )
	cmds.delete(constructionHistory=True)
	if(cmds.objExists('combined')):
		cmds.xform('combined', cp=1)
	else:
		print('error')
			
def secondCyl(rad):
	cmds.duplicate('pCylinder1',n='pCylinder2')
	cmds.setAttr('pCylinder2.translate',0,-0.5,rad*2)	

def thirdCyl(rad):
	cmds.duplicate('pCylinder1',n='pCylinder3')
	cmds.setAttr('pCylinder3.translate',rad*2-0.5,-0.5,rad)

def thirdCyl1(rad):
	cmds.duplicate('pCylinder1',n='pCylinder3')
	cmds.setAttr('pCylinder3.translate',rad*2,-0.5,rad*2)
	
def forthCyl(rad):
	cmds.duplicate('pCylinder1',n='pCylinder4')
	cmds.setAttr('pCylinder4.translate',rad*2,-0.5,0)

def checkFaces(subdX):
	if(subdX==6):
		cmds.delete( 'pCylinder1.f[0:11]')
	if(subdX==7): 
		cmds.delete( 'pCylinder1.f[0:13]')
	if(subdX==8):
		cmds.delete('pCylinder1.f[0:15]')
	if(subdX==9):
		cmds.delete( 'pCylinder1.f[0:17]')
	if(subdX==10):
		cmds.delete( 'pCylinder1.f[0:19]')
	if(subdX==11):
		cmds.delete( 'pCylinder1.f[0:21]')
	if(subdX==12):
		cmds.delete('pCylinder1.f[0:23]')
'''func_dict ={6:cmds.delete( 'pCylinder1.f[0:11]'),
				7:cmds.delete( 'pCylinder1.f[0:13]'), 
				8:cmds.delete( 'pCylinder1.f[0:15]'), 
				9:cmds.delete( 'pCylinder1.f[0:17]'), 
				10:cmds.delete( 'pCylinder1.f[0:19]'), 
				11:cmds.delete( 'pCylinder1.f[0:21]'), 
				12:cmds.delete( 'pCylinder1.f[0:23]')}
	func_dict[subdX]'''
		
def checkFaces2(subdX,number):
	if(number==2):
		if(subdX==6):
			cmds.select( 'combined.f[0:11]',add=True)
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:11]')
		if(subdX==7):
			cmds.select( 'combined.f[0:13]',add=True)
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:13]')
		if(subdX==8):
			cmds.select('combined.f[0:15]',add=True)	
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:15]')
		if(subdX==9):
			cmds.select( 'combined.f[0:17]',add=True)
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:17]')
		if(subdX==10):
			cmds.select( 'combined.f[0:19]',add=True)
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:19]')
		if(subdX==11):
			cmds.select( 'combined.f[0:21]',add=True)
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:21]')
		if(subdX==12):
			cmds.select('combined.f[0:23]',add=True)
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:23]')

	if(number==3):
		if(subdX==6):
			cmds.select( 'combined.f[0:11]',add=True)
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:17]')
		if(subdX==7):
			cmds.select( 'combined.f[0:13]',add=True)
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:20]')
		if(subdX==8):
			cmds.select('combined.f[0:15]',add=True)	
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:23]')
		if(subdX==9):
			cmds.select( 'combined.f[0:17]',add=True)
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:26]')
		if(subdX==10):
			cmds.select( 'combined.f[0:19]',add=True)
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:29]')
		if(subdX==11):
			cmds.select( 'combined.f[0:21]',add=True)
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:32]')
		if(subdX==12):
			cmds.select('combined.f[0:23]',add=True)
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:35]')

	if(number==4):
		if(subdX==6):
			cmds.select( 'combined.f[0:11]',add=True)
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:23]')
		if(subdX==7):
			cmds.select( 'combined.f[0:13]',add=True)
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:27]')
		if(subdX==8):
			cmds.select('combined.f[0:15]',add=True)	
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:31]')
		if(subdX==9):
			cmds.select( 'combined.f[0:17]',add=True)
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:35]')
		if(subdX==10):
			cmds.select( 'combined.f[0:19]',add=True)
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:39]')
		if(subdX==11):
			cmds.select( 'combined.f[0:21]',add=True)
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:43]')
		if(subdX==12):
			cmds.select('combined.f[0:23]',add=True)
			mel.eval('polyExtrudeFacet -constructionHistory 1 -keepFacesTogether 1 -pvx 0 -pvy 0 -pvz 0 -divisions 1 -twist 0 -taper 1 -off 0 -thickness 0 -smoothingAngle 30 -inputCurve curve1  combined.f[0:47]')

		
#arguments-subdivisions X, radius R
def createCable(subdX,rad,number):
	cmds.polyCylinder(r=rad,h=1, sx=subdX, sy=1, sz=1)
	cmds.setAttr('pCylinder1.translate',0,-0.5,0)
	checkFaces(subdX)
	
	if(number==2):
		secondCyl(rad)
	if(number==3):
		secondCyl(rad)
		thirdCyl(rad)
	if(number==4):
		secondCyl(rad)
		thirdCyl1(rad)
		forthCyl(rad)
		
	selectAllDelHis(number)

def readyToExtrude(subdX,twistT,divisionsD,number):
	cmds.setAttr('combined.rotate',0,0,90);
	cmds.select('curve1')
	checkFaces2(subdX,number)
	cmds.setAttr('polyExtrudeFace1.divisions', divisionsD)
	cmds.setAttr('polyExtrudeFace1.twist', twistT)
	cmds.select('combined')
	cmds.polyNormal(normalMode=0,userNormalMode=0)
	cmds.polySeparate('combined')
	#selectAllDelHis()
		
def cableGUI():
	windowID = 'cables gen'
	if cmds.window(windowID, exists=True):
		cmds.deleteUI(windowID)
	#cmds.file(force=True, new=True)
		
	myWin=cmds.window(windowID,title="Cable Generator", w=200, h=200,mxb=True,mnb=True)
	cmds.columnLayout( adjustableColumn=True )
	
	#instructions for the user
	cmds.text(align='left',label="Draw a curve around the object to make the cable:	")
	cmds.text(align='left',label="Create a shape and it will follow the curve:	")
	cmds.text(align='left',label="hold C + MMB to snap it to the beginning of the curve:	")
	cmds.text(align='left',label="Twist it and attach bulbs later!")
	
	cmds.text(align='left',label="Subdivisions X; min=6 max=12");
	subdXctrl=cmds.intField(ed=True,minValue=6, maxValue=12, value=8 )
	cmds.text(align='left',label="Radius R; min=1 max=10")
	radR=cmds.intField(ed=True,minValue=1, maxValue=10, value=5 )
	cmds.text(align='left',label="number N; min=1 max=4")
	numberN=cmds.intField(ed=True,minValue=1, maxValue=4, value=2 )
	cmds.text(align='left',label="Divisions D; min=1 max=40")
	divD=cmds.intField(ed=True,minValue=1, maxValue=40, value=20 )
	cmds.text(align='left',label="Twist T; min=1000 max=5000")
	twistT=cmds.intField(ed=True,minValue=1, maxValue=5000, value=1000 )
	
	cmds.button(label = "Create a cable", command =lambda *args: createCable(cmds.intField(subdXctrl, query = True, value = True),cmds.intField(radR, query = True, value = True),cmds.intField(numberN, query = True, value = True)))
	cmds.button(label = "Delete All Objects ", command =deleteAll)
	cmds.button(label = "Twist it ", command =lambda *args: readyToExtrude(cmds.intField(subdXctrl, query = True, value = True),cmds.intField(twistT, query = True, value = True),cmds.intField(divD, query = True, value = True),cmds.intField(numberN, query = True, value = True)))
	#cmds.button(label = "Attatch bulbs", command = 
	cmds.showWindow(myWin)


if __name__ == "__main__":
	cableGUI()
