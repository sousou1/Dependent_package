import sys

args = sys.argv
len_args = len(args)

# input python3-lark-parser ros-dashing-uncrustify-vendor-dbgsym


path = 'src/package.txt'

with open(path) as f:
    lines = f.readlines()

lines_strip = [line.strip() for line in lines]

packages_num = [(i, line) for i, line in enumerate(lines_strip) if 'Package: ' in line]

depends_num = [(i, line) for i, line in enumerate(lines_strip) if 'Depends: ' in line]

depends_nest_list = [[]]


def add_depends_nest_list(package_name, package_depend_depth):
    if len(depends_nest_list) < package_depend_depth:
        package_depend_depth.append([])
        if package_name in depends_nest_list[package_depend_depth]:
            depends_nest_list[package_depend_depth].append(package_name)


def search_depends(package_name):
    package_line_num = 0
    for package in packages_num:
        if package[1] == 'Package: ' + package_name:
            package_line_num = package[0]
    if package_line_num == 0:
        return 0
    for depend in depends_num:
        if depend[0] >= package_line_num:
            result_depends_list = [x.strip() for x in depend[1].replace('Depends: ', '')[0].split(',')]
            return [x[0] for x in result_depends_list.split('(')]


def recursive_search(package_name):
    depends = search_depends(package_name)
    package_depend_depth = 0
    for depend in depends:
        depth = recursive_search(depend)
        if depth >= package_depend_depth:
            package_depend_depth = depth + 1
    add_depends_nest_list(package_name, package_depend_depth)
    return package_depend_depth


for i in range(len_args):
    recursive_search(args[i])


print("search python3-colcon-common-extensions")
x = search_depends('python3-colcon-common-extensions')
print(x)
# packageに対応したdependsを取得
