import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

class HelloWorld(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)

    def doIt(self, argList):
        print 'Hello World!'

def creator():
    return OpenMayaMPx.asMPxPtr( HelloWorld() )

def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Chad Vernon', '1.0', 'Any')
    try:
        plugin.registerCommand('helloWorld', creator)
    except:
        raise RuntimeError, 'Failed to register command'

def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterCommand('helloWorld')
    except:
        raise RuntimeError, 'Failed to unregister command'
