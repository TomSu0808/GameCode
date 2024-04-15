import maya.cmds as cmds
import maya.mel as mel
from PySide2 import QtWidgets, QtCore


class generate_grp():

    ### card mesh windows
    def generate_mesh_grp_window(self):
        if cmds.window("mesh_window", exists=True):
            cmds.deleteUI("mesh_window", window=True)

        cmds.window( "mesh_windowd", title = "Choose Nodel Type - Card", widthHeight=(320, 50 ))
        cmds.columnLayout(adjustableColumn=True)
        cmds.button(label="Generate Group Node", c = generate_grp.curve_to_card_mesh_grp)
        cmds.button(label="Generate Single Node", c = generate_grp.curve_to_card_mesh_single)
        cmds.showWindow()

    ### Generator grp sweep Mesh
    def curve_to_card_mesh_grp(self):
        select_object = cmds.ls(selection=True)

        if select_object:
            mel.eval("sweepMeshFromCurve -oneNodePerCurve 1;")
            all_sweep_creators = cmds.ls(type="sweepMeshCreator")
            
            for creator in all_sweep_creators:
                cmds.setAttr(creator + ".sweepProfileType", 2)

        get_object_name = [f"sweep{i}" for i in range(1, 10000)]
        object_to_group = [obj for obj in get_object_name if cmds.objExists(obj)]

        if object_to_group:
            cmds.group(em = True, name="Mesh_Group")
            cmds.parent(object_to_group, "Mesh_Group")

    ### Generator single sweep Mesh
    def curve_to_card_mesh_single(self):
        select_object = cmds.ls(selection=True)

        if select_object:
            mel.eval("sweepMeshFromCurve -oneNodePerCurve 0;")
            all_sweep_creators = cmds.ls(type="sweepMeshCreator")
            
            for creator in all_sweep_creators:
                cmds.setAttr(creator + ".sweepProfileType", 2)

        get_object_name = [f"sweep{i}" for i in range(1, 10000)]
        object_to_group = [obj for obj in get_object_name if cmds.objExists(obj)]

        if object_to_group:
            cmds.group(em = True, name="Mesh_Group")
            cmds.parent(object_to_group, "Mesh_Group")

    ### arc mesh windows
    def generate_arc_mesh_grp_window(self):
        if cmds.window("arc_window", exists=True):
            cmds.deleteUI("arc_window", window=True)

        cmds.window( "arc_window", title = "Choose Node Type - Arc", widthHeight=(320, 50 ))
        cmds.columnLayout(adjustableColumn=True)
        cmds.button(label="Generate Group Node", c = generate_grp.curve_to_arc_mesh_grp)
        cmds.button(label="Generate Single Node", c = generate_grp.curve_to_arc_mesh_single)
        cmds.showWindow()

    ### Generator grp sweep Arc Mesh
    def curve_to_arc_mesh_grp(self):
        select_object = cmds.ls(selection=True)

        if select_object:
            mel.eval("sweepMeshFromCurve -oneNodePerCurve 1;")
            all_sweep_creators = cmds.ls(type="sweepMeshCreator")
            
            for creator in all_sweep_creators:
                cmds.setAttr(creator + ".sweepProfileType", 3)

        get_object_name = [f"sweep{i}" for i in range(1, 10000)]
        object_to_group = [obj for obj in get_object_name if cmds.objExists(obj)]

        if object_to_group:
            cmds.group(em = True, name="Mesh_Group")
            cmds.parent(object_to_group, "Mesh_Group")

    ### Generator single sweep Arc Mesh
    def curve_to_arc_mesh_single(self):
        select_object = cmds.ls(selection=True)

        if select_object:
            mel.eval("sweepMeshFromCurve -oneNodePerCurve 0;")
            all_sweep_creators = cmds.ls(type="sweepMeshCreator")
            
            for creator in all_sweep_creators:
                cmds.setAttr(creator + ".sweepProfileType", 3)

        get_object_name = [f"sweep{i}" for i in range(1, 10000)]
        object_to_group = [obj for obj in get_object_name if cmds.objExists(obj)]

        if object_to_group:
            cmds.group(em = True, name="Mesh_Group")
            cmds.parent(object_to_group, "Mesh_Group")
    
    
    
###Visible
def visible(*args):
    selected_objects = cmds.ls(sl=True)
    
    for obj in selected_objects:
        
        is_visible = cmds.getAttr(obj + '.visibility')
        cmds.setAttr(obj + '.visibility', not is_visible)

### Center Pivot
def center_pivot(*args):
    selected_objects = cmds.ls(sl=True)
    
    for obj in selected_objects:
        cmds.xform(obj, centerPivots = True)

### flip normal
def flip_normals():
    selected_objects = cmds.ls(sl=True)
    
    for obj in selected_objects:
        cmds.polyNormal(obj, normalMode=0, userNormalMode=0, ch=1)


######### change vertex number
def get_curve_vertex_count(curve):
    
    shape = cmds.listRelatives(curve, shapes=True, Type = True)[0]
    vertex_count = cmds.getAttr(shape + '.controlPoints', size=True)
    return vertex_count

def rebuild_curve(curve, vertex_count):

    cmds.rebuildCurve(curve, rt=0, s=vertex_count)

###################################
### Change Vertex Number
def update_vertex_count(*args):
    
    vertex_count = cmds.intSliderGrp(vertex_count_slider, query=True, value=True)
    
    selection = cmds.ls(selection=True)
    if selection:
        curve = selection[0]
        rebuild_curve(curve, vertex_count -1) 

### Convert Edge to Curve
def convert_edge_to_curve(*args):
    selection = cmds.ls(selection=True)
    if selection:
        poly_to_mesh = cmds.polyToCurve(form=2, degree=1, conformToSmoothMeshPreview=1)
        cmds.xform(poly_to_mesh, centerPivots = True)



### Plane Card Transformation Grp
class plane_mesh_transform():
    ### Change Plane Width
    def get_nodes_in_history_by_type(typ, selection):
        nodes = []
        for obj in selection:
            for node in cmds.listHistory(obj):
                if cmds.nodeType(node) == typ:
                    nodes.append(node)
        return nodes

    ### Change Plane Width
    def update_plane_objectW(*args):
        select_object = cmds.ls(selection=True)

        width_value = cmds.floatSliderGrp(scale_plane_W, query=True, value=True)
        nodes = plane_mesh_transform.get_nodes_in_history_by_type('sweepMeshCreator', select_object)
        cmds.setAttr(nodes[0] + '.scaleProfileX', width_value)

        
    ### Change Plane Rotate
    def update_plane_rotate(*args):
        select_object = cmds.ls(selection=True)
        
        rotate_value = cmds.intSliderGrp(rotate_plane_object, query=True, value=True)
        nodes = plane_mesh_transform.get_nodes_in_history_by_type('sweepMeshCreator', select_object)
        cmds.setAttr(nodes[0] + ' .rotateProfile', rotate_value)

    ### Change Twist
    def update_plane_twist(*args):
        select_object = cmds.ls(selection=True)
        
        twist_value = cmds.floatSliderGrp(twist_plane_object, query=True, value=True)
        nodes = plane_mesh_transform.get_nodes_in_history_by_type('sweepMeshCreator', select_object)
        cmds.setAttr(nodes[0] + ' .twist', twist_value)

    ### Change Subdivision
    def modify_plane_subdivision(*args):
        select_object = cmds.ls(selection=True)
        
        subdivision_value = cmds.intSliderGrp(add_plane_subdivision, query=True, value=True)
        nodes = plane_mesh_transform.get_nodes_in_history_by_type('sweepMeshCreator', select_object)
        cmds.setAttr(nodes[0] + '.interpolationPrecision', subdivision_value)

###################################
### Arc Transformation Grp
class arc_mesh_transform():
    def get_nodes_in_history_by_type(typ, selection):
        nodes = []
        for obj in selection:
            for node in cmds.listHistory(obj):
                if cmds.nodeType(node) == typ:
                    nodes.append(node)
        return nodes
    
    def update_arc_objectW(*args):
        select_object = cmds.ls(selection=True)

        width_value = cmds.floatSliderGrp(scale_arc_W, query=True, value=True)
        nodes = arc_mesh_transform.get_nodes_in_history_by_type('sweepMeshCreator', select_object)
        cmds.setAttr(nodes[0] + '.scaleProfileX', width_value)

        
    ### Change Arc Rotate
    def update_arc_rotate(*args):
        select_object = cmds.ls(selection=True)
        
        rotate_value = cmds.intSliderGrp(rotate_arc_object, query=True, value=True)
        nodes = arc_mesh_transform.get_nodes_in_history_by_type('sweepMeshCreator', select_object)
        cmds.setAttr(nodes[0] + ' .rotateProfile', rotate_value)

    ### Change Arc Twist
    def update_arc_twist(*args):
        select_object = cmds.ls(selection=True)
        
        twist_value = cmds.floatSliderGrp(twist_arc_object, query=True, value=True)
        nodes = arc_mesh_transform.get_nodes_in_history_by_type('sweepMeshCreator', select_object)
        cmds.setAttr(nodes[0] + ' .twist', twist_value)

    ### Change Arc Angle
    def update_arc_angle(*args):
        select_object = cmds.ls(selection=True)
        
        angle_value = cmds.intSliderGrp(angle_arc_object, query=True, value=True)
        nodes = arc_mesh_transform.get_nodes_in_history_by_type('sweepMeshCreator', select_object)
        cmds.setAttr(nodes[0] + ' .profileArcAngle', angle_value)

    ### Change Arc Segments
    def update_arc_segment(*args):
        select_object = cmds.ls(selection=True)
        
        segments_value = cmds.intSliderGrp(segments_arc_object, query=True, value=True)
        nodes = arc_mesh_transform.get_nodes_in_history_by_type('sweepMeshCreator', select_object)
        cmds.setAttr(nodes[0] + ' .profileArcSegments', segments_value)
           
### create new layer 
def create_dialog_window():
    result = cmds.promptDialog(
		title='New Layer',
		message='Enter Layer Name:',

		button=['OK', 'Cancel'],
		defaultButton='OK',
		cancelButton='Cancel',
		dismissString='Cancel')

    if result == 'OK':
        text = cmds.promptDialog(query=True, text=True)

        if cmds.objExists(text):
            cmds.warning("Layer already exists")
            return
        else:
            cmds.createDisplayLayer(name = text, empty = True)
        
        select_objects = cmds.ls(selection = True)

        if select_objects:
            cmds.editDisplayLayerMembers(text, select_objects)

### Mirror Curve
def mirror_curve(*args):
    select_curve = cmds.ls(selection = 1)

    curve_to_mirror = select_curve[0]

    mirror_object = cmds.duplicate(curve_to_mirror, name = curve_to_mirror + "_mirror_object")[0]
    cmds.scale(-1, 1, 1, mirror_object)

############# UI Window #############   
class UI_GRP():
    def UI():  
        if cmds.window("Window", exists=True):
            cmds.deleteUI("Window", window=True)

        window = cmds.window("Window", title="Tom's Hair Tool", widthHeight=(300, 800))
        cmds.columnLayout(adjustableColumn=True)

        cmds.text(label="Card Hair Editor", font = "boldLabelFont")
        cmds.separator(h=5, style="none")
        
        ########### window 1
        cmds.columnLayout("window", adjustableColumn=True, rs=5)
        cmds.frameLayout ("layoutFrame01", label = "Speed Tool", collapsable = True, borderVisible=0, parent = "window")

        cmds.separator(h=1, style="none")

        cmds.button(label="Visible", c = visible)
        
        cmds.button(label = "Center Pivot", c = "center_pivot()" )
        
        cmds.button(label = "Revert Face", command = "flip_normals()")
        
        melScript = """
        button -label "UV Editor" 
        -width 100 -height 25 
        -command "TextureViewWindow";
        """
        mel.eval(melScript)

        ### Layer Button
        cmds.button(label = "Create Layer", c= "create_dialog_window()")

        cmds.separator(h=1, style="none")

        ########### window 2
        cmds.frameLayout ("layoutFrame02", label = "Plane Mesh Tool", collapsable = True, borderVisible=0, parent = "window")

        cmds.separator(h=1, style="none")

        cmds.button(label = "Generate Plane Mesh", command = generate_grp.generate_mesh_grp_window, width=300, height=40)
        ###
        global scale_plane_W
        scale_plane_W = cmds.floatSliderGrp(label="Width", field=True, minValue=1.0, maxValue=3.0, fieldMinValue=0, fieldMaxValue=0, value=0, dc=plane_mesh_transform.update_plane_objectW)

        global rotate_plane_object
        rotate_plane_object = cmds.intSliderGrp(label="Rotate", field=True, minValue=-180, maxValue=180, value=0,dc=plane_mesh_transform.update_plane_rotate)

        global twist_plane_object
        twist_plane_object = cmds.floatSliderGrp(label="Twist", field=True, minValue=-1, maxValue=1, value=0 , dc=plane_mesh_transform.update_plane_twist)

        global add_plane_subdivision 
        add_plane_subdivision = cmds.intSliderGrp(label="Subdivision Face", field=True, minValue=50, maxValue=100, value=90, dc=plane_mesh_transform.modify_plane_subdivision)


        ########### window 3
        cmds.frameLayout ("layoutFrame03", label = "Arc Mesh Tool", collapsable = True, borderVisible=0, parent = "window")
        cmds.separator(h=1, style="none")
        cmds.button(label = "Generate Arc Mesh", command = generate_grp.generate_arc_mesh_grp_window, width=300, height=40)

        ###
        global angle_arc_object
        angle_arc_object = cmds.intSliderGrp(label = "Angle", field = True, minValue = 0, maxValue = 360, value = 0, dc = arc_mesh_transform.update_arc_angle )

        global segments_arc_object
        segments_arc_object = cmds.intSliderGrp(label = "Segments", field = True, minValue = 1, maxValue = 20, value = 0, dc = arc_mesh_transform.update_arc_segment )

        global scale_arc_W
        scale_arc_W = cmds.floatSliderGrp(label="Width", field=True, minValue=1.0, maxValue=3.0, fieldMinValue=0, fieldMaxValue=0, value=0, dc=arc_mesh_transform.update_arc_objectW)

        global rotate_arc_object
        rotate_arc_object = cmds.intSliderGrp(label="Rotate", field=True, minValue=-180, maxValue=180, value=0,dc=arc_mesh_transform.update_arc_rotate)

        global twist_arc_object
        twist_arc_object = cmds.floatSliderGrp(label="Twist", field=True, minValue=-1, maxValue=1, value=0 , dc=arc_mesh_transform.update_arc_twist)

        ##### window 4
        cmds.frameLayout ("layoutFrame04", label = "Curve Tool", collapsable = True, borderVisible=0, parent = "window")

        cmds.text("Regenerate Vertax", font = "boldLabelFont", al="center")

        global vertex_count_slider
        vertex_count_slider = cmds.intSliderGrp(label="Vertex Number", field=True, minValue=2, maxValue=20, value=1)

        cmds.button(label="Add Vertex", c = update_vertex_count)

        cmds.button(label="Convert Edge to Curve", c = convert_edge_to_curve)

        cmds.button(label = "Mirror Curve", c = mirror_curve)

        cmds.showWindow("Window")
    UI()



