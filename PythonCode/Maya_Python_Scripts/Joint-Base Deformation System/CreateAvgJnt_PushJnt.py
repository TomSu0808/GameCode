import pymel.core as cmds
import maya.cmds as cmds

def getSelectJnt():
    select_nodes = cmds.ls(sl=True)
    if len(select_nodes) < 2:
        cmds.error("Please select 2 joints!")
        return
    return select_nodes
def createAvgJnt(weight=0.5):

    selected_nodes = getSelectJnt()

    source_node = selected_nodes[0]
    createAvgJnt = cmds.createNode("joint", name=source_node + "_AvgJnt")
    cmds.matchTransform(createAvgJnt, source_node, position=True, rotation=True)

    constraint_node = cmds.orientConstraint(selected_nodes, createAvgJnt, maintainOffset=False)[0]
    cmds.setAttr(constraint_node + ".interpType", 2)
    cmds.setAttr("{}.{}W0".format(constraint_node, source_node), weight)
    cmds.setAttr("{}.{}W1".format(constraint_node, selected_nodes[1]), 1 - weight)

    cmds.delete(constraint_node)
    # freeze the transformation
    cmds.makeIdentity(createAvgJnt, apply = True, translate = True, rotate = True, scale = True)

    cmds.parent(createAvgJnt, source_node)

    constraint_node = cmds.orientConstraint(selected_nodes, createAvgJnt, maintainOffset=False)[0]
    cmds.setAttr(constraint_node + ".interpType", 2)
    cmds.setAttr("{}.{}W0".format(constraint_node, source_node), weight)
    cmds.setAttr("{}.{}W1".format(constraint_node, selected_nodes[1]), 1 - weight)

    return createAvgJnt

def createPushJnt(avg_jnt, select_nodes, driver_axis = "y", distance_axis = "z", scale_axis = "x", driver_value = 60,
                  distance_value = -1, scale_value = 0.2):
    '''
    :param avg_jnt: average joint's name
    :param driver_axis: driver rotation axis
    :param distance_axis: pushing axis
    :param scale_axis: scale axis
    :param driver_value: driver rotation maximum value
    :param distance_value: maximum pushing value
    :param scale_value: maximum scaling value
    :return:
        push_jnt (str): push joint's name
    '''
    selectedNodes = select_nodes[0]
    createPushJnt = cmds.createNode("joint", name = selectedNodes + "_pushJnt")

    cmds.matchTransform(createPushJnt, avg_jnt, position = True, rotation = True)
    cmds.makeIdentity(createPushJnt, apply = True, translate = True, rotate = True, scale = True)
    cmds.parent(createPushJnt, avg_jnt)

    # adding remap value node to drive the push distance
    remap_dis = cmds.createNode("remapValue", name = "remap_pushJnt")
    # connect driver attr to remap node and set range
    cmds.connectAttr("{}.rotate{}".format(avg_jnt, driver_axis.upper()), remap_dis + ".inputValue")
    cmds.setAttr(remap_dis + ".inputMin", 0)
    cmds.setAttr(remap_dis + ".inputMax", driver_value)
    cmds.setAttr(remap_dis + ".outputMin", 0)
    cmds.setAttr(remap_dis + ".outputMax", distance_value)
    cmds.connectAttr(remap_dis + ".outValue", "{}.translate{}".format(createPushJnt, distance_axis.upper()))
    '''
    # adding remap value node to drive the scale
    remap_scale = cmds.createNode("remapValue", name="remap_pushJnt_scale")
    # connect driver attr to remap node and set range
    cmds.connectAttr("{}.scale{}".format(avg_jnt, driver_axis.upper()), remap_scale + ".inputValue")
    cmds.setAttr(remap_scale + ".inputMin", 0)
    cmds.setAttr(remap_scale + ".inputMax", driver_value)
    cmds.setAttr(remap_scale + ".outputMin", 1)
    cmds.setAttr(remap_scale + ".outputMax", scale_value)
    cmds.connectAttr(remap_scale + ".outValue", "{}.translate{}".format(createPushJnt, scale_axis.upper()))
    '''
    return createPushJnt



def codeAssmuble(*args):
    selected_nodes = getSelectJnt()

    avg_jnt = createAvgJnt(0.5)
    print("avg_jnt is :{}".format(avg_jnt))

    createPushJnt(avg_jnt = avg_jnt, select_nodes = selected_nodes, driver_axis = "y", distance_axis = "z", scale_axis = "x", driver_value = 60,
                  distance_value = -1, scale_value = 0.2)

def UI(*args):
    if cmds.window("Add Avg/Push Joints", exists = True):
        cmds.deleteUI("Add Avg/Push Joints", window = True)

    cmds.window(title = "Add Avg/Push Joints", s=True, rtf=True, widthHeight=(300,100))
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(label="Select joint and create Avg/Push Joint.")

    cmds.button(label="Create", c = codeAssmuble)

    cmds.showWindow()

if __name__ == "__main__":
    UI()