def makeCity():
    cmds.select(all=True)
    cmds.delete()
    for i in range( 0,10):	
        cmds.polyPlane( sx=1, sy=1, w=10, h=10, name = 'myP'+str(i))
    	cmds.move(i*10, 0, 0, 'myP'+str(i))
    	for j in range(0,10):
    	    cmds.duplicate('myP'+str(i), n='myP'+str(i)+str(j))
    	    cmds.move(i*10, 0, j*10, 'myP'+str(i)+str(j), a=True, ws=True)   #absolute  
makeCity()
