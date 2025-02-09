# project1.py
#
# ICS 32 Fall 2024
# Project #1: File System Explorer
# 
# NAME: Jin Woo Choi
# EMAIL: jinwc4@uci.edu
# STUDENT ID: 61646260
#
# High-level Design: This project is "The File System Explorer". It has 4 commands man (manual), ls (list), cat(concatenate) and q(quit).
# The function 'man' can be called alongside the name of another function to get the instructions of what that function does. The function 
# 'ls' lists directories and can also be called with options to specify what you want listed. The 'ls' function has 6 options, 'f', 'r', 'e',
# 's', 'g' and 'l'. 
# 

from pathlib import Path

# These string constants are provided to avoid typo errors for the man command.
# Each constant holds one line of text. 
# These can be concatenated to create the correct man directions.

GENERIC1 = "The File System Explorer supports this command in the following format/s:\n"
GENERIC2 = "[COMMAND]\n"
GENERIC3 = "[COMMAND] [INPUT]\n"
GENERIC4 = "[COMMAND] [-OPTIONS] [INPUT]\n"
GENERIC5 = "[COMMAND] [-OPTIONS] [INPUT] [OPTION_INPUT]\n"
GENERIC6 = "The [INPUT] corresponds to the [COMMAND].\n"
GENERIC7 = "The [OPTIONAL_INPUT] corresponds to [-OPTIONS].\n"
LS_DIR = "ls is a command that lists the contents of a directory. [INPUT] is the path.\n"
LS_DIR2 = "ls options include -r, -f, -s, -e, -g and -l.\n"
LS_DIR3 = "-r = recursive, -f file only, -s match specific file name, -e match specific extension.\n"
LS_DIR4 = "-g and -l prints only files with size greater (g) or less (l) than [OPTION_INPUT].\n"
CAT_DIR = "cat is a command that prints the contents of a file. [INPUT] is the file path.\n"
CAT_DIR2 = "cat options include -f and -d.\n"
CAT_DIR3 = "-f = prints the first line only, -d duplicates the file into filename.dup.\n"
MAN_DIR = "man is a command that prints the directions for the command. [INPUT] is the command.\n"
Q_DIR = "q is a command that quits the file system explorer.\n"


def man(user_input):
    inputs = user_input.split()
    ans = ""
    if inputs[0] not in commands:
        return "ERROR: Invalid Command.\n"
    if len(inputs) != 1:
        return "ERROR: Invalid Format.\n"
    elif inputs[0] == "man":
        ans += GENERIC1 + GENERIC3 + MAN_DIR
    elif inputs[0] == "ls":
        ans += GENERIC1 + GENERIC3 + GENERIC4 + GENERIC5
        ans += GENERIC6 + GENERIC7 + LS_DIR + LS_DIR2 + LS_DIR3 + LS_DIR4
    elif inputs[0] == "cat":
        ans += GENERIC1 + GENERIC3 + GENERIC4 + GENERIC6
        ans += CAT_DIR + CAT_DIR2 + CAT_DIR3
    elif inputs[0] == "q":
        ans += GENERIC1 + GENERIC2 + Q_DIR
    return ans


def ls(user_input):
    try:
        inputs = user_input.split()
        if len(inputs) == 0:
            return "ERROR: Invalid Format.\n"
        if inputs[0].count(".") > 1:
                add = inputs[0] +'/'
        else:
            add = ""
        cwd = Path.cwd()
        if len(inputs) == 1:
            p = cwd / inputs[0]
            files = []
            directories = []
            for item in p.iterdir():
                if item.is_file():
                    files.append(item.name)
                elif item.is_dir():
                    directories.append(item.name)
            ans = ""
            files.sort()
            directories.sort()
            for file in files:
                ans += add
                ans += file
                ans += '\n'
            for dir in directories:
                ans += add
                ans += dir
                ans += '\n'
            return ans
        else:
            if inputs[0][0] == '-':
                if inputs[1].count(".") > 1:
                    add = inputs[1] + "/"
                else:
                    add = ""
                opt = 0
                paths = [""]
                ans = ""
                if 'r' in inputs[0] and len(inputs[0]) != 2:
                    paths = ls_r(inputs[1])[1]
                    swap = inputs[0].replace('r', "")
                    inputs[0] = swap
                elif 'r' in inputs[0] and len(inputs[0]) == 2:
                    if len(inputs) == 3 and opt == 0:
                        return "ERROR: Invalid Format.\n"
                    else:
                        return ls_r(inputs[1])[0]
                for c in range(1, len(inputs[0])):     
                    if inputs[0][c] in ls_optional:
                        opt += 1
                        if opt > 1 or len(inputs) != 3:
                            return "ERROR: Invalid Format.\n"
                        else:
                            for path in paths:
                                p = add / cwd / inputs[1] / path
                                if path == "":
                                    ans += (ls_optional[
                                        inputs[0][c]](p, inputs[2]))
                                else:
                                    ans += (ls_optional[
                                        inputs[0][c]](p, inputs[2], path + '/'))             
                        if len(inputs) == 3 and opt == 0:
                            return "ERROR: Invalid Format.\n"
                if 'f' in inputs[0] and len(inputs[0]) != 2:
                    ans_ls = ans.split()
                    ans = ""
                    filter = []
                    for path in paths:
                            p = add/ cwd / inputs[1] / path
                            if path == "":
                                filter.extend(ls_f(p).split())
                            else:
                                filter.extend(ls_f(p, path + '/').split())
                    for s in filter:
                        if s in ans_ls:
                            ans += add + s + '\n'
                elif 'f' in inputs[0] and len(inputs[0]) == 2:
                    if len(inputs) == 3 and opt == 0:
                            return "ERROR: Invalid Format.\n" 
                    else:
                        for path in paths:
                            p = add / cwd / inputs[1] / path
                            if path == "":
                                ans += add + ls_f(p)
                            else:
                                ans += add + ls_f(p, path + '/')
                return ans
            else:
                return "ERROR: Invalid Format.\n" 
    except FileNotFoundError:
        return "ERROR: Invalid Path.\n"
    
def ls_r(path):
    file_path = Path(path)
    names = []
    paths = [""]
    ans = ""
    for item in sorted(file_path.iterdir()):
        if item.is_file():
            names.append(item.name)
        elif item.is_dir():
            paths.append(item.name)
    for name in names:
        ans += name + '\n'
    for p in sorted(paths):
        if p != "":
            ans += f"{p}\n"
    for p in sorted(paths):
        if p == "":
            continue
        path_files = ls_r(file_path / p)[0]
        for file in path_files.split():
            if len(path_files.split()) > 0:
                ans += f"{p}/{file}\n"
            else:
                continue
    return ans, paths
def ls_f(path, deep_path=""):
    file_path = Path(path)
    files = ""
    for item in sorted(file_path.iterdir()):
        if item.is_file():
            files += deep_path + item.name + '\n'
    return files

def ls_s(path, target, deep_path=""):
    file_path = Path(path)
    files = ""
    for item in sorted(file_path.iterdir()):
        if target in item.name:
            files += deep_path + item.name + '\n'
    return files
def ls_e(path, ext, deep_path=""):
    file_path = Path(path)
    files = ""
    for item in sorted(file_path.iterdir()):
        if item.suffix == ext:
            files += deep_path + item.name + '\n'
    return files
def ls_g(path, size, deep_path=""):
    file_path = Path(path)
    files = ""
    for item in sorted(file_path.iterdir()):
        if item.stat().st_size > int(size):
            files += deep_path + item.name + '\n'
    return files
def ls_l(path, size, deep_path=""):
    file_path = Path(path)
    files = ""
    for item in sorted(file_path.iterdir()):
        if item.stat().st_size < int(size):
            files += deep_path + item.name + '\n'
    return files
def cat(user_input):
    try:
        inputs = user_input.split()
        if len(inputs) == 0 or len(inputs) > 2:
            return "ERROR: Invalid Format.\n"
        if inputs[0][0] == "-":
            if inputs[0][1] == "f":
                with open(inputs[1], 'r') as f:
                    line = f.readline()
                    return line
            elif inputs[0][1] == "d":
                with open(inputs[1], 'r') as f:
                    content = f.read()
                with open(inputs[1] + '.dup', 'w') as f:
                    f.write(content)
                    return("file duplicated")
            else:
                return "ERROR: Invalid Format.\n"
        else:
            with open(inputs[0], 'r') as f:
                content = f.read()
                return content
    except FileNotFoundError:
        return "ERROR: Invalid Path.\n"
def parse_command(user_input):
    inputs = user_input.split()
    try:
        if inputs[0].lower() not in commands:
            return "ERROR: Invalid Command.\n"
        elif inputs[0].lower() == 'q':
            return "quit"
        else:
            arg = ""
            if inputs[0] == "man":
                if len(inputs) == 1:
                    return "ERROR: Invalid Format.\n"
            for i in range(1, len(inputs)):
 
                arg += inputs[i]
                arg += ' '
            return commands[inputs[0].lower()](arg)
    except IndexError:
        return ""
def main() -> None:
    while True:
        user_input = input()
        value = parse_command(user_input)
        if (value == "quit"):
            exit()
        else:
            print(value, end="")
commands = {'man': man,
            'ls': ls,
            'cat': cat,
            'q': 'quit'}
ls_options = {'r': ls_r,
              'f': ls_f}
ls_optional = {'s':ls_s,
               'e':ls_e,
               'g':ls_g,
               'l':ls_l}
if __name__ == '__main__':
    main()