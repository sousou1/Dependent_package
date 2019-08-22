import sys
import re

args = sys.argv
len_args = len(args)


path = 'src/package.txt'

outfile_path = 'out.txt'
with open(path) as f:
    lines = f.readlines()

lines_strip = [line.strip() for line in lines]

packages_num = [(i, line) for i, line in enumerate(lines_strip) if 'Package: ' in line]

depends_num = [(i, line) for i, line in enumerate(lines_strip) if 'Depends: ' in line]

depends_nest_list = []


def add_depends_nest_list(package_name, package_depend_depth):
    if len(depends_nest_list) < package_depend_depth + 1:
        depends_nest_list.append([])
    if package_name not in depends_nest_list[package_depend_depth]:
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
            result_depends_list = [x.strip() for x in depend[1].replace('Depends: ', '').split(',')]
            return [re.split('[: (]', x)[0] for x in result_depends_list]


def recursive_search(package_name):
    depends = search_depends(package_name)
    package_depend_depth = 0
    if depends != 0:
        for depend in depends:
            depth = recursive_search(depend)
            if depth >= package_depend_depth:
                package_depend_depth = depth + 1
    add_depends_nest_list(package_name, package_depend_depth)
    return package_depend_depth


for i in range(len_args - 1):
    recursive_search(args[i + 1])

len_depends_nest_list = len(depends_nest_list)
for i in range(len(depends_nest_list)):
    print(i)
    for tmp in depends_nest_list[i]:
        print(tmp, end=" ")
    print("\n")
