#!/usr/bin/python
# -*- coding: UTF-8 -*-
import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mm

def create_weight_tool_ui(window_name, window_w, window_h, window_title):
    if cmds.window(window_name, query=True, exists=True):
        cmds.deleteUI(window_name)
    cmds.window(window_name)
    cmds.window(window_name, edit=True, w=window_w+4, h=window_h, title=window_title, mnb=0, mxb=0, s=0)
    cmds.columnLayout('main_column', adjustableColumn=True, w=window_w, h=window_h)
    cmds.text(label='influences:', w=50)
    NubInput = cmds.intSliderGrp("numJoints", field=True, min=2, max=20, value=4)
    cmds.button(label="Check", width=180, p='main_column', c=check_4_c)
    cmds.separator(w=window_w,h=10,p='main_column')
    cmds.button(label="Clear", width=180, p='main_column', c=nub_to_jnt)
    cmds.showWindow(window_name)
    

def check_4_c(*args):
    nub=cmds.intSliderGrp("numJoints", q = True, value = True)
    check_4(nub)
        
def nub_to_jnt(*args):
    nub=cmds.intSliderGrp("numJoints", q = True, value = True)
    do_all(nub)

create_weight_tool_ui("rigg_tool", 250, 120, "ClearWeightTool_v1.1(20240718)")
def weighted_average(a, b):
    return (a) / (a+b)

    # def check_relationship(joint1, joint2):

    #     if unique_joints == joint2:
    #         return True
    #     elif joint2 in unique_joints:
    #         return True
    #     else:
    #         return False


def get_first_child_bone(jnt, result_list):
    #result_list.append(bone)
    children = cmds.listRelatives(jnt, children=True, type='joint')  # 获取骨骼的子骨骼
    if children:  # 如果有子骨骼
        first_child_bone = children[0]  # 获取第一根子骨骼
        result_list.append(first_child_bone)  # 将第一根子骨骼添加到结果列表中
        get_first_child_bone(first_child_bone, result_list)  # 递归调用自身，获取第一根子骨骼的子骨骼
# 获取所有骨骼
all_first_children_list=[]
all_bones = cmds.ls(type='joint')
for bone_t in all_bones:
    first_children_list = []
    first_children_list.append(bone_t)
    get_first_child_bone(bone_t, first_children_list)
    all_first_children_list.append(first_children_list)
all_first_children_sort_list = sorted(all_first_children_list, key=len, reverse=True)
unique_elements = set()
merged_list = []

# 遍历子列表，将重复的元素合并到集合中，保留没有重复的子列表
for sublist in all_first_children_sort_list:
    unique_sublist = []
    for item in sublist:
        if item not in unique_elements:
            unique_elements.add(item)
            unique_sublist.append(item)
    if unique_sublist:
        merged_list.append(unique_sublist)
def check_relationship(joint1, joint2):

    joint1_hierarchy = cmds.listRelatives(joint1, allDescendents=True, type='joint', fullPath=True) or []
    unique_joints_1 = list(set(joint for hierarchy in joint1_hierarchy for joint in hierarchy.split('|') if joint))
    if joint2 in unique_joints_1:
        for sublist in merged_list:
            if joint1 in sublist and joint2 in sublist:
                return True
    else:
        return False
def unlock_weight(model):
    
    # 获取选择的模型的蒙皮骨骼
    skin_cluster_modle = cmds.ls(cmds.listHistory(model), type='skinCluster')

    # 解锁所有骨骼
    for s in skin_cluster_modle:
        bones = cmds.skinCluster(s, query=True, influence=True)
        for bone in bones:
            cmds.setAttr(bone + '.liw', 0)
def clear_weight(number):

    selected_vertex = cmds.ls(selection=True,fl=1)
    if not selected_vertex:
        print('vertex_weights less than number')
    else:
        selected_model = cmds.listRelatives(selected_vertex, parent=True) 

        model = selected_model[0]
        model_nt = pm.PyNode(model)
        skin_cluster = cmds.ls(cmds.listHistory(model), type='skinCluster')[0]
        pm.skinPercent(skin_cluster, normalize=True)
        num_vertices = len(selected_vertex)
        #vertex_weights = {}
        unlock_weight(model)
        num_vertices = len(selected_vertex)
        for i in range(num_vertices):
        #vertex = '{}.vtx[{}]'.format(model_nt.name(), i)
            vertex_influence_4_weights = {}
            new_vertex_influence_4_weights={}
            influences = cmds.skinPercent(skin_cluster, '{0}.vtx[{1}]'.format(model, i), query=True, transform=None)
            weights = cmds.skinPercent(skin_cluster, selected_vertex[i], query=True, value=True)
            influence_weights = dict(zip(influences, weights))
            influence_weights = {k: v for k, v in influence_weights.items() if v != 0.0}
            top_influences = sorted(influence_weights, key=influence_weights.get, reverse=True)[:number]
            top_influence_weights = {influence: influence_weights[influence] for influence in top_influences}
            #vertex_weights[selected_vertex[i]] = influence_weights
            vertex_influence_4_weights[selected_vertex[i]] = top_influence_weights
            if len(influence_weights) <= number:
                print('vertex_weights less than number')
                
            if len(influence_weights) > number:
                sorted_items = sorted(influence_weights.items(), key=lambda x: x[1])
                keys_to_remove = [item[0] for item in sorted_items[:-number]]
                max_four_key = [item[0] for item in sorted_items[-number:]]

                max_four_values = sorted(sorted_items, key=lambda x: x[1], reverse=True)[:number]
                remove_values = [item for item in sorted_items if item not in max_four_values]
                result = []

                for w in range(len(max_four_values)):
                    joint1 = max_four_values[w][0]
                    group = []
                    
                    for j in range(len(max_four_values)):
                        joint2 = max_four_values[j][0]
                        if check_relationship(joint1, joint2):
                            group.append(joint2)
                    if group not in result:
                        result.append(group)

                joint_values = {joint[0]: joint[1] for joint in max_four_values}
                result_with_values = [[(joint, joint_values[joint]) for joint in group] for group in result]

                # 
                result_with_percent = []
                for group in result_with_values:
                    new_group = []
                    for item in group:
                        weighted_avg = weighted_average(item[1], sum([x[1] for x in group]) - item[1])
                        new_group.append((item[0], weighted_avg))
                    result_with_percent.append(new_group)

                new_result_with_percent = [item for sublist in result_with_percent for item in sublist]
                new_max_four_values = []
                new_remove_values =[]
                new_remove_values_1=[]
                new_result_with_adjusted_values = []
                
                for remove_joint, remove_value in remove_values:
                    for result_joint, result_value in new_result_with_percent:
                        related = check_relationship(remove_joint, result_joint)
                        if related:
                            new_remove_value = remove_value * result_value 
                            new_remove_values.append((result_joint,new_remove_value))
                for remove_joint, remove_value in remove_values:
                    related = False  # 默认设置related为False
                    # 遍历new_result_with_percent列表
                    for result_joint, result_value in new_result_with_percent:
                        if check_relationship(remove_joint, result_joint):
                            related = True  # 如果remove_joint和result_joint存在父子关系，则将related设置为True
                            break  # 找到父子关系后跳出循环
                    if not related:  # 如果remove_joint和new_result_with_percent里的所有骨骼都不存在父子关系
                        new_remove_values_1.append((remove_joint, remove_value))  # 将remove_joint和其value添加到new_remove_values列表中
                total_sum = sum(value for key, value in new_remove_values_1)
                if len(new_remove_values) != 0:
                    value_to_assign = total_sum / len(new_remove_values)
                else:
                    value_to_assign = 0

                # 分配值并存储到 new_result_with_adjusted_values
                for bone, _ in new_remove_values:
                    new_result_with_adjusted_values.append((bone, value_to_assign))
                new_ad_value=new_remove_values+new_result_with_adjusted_values
                new_values = {}
                for joint, value in new_ad_value:
                    if joint in new_values:
                        new_values[joint].append(value)
                    else:
                        new_values[joint] = [value]
                new_values_sum = {joint: sum(values) for joint, values in new_values.items()}
                new_top_influence_weights = top_influence_weights.copy()  # 锟斤拷锟斤拷top_influence_weights锟斤拷new_top_influence_weights
                for joint, value in new_values_sum.items():
                    if joint in new_top_influence_weights:
                        new_top_influence_weights[joint] += value
                    else:
                        new_top_influence_weights[joint] = value
                new_sum = sum(new_top_influence_weights.values())
                # Convert sum_values dictionary into a list of tuples with normalized weights
                normalized_list = [(joint, weight/new_sum) for joint, weight in new_top_influence_weights.items()]

                pm.skinPercent(skin_cluster, selected_vertex[i], transformValue=normalized_list)
                pm.skinPercent(skin_cluster, normalize=True)
        print('success to clear weight')
        cmds.confirmDialog(title='Confirm', message='Succes',button=['Close'])
def get_selected_model():
    selected_model = cmds.ls(selection=True, fl=True)
    if not selected_model:
        cmds.warning("Please select a model.")
        return None
    return selected_model[0]

def get_skin_cluster(model):
    skin_clusters = cmds.ls(cmds.listHistory(model), type='skinCluster')
    if not skin_clusters:
        cmds.warning("No skinCluster found on the selected model.")
        return None
    return skin_clusters[0]

def get_over_4_vertices(model, skin_cluster, number):
    over_4_vertices = set()
    vertices = cmds.ls(model + '.vtx[*]', flatten=True)
    vtx_influences = cmds.skinCluster(skin_cluster, query=True, influence=True)
    for vertex in vertices:
        vtx_weights = cmds.skinPercent(skin_cluster, vertex, query=True, value=True)
        influence_weights = {vtx_influences[i]: vtx_weights[i] for i in range(len(vtx_influences)) if vtx_weights[i] != 0.0}
        if len(influence_weights) > number:
            over_4_vertices.add(vertex)
    return list(over_4_vertices)

def check_4(number):
    model = get_selected_model()
    if not model:
        return
    skin_cluster = get_skin_cluster(model)
    if not skin_cluster:
        return
    over_4_vertices = get_over_4_vertices(model, skin_cluster, number)
    cmds.select(over_4_vertices)

def do_all(number):
    selection = cmds.ls(selection=True)

    # 判断选择的是模型还是顶点
    if cmds.filterExpand(selection, selectionMask=12, expand=True):
        cmds.select(selection)
        check_4(number)
        clear_weight(number)

    else:
        cmds.select(selection)
        clear_weight(number)

        