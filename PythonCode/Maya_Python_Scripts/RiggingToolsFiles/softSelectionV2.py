import maya.OpenMaya as om
import maya.cmds as cmds
import pymel.core as pm

def softSelect(*args):

    selection = om.MSelectionList()

    if not cmds.ls(sl=True):
        raise RuntimeError("No object selected")
    
    softSelection = om.MRichSelection()
    om.MGlobal.getRichSelection(softSelection)
    check = softSelection.getSelection(selection)

    ObjectDag = om.MDagPath()

    # Get the DAG path of the first object in the selection list and store it in ObjectDag
    selection.getDagPath(0, ObjectDag)

    # Get the world space coordinates of the selected components
    select_locations = pm.xform(pm.ls(sl=1), q=1, t=1, ws=1)


    #The purpose of this code is to calculate the sum and average of the sublists of every three elements in the select_locations list.
    select_length = float(len(select_locations[0::3]))
    select_sums = [sum(select_locations[0::3]),sum(select_locations[1::3]),sum(select_locations[2::3])]
    select_pivot = [select_sums[0] / select_length, select_sums[1] / select_length, select_sums[2] / select_length]

    print(ObjectDag.apiType())

    if ObjectDag.apiType() == 296:
        
        objIter = om.MItSelectionList(selection, om.MFn.kMeshVertComponent)
        componentType = "vtx"
    elif ObjectDag.apiType() == 267:
        
        objIter = om.MItSelectionList(selection, om.MFn.kCurveCVComponent)
        componentType = "cv"
    elif ObjectDag.apiType() == 279:
        componentType = "pt"
        objIter = om.MItSelectionList(selection, om.MFn.kLatticeComponent)
    else:
        raise TypeError("Not this Object type !!!")
    
    # stores string used for full compent selection when cluster made
    elemList = []
    # stores the weights for each selected component
    weights = om.MFloatArray()
    # stores the index of each selected component
    indexList = om.MIntArray()
    # on lattices stores array of tripple-idexed strings representing indexes
    latticeIndexList = []
    # MObject initated from DagPath that will be used by MFnComponent type functions
    components = om.MObject()

    

softSelect()