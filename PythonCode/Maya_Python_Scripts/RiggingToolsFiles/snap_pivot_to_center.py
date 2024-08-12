import maya.cmds as cmds

def snap_to_pivot():
    select_node = cmds.ls(selection=True, flatten=True)
    
    if not select_node or len(select_node) < 2:
        cmds.warning("Please select at least one object")
        return
    
    driver_nodes = select_node[:-1]
    driven_nodes = select_node[-1]
    
    drivers_x = []
    drivers_y = []
    drivers_z = []
    
    for driver in driver_nodes:
        driver_pos = cmds.xform(driver, query=True, worldSpace=True, translation=True)
        drivers_x.append(driver_pos[0])
        drivers_y.append(driver_pos[1])
        drivers_z.append(driver_pos[2])
        
    max_x = max(drivers_x)
    min_x = min(drivers_x)
    
    max_y = max(drivers_y)
    min_y = min(drivers_y)
    
    max_z = max(drivers_z)
    min_z = min(drivers_z)
    
    pos_x = 0.5 * (max_x + min_x)
    pos_y = 0.5 * (max_y + min_y)
    pos_z = 0.5 * (max_z + min_z)
    
    cmds.xform(driven_nodes, worldSpace=True, translation=[pos_x, pos_y, pos_z], ws=True)

def create_ui():
    if cmds.window("snapPivotWindow", exists=True):
        cmds.deleteUI("snapPivotWindow")
    
    window = cmds.window("snapPivotWindow", title="Snap Tool", sizeable = False, widthHeight=(260, 80))
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(label="Select multiple objects, then click:")
    cmds.button(label="Snap to Pivot", command=lambda x: snap_to_pivot())
    cmds.showWindow(window)

create_ui()
