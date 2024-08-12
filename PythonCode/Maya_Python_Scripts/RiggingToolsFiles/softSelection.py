import maya.OpenMaya as om
import maya.cmds as cmds


def softCluster():
    """
    :return: A cluster deformer with the same weights as the soft selection
    """
    
    # get our selection, rich selection, and a dag path
    sel = om.MSelectionList()
    
    if not cmds.ls(sl = True):
        raise RuntimeError("No components are selected")
 
    softSel = om.MRichSelection()
    om.MGlobal.getRichSelection(softSel)
    softSel.getSelection(sel)

    
    dag = om.MDagPath()
    sel.getDagPath(0, dag)
    
    selLocs = cmds.xform(cmds.ls(sl=1), q=1, t=1, ws=1)
    selLen = float(len(selLocs[0::3]))
    selSums = [sum(selLocs[0::3]),sum(selLocs[1::3]),sum(selLocs[2::3])]
    selPivot = [selSums[0] / selLen, selSums[1] / selLen, selSums[2] / selLen]
    
    print (dag.apiType())
    '''
    if dag.apiType() == 296:
        #mesh
        objIter = om.MItSelectionList(sel, om.MFn.kMeshVertComponent)
        componentType = "vtx"
    elif dag.apiType() == 267:
        #nurbs curve
        objIter = om.MItSelectionList(sel, om.MFn.kCurveCVComponent)
        componentType = "cv"
    elif dag.apiType() == 279:
        # lattice
        componentType = "pt"
        objIter = om.MItSelectionList(sel, om.MFn.kLatticeComponent)
    else:
        raise TypeError("Object type not supported")
        
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
    
    # iterate through each selected mesh (there should only be one)
    while not objIter.isDone():
        #get dag path of current iter obj
        objIter.getDagPath(dag, components)
        #if apiType is mesh or nurbs curve:
        if dag.apiType() in [296, 267]:
            #function set for getting info from seletion
            fnComp = om.MFnSingleIndexedComponent(components)
            fnComp.getElements(indexList)
            # iterate through selection, add weight influence to weight list
            for i in range (indexList.length()):
                if fnComp.hasWeights():
                    weights.append(fnComp.weight(i).influence())
                else:
                    weights.append(1)
                # append string representing selection to elements list
                elemList.append("%s.%s[%i]" % (dag.fullPathName(), componentType, indexList[i]))
        # if apiType is Lattice:
        elif dag.apiType() == 279:                
            #int arrays that store triple indexed data (lattice has points with 3D indexes)
            u = om.MIntArray()
            v = om.MIntArray()
            w = om.MIntArray()
            #make a function to get information from these elements
            fnComp = om.MFnTripleIndexedComponent(components)
            fnComp.getElements(u, v, w)
            
            # iterate through selection, add weight influence to weight list.
            for i in range (u.length()):
                if fnComp.hasWeights():
                    weights.append(fnComp.weight(i).influence())
                else:
                    weights.append(1)
                # append string representing 3D index of current lattice point
                latticeIndexList.append("[%i][%i][%i]" % (u[i], v[i], w[i]))
                # append string representing selection to elements list
                elemList.append("%s.pt[%i][%i][%i]" % (dag.fullPathName(), u[i], v[i], w[i]))
        objIter.next()
    
    cmds.select(elemList)
    cluster = cmds.cluster(n="softCluster#")
    cmds.xform(cluster[1], piv=selPivot)
    i=0
    
    if dag.apiType in [296, 267]:
        #set weights on cluster for mesh and nurbsCurve:
        while i < weights.length():
            cmds.percent(cluster[0],"%s.%s[%i]" % (dag.fullPathName(), componentType, indexList[i]), v=weights[i])
            i+=1
    else:
        while i < weights.length():
            #set weights on cluster for lattice
            cmds.percent(cluster[0], "%s.pt%s" % (dag.fullPathName(), latticeIndexList[i]), v=weights[i])
            i+=1
            
    return cluster
    '''

softCluster()