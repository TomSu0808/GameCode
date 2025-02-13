import sys
sys.path.append("G:\\Utah EAE\\StudyProject\\SelfStudy\\RiggingClassStudy\\MyWorks\\JointBasedMucleDeformation\\Code\\Complete")

import maya.cmds as cmds
import maya.api.OpenMaya as om
import math



twist_axis_vectors = {
    "X": om.MVector.kXaxisVector,
    "-X": om.MVector.kXnegAxisVector,
    "Y": om.MVector.kYaxisVector,
    "-Y": om.MVector.kYnegAxisVector,
    "Z": om.MVector.kZaxisVector,
    "-Z": om.MVector.kZnegAxisVector
}

up_axis_vectors = {
    "Y": om.MVector.kYaxisVector,
    "-Y": om.MVector.kYnegAxisVector,
    "X": om.MVector.kXaxisVector,
    "-X": om.MVector.kXnegAxisVector,
    "Z": om.MVector.kZaxisVector,
    "-Z": om.MVector.kZnegAxisVector
}



def check_and_setup_twist_joints(*args):
    counter_twist_checked = cmds.checkBox(counter_twist_checkbox, q=True, value=True)
    twist_checked = cmds.checkBox(twist_checkbox, q=True, value=True)
    
    if counter_twist_checked and twist_checked:
        cmds.error("Please select only one of the checkboxes.")
        return None
    
    if not counter_twist_checked and not twist_checked:
        cmds.error("Please select one of the checkboxes.")
        return None
    
    if twist_checked:
        setup_twist_joints(
            start_joint=cmds.textField(start_joint_field, q=True, text=True),
            end_joint=cmds.textField(end_joint_field, q=True, text=True),
            twist_joint_num=cmds.intSliderGrp(twist_joint_slider, q=True, value=True)
        )
    
    if counter_twist_checked:
        setup_counter_twist_joints(
            start_joint=cmds.textField(start_joint_field, q=True, text=True),
            end_joint=cmds.textField(end_joint_field, q=True, text=True),
            twist_joint_num=cmds.intSliderGrp(twist_joint_slider, q=True, value=True)
        )
    


def setup_twist_joints(start_joint, end_joint, twist_joint_num):
    twist_axis_value = cmds.optionMenuGrp("twistAxisMenu", query=True, value=True)
    up_axis_value = cmds.optionMenuGrp("upAxisMenu", query=True, value=True)

    TwistAxis = twist_axis_vectors[twist_axis_value]
    UpAxis = up_axis_vectors[up_axis_value]

    if cmds.objExists(start_joint) and cmds.objExists(end_joint):
        SetUpTwistJointChain(
            StartJoint = start_joint, 
            EndJoint = end_joint, 
            TwistJointNum = twist_joint_num, 
            TwistAxis = TwistAxis, 
            UpAxis = UpAxis
        )

def setup_counter_twist_joints(start_joint, end_joint, twist_joint_num):
    twist_axis_value = cmds.optionMenuGrp("twistAxisMenu", query=True, value=True)
    up_axis_value = cmds.optionMenuGrp("upAxisMenu", query=True, value=True)

    TwistAxis = twist_axis_vectors[twist_axis_value]
    UpAxis = up_axis_vectors[up_axis_value]

    if cmds.objExists(start_joint) and cmds.objExists(end_joint):
        SetUpCounterTwistJointChain(
            StartJoint = start_joint, 
            EndJoint = end_joint, 
            TwistJointNum = twist_joint_num, 
            TwistAxis = TwistAxis, 
            UpAxis = UpAxis
        )
        


def CreateJoint(name, query = False):
    if not query:
        cmds.joint(name = name)
    if query and not cmds.ls(name, type = "joint"):
        return None
    return name

def SoftParent(child, parent):
    try:
        cmds.parent(child, parent)
    except RuntimeError:
        pass

def ResetJoint(joint_list):
    for joint in joint_list:
        cmds.setAttr("{}.translate".format(joint), 0, 0, 0)
        cmds.setAttr("{}.rotate".format(joint), 0, 0, 0)
        cmds.setAttr("{}.scale".format(joint), 1, 1, 1)

        cmds.setAttr("{}.rotateOrder".format(joint), 0)

        cmds.setAttr("{}.preferredAngle".format(joint), 0, 0, 0)

def TwistAxisSetUp(self):
    twist_axis_set_up = cmds.optionMenuMenu(twist_joint_ui, query = True, value = True)
    
    if twist_axis_set_up == "X":
        return om.MVector.kXaxisVector
    elif twist_axis_set_up == "-X":
        return om.MVector.kXnegAxisVector
    elif twist_axis_set_up == "Y":
        return om.MVector.kYaxisVector
    elif twist_axis_set_up == "-Y":
        return om.MVector.kYnegAxisVector
    elif twist_axis_set_up == "Z":
        return om.MVector.kZaxisVector
    elif twist_axis_set_up == "-Z":
        return om.MVector.kZnegAxisVector
        
def UpAxisSetUp():
    up_axis_set_up = cmds.optionMenuMenu(twist_joint_ui, query = True, value = True)
    
    if up_axis_set_up == "X":
        om.MVector.kXaxisVector
    elif up_axis_set_up == "-X":
        om.MVector.kXnegAxisVector
    elif up_axis_set_up == "Y":
        om.MVector.kYaxisVector
    elif up_axis_set_up == "-Y":
        om.MVector.kYnegAxisVector
    elif up_axis_set_up == "Z":
        om.MVector.kZaxisVector
    elif up_axis_set_up == "-Z":
        om.MVector.kZnegAxisVector

def SetUpTwistJointChain(StartJoint, EndJoint, TwistJointNum, 
                            TwistAxis = om.MVector.kXaxisVector, UpAxis = om.MVector.kYaxisVector, query = False):   

    if not EndJoint:
        children_joints = cmds.listRelatives(StartJoint, children = True, type = "joint")
        if children_joints:
            EndJoint = children_joints[0]

    if not cmds.ls(EndJoint):
        cmds.error("{} is not valid".format(StartJoint))

    ###


    # start_joint_aim_target = CreateJoint(name = StartJoint + "AimTarget1", query = query)

    # create twist joints
    twist_joints_list = []
    for i in range (TwistJointNum):
        cmds.select(StartJoint)
        twist_joints_name = StartJoint + "_TwistJoint_00{}".format(i+1)
        CreateJoint(name = twist_joints_name, query = query)
        twist_joints_list.append(twist_joints_name)

    


    # set up basis joint group

    cmds.select(clear = True)

    twist_basis_joint = CreateJoint(name = StartJoint + "TwistBasis_001", query = query)

    cmds.select(twist_basis_joint)
    twist_value_joint = CreateJoint(name = StartJoint + "TwistValue_001", query = query)

    # create twist offset joint
    # cmds.select(twist_basis_joint)
    # twist_offset_joint = CreateJoint(name = StartJoint + "BasisOffset_001", query = query)

    

    
    ###
    if not query:
        # position joints
        # SoftParent(start_joint_aim_target, StartJoint)
        # cmds.matchTransform(start_joint_aim_target, EndJoint)

        cmds.matchTransform(twist_basis_joint, StartJoint)
        SoftParent(twist_basis_joint, StartJoint)
        cmds.setAttr("{}.radius".format(twist_basis_joint), 0.5)
        
        # twist set up
        # cmds.orientConstraint(EndJoint, start_joint_aim_target, mo = False, w = 1)

        # caculate length for joint chain
        joint_chain_length = (om.MVector(cmds.xform(EndJoint, translation = True, q = True, ws = True)) - om.MVector(
            cmds.xform(StartJoint, translation = True, q = True, ws = True) )).length()

        # create offset between the last twist joint and end joint, this is used for skinweights transfer
        offset_ratio = 0.02
        joint_chain_length *= (1 - offset_ratio)
        # divide the current number of joint in joint chain list
        distribution_distance = joint_chain_length / (len(twist_joints_list))
        
        for i, twist_joint in enumerate(twist_joints_list):
            translation = distribution_distance * TwistAxis * (i + 1)
            cmds.setAttr("{}.t".format(twist_joint), *translation)
            cmds.setAttr("{}.radius".format(twist_joint), 2.0)
        
        # reset joints
        # TwistJoint.ResetJoint(twist_joints_list)

        cmds.aimConstraint(EndJoint, twist_value_joint, 
                            aimVector = TwistAxis,
                            upVector = UpAxis,
                            worldUpType = "objectrotation",
                            worldUpObject = EndJoint,
                            worldUpVector = UpAxis)
        
        # use orient constraint to distribute the twisting along the joint chain
        orient_constraint = cmds.orientConstraint([twist_basis_joint, twist_value_joint], twist_joints_list[-1], mo = False, weight = 1)[0]
        
        cmds.setAttr("{0}.interpType".format(orient_constraint), 2)
        cmds.setAttr("{0}.{1}W0".format(orient_constraint, twist_basis_joint), 0)
        cmds.setAttr("{0}.{1}W1".format(orient_constraint, twist_value_joint), 1)
        
        weight_unit = 1.0 / (TwistJointNum)
        for i in range(TwistJointNum - 1):
            orient_constraint = cmds.orientConstraint([twist_basis_joint, twist_value_joint], twist_joints_list[i],
                                                        mo = False, weight = 1)[0]
            
            # set orientaionConstraint interp type to shortest
            cmds.setAttr("{0}.interpType".format(orient_constraint), 2)
            cmds.setAttr("{0}.{1}W0".format(orient_constraint, twist_basis_joint), (1 - weight_unit * (i + 1)))
            cmds.setAttr("{0}.{1}W1".format(orient_constraint, twist_value_joint), weight_unit * (i + 1))
        
        # TwistJoint.ResetJoint([twist_basis_joint, twist_value_joint, twist_offset_joint])

    
    return twist_joints_list, [twist_basis_joint, twist_value_joint]

def aim_joint_upper_level_joint():
    
    selected_joints = cmds.ls(selection=True, type="joint")

    if selected_joints:
        for joint in selected_joints:
            parent_joint = cmds.listRelatives(joint, parent=True, type="joint")
            return parent_joint

def SetUpCounterTwistJointChain(StartJoint, EndJoint, TwistJointNum, 
                            TwistAxis = om.MVector.kXaxisVector, UpAxis = om.MVector.kYaxisVector, query = False):   

    if not EndJoint:
        children_joints = cmds.listRelatives(StartJoint, children = True, type = "joint")
        if children_joints:
            EndJoint = children_joints[0]

    if not cmds.ls(EndJoint):
        cmds.error("{} is not valid".format(StartJoint))

    ###
    # create twist joints
    counter_twist_joints_list = []
    for i in range (TwistJointNum):
        cmds.select(StartJoint)
        twist_joints_name = StartJoint + "_TwistJoint_00{}".format(i+1)
        CreateJoint(name = twist_joints_name, query = query)
        counter_twist_joints_list.append(twist_joints_name)

    # Set up Aim joint for parent joint
    cmds.select(clear = True)
    cmds.select(StartJoint)
    aim_joints_upper = aim_joint_upper_level_joint()
    cmds.select(clear = True)
    # cmds.select(aim_joints_upper)
    cmds.select(StartJoint)
    aim_joint = cmds.joint(name = StartJoint + "_TwistUpJoint")

    # Move along only one axis based on UpAxis
    if abs(UpAxis.x) > 0:
        cmds.move(3 * UpAxis.x, 0, 0, aim_joint, os=True, relative=True)
        
    elif abs(UpAxis.y) > 0:
        cmds.move(0, 3 * UpAxis.y, 0, aim_joint, os=True, relative=True)
        
    elif abs(UpAxis.z) > 0:
        cmds.move(0, 0, 3 * UpAxis.z, aim_joint, os=True, relative=True)

    cmds.setAttr("{}.radius".format(aim_joint), 2)
    cmds.parent(aim_joint, aim_joints_upper)

    
    # set up basis joint group

    cmds.select(clear = True)

    twist_basis_joint = CreateJoint(name = StartJoint + "TwistBasis_001", query = query)

    cmds.select(twist_basis_joint)
    twist_value_joint = CreateJoint(name = StartJoint + "TwistValue_001", query = query)

    # create twist offset joint
    cmds.select(twist_basis_joint)
    twist_offset_joint = CreateJoint(name = StartJoint + "BasisOffset_001", query = query)  

    ###
    if not query:

        cmds.matchTransform(twist_basis_joint, StartJoint)
        SoftParent(twist_basis_joint, StartJoint)
        cmds.setAttr("{}.radius".format(twist_basis_joint), 0.5)
        
        # twist set up

        # caculate length for joint chain
        joint_chain_length = (om.MVector(cmds.xform(EndJoint, translation = True, q = True, ws = True)) - om.MVector(
            cmds.xform(StartJoint, translation = True, q = True, ws = True) )).length()

        # create offset between the last twist joint and end joint, this is used for skinweights transfer
        offset_ratio = 0.02
        joint_chain_length *= (1 - offset_ratio)
        # divide the current number of joint in joint chain list
        distribution_distance = joint_chain_length / (len(counter_twist_joints_list))
        
        for i, twist_joint in enumerate(counter_twist_joints_list):
            translation = distribution_distance * TwistAxis * i
            cmds.setAttr("{}.t".format(twist_joint), *translation)
            cmds.setAttr("{}.radius".format(twist_joint), 2.0)
        
        first_counter_twist_joint = counter_twist_joints_list[0]
        first_counter_joint_translation = [axis * 0.2 for axis in TwistAxis]
        cmds.setAttr("{}.t".format(first_counter_twist_joint), *first_counter_joint_translation)

        # aim constraint TwistBasis joint to aim_joint
        cmds.aimConstraint(EndJoint, twist_basis_joint, 
                            aimVector = TwistAxis,
                            upVector = UpAxis,
                            worldUpType = "object",
                            worldUpObject = aim_joint,
                            worldUpVector = UpAxis)
        
        
        cmds.aimConstraint(EndJoint, twist_value_joint, 
                            aimVector = TwistAxis,
                            upVector = UpAxis,
                            worldUpType = "objectrotation",
                            worldUpObject = StartJoint,
                            worldUpVector = UpAxis)
        
        # use orient constraint to distribute the twisting along the joint chain
        orient_constraint = cmds.orientConstraint([twist_value_joint, twist_offset_joint], counter_twist_joints_list[0], mo = False, weight = 1)[0]
        
        cmds.setAttr("{0}.interpType".format(orient_constraint), 2)
        cmds.setAttr("{0}.{1}W0".format(orient_constraint, twist_value_joint), 0.1)
        cmds.setAttr("{0}.{1}W1".format(orient_constraint, twist_offset_joint), 0.9)

        counter_twist_joints_list.pop(0)
        
        weight_unit = 1.0 / (TwistJointNum)
        
        for i in range(TwistJointNum - 1):
            orient_constraint = cmds.orientConstraint([twist_value_joint, twist_offset_joint], counter_twist_joints_list[i],
                                                        mo = False, weight = 1)[0]
            
            # set orientaionConstraint interp type to shortest
            cmds.setAttr("{0}.interpType".format(orient_constraint), 2)
            cmds.setAttr("{0}.{1}W0".format(orient_constraint, twist_value_joint), weight_unit * (i + 1))
            cmds.setAttr("{0}.{1}W1".format(orient_constraint, twist_offset_joint), (1 - weight_unit * (i + 1)))

        # Run the non-flip twist joint function
        setUpNonFlipTwistJoint(StartJoint, EndJoint, aim_joint, twist_basis_joint, upAxis = UpAxis)
                            
        

    return counter_twist_joints_list, [twist_basis_joint, twist_value_joint]
    
def setUpNonFlipTwistJoint(startJoint, endJoint, upJoint, startJointBase, upAxis, query = False):
    startJointParent = cmds.listRelatives(startJoint, parent = True, type = "joint")
    if not startJointParent:
        cmds.error("Start joint must have a parent joint.")
        return
    
    startJointParent = startJointParent[0]
    dotProductJoint = CreateJoint(name = startJoint.lstrip("JO") + "_Twist_{0}".format(startJointParent.lstrip("JO")),
                                  query = query)
    
    if not query:
        # Create the dot product joint
        SoftParent(dotProductJoint, startJoint)
        cmds.setAttr("{0}.translate".format(dotProductJoint), 0, 0, 0)
        offsetVector = -0.1 * upAxis
        cmds.move(offsetVector.x, offsetVector.y, offsetVector.z, dotProductJoint, r = True, os = True)
        
        cmds.setAttr("{0}.rotate".format(dotProductJoint), 0, 0, 0)



        # Move along only one axis based on UpAxis
        if abs(upAxis.x) > 0:
            cmds.move(-3 * upAxis.x, 0, 0, dotProductJoint, os=True, relative=True)
            print("x")
        elif abs(upAxis.y) > 0:
            cmds.move(0, -3 * upAxis.y, 0, dotProductJoint, os=True, relative=True)
            print("y")
        elif abs(upAxis.z) > 0:
            cmds.move(0, 0, -3 * upAxis.z, dotProductJoint, os=True, relative=True)
            print("z")
        


        SoftParent(dotProductJoint, startJointParent)

        
        
        dotProductNode = cmds.shadingNode("vectorProduct", asUtility = True, name = startJoint + "_DPN")
        multiplyMatrixNode = cmds.shadingNode("multMatrix", asUtility = True, name = startJoint + "_MMN")
        docomposeMatrixNode = cmds.shadingNode("decomposeMatrix", asUtility = True, name = startJoint + "_DMN")

        cmds.connectAttr("{0}.worldMatrix".format(dotProductJoint), "{0}.matrixIn[0]".format(multiplyMatrixNode))
        cmds.connectAttr("{0}.worldInverseMatrix".format(startJointBase), "{0}.matrixIn[1]".format(multiplyMatrixNode))
        cmds.connectAttr("{0}.matrixSum".format(multiplyMatrixNode), "{0}.inputMatrix".format(docomposeMatrixNode))

        cmds.connectAttr("{0}.outputTranslate".format(docomposeMatrixNode), "{0}.input1".format(dotProductNode))
        cmds.connectAttr("{0}.translate".format(endJoint), "{0}.input2".format(dotProductNode))

        cmds.setAttr("{0}.normalizeOutput".format(dotProductNode), 1.0)

        upJointMatrix = om.MMatrix(cmds.getAttr("{0}.worldMatrix".format(upJoint)))
        startJointMatrix = om.MMatrix(cmds.getAttr("{0}.worldMatrix".format(startJoint)))
        offsetMatrix = upJointMatrix * startJointMatrix.inverse()

        def setDrivenKeys():
            cmds.setDrivenKeyframe(upJoint + '.translateX', cd=dotProductNode + '.' + 'outputX',
                                inTangentType='linear', outTangentType='linear')
            cmds.setDrivenKeyframe(upJoint + '.translateY', cd=dotProductNode + '.' + 'outputX',
                                inTangentType='linear', outTangentType='linear')
            cmds.setDrivenKeyframe(upJoint + '.translateZ', cd=dotProductNode + '.' + 'outputX',
                                inTangentType='linear', outTangentType='linear')

        # create a temp dagpose
        cmds.dagPose(startJoint, save=True, name='tempDagPose1')
        setDrivenKeys()

        projectJointChainToPlane(startJoint, endJoint, upAxis)
        
        # calculate the up vector position
        calculateUpVecterPosition(startJoint, upJoint, offsetMatrix)
        setDrivenKeys()

        cmds.dagPose('tempDagPose1', restore=True)
        projectJointChainToPlane(startJoint, endJoint, upAxis, negative=True)

        # calculate upJoint position
        calculateUpVecterPosition(startJoint, upJoint, offsetMatrix)
        setDrivenKeys()

        cmds.dagPose('tempDagPose1', restore=True)

        cmds.delete('tempDagPose1')

        return dotProductJoint

def calculateUpVecterPosition(startJoint, upJoint, offsetMatrix):
    #计算一个新的世界矩阵，并将其转换为局部矩阵，然后提取平移部分并设置到一个关节上。

    newWorldMatrix = offsetMatrix * om.MMatrix(cmds.getAttr('{0}.worldMatrix'.format(startJoint)))
    localMatrix = newWorldMatrix * om.MMatrix(cmds.getAttr('{0}.parentInverseMatrix'.format(upJoint)))
    translation = om.MTransformationMatrix(localMatrix).translation(4)
    cmds.setAttr('{0}.t'.format(upJoint), *translation)

def projectJointChainToPlane(startJoint, endJoint, upAxis, planeNormal=None, negative=False):
    """rotate the joint chain with local axis cross product by aimAxis and upAxis to project it to plane with given normal
    Args:
        startJoint (str): parent joint name of the joint chain
        endJoint (str): child joint name of the joint chain
        upAxis (MVector): up axis of the joint chain (project direction to the plane)
        planeNormal (MVector, optional): rotate the joint chain to the plane with normal specified, otherwise use the
        aim vector of the joint chain as the plane normal
        negative (boolean, optional): project the joint chain to the plane with obtuse angle
    """
    # rotate joint with one axis to project it to plane with given normal
    startJointMatrix = om.MMatrix(cmds.getAttr('{0}.worldMatrix'.format(startJoint)))
    # get start joint world position
    startJointWs = om.MVector([startJointMatrix.getElement(3, index) for index in range(3)])
    # get end joint world position
    endJointMatrix = om.MMatrix(cmds.getAttr('{0}.worldMatrix'.format(endJoint)))
    endJointWs = om.MVector([endJointMatrix.getElement(3, index) for index in range(3)])
    # get world space up vector for start joint:
    startJointUpVec = upAxis * startJointMatrix
    # vector for joint chain
    aimVec = endJointWs - startJointWs

    if not planeNormal:
        planeNormal = aimVec

    # if the joint chain is perpendicular to the plane...
    if not startJointUpVec * planeNormal:
        axis = aimVec ^ startJointUpVec
        quaternion = om.MQuaternion()
        if negative:
            quaternion.setValue(axis, -math.pi / 2.0)
        else:
            quaternion.setValue(axis, math.pi / 2.0)
    else:
        d = aimVec * planeNormal / (startJointUpVec * planeNormal)
        # get the point projected to the plane
        p_ = endJointWs - d * startJointUpVec
        if negative:
            targetVec = -om.MVector(p_ - startJointWs)
        else:
            targetVec = om.MVector(p_ - startJointWs)
        axis = aimVec ^ targetVec
        quaternion = om.MQuaternion()
        quaternion.setValue(axis, targetVec.angle(aimVec))

    sel_list = om.MSelectionList()
    sel_list.add(startJoint)
    dagPath = sel_list.getDagPath(0)
    transformFn = om.MFnTransform(dagPath)
    transformFn.rotateBy(quaternion, om.MSpace.kWorld)       






# setUpNonFlipTwistJoint("upperarm_L", "lowerarm_L", "upper_joint_L", "upperarm_twist_base_L", upAxis = om.MVector(0, 0, 1))



def UI(*args):
    ### Window UI
    if cmds.window("twistJointUI", exists=True):
        cmds.deleteUI("twistJointUI", window=True)
    cmds.window("twistJointUI", title="Upper/Lower Twist Setup", s=True, rtf=True, height=250, width=290)
    cmds.columnLayout(adj=True)

    # Start Joint input
    cmds.text(label="Start Joint:")
    global start_joint_field
    start_joint_field = cmds.textField()

    # End Joint input
    cmds.text(label="End Joint:")
    global end_joint_field
    end_joint_field = cmds.textField()

    if start_joint_field and end_joint_field == None:
        print("Please input start and end joint")

    # Twist Joint Number Slider
    cmds.text(label="Number of Twist Joints:")

    global twist_joint_slider
    # twist_joint_slider = cmds.intSlider(min=1, max=5, value=3, step=1)
    twist_joint_slider = cmds.intSliderGrp( field=True, minValue=3, maxValue=5, fieldMinValue=3, fieldMaxValue=5, value = 3 )

    ### TwistAxis
    global twist_joint_ui
    twist_joint_ui = cmds.optionMenuGrp("twistAxisMenu", label="Twist Axis")
    for axis in twist_axis_vectors.keys():
        cmds.menuItem(label=axis)

    ### UpAxis
    global up_joint_ui
    up_joint_ui = cmds.optionMenuGrp("upAxisMenu", label="Up Axis")
    for axis in up_axis_vectors.keys():
        cmds.menuItem(label=axis)

    # counter twist joint or twist joint
    global counter_twist_checkbox
    counter_twist_checkbox = cmds.checkBox("counterTwistCheckbox", label="Counter Twist Joint")
    global twist_checkbox
    twist_checkbox = cmds.checkBox("twistCheckbox", label="Twist Joint")

    cmds.button(label="Set Up", c = check_and_setup_twist_joints)

    cmds.showWindow("twistJointUI")



if __name__ == "__main__":
    UI()






            