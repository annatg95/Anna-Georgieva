"""CODE WRITTEN BY ANNA GEORGIEVA"""
"""Feather GENERATOR """
"""1.it creates three types of wings, regarding the height, width and number of wings
	2.it colours the wings, depending on which type they are
	3.when you select the same colour of wings,it also changes the degree and the distance between the wings 
	4.it can be changes n-number of times 
	5.finally, the user can group them all in terms of the type of wing """

import maya.cmds as cmds

#CHECKS IF THE OBJ EXISTS AND FREEZES TRANSFORMATIONS AND DELETES HISTORY AFTER ALL THE CHANGES
def checkAndDel(string): 
	if cmds.objExists(string):
		print("%s is created." % string)
		cmds.select(string)
		cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0 )
		cmds.delete(constructionHistory=True)	
	else:
		print("Warning: NO %s." % string)
		
#RENAMES OBJECTS NAMES
def renameObj(string,string2,string3):
	
	if cmds.objExists(string):
		cmds.select(string)
		cmds.rename(string,'firstRowS')
		for i in range(0,10):
			if(cmds.objExists(string+str(i))):
				cmds.select(string+str(i),add=True)
				cmds.rename(string+str(i), 'firstRowS'+str(i))
		cmds.group(n='fRSecondary')
	if cmds.objExists(string2):	
		cmds.select(string2)
		cmds.rename(string2,'firstRowC')
		for i in range(0,10):
			if(cmds.objExists(string2+str(i))):
				cmds.select(string2+str(i),add=True)
				cmds.rename(string2+str(i), 'firstRowC'+str(i))	
		cmds.group(n='fRCover')
	if cmds.objExists(string3):
		cmds.select(string3)
		cmds.rename(string3,'firstRowP')
		for i in range(0,10):
			if(cmds.objExists(string3+str(i))):
				cmds.select(string3+str(i),add=True)
				cmds.rename(string3+str(i), 'firstRowP'+str(i))
		cmds.group(n='fRPrimary')

	
#SETS COLOURS, DEPENDING ON THE GROUP OF WINGS
def colorW(string, r,g,b):
	
	if(string=='covF'):
		lambert2=cmds.shadingNode('lambert',asShader=True)
		cmds.select(string)
		lambert2SG=cmds.sets(r=True,nss=True,em=True,n='lambert2SG')
		cmds.sets( e=True,fe='lambert2SG')
		cmds.connectAttr('lambert2.outColor','lambert2SG.surfaceShader',f=True)
		cmds.setAttr('lambert2.color',r,g,b,type='double3') 

	if(string=='primaryF'):
		lambert3=cmds.shadingNode('lambert',asShader=True)
		cmds.select(string)
		lambert3SG=cmds.sets(r=True,nss=True,em=True,n='lambert3SG')
		cmds.sets( e=True,fe='lambert3SG')
		cmds.connectAttr('lambert3.outColor','lambert3SG.surfaceShader',f=True)
		cmds.setAttr('lambert3.color',r,g,b,type='double3') 


#SECONDARY Featers 
def secondaryF( height,width):

	base1=cmds.polyCylinder(h=0.5,r=0.1,sx=6,sy=1,sz=1,name='bbase')
	cmds.move(0,0,height*0.45)
	cmds.rotate( '90deg', 0, 0, 'bbase' )
	
	wing1=cmds.polyPlane(h=height,w=width, sx=2, sy=4,name='bwing')
	cmds.rotate(0,0,'0','bwing')
	
	cmds.select('bwing.vtx[0]','bwing.vtx[2]','bwing.vtx[12]','bwing.vtx[14]')
	cmds.scale(0.7,0.7,0.7,absolute=True)
	
	secW=cmds.polyUnite( 'bbase', 'bwing', n='secF' )
	
	cmds.select('secF.vtx[18]','secF.vtx[21]','secF.vtx[24]')
	cmds.move(0,0.35,0, relative=True)
	cmds.setAttr('lambert1.color', 0.201554,0.502877,0.806955 ,type='double3') 
	cmds.rotate('180deg',0,0,'secF')
	checkAndDel('secF');


#COVER Feathers 
def coverF(height, width):
	base2=cmds.polyCylinder(h=.5,r=0.1,sx=6,sy=1,sz=1,name='sbase')
	cmds.move(-0.08,0,height*0.45)
	cmds.rotate( '90deg', 0, 0, 'sbase' )
	
	wing2=cmds.polyPlane(h=height,w=width, sx=2, sy=4,name='swing')
	cmds.rotate(0,0,'0','swing')
	
	cmds.select('swing.vtx[0]','swing.vtx[2]','swing.vtx[12]','swing.vtx[14]')
	cmds.scale(0.7,0.7,0.7,absolute=True)
	
	sideW=cmds.polyUnite( 'sbase', 'swing', n='covF' )

	cmds.select('covF.vtx[28]','covF.vtx[16]')
	cmds.move(-0.45,0,0, relative=True)
	cmds.select('covF.vtx[18]','covF.vtx[21]','covF.vtx[24]')
	cmds.move(-0.45,0.30,0, relative=True)
	cmds.select('covF.vtx[19]','covF.vtx[22]','covF.vtx[25]')
	cmds.move(-0.52,0,0, relative=True)
	cmds.select('covF.vtx[14]','covF.vtx[17]')
	cmds.move(0.18,0,0, relative=True)
	cmds.select('covF.vtx[23]','covF.vtx[26]')
	cmds.move(0.067,0,0, relative=True)
	cmds.select('covF.vtx[23]','covF.vtx[26]')
	cmds.move(-0.16,0,0, relative=True)	
	
	colorW('covF',0.176294,0.362,0.176294);
	cmds.move(-(width*5), 0 ,0, 'covF')
	cmds.rotate('180deg',0,0,'covF')
	checkAndDel('covF');


#PRIMARY Feathers 
def primaryF(height,width):
	base3=cmds.polyCylinder(h=.5,r=0.1,sx=6,sy=1,sz=1,name='ebase')
	cmds.move(0.2,0,height*0.48)
	cmds.rotate( '90deg', 0, 0, 'ebase' )

	wing3=cmds.polyPlane(w=width,h=height, sx=2, sy=5, name='ewing')
	cmds.rotate(0,0,'0','ewing')

	cmds.select('ewing.vtx[0:2]','ewing.vtx[15:17]')
	cmds.move(0.172,0,0,r=True)
	cmds.scale(0.514005,1,1,r=True,p=[0,0.107375,2.32372])
	cmds.select('ewing.vtx[0:14]')
	cmds.move(0.105,0,0,r=True)
	cmds.select('ewing.vtx[4]','ewing.vtx[7]','ewing.vtx[10]','ewing.vtx[13]')
	cmds.move(-0.23,0.214,0,r=True)
	cmds.select('ewing.vtx[0:5]')
	cmds.move(0.138,0,0,r=True)
	cmds.select('ewing.vtx[9:17]')
	cmds.move(-0.052,0,0,r=True)
	cmds.select('ewing.vtx[0:8]')
	cmds.move(-0.037,0,0,r=True)
	cmds.select('ewing.vtx[5]','ewing.vtx[8]','ewing.vtx[11]','ewing.vtx[14]')
	cmds.move(-0.156,0,0,r=True)
	cmds.select('ewing.vtx[0]','ewing.vtx[2]')
	cmds.move(-0.065,0,-0.33,r=True)
	cmds.select('ewing.vtx[1]')
	cmds.move(0,0,-0.356,r=True)

	primW=cmds.polyUnite( 'ebase', 'ewing', n='primaryF' )
	cmds.select('primaryF.vtx[30]')
	cmds.move(0,0,-1.1 ,r=True)
	cmds.select('primaryF.vtx[31]')
	cmds.move(-0.405016,0,0 ,r=True)
	
	cmds.move(-(width*10), 0 ,0, 'primaryF')
	cmds.rotate('180deg',0,0,'primaryF')
	
	colorW('primaryF',0.493,0.183396,0.183396)
	checkAndDel('primaryF');



#CALLS THE WING FUNCTIONS, DEPENDING ON THE STR VALUE
def modelWingProc(height,width,number,str):
	if(cmds.objExists(str)):
		print("%s EXISTS" % str)
	else:
		if(str=='secF'):
			secondaryF( height,width);
		if(str=='covF'):
			coverF( height,width);
		if(str=='primaryF'):
			primaryF( height,width);
			
#CLOSES THE GUI	
def cancelProc(*pArgs):
	print "action is cancelled"
	cmds.deleteUI("wing_gen")

#DUPLICATES THE WINGS, DEPENDING ON THE STRING VALUE  for labs*** height/i
def differentModelType(number,width,height, string):
	if(cmds.objExists(string+str(number))):
		print("% name: "% string.format(number))
	else:
		for i in range( 1,number):
			bw=cmds.duplicate(string,n=string+str(i))
			cmds.move(i*(width/4), 0, 0, string+str(i),a=True, ws=True)   

	return number

#SYMMETRY TIME!
#CHANGES THE DISTANCE AND THE DEGREE BETWEEN WINGS			
def degree(degrees,moveN):
	deg=degrees
	fDegree=str(deg)
	
	selected = cmds.ls(sl=True)
	print len(selected)
	for item in selected:
		for i in range(1,len(selected)):
			if(cmds.objExists(item+str(i))):
				cmds.rotate( 0, i*degrees/2,0 , item+str(i), os=True)
				cmds.move(i*(moveN/1.5), 0,0, item+str(i))
				
			
#GUI STARTS HERE
def wingGUI():
	
	
	windowID = 'wing_gen tabs'
	if cmds.window(windowID, exists=True):
		cmds.deleteUI(windowID)
	
	cmds.file(force=True, new=True)	

	myWin=cmds.window(windowID,title="Feather Generator", w=100, h=100,mxb=True,mnb=True)
	cmds.columnLayout( adjustableColumn=True )
	form = cmds.formLayout()
	tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
	cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )
	
	child1 = cmds.rowColumnLayout(numberOfColumns=2)
	# first section: give parameters for the wings

	cmds.text(align='left',label="HEIGHT between 4 and 10")
	heightCtrl=cmds.intField(ed=True,minValue=4, maxValue=10, value=8 )
	cmds.text(align='left',label="WIDTH between 2 and 4")
	widthCtrl=cmds.intField(ed=True,minValue=2, maxValue=4, value=2 )

	# second section: choose number of secondary wings, primary wings, cover wings
	cmds.text(align='left',label="Values between 1 and 10")
	numberCtrl=cmds.intField(ed=True,minValue=1, maxValue=10, value=5 )
	cmds.button(l="Create a secF", command = lambda *args:modelWingProc(cmds.intField(heightCtrl, query = True, value = True),cmds.intField(widthCtrl, query = True, value = True),cmds.intField(numberCtrl, query = True, value = True),'secF'))
	x='secF'
	x1='firstRowS'
	cmds.button(label = "Create secF", command = lambda *args:differentModelType(cmds.intField(numberCtrl, query = True, value = True),cmds.intField(heightCtrl, query = True, value = True),cmds.intField(widthCtrl, query = True, value = True),x))
	
	#third section
	cmds.button(l="Create a covF", command = lambda *args:modelWingProc(cmds.intField(heightCtrl, query = True, value = True),cmds.intField(widthCtrl, query = True, value = True),cmds.intField(numberCtrl, query = True, value = True),'covF'))
	y='covF'
	y1='firstRowC'
	cmds.button(label = "Create covF", command = lambda *args:differentModelType(cmds.intField(numberCtrl, query = True, value = True),cmds.intField(heightCtrl, query = True, value = True),cmds.intField(widthCtrl, query = True, value = True),y))
	
	#forth section
	cmds.button(l="Create a primF", command = lambda *args:modelWingProc(cmds.intField(heightCtrl, query = True, value = True),cmds.intField(widthCtrl, query = True, value = True),cmds.intField(numberCtrl, query = True, value = True),'primaryF'))
	z='primaryF'
	z1='firstRowP'
	cmds.button(label = "Create primF", command = lambda *args:differentModelType(cmds.intField(numberCtrl, query = True, value = True),cmds.intField(heightCtrl, query = True, value = True),cmds.intField(widthCtrl, query = True, value = True),z))
	
	cmds.setParent( '..' )
	
	child2 = cmds.rowColumnLayout(numberOfColumns=2)
	#choose the degree for the wings to rotate
	cmds.text(align='left',label="Change the degree,10< values <45")
	degreeCtrl=cmds.intField(ed=True,minValue=10, maxValue=45, value=30 )
	cmds.text(align='left',label="Change the distance,  1< values <6")
	moveCtrl=cmds.intField(ed=True,minValue=1, maxValue=6, value=3 )
	cmds.button(l="Change degree and distance", command = lambda *args:degree(cmds.intField(degreeCtrl, query = True, value = True),cmds.intField(moveCtrl, query = True, value = True)))

	#destroy GUI
	cmds.button(label = "Close", width=100,command = cancelProc)
	
	cmds.setParent( '..' )

	#rename and group
	child3 = cmds.rowColumnLayout(numberOfColumns=2)
	cmds.text(align='left',label="Rename and group")
	cmds.button( label='Go', command=lambda *args:renameObj(x,y,z) )
	cmds.setParent( '..' )
	
	cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Wings'), (child2, 'Numbers'), (child3, 'Rename and Grp'))) 
	cmds.showWindow(myWin)


	
# main program, starts here
if __name__ == "__main__":
	wingGUI()

