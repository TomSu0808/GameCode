from __future__ import absolute_import, division, print_function
from builtins import ascii, bytes, chr, dict, filter, hex, input, int, map, next, oct, open, pow, range, round, str, super, zip
from builtins import object as builtin_object
import random as rand
import colorsys as csys
import sys
import pymel.core as pmc                    
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma

class ProxyMeshesCreator(builtin_object):
    
    @classmethod
    def showUI(cls):
        win = cls()
        win.create()
        return win
        
    def __init__(self):
        super(ProxyMeshesCreator, self).__init__()
        self.win_name = 'PMCwindow'
        self.win_title = 'Proxy Meshes Creator'
        self.input_mesh = []
        self.hierarchy_scroll_list = []
        self.flat_scroll_list = []
        self.color_map = {}
        self.lookup_table = {}
        self.reset_joint = []
        self.symmetry_axis = {1:0, 2:1, 3:2}
        self.symmetry_conversion = {1:[-1, 1, 1], 2:[1, -1, 1], 3:[1, 1, -1]}
        self.symmetry_option = {1:1, 2:-1}
        self.symmetry_map = {}
        self.inMesh_source_plug = []
        self.display_colors_flag = False
        self.color_sets = []
        self.current_color_set = []
    
    def cleaning_command(self):
        if self.input_mesh:
            input_mesh_node = self.get_depend_node(self.input_mesh)
            inMesh_plug = om.MFnDependencyNode(input_mesh_node).findPlug('inMesh', False)
            current_inMesh_source_plug = inMesh_plug.source()
            if not current_inMesh_source_plug.isNull:
                if not current_inMesh_source_plug == self.inMesh_source_plug:
                    source_node = current_inMesh_source_plug.node()
                    om.MDGModifier().connect(self.inMesh_source_plug, inMesh_plug)
                    pmc.delete(om.MFnDependencyNode(source_node).name())
            
            self.input_mesh.displayColors.set(self.display_colors_flag)
            
            actual_color_sets = pmc.polyColorSet(self.input_mesh, query=True, allColorSets=True)
            if actual_color_sets is not None:
                if not actual_color_sets == self.color_sets:
                    for item in actual_color_sets:
                        if not item in self.color_sets:
                            pmc.polyColorSet(self.input_mesh, edit=True, colorSet=item, delete=True)
                if self.current_color_set:
                    pmc.polyColorSet(self.input_mesh, edit=True, colorSet=self.current_color_set[0], currentColorSet=True)
    
    def create(self):
        if(pmc.window(self.win_name, exists=True)):
            pmc.deleteUI(self.win_name, window=True)
        pmc.window(self.win_name, title=self.win_title, resizeToFitChildren=True, sizeable=False, closeCommand=self.cleaning_command)
        
        self.mainForm = pmc.formLayout(numberOfDivisions=100)
        self.winTabs = pmc.tabLayout(parent=self.mainForm, innerMarginWidth=5, innerMarginHeight=5)
        pmc.formLayout(self.mainForm, edit=True,
            attachForm=([self.winTabs, 'left', 0], [self.winTabs, 'top', 0]))
        
        self.createForm = pmc.formLayout(parent=self.winTabs, numberOfDivisions=100)
        self.mirrorForm = pmc.formLayout(parent=self.winTabs, numberOfDivisions=100)
        pmc.tabLayout(self.winTabs, edit=True, tabLabel=([self.createForm, 'Create'], [self.mirrorForm, 'Mirror']))
        
        self.meshGroup = pmc.textFieldButtonGrp(parent=self.createForm, label='Mesh:', buttonLabel='   <<<   ', placeholderText='- input mesh -', adjustableColumn=2, columnAttach3=['left', 'left', 'left'], columnWidth3=[40, 100, 100], columnOffset3=[2, 10, 10], annotation='Select a polygon geometry from which to extract proxy meshes', changeCommand=self.mesh_field_command, buttonCommand=self.mesh_button_command)
        self.initialGuess = pmc.radioButtonGrp(parent=self.createForm, numberOfRadioButtons=2, label='Initial Guess:    ', labelArray2=['closest distance', 'from skinCluster'], select=1, columnWidth3=[80, 120, 120])
        self.proxyJointsButton = pmc.button(parent=self.createForm, label='Select Proxy Joints', width=150, annotation='Store the selected joints in the Proxy Joints scroll list and build a color map based on the Initial Guess method', command=self.select_proxy_joints_command)
        self.colorMapButton = pmc.button(parent=self.createForm, label='Reset Color Map', width=150, annotation='Build a new color map based on the Initial Guess method', command=self.reset_color_map_command)
        self.proxyJointsSort = pmc.radioButtonGrp(parent=self.createForm, numberOfRadioButtons=3, label='Sort:    ', labelArray3=['alphabetically', 'by hierarchy', 'flat'], select=2, columnWidth4=[40, 120, 120, 120], changeCommand=self.sort_command)
        self.proxyJointsList = pmc.textScrollList(parent=self.createForm, allowMultiSelection=False, numberOfRows=1, height=235, selectCommand=self.highlight_selection)
        self.mirrorButton = pmc.button(parent=self.createForm, label='Mirror Color Map', width=150, command=self.mirror_color_map_command)
        self.paintFacesButton = pmc.button(parent=self.createForm, label='Paint Selected Faces', width=150, annotation='Associate input faces to the selected Proxy Joint in the scroll list', command=self.paint_faces_command)
        self.buildProxyButton = pmc.button(parent=self.createForm, label='Build Proxy Meshes', width=150, annotation='Create Proxy Meshes for the input geometry, according to the existing color map', command=self.build_proxy_meshes_command)
        self.constrainProxyButton = pmc.button(parent=self.createForm, label='Constrain Proxy Meshes', width=150, annotation='Constrain Proxy Meshes to Proxy Joints if nothing is selected. Otherwise constrain targets to objects in order of selection (object1, object2 ... objectN, target1, target2 ... targetN)', command=self.constrain_proxy_command)
        pmc.formLayout(self.createForm, edit=True,
            attachForm=([self.meshGroup, 'left', 10], [self.meshGroup, 'top', 10], [self.meshGroup, 'right', 10], [self.initialGuess, 'left', 10], [self.proxyJointsButton, 'left', 50], [self.colorMapButton, 'right', 50], [self.proxyJointsSort, 'left', 10], [self.proxyJointsList, 'left', 10], [self.proxyJointsList, 'right', 10], [self.paintFacesButton, 'left', 50], [self.mirrorButton, 'right', 50], [self.buildProxyButton, 'left', 135], [self.constrainProxyButton, 'left', 135], [self.constrainProxyButton, 'bottom', 10]),
            attachControl=([self.initialGuess, 'top', 10, self.meshGroup], [self.proxyJointsButton, 'top', 10, self.initialGuess], [self.colorMapButton, 'left', 25, self.proxyJointsButton], [self.colorMapButton, 'top', 10, self.initialGuess], [self.proxyJointsSort, 'top', 10, self.proxyJointsButton], [self.proxyJointsList, 'top', 1, self.proxyJointsSort], [self.paintFacesButton, 'top', 12, self.proxyJointsList], [self.mirrorButton, 'left', 25, self.paintFacesButton], [self.mirrorButton, 'top', 12, self.proxyJointsList], [self.buildProxyButton, 'top', 12, self.mirrorButton], [self.constrainProxyButton, 'top', 12, self.buildProxyButton]))
        
        self.symmetryMatchesText = pmc.text(parent=self.mirrorForm, label='Symmetry Pairs:    Source    ->    Destination')
        self.symmetryMatchesList = pmc.textScrollList(parent=self.mirrorForm, allowMultiSelection=False, numberOfRows=1, height=137)
        self.selfMatchesText = pmc.text(parent=self.mirrorForm, label='Independent Joints:    ( ->    Self )')
        self.selfMatchesList = pmc.textScrollList(parent=self.mirrorForm, allowMultiSelection=False, numberOfRows=1, height=137)
        self.connectButton = pmc.button(parent=self.mirrorForm, label='Connect', width=150, annotation='Connect two items from the Self-Matched Joints list', command=self.connect_command)
        self.disconnectButton = pmc.button(parent=self.mirrorForm, label='Disconnect', width=150, annotation='Disconnect one macth from the Symmetry Matches list', command=self.disconnect_command)
        self.symmetryDirection = pmc.radioButtonGrp(parent=self.mirrorForm, numberOfRadioButtons=2, label='Direction:    ', labelArray2=['from positive to negative', 'from negative to positive'], select=1, columnWidth3=[65, 160, 160], changeCommand=self.mirror_direction_command)
        self.symmetryPlane = pmc.radioButtonGrp(parent=self.mirrorForm, numberOfRadioButtons=3, label='Symmetry Plane:    ', labelArray3=['YZ', 'XZ', 'XY'], select=1, columnWidth4=[97, 50, 50, 50], changeCommand=self.symmetry_plane_command)
        self.mirrorBisButton = pmc.button(parent=self.mirrorForm, label='Mirror Color Map', width=150, command=self.mirror_color_map_command)
        pmc.formLayout(self.mirrorForm, edit=True,
            attachForm=([self.symmetryMatchesText, 'left', 90], [self.symmetryMatchesText, 'top', 10], [self.symmetryMatchesList, 'left', 10], [self.symmetryMatchesList, 'right', 10],[self.selfMatchesText, 'left', 115], [self.selfMatchesList, 'left', 10], [self.selfMatchesList, 'right', 10], [self.connectButton, 'left', 50], [self.disconnectButton, 'right', 50], [self.symmetryDirection, 'left', 10], [self.symmetryPlane, 'left', 10], [self.mirrorBisButton, 'left', 135], [self.mirrorBisButton, 'bottom', 10]),
            attachControl=([self.symmetryMatchesList, 'top', 10, self.symmetryMatchesText], [self.selfMatchesText, 'top', 10, self.symmetryMatchesList], [self.selfMatchesList, 'top', 10, self.selfMatchesText], [self.connectButton, 'top', 12, self.selfMatchesList], [self.disconnectButton, 'left', 25, self.connectButton], [self.disconnectButton, 'top', 12, self.selfMatchesList], [self.symmetryDirection, 'top', 10, self.connectButton], [self.symmetryPlane, 'top', 10, self.symmetryDirection], [self.mirrorBisButton, 'top', 10, self.symmetryPlane]))
        
        pmc.showWindow()
    
    def get_target_shape(self, target):
        target_shape = None
        
        if pmc.objExists(target):
            sel_list = pmc.ls(target)
            shape_list = pmc.listRelatives(sel_list[0], shapes=True, path=True, noIntermediate=True)
            if shape_list:
                target_shape = shape_list[0]
            else:
                target_shape = sel_list[0]
                
        return target_shape
        
    def get_dag_path(self, target):
        sel_list = om.MSelectionList()
        sel_list.add(str(target))            
        target_path = sel_list.getDagPath(0)
        
        return target_path
        
    def get_depend_node(self, target):
        sel_list = om.MSelectionList()
        sel_list.add(str(target))
        target_node = sel_list.getDependNode(0)
        
        return target_node
        
    def is_a_mesh(self, target_shape):
        return_value = False

        target_type = pmc.objectType(target_shape)
        if target_type == 'mesh':
            return_value = True
                
        return return_value
    
    def hierarchy_counter(self, target, picklist):
        counter = 0
        parent_list = pmc.listRelatives(target, parent=True, path=True)
        while parent_list:
            parent_item = parent_list[0]
            if parent_item in picklist:
                counter += 1
            parent_list = pmc.listRelatives(parent_item, parent=True, path=True)
        return counter
        
    def sort_by_hierarchy(self, proxy_joints, padding=0, flat=False):        
        hierarchy_counter_list = [self.hierarchy_counter(prx_jnt, proxy_joints) for prx_jnt in proxy_joints]
        hierarchy_top = min(hierarchy_counter_list)
        top_proxy_joints = [proxy_joints[index] for index in range(0, len(proxy_joints)) if hierarchy_counter_list[index] == hierarchy_top]
        top_proxy_joints.sort()
        for item in top_proxy_joints:
            if flat:
                list_entry = str(item)
                self.hierarchy_scroll_list.append(list_entry.rjust(len(str(item))+padding*4, ' '))
                self.flat_scroll_list.append(list_entry)
            else:
                list_entry = str(item).rjust(len(str(item))+padding*4, ' ')
                self.hierarchy_scroll_list.append(list_entry)
                self.flat_scroll_list.append(list_entry.strip())
            pmc.textScrollList(self.proxyJointsList, edit=True, append=list_entry)
            children_list = pmc.listRelatives(item, allDescendents=True, type='joint')
            proxy_joints_children = [token for token in children_list if token in proxy_joints]
            if proxy_joints_children:
                self.sort_by_hierarchy(proxy_joints_children, padding+1, flat)

    def sort_routine(self, sort_order, proxy_joints):
        if sort_order == 1:      # alphabetically
            proxy_joints.sort()
            for item in proxy_joints:
                pmc.textScrollList(self.proxyJointsList, edit=True, append=str(item))
        elif sort_order == 2:    # by hierarchy
            if self.hierarchy_scroll_list:
                for item in self.hierarchy_scroll_list:
                    pmc.textScrollList(self.proxyJointsList, edit=True, append=str(item))
            else:
                self.sort_by_hierarchy(proxy_joints, padding=0, flat=False)
        elif sort_order == 3:    # flat
            if self.flat_scroll_list:
                for item in self.flat_scroll_list:
                    pmc.textScrollList(self.proxyJointsList, edit=True, append=str(item))
            else:
                self.sort_by_hierarchy(proxy_joints, padding=0, flat=True)
                    
    def build_color_map(self):
        # preliminary operations
        input_mesh_path = self.get_dag_path(self.input_mesh)
        
        faces_num = pmc.polyEvaluate(self.input_mesh, face=True)
        faces_ID = om.MIntArray(range(0, faces_num))
        vtx_num = pmc.polyEvaluate(self.input_mesh, vertex=True)
        vtx_ID = om.MIntArray(range(0, vtx_num))
        
        proxy_joints_raw = pmc.textScrollList(self.proxyJointsList, query=True, allItems=True)
        proxy_joints_name = [joint_token.strip() for joint_token in proxy_joints_raw]
        proxy_joints = pmc.ls(proxy_joints_name)
        
        face_component_fnSet = om.MFnSingleIndexedComponent()
        face_component = face_component_fnSet.create(om.MFn.kMeshPolygonComponent)
        face_component_fnSet.addElements(faces_ID)
        faces_iterator = om.MItMeshPolygon(input_mesh_path, face_component)
        
        init_guess = pmc.radioButtonGrp(self.initialGuess, query=True, select=True)
        
        if init_guess == 1:    # closest distance
            faces_center = om.MPointArray()
            while not faces_iterator.isDone():
                faces_center.append(faces_iterator.center(om.MSpace.kWorld))
                try:
                    faces_iterator.next()
                except:
                    faces_iterator.next(None)
            
            proxy_joints_positions = om.MPointArray()
            for proxy_joint in proxy_joints:
                proxy_joint_position = om.MPoint(proxy_joint.getTranslation('world'))
                proxy_joints_positions.append(proxy_joint_position)
                
        elif init_guess == 2:    # from skinCluster
            input_mesh_history = pmc.listHistory(self.input_mesh)
            input_mesh_skinCluster = pmc.ls(input_mesh_history, type='skinCluster')
            if not input_mesh_skinCluster:
                pmc.warning('The selected mesh is not affected by a skinCluster. Choose another Initial Guess method')
                return
            
            skinCluster_node = self.get_depend_node(input_mesh_skinCluster[0])
            skinCluster_fnSet = oma.MFnSkinCluster(skinCluster_node)
            skinCluster_influences = skinCluster_fnSet.influenceObjects()
            skinCluster_influences_name = [om.MFnDagNode(skin_inf.node()).name() for skin_inf in skinCluster_influences]
            skinCluster_influences_index = om.MIntArray()
            for skin_inf in skinCluster_influences:
                skinCluster_influences_index.append(skinCluster_fnSet.indexForInfluenceObject(skin_inf))
            influences_num = len(skinCluster_influences_name)
            for prx_jnt in proxy_joints_name:
                if not prx_jnt in skinCluster_influences_name:
                    pmc.warning('Joint {jnt_name} is not an influence of skinCluster'.format(jnt_name=prx_jnt))
            
            vtx_component_fnSet = om.MFnSingleIndexedComponent()
            vtx_component = vtx_component_fnSet.create(om.MFn.kMeshVertComponent)
            vtx_component_fnSet.addElements(vtx_ID)
            vtx_skinWeights = skinCluster_fnSet.getWeights(input_mesh_path, vtx_component, skinCluster_influences_index)
            
            vtx_influence_map = {}
            for id in vtx_ID:
                vtx_weights = [wgt for wgt in vtx_skinWeights[id*influences_num:(id*influences_num)+influences_num]]
                max_weight = max(vtx_weights)
                max_influence = skinCluster_influences_name[vtx_weights.index(max_weight)]
                vtx_influence_map.setdefault(id, (max_influence, max_weight))

        # building color map
        joints_num = len(proxy_joints)
        h_step = 1/joints_num
        h_value = [h_step*counter for counter in range(0, joints_num)]
        rand.shuffle(h_value)
        self.color_map = {proxy_joints_name[counter]:{'color':om.MColor(csys.hls_to_rgb(h_value[counter], rand.uniform(0.3, 0.6), rand.uniform(0.3, 0.8))), 'faces_ID':[]} for counter in range(0, joints_num)}
        self.color_map.setdefault('void',{'color':om.MColor([0, 0, 0]), 'faces_ID':[]})
        faces_color = om.MColorArray()
        self.lookup_table = {}
        
        if init_guess == 1:         # closest distance
            for face_index, face_center in enumerate(faces_center):
                face_to_joint_distances = [face_center.distanceTo(prx_jnt_pos) for prx_jnt_pos in proxy_joints_positions]
                closest_distance = min(face_to_joint_distances)
                closest_joint = face_to_joint_distances.index(closest_distance)
                self.color_map[proxy_joints_name[closest_joint]]['faces_ID'].append(face_index)
                faces_color.append(self.color_map[proxy_joints_name[closest_joint]]['color'])
                self.lookup_table.setdefault(face_index, proxy_joints_name[closest_joint])
        
        elif init_guess == 2:       # from skinCluster
            while not faces_iterator.isDone():
                face_vtx = faces_iterator.getVertices()
                face_vtx_influences = [vtx_influence_map[index][0] for index in face_vtx]
                influences_filter = list(set(face_vtx_influences))
                influences_rate = [face_vtx_influences.count(inf_item) for inf_item in influences_filter]
                max_rate = max(influences_rate)
                major_influences_num = influences_rate.count(max_rate)
                if major_influences_num == 1:                 # there is only one influence per face with max rate
                    major_influences_id = influences_rate.index(max_rate)
                    face_influence = influences_filter[major_influences_id]
                else:                                         # there is more than one influence per face with max rate
                    major_influences_id = [index for index in range(0, major_influences_num) if influences_rate[index] == max_rate]
                    major_influences_face_vtx = [face_vtx_influences.index(influences_filter[index]) for index in major_influences_id]
                    major_influences_weight = [vtx_influence_map[face_vtx[index]][1] for index in major_influences_face_vtx]
                    max_weight = max(major_influences_weight)
                    major_influence = major_influences_id[major_influences_weight.index(max_weight)]
                    face_influence = influences_filter[major_influence]
                if face_influence in proxy_joints_name:
                    self.color_map[face_influence]['faces_ID'].append(faces_iterator.index())
                    faces_color.append(self.color_map[face_influence]['color'])
                    self.lookup_table.setdefault(faces_iterator.index(), face_influence)
                else:
                    self.color_map['void']['faces_ID'].append(faces_iterator.index())
                    faces_color.append(self.color_map['void']['color'])
                    self.lookup_table.setdefault(faces_iterator.index(), 'void')
                try:
                    faces_iterator.next()
                except:
                    faces_iterator.next(None)
                
        # applying color map
        input_mesh_fnSet = om.MFnMesh(input_mesh_path)
        input_mesh_fnSet.setFaceColors(faces_color, faces_ID)
        self.input_mesh.displayColors.set(True)
        if self.color_map['void']['faces_ID']:
            pmc.warning('Faces assigned to influences not listed in the Proxy Joints scroll list will be painted black')
        
    def highlight_selection(self):
        selected_joint_raw = pmc.textScrollList(self.proxyJointsList, query=True, selectItem=True)
        selected_joint = selected_joint_raw[0].strip()
        input_mesh_path = self.get_dag_path(self.input_mesh)
        input_mesh_fnSet = om.MFnMesh(input_mesh_path)
        faces_color = om.MColorArray()
        faces_ID = []
        if self.reset_joint:
            if self.reset_joint == selected_joint:
                return        # do nothing
            reset_faces_ID = self.color_map[self.reset_joint]['faces_ID']
            faces_ID.extend(reset_faces_ID)
            for id in reset_faces_ID:
                faces_color.append(self.color_map[self.reset_joint]['color'])
        selected_faces_ID = self.color_map[selected_joint]['faces_ID']
        faces_ID.extend(selected_faces_ID)
        for id in selected_faces_ID:
            faces_color.append(om.MColor([1, 1, 1]))
        void_faces_ID = self.color_map['void']['faces_ID']
        faces_ID.extend(void_faces_ID)
        for id in void_faces_ID:
            faces_color.append(self.color_map['void']['color'])
        input_mesh_fnSet.setFaceColors(faces_color, faces_ID)
        self.reset_joint = selected_joint

    def mirror_proxy_joints(self):
        # preliminary operations
        pmc.textScrollList(self.symmetryMatchesList, edit=True, removeAll=True)
        pmc.textScrollList(self.selfMatchesList, edit=True, removeAll=True)
        
        proxy_joints_raw = pmc.textScrollList(self.proxyJointsList, query=True, allItems=True)
        proxy_joints_name = [prx_jnt.strip() for prx_jnt in proxy_joints_raw]
        proxy_joints = pmc.ls(proxy_joints_name)
        proxy_joints_num = len(proxy_joints)
        proxy_joints_positions = {proxy_joints_name[index]:proxy_joints[index].getTranslation('world') for index in range(0, proxy_joints_num)}
        
        #picklist = proxy_joints_name.copy()
        picklist = list(proxy_joints_name)
        
        sym_direction = pmc.radioButtonGrp(self.symmetryDirection, query=True, select=True)
        sym_plane = pmc.radioButtonGrp(self.symmetryPlane, query=True, select=True)
        sym_tolerance = 0.001
        
        # build symmetry map
        for src_jnt in proxy_joints_name:
            source_position = proxy_joints_positions[src_jnt]
            if source_position[self.symmetry_axis[sym_plane]]*self.symmetry_option[sym_direction] >= -sym_tolerance:
                mirror_position = [source_position[index]*self.symmetry_conversion[sym_plane][index] for index in range(0, 3)]
                mirror_point = pmc.datatypes.Point(mirror_position)
                for tgt_jnt in picklist:
                    target_position = proxy_joints_positions[tgt_jnt]
                    target_point = pmc.datatypes.Point(target_position)
                    if mirror_point.distanceTo(target_point) < sym_tolerance:
                        self.symmetry_map.setdefault(src_jnt, tgt_jnt)
                        picklist.remove(tgt_jnt)
                        if not src_jnt == tgt_jnt:
                            picklist.remove(src_jnt)
                        break
        
        for remainder in picklist:
            self.symmetry_map.setdefault(remainder, remainder)
        
        # fill matches lists
        source_joints = [item for item in self.symmetry_map.keys()]
        source_joints.sort()
        for src_jnt in source_joints:
            target_joint = self.symmetry_map[src_jnt]
            if src_jnt == target_joint:
                pmc.textScrollList(self.selfMatchesList, edit=True, append=src_jnt)
            else:
                pmc.textScrollList(self.symmetryMatchesList, edit=True, append=src_jnt+'    ->    '+target_joint)

    def mirror_color_map_routine_legacy(self):
        # preliminary operations
        source_joints = self.symmetry_map.keys()
        
        proxy_joints_raw = pmc.textScrollList(self.proxyJointsList, query=True, allItems=True)
        proxy_joints_name = [prx_jnt.strip() for prx_jnt in proxy_joints_raw]
        selected_joint_raw = pmc.textScrollList(self.proxyJointsList, query=True, selectItem=True)
        selected_joint = selected_joint_raw[0].strip()
        
        input_mesh_path = self.get_dag_path(self.input_mesh)
        input_mesh_fnSet = om.MFnMesh(input_mesh_path)

        sym_plane = pmc.radioButtonGrp(self.symmetryPlane, query=True, select=True)
        sym_axis = self.symmetry_axis[sym_plane]
        mirror_transformation = om.MMatrix().setElement(sym_axis, sym_axis, -1)
        sym_direction = pmc.radioButtonGrp(self.symmetryDirection, query=True, select=True)
        
        mirror_faces_ID = om.MIntArray()
        mirror_faces_color = om.MColorArray()
        highlighted_faces_ID = om.MIntArray()
        highlighted_faces_color = om.MColorArray()
        
        pBar_title = '...Mirroring Color Map...'
        pBar_win_name = 'PBwindow'
        if pmc.window(pBar_win_name, exists=True):
            pmc.deleteUI(pBar_win_name)
        pmc.window(pBar_win_name, title=pBar_title, sizeable=False, widthHeight=[370, 50])
        pBar_layout = pmc.formLayout(numberOfDivisions=100)
        pBar_control = pmc.progressBar(parent=pBar_layout, width=350, height=30, minValue=0, maxValue=len(source_joints), progress=0)
        pmc.formLayout(pBar_layout, edit=True, attachForm=([pBar_control, 'left', 10], [pBar_control, 'top', 10]))
        pmc.showWindow(pBar_win_name)
        
        # mirror color map
        for src_jnt in source_joints:
            faces_ID = self.color_map[src_jnt]['faces_ID']
            face_component_fnSet = om.MFnSingleIndexedComponent()
            face_component = face_component_fnSet.create(om.MFn.kMeshPolygonComponent)
            face_component_fnSet.addElements(faces_ID)
            faces_iterator = om.MItMeshPolygon(input_mesh_path, face_component)
            
            mirror_joint = self.symmetry_map[src_jnt]
            
            while not faces_iterator.isDone():
                face_center = faces_iterator.center(om.MSpace.kWorld)
                if (face_center[self.symmetry_axis[sym_plane]]*self.symmetry_option[sym_direction] >= 0):
                    mirror_point = face_center * mirror_transformation
                    closest_point = input_mesh_fnSet.getClosestPoint(mirror_point, om.MSpace.kWorld)
                    
                    if closest_point:
                        mirror_face_ID = closest_point[1]
                        
                        if not mirror_face_ID in self.color_map[mirror_joint]['faces_ID']:
                            remove_joint = self.lookup_table[mirror_face_ID]
                            self.color_map[remove_joint]['faces_ID'].remove(mirror_face_ID)
                            self.color_map[mirror_joint]['faces_ID'].append(mirror_face_ID)
                            self.color_map[mirror_joint]['faces_ID'].sort()
                            self.lookup_table[mirror_face_ID] = mirror_joint
                            
                            mirror_faces_ID.append(mirror_face_ID)
                            mirror_faces_color.append(self.color_map[mirror_joint]['color'])
                            if mirror_joint == selected_joint:
                                highlighted_faces_ID.append(mirror_face_ID)
                                highlighted_faces_color.append(om.MColor([1, 1, 1]))
                
                try:
                    faces_iterator.next()
                except:
                    faces_iterator.next(None)
                    
            pmc.progressBar(pBar_control, edit=True, step=1)
            
        pmc.deleteUI(pBar_win_name)
        
        # apply color map
        if mirror_faces_ID:
            input_mesh_fnSet.setFaceColors(mirror_faces_color, mirror_faces_ID)
        if highlighted_faces_ID:
            input_mesh_fnSet.setFaceColors(highlighted_faces_color, highlighted_faces_ID)
    
    def mirror_color_map_routine(self):
        # preliminary operations
        source_joints = self.symmetry_map.keys()
        
        proxy_joints_raw = pmc.textScrollList(self.proxyJointsList, query=True, allItems=True)
        proxy_joints_name = [prx_jnt.strip() for prx_jnt in proxy_joints_raw]
        selected_joint_raw = pmc.textScrollList(self.proxyJointsList, query=True, selectItem=True)
        selected_joint = selected_joint_raw[0].strip()
        
        input_mesh_path = self.get_dag_path(self.input_mesh)
        input_mesh_node = input_mesh_path.node()
        input_mesh_matrix = input_mesh_path.inclusiveMatrixInverse()
        input_mesh_fnSet = om.MFnMesh(input_mesh_path)
        
        mesh_intersector = om.MMeshIntersector()
        mesh_intersector.create(input_mesh_node, input_mesh_matrix)

        sym_plane = pmc.radioButtonGrp(self.symmetryPlane, query=True, select=True)
        sym_axis = self.symmetry_axis[sym_plane]
        mirror_transformation = om.MMatrix().setElement(sym_axis, sym_axis, -1)
        sym_direction = pmc.radioButtonGrp(self.symmetryDirection, query=True, select=True)
        
        mirror_faces_ID = om.MIntArray()
        mirror_faces_color = om.MColorArray()
        highlighted_faces_ID = om.MIntArray()
        highlighted_faces_color = om.MColorArray()
        
        # mirror color map
        for src_jnt in source_joints:
            faces_ID = self.color_map[src_jnt]['faces_ID']
            face_component_fnSet = om.MFnSingleIndexedComponent()
            face_component = face_component_fnSet.create(om.MFn.kMeshPolygonComponent)
            face_component_fnSet.addElements(faces_ID)
            faces_iterator = om.MItMeshPolygon(input_mesh_path, face_component)
            
            mirror_joint = self.symmetry_map[src_jnt]
            
            while not faces_iterator.isDone():
                face_center = faces_iterator.center(om.MSpace.kWorld)
                if (face_center[self.symmetry_axis[sym_plane]]*self.symmetry_option[sym_direction] >= 0):
                    mirror_point = face_center * mirror_transformation
                    closest_point = mesh_intersector.getClosestPoint(mirror_point)
                    
                    if closest_point:
                        mirror_face_ID = closest_point.face
                        
                        if not mirror_face_ID in self.color_map[mirror_joint]['faces_ID']:
                            remove_joint = self.lookup_table[mirror_face_ID]
                            self.color_map[remove_joint]['faces_ID'].remove(mirror_face_ID)
                            self.color_map[mirror_joint]['faces_ID'].append(mirror_face_ID)
                            self.color_map[mirror_joint]['faces_ID'].sort()
                            self.lookup_table[mirror_face_ID] = mirror_joint
                            
                            mirror_faces_ID.append(mirror_face_ID)
                            mirror_faces_color.append(self.color_map[mirror_joint]['color'])
                            if mirror_joint == selected_joint:
                                highlighted_faces_ID.append(mirror_face_ID)
                                highlighted_faces_color.append(om.MColor([1, 1, 1]))
                
                try:
                    faces_iterator.next()
                except:
                    faces_iterator.next(None)
        
        # apply color map
        if mirror_faces_ID:
            input_mesh_fnSet.setFaceColors(mirror_faces_color, mirror_faces_ID)
        if highlighted_faces_ID:
            input_mesh_fnSet.setFaceColors(highlighted_faces_color, highlighted_faces_ID)

    def mesh_button_command(self, *args):
        self.input_mesh = []
        self.inMesh_source_plug = []
        self.display_colors_flag = False
        self.color_sets = []
        self.current_color_set = []
        
        selection = pmc.ls(selection=True)
        if selection:
            target = selection[-1]
            pmc.textFieldButtonGrp(self.meshGroup, edit=True, text=str(target))
            target_shape = self.get_target_shape(target)
            if target_shape is not None:
                if self.is_a_mesh(target_shape):
                    self.input_mesh = target_shape
                    input_mesh_node = self.get_depend_node(target_shape)
                    self.inMesh_source_plug = om.MFnDependencyNode(input_mesh_node).findPlug('inMesh', False).source()
                    self.display_colors_flag = target_shape.displayColors.get()
                    target_color_sets = pmc.polyColorSet(target_shape, query=True, allColorSets=True)
                    if target_color_sets is not None:
                        self.color_sets = target_color_sets
                        self.current_color_set = pmc.polyColorSet(target_shape, query=True, currentColorSet=True)
                    return
        
        pmc.warning('Select a valid mesh')
            
    def mesh_field_command(self, *args):
        self.input_mesh = []
        self.inMesh_source_plug = []
        self.display_colors_flag = False
        self.color_sets = []
        self.current_color_set = []
        
        target = pmc.textFieldButtonGrp(self.meshGroup, query=True, text=True)
        target_shape = self.get_target_shape(target)
        if target_shape is not None:
            if self.is_a_mesh(target_shape):
                self.input_mesh = target_shape
                input_mesh_node = self.get_depend_node(target_shape)
                self.inMesh_source_plug = om.MFnDependencyNode(input_mesh_node).findPlug('inMesh', False).source()
                self.display_colors_flag = target_shape.displayColors.get()
                target_color_sets = pmc.polyColorSet(target_shape, query=True, allColorSets=True)
                if target_color_sets is not None:
                    self.color_sets = target_color_sets
                    self.current_color_set = pmc.polyColorSet(target_shape, query=True, currentColorSet=True)
                return
        
        pmc.warning('Select a valid mesh')
        
    def select_proxy_joints_command(self, *args):
        # preliminary operations
        self.hierarchy_scroll_list = []
        self.flat_scroll_list = []
        self.color_map = {}
        self.reset_joint = []
        pmc.textScrollList(self.proxyJointsList, edit=True, removeAll=True)
        self.cleaning_command()
        
        # input validation
        sort_order = pmc.radioButtonGrp(self.proxyJointsSort, query=True, select=True)
        selection = pmc.ls(selection=True)
        valid_selection = pmc.ls(selection=True, type='joint')
        if valid_selection:
            if len(selection) > len(valid_selection):
                for item in selection:
                    if not item in valid_selection:
                        pmc.warning('Skipping {name}: not a valid joint'.format(name=str(item)))
        else:
            pmc.warning('Select Proxy Joints to determine Proxy Meshes. Only objects of type \"joint\" are accepted')    
            return
        if not self.input_mesh:
            pmc.warning('Select a valid mesh')    
            return
        
        # sorting proxy joints
        self.sort_routine(sort_order, valid_selection)
        pmc.textScrollList(self.proxyJointsList, edit=True, selectIndexedItem=1)
        
        # building symmetry map
        self.symmetry_map = {}
        self.mirror_proxy_joints()
        
        # applying color to mesh
        self.build_color_map()
        self.highlight_selection()

    def reset_color_map_command(self, *args):
        proxy_joints_raw = pmc.textScrollList(self.proxyJointsList, query=True, allItems=True)
        if proxy_joints_raw:
            self.reset_joint = []
            self.build_color_map()
            self.highlight_selection()
        else:
            pmc.warning('Proxy Joints list is empty. Please select Proxy Joints first')

    def sort_command(self, *args):
        sort_order = pmc.radioButtonGrp(self.proxyJointsSort, query=True, select=True)
        proxy_joints_raw = pmc.textScrollList(self.proxyJointsList, query=True, allItems=True)
        if proxy_joints_raw:
            proxy_joints_name = [joint_token.strip() for joint_token in proxy_joints_raw]
            pmc.textScrollList(self.proxyJointsList, edit=True, removeAll=True)
            proxy_joints = pmc.ls(proxy_joints_name)
            # sorting proxy joints
            self.sort_routine(sort_order, proxy_joints)
            pmc.textScrollList(self.proxyJointsList, edit=True, selectIndexedItem=1)
            
    def paint_faces_command(self, *args):
        # input validation
        if not self.input_mesh:
            pmc.warning('Select a valid mesh')
            return
        input_mesh_path = self.get_dag_path(self.input_mesh)
        input_mesh_fnSet = om.MFnMesh(input_mesh_path)
        
        face_component_fnSet = om.MFnSingleIndexedComponent()
        face_component = face_component_fnSet.create(om.MFn.kMeshPolygonComponent)
        input_selection = om.MGlobal.getActiveSelectionList()
        input_selection_iterator = om.MItSelectionList(input_selection)
        while not input_selection_iterator.isDone():
            try:
                current_item = input_selection_iterator.getComponent()
                if current_item[1].apiTypeStr == 'kMeshPolygonComponent':
                    if current_item[0] == input_mesh_path:
                        face_component_fnSet.addElements(om.MFnSingleIndexedComponent(current_item[1]).getElements())
            except:
                pass
            input_selection_iterator.next()
        faces_ID = face_component_fnSet.getElements()
        if not faces_ID:
            pmc.warning('Select the Input Mesh faces you want to paint')
            return
        
        proxy_joints_raw = pmc.textScrollList(self.proxyJointsList, query=True, allItems=True)
        if not proxy_joints_raw:
            pmc.warning('Proxy Joints list is empty. Please select Proxy Joints first')
            return
        proxy_joints_name = [joint_token.strip() for joint_token in proxy_joints_raw]
        selected_joint_raw = pmc.textScrollList(self.proxyJointsList, query=True, selectItem=True)
        selected_joint = selected_joint_raw[0].strip()

        faces_color = om.MColorArray()
        
        # paint selected faces
        for id in faces_ID:
            remove_joint = self.lookup_table[id]
            self.color_map[remove_joint]['faces_ID'].remove(id)
            self.color_map[selected_joint]['faces_ID'].append(id)
            self.color_map[selected_joint]['faces_ID'].sort()
            faces_color.append(om.MColor([1, 1, 1]))
            self.lookup_table[id] = selected_joint
        
        input_mesh_fnSet.setFaceColors(faces_color, faces_ID)
    
    def mirror_direction_command(self, *args):
        self.symmetry_map = {}
        self.mirror_proxy_joints()
        
    def symmetry_plane_command(self, *args):
        self.symmetry_map = {}
        self.mirror_proxy_joints()
        
    def connect_command(self, *args):
        # input validation
        selection = pmc.textScrollList(self.selfMatchesList, query=True, selectItem=True)
        if not selection:
            pmc.warning('Select an item from the Independent Joints list')
            return
            
        source_joint_string = []
        self_matched_joints = pmc.textScrollList(self.selfMatchesList, query=True, allItems=True)
        for item in self_matched_joints:
            if item.startswith('[Source]'):
                source_joint_string = item
                break
        
        # connect operations
        if not source_joint_string:                     # first click
            source_name = '[Source] ' + selection[0]            
            for index, item in enumerate(self_matched_joints):
                if item == selection[0]:
                    source_index = index+1
                    break
            
            # update lists
            pmc.textScrollList(self.selfMatchesList, edit=True, removeIndexedItem=source_index)
            pmc.textScrollList(self.selfMatchesList, edit=True, appendPosition=[source_index, source_name])
            pmc.textScrollList(self.selfMatchesList, edit=True, selectIndexedItem=source_index)
            
            # print message
            sys.stdout.write('Select another item from the Independent Joints list and press Connect again to create a connection')
            sys.stdout.flush()
                
        else:                                            # second click
            source_joint = source_joint_string.replace('[Source] ', '').replace('[Manual] ', '')
            
            if selection[0].startswith('[Source]'):
                pmc.warning('Select another item from the Independent Joints list to connect to the Source')
                return
            target_joint = selection[0].replace('[Manual] ', '')
    
            # update symmetry map
            self.symmetry_map.pop(source_joint)
            self.symmetry_map.pop(target_joint)
            self.symmetry_map.setdefault(source_joint, target_joint)
            
            # update lists
            prefix = '[Manual] '
            pmc.textScrollList(self.symmetryMatchesList, edit=True, appendPosition=[1, prefix+source_joint+'    ->    '+target_joint])
            pmc.textScrollList(self.selfMatchesList, edit=True, removeItem=selection[0])
            pmc.textScrollList(self.selfMatchesList, edit=True, removeItem=source_joint_string)
            
            # print message
            sys.stdout.write('')
            sys.stdout.flush()
        
    def disconnect_command(self, *args):
        selection = pmc.textScrollList(self.symmetryMatchesList, query=True, selectItem=True)
        if not selection:
            pmc.warning('Select one item from the Symmetry Pairs list')
            return
        selected_items = selection[0].replace('[Manual] ', '').split('->')
        first_joint = selected_items[0].strip()
        second_joint = selected_items[1].strip()
        
        # update symmetry map
        self.symmetry_map.pop(first_joint)
        self.symmetry_map.setdefault(first_joint, first_joint)
        self.symmetry_map.setdefault(second_joint, second_joint)
        
        # update lists
        prefix = '[Manual] '
        pmc.textScrollList(self.symmetryMatchesList, edit=True, removeItem=selection[0])
        pmc.textScrollList(self.selfMatchesList, edit=True, appendPosition=[1, prefix+second_joint])
        pmc.textScrollList(self.selfMatchesList, edit=True, appendPosition=[1, prefix+first_joint])

    def mirror_color_map_command(self, *args):
        # input validation
        if not self.input_mesh:
            pmc.warning('Select a valid mesh')
            return
        proxy_joints_raw = pmc.textScrollList(self.proxyJointsList, query=True, allItems=True)
        if not proxy_joints_raw:
            pmc.warning('Proxy Joints list is empty. Please select Proxy Joints first')
            return
        
        # choose routine
        selection_list = om.MGlobal.getActiveSelectionList()
        
        dummy = pmc.polyCube()
        dummy_mesh = self.get_target_shape(dummy[0])
        dummy_path = self.get_dag_path(dummy_mesh)
        dummy_node = dummy_path.node()
        dummy_matrix = dummy_path.inclusiveMatrixInverse()
        routine_choice = 'legacy'
        try:
            dummy_intersector = om.MMeshIntersector()
            dummy_intersector.create(dummy_node, dummy_matrix)
            routine_choice = 'new'
        except:
            pass
        
        pmc.delete(dummy)
        om.MGlobal.setActiveSelectionList(selection_list)
        
        # mirror routine
        if routine_choice == 'legacy':
            self.mirror_color_map_routine_legacy()
        elif routine_choice == 'new':
            self.mirror_color_map_routine()

    def build_proxy_meshes_command(self, *args):
        # input validation
        if not self.input_mesh:
            pmc.warning('Select a valid mesh')
            return
        proxy_joints_raw = pmc.textScrollList(self.proxyJointsList, query=True, allItems=True)
        if not proxy_joints_raw:
            pmc.warning('Proxy Joints list is empty. Please select Proxy Joints first')
            return
        
        # preliminary operations
        proxy_joints_name = [prx_jnt for prx_jnt in self.color_map.keys()]
        proxy_joints_name.remove('void')
        proxy_joints_num = len(proxy_joints_name)
        proxy_meshes_group = pmc.group(name='Proxy_Meshes_Grp', empty=True, world=True)
        
        input_mesh_path = self.get_dag_path(self.input_mesh)
        input_mesh_node = input_mesh_path.node()
        input_mesh_fnSet = om.MFnMesh(input_mesh_path)
        input_mesh_faces_num = input_mesh_fnSet.numPolygons
        shading_groups_map = input_mesh_fnSet.getConnectedShaders(0)
        shading_groups = shading_groups_map[0]
        faces_shader_index = shading_groups_map[1]
        
        face_component_fnSet = om.MFnSingleIndexedComponent()
        face_component = face_component_fnSet.create(om.MFn.kMeshPolygonComponent)
        face_component_fnSet.addElements(range(0, input_mesh_faces_num))
        face_iterator = om.MItMeshPolygon(input_mesh_path, face_component)
        
        pBar_win_name = 'PBwindow'
        if pmc.window(pBar_win_name, exists=True):
            pmc.deleteUI(pBar_win_name)
        pmc.window(pBar_win_name, title='...Building Proxy Meshes...', sizeable=False, widthHeight=[300, 50])
        pmc.windowPref(pBar_win_name, remove=True)
        pmc.window(pBar_win_name, edit=True, widthHeight=[320, 50])
        pBar_layout = pmc.formLayout(numberOfDivisions=100)
        pBar_control = pmc.progressBar(parent=pBar_layout, width=300, height=30, minValue=0, maxValue=proxy_joints_num, progress=0)
        pmc.formLayout(pBar_layout, edit=True, attachForm=([pBar_control, 'left', 10], [pBar_control, 'top', 10]))
        pmc.showWindow(pBar_win_name)
        
        # build proxy meshes
        for prx_jnt in proxy_joints_name:           
            proxy_faces_ID = self.color_map[prx_jnt]['faces_ID']
            if proxy_faces_ID:            
                current_proxy = prx_jnt + '_Wip'
                proxy_mesh_node = input_mesh_fnSet.copy(input_mesh_node)
                proxy_mesh_name = om.MFnDependencyNode(proxy_mesh_node).name()
                pmc.rename(proxy_mesh_name, current_proxy)
                proxy_mesh_path = self.get_dag_path(current_proxy)
            
                complementary_faces_ID = [id for id in range(0, input_mesh_faces_num) if not id in proxy_faces_ID]
                
                shader_faces_map = {index:[] for index in range(0, len(shading_groups))}
                for id in proxy_faces_ID:
                    shader_faces_map[faces_shader_index[id]].append(id)
                for index, SG in enumerate(shading_groups):
                    if shader_faces_map[index]:
                        SG_faces = [current_proxy+'.f['+str(id)+']' for id in shader_faces_map[index]]
                        SG_fnSet = om.MFnDependencyNode(SG)
                        SG_name = SG_fnSet.name()
                        pmc.sets(SG_name, edit=True, forceElement=SG_faces)            
                
                proxy_face_component_fnSet = om.MFnSingleIndexedComponent()
                proxy_face_component = proxy_face_component_fnSet.create(om.MFn.kMeshPolygonComponent)
                proxy_face_component_fnSet.addElements(complementary_faces_ID)
                proxy_faces_to_delete = om.MSelectionList()
                proxy_faces_to_delete.add((proxy_mesh_path, proxy_face_component))
                om.MGlobal.setActiveSelectionList(proxy_faces_to_delete)
                pmc.delete()
                
                pmc.parent(current_proxy, proxy_meshes_group)
                pmc.rename(current_proxy, current_proxy.replace('_Wip', '_Prx'))
            
            pmc.progressBar(pBar_control, edit=True, step=1)
        
        pmc.deleteUI(pBar_win_name)
        
        # cleaning operations
        self.cleaning_command()
        pmc.select(clear=True)

    def constrain_proxy_command(self, *args):
        # input validation
        selection = pmc.ls(selection=True)
        proxy_joints_raw = pmc.textScrollList(self.proxyJointsList, query=True, allItems=True)
        
        # creating constraints
        if selection:            # constrain by selection
            items_num = len(selection)
            if not items_num%2 == 0:
                pmc.warning('Invalid selection: the number of objects and targets do not match')
                return
            obj_num = int(items_num/2)
            sel_objects = selection[:obj_num]
            sel_targets = selection[obj_num:]
            for index, obj_item in enumerate(sel_objects):
                tgt_item = sel_targets[index]
                try:
                    pmc.parentConstraint(obj_item, tgt_item, maintainOffset=True)
                except:
                    pmc.warning('Unable to create Parent Constraint between {Name1} and {Name2}'.format(Name1=str(obj_item), Name2=str(tgt_item)))
                try:
                    pmc.scaleConstraint(obj_item, tgt_item, maintainOffset=True)
                except:
                    pmc.warning('Unable to create Scale Constraint between {Name1} and {Name2}'.format(Name1=str(obj_item), Name2=str(tgt_item)))
            
        else:                    # constrain by name
            if not proxy_joints_raw:
                pmc.warning('Proxy Joints list is empty. Please select Proxy Joints first')
                return
            proxy_joints_name = [prx_jnt.strip() for prx_jnt in proxy_joints_raw]
            for prx_jnt in proxy_joints_name:
                proxy_mesh = prx_jnt + '_Prx'
                if not pmc.objExists(proxy_mesh):
                    pmc.warning('Skipping constraint on /"{mesh_name}/": mesh not found'.format(mesh_name=proxy_mesh))
                    continue
                try:
                    pmc.parentConstraint(prx_jnt, proxy_mesh, maintainOffset=True)
                except:
                    pmc.warning('Unable to create Parent Constraint between {Name1} and {Name2}'.format(Name1=prx_jnt, Name2=proxy_mesh))
                try:
                    pmc.scaleConstraint(prx_jnt, proxy_mesh, maintainOffset=True)
                except:
                    pmc.warning('Unable to create Scale Constraint between {Name1} and {Name2}'.format(Name1=prx_jnt, Name2=proxy_mesh))

pmc_win = ProxyMeshesCreator.showUI()