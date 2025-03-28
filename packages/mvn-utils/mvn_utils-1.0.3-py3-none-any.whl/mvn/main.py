import argparse
import glob
import os
import xml.etree.ElementTree as ET
import collections
from collections import defaultdict

colors = ['#FFE4E1','#FAEBD7','#FFFFCC','#FFFDD0','#E5F3E5','#E6F5E9','#E0EEF7','#CCECFF','#E6E6FA','#EEE8EF','#FDF5E6','#FFFFF0','#E6E6E6','#F0F0F0','#F08080','#ADD8E6','#FAFAD2','#FA8072','#E6F5E9','#DDA0DD']*10


def list_project_on_disk(directory="."):
    subdirectories = []
    for subdirectory in glob.glob(os.path.join(directory, "*/")):  # 查找所有子目录
        if glob.glob(os.path.join(subdirectory, "**/pom.xml"), recursive=True):  # 检查子目录中是否包含 .a 文件
            subdirectories.append(os.path.abspath(subdirectory))  # 添加子目录的绝对路径到列000080表
    return subdirectories


def get_group_id(element, namespace):
    """从当前元素及其父元素获取groupId"""
    group_id = element.find('ns:groupId', namespace)
    if group_id is not None:
        return group_id.text
    parent = element.find('ns:parent', namespace)
    if parent is not None:
        return parent.find('ns:groupId', namespace).text
    return None


def get_sub_modules(filename, filtered_group=''):
    if not filename.endswith(".pom"):
        filename = os.path.join(filename, "pom.xml")
    # 加载POM文件
    tree = ET.parse(filename)
    root = tree.getroot()

    # 获取命名空间
    namespace = {'ns': 'http://maven.apache.org/POM/4.0.0'}

    # 获取项目信息
    artifact_id = root.find('ns:artifactId', namespace).text
    group_id = get_group_id(root, namespace)

    # 获取依赖信息
    dependencies = root.find('ns:dependencies', namespace)
    submodules = root.find('ns:modules', namespace)
    kyc_dependencies = []
    kyc_submodules = []
    if dependencies is not None:
        for dependency in dependencies.findall('ns:dependency', namespace):
            m_group_id = get_group_id(dependency, namespace)
            m_artifact_id = dependency.find('ns:artifactId', namespace).text
            if filtered_group:
                if m_group_id.startswith(filtered_group):
                    kyc_dependencies.append((m_group_id,m_artifact_id))
            else:
                kyc_dependencies.append((m_group_id,m_artifact_id))

    if submodules is not None:
        kyc_submodules = [(group_id,x.text) for x in submodules.findall('ns:module', namespace)]

    return (group_id,artifact_id), kyc_dependencies, kyc_submodules


def bfs_traverse_directory_structure(root_dir, filter_func=None):
    """
    使用廣度優先搜尋遍歷目錄並建立目錄結構字典。

    Args:
        root_dir (str): 要遍歷的根目錄路徑。
        filter_func (function, optional): 用於過濾子目錄的函式。

    Returns:
        dict: 表示目錄結構的字典。
    """

    structure = {root_dir: {}}  # 初始化根目錄的字典
    queue = collections.deque([(root_dir, structure[root_dir], 0)])  # 佇列包含 (目錄路徑, 父目錄字典, 層級)
    visited = set()

    while queue:
        current_dir, parent_dict, level = queue.popleft()
        if current_dir in visited:
            continue
        visited.add(current_dir)

        try:
            for item in os.listdir(current_dir):
                item_path = os.path.join(current_dir, item)
                if os.path.isdir(item_path):
                    if filter_func is None or filter_func(item_path):
                        # 將子目錄加入父目錄字典
                        parent_dict[item_path] = {}
                        # 將子目錄加入佇列
                        queue.append((item_path, parent_dict[item_path], level + 1))
        except OSError as error:
            print('OSError encountered:', error)

    return structure


def get_name(path, is_leaf):
    if is_leaf:
        return os.path.basename(path)
    else:
        return f"project-{os.path.basename(path)}"


def print_directory_structure(structure, level=1):
    # 獲取根目錄的子目錄
    for full_path, sub_structure in structure.items():
        is_leaf = not bool(sub_structure)  # 檢查是否為葉子節點
        leaf_marker = "" if is_leaf else "subgraph "
        indent = '\t' * level
        print(indent + f"{leaf_marker}{get_name(full_path, is_leaf)}")
        print_directory_structure(sub_structure, level + 1)
        if not is_leaf:
            print(f"{indent}end")


def get_maven_structure(base_path, group, my_filter):
    # 存储项目的一级目录对应的子项目
    pro_lv1_children = defaultdict(list)
    # 存储一级目录对应的颜色
    pro_lv1_colors = {}
    # 存储项目列表
    pro_gl_list = []

    def print_directory_gl_structure(structure, level=1, lv1_parent_name='', group=''):
        # 獲取根目錄的子目錄
        indent = ''  # '\t' * level
        for full_path, sub_structure in structure.items():
            (group_id,artifact_id), dependencies, sub_modules = get_sub_modules(os.path.join(full_path), filtered_group=group)
            project_name  = f"{group_id}:{artifact_id}"
            if level == 1:
                pro_lv1_colors[project_name] = colors.pop()
                lv1_parent_name = project_name
            pro_lv1_children[lv1_parent_name].append(project_name)
            # show_name = f"{name}[{lv1_parent_name} - {name}]"
            if dependencies:
                for g,d in dependencies:
                    pro_gl_list.append((project_name, d, f"{indent}{project_name} --> {g}:{d}"))
            else:
                pro_gl_list.append((project_name, None, f"{indent}{project_name}"))
            if sub_modules:
                for g,m in sub_modules:
                    pro_gl_list.append((project_name, m, f"{indent}{project_name} --> {g}:{m}"))

            print_directory_gl_structure(sub_structure, level + 1, project_name if level == 1 else lv1_parent_name,
                                         group=group)

    directory_structure = bfs_traverse_directory_structure(base_path, my_filter)
    root_sub_structure = next(iter(directory_structure.values()))
    print_directory_gl_structure(root_sub_structure, level=1, group=group)
    return pro_lv1_colors, pro_gl_list, pro_lv1_children


# 使用範例
root_directory = '/Users/xuwuqiang/Documents/workspace/ekyc'


def my_filter(path):
    # 此範例過濾包含 "test" 的子目錄
    return os.path.exists(os.path.join(path, 'pom.xml'))


def pro_structure(base_path):
    directory_structure = bfs_traverse_directory_structure(base_path, my_filter)
    root_sub_structure = next(iter(directory_structure.values()))
    print("graph LR")
    print_directory_structure(root_sub_structure)


def pro_module_releation_main(base_path, focus_modules=[], group='', depth=1):
    pro_lv1_colors, pro_gl_list, pro_lv1_children = get_maven_structure(base_path=base_path, group=group,
                                                                        my_filter=my_filter)

    def relation_modules(focus_modules, pro_gl_list, depth):
        def get_depth_module(focus_modules, pro_gl_list, depth):
            relation_modules = focus_modules.copy()
            for i in range(depth - 1):
                for source, destination, desc in pro_gl_list:
                    if relation_modules:
                        if source in relation_modules or destination in relation_modules:
                            relation_modules.append(source)
                            relation_modules.append(destination)
            return [x for x in set(relation_modules)]

        if depth == 1:
            return focus_modules.copy()
        return get_depth_module(focus_modules, pro_gl_list, depth)

    def print_header():
        print("graph LR")

    def get_content(relation_modules,pro_gl_list):
        result = []
        for item in pro_gl_list:
            source, destination, desc = item
            if relation_modules:
                if source in relation_modules or destination in relation_modules:
                    result.append(item)
            else:
                result.append(item)
        return result

    def print_color(relation_modules, pro_lv1_colors):
        for item, children in pro_lv1_children.items():
            for c in children:
                if relation_modules:
                    if c in relation_modules:
                        print(f'style {c} fill:{pro_lv1_colors[item]},stroke:#333,stroke-width:4px')
                else:
                    print(f'style {c} fill:{pro_lv1_colors[item]},stroke:#333,stroke-width:4px')

    relation_modules = relation_modules(focus_modules, pro_gl_list, depth=depth)
    print_header()
    content = get_content(relation_modules,pro_gl_list)
    for source, dest, desc in content:
        print(desc)
    relation_modules = [source for source, dest, desc in content] + [dest for source, dest, desc in content]
    print_color(relation_modules=[x for x in relation_modules if x], pro_lv1_colors=pro_lv1_colors)


def mvn_graph_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', '-d', help='dir path')
    parser.add_argument('--depth', '-depth', default=1, help='search depth')
    parser.add_argument('--modules', '-m', help='modules to focus on,split by ,')
    parser.add_argument('--group', '-g', help='groupId of you pom to filter')
    args = parser.parse_args()
    base_path = args.dir
    focus_modules = args.modules.split(',') if args.modules else []
    # 生成module依赖（无项目结构关系： 加上结构之后太乱了）
    pro_module_releation_main(base_path, focus_modules=focus_modules, group=args.group, depth=args.depth)


def pro_graph_command():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', '-d', help='dir path')
    args = parser.parse_args()
    base_path = args.dir
    # 生成module依赖（无项目结构关系： 加上结构之后太乱了）
    pro_structure(base_path)


if __name__ == "__main__":
    """
    view here: https://www.min2k.com/tools/mermaid/
    """
    # base_path = '/Users/xuwuqiang/Documents/workspace/ekyc'
    base_path = '/Users/xuwuqiang/Documents/workspace/ekyc/service-ekyc'
    # base_path = '/Users/xuwuqiang/Documents/workspace/game'

    # 生成项目结构
    pro_structure(base_path)
    # 生成module依赖（无项目结构关系： 加上结构之后太乱了）
    # pro_module_releation_main(base_path, focus_modules=['dev.ekyc.api:api-core'], group='dev.ekyc', depth=1)
    # pro_module_releation_main(base_path, focus_modules=[], group='com.lucy', depth=1)
    # pro_module_releation_main(base_path, focus_modules=[], group='dev.ekyc', depth=1)
