
# -*- codeing = utf-8 -*-
# @Name：hhOs
# @Version：2.0.0
# @Author：立树
# @Time：2025-03-30 17:30

"""
更新：
- readFile 读取文件功能
- createFile 创建文件功能
- resetFile 重置文件功能
- editFile 修改文件功能
- remove 删除文件、文件夹
"""

import os
from common.result import Result

# 打开文件（文本类型的文件）
def readFile(file = "", encoding = "utf-8"):
    # 状态
    result = Result().initMethod()

    # 参数判断
    if file == "":
        return result.setMsg("Error - 缺少参数（file）").print()

    # 路径判断
    if not os.path.exists(file):
        return result.setMsg(f"Error - 文件路径不存在（'{file}'）").print()

    try:
        with open(file, mode = "r", encoding = encoding) as f:
            contt = f.read()
            # print(contt)
            result.fileName = file
            result.fileContent = contt
            result.msg = "文件读取成功"
            return result
    except Exception as err:
        return result.setMsg(f"{str(err)}").print()

# 编辑文件（内部函数）
def _writeFile(path = "", content = "", mode = "w+", encoding = "utf-8", msg = ""):
    # 状态
    result = Result().initMethod(depth = 2)

    # 参数判断
    if path == "":
        return result.setMsg("Error - 请补全参数（path）").print()

    # 路径检测
    if path.find("/") > -1:
        if path[-1] != "/":
            # 匹配内容：
            # - [./][dir/].filename
            # - [./][dir/]filename
            # - [./][dir/]filename.ext
            dir = path[0:path.rfind("/") + 1]
            if not os.path.exists(dir):
               os.makedirs(dir)
        else:
            # 匹配内容：
            # - ./
            # - ./dir/
            # - ./dir/dir/
            # - ../dir/
            # - dir/dir/
            return result.setMsg(f"Error - path 参数不合法（'{path}'不是有效的文件路径）").print()
    else:
        # 匹配内容：
        # - .filename
        # - filename
        # - filename.ext
        pass

    try:
        with open(path, mode, encoding = encoding) as f:
            f.write(content)
            f.seek(0)
            content = f.read()
            result.fileName = path
            result.fileContent = content
            result.msg = msg
            return result
    except IOError as err:
        return result.setMsg(f"{str(err)}").print()

# 创建文件（文本类型的文件）
def createFile(path = "", content = "", encoding = "utf-8"):
    return _writeFile(path, content, "w+", encoding, "文件创建成功")

# 重置文件（文本类型的文件）
def resetFile(path = "", content = "", encoding = "utf-8"):
    return _writeFile(path, content, "w+", encoding, "文件重置成功")

# 修改文件（文本类型的文件）
def editFile(path = "", content = "", encoding = "utf-8"):
    return _writeFile(path, content, "a+", encoding, "文件修改成功")

# 删除文件、文件夹
def remove(path = ""):
    # 状态
    result = Result().initMethod()

    # 参数判断
    if path == "":
        return result.setMsg("Error - 缺少参数（path）")

    # 路径判断
    if not os.path.exists(path):
        return result.setMsg(f"Error - 路径不存在（'{path}'）")

    # 屏蔽风险操作
    if path == "." or path == "./" or path[0] == "/" or path.find("..") > -1:
        return result.setMsg(f"Error - 路径无法删除（'{path}'）")

    # 删除
    try:
        if os.path.isfile(path):
            # 删除文件
            os.remove(path)
            result.fileName = path
            result.msg = "文件删除成功"
            return result
        else:
            # 删除当前文件夹下的所有文件、子文件夹
            # os.removedirs() 递归删除目录树中的‌空目录‌，从最深层子目录开始，逐级向上删除，直到遇到非空目录或根目录。
            # os.rmdir() 删除单个空的目录。
            # shutil.rmtree() 则可以删除非空目录，但更危险。
            for root, dirs, files in os.walk(path, topdown = False):
                # print("root - ", root, dirs, files)
                for name in files:
                    file = os.path.join(root, name).replace("\\", "/")
                    # print("file - ", file)
                    if os.path.exists(file):
                        os.remove(file)
                for name in dirs:
                    dir = os.path.join(root, name).replace("\\", "/")
                    # print("folder - ", dir)
                    if os.path.exists(dir):
                        os.rmdir(dir)
            # 删除当前文件夹
            os.rmdir(path)

            result.dirPath = path
            result.msg = "文件夹删除成功"
            return result
    except IOError as err:
        return result.setMsg(f"{str(err)}").print()
