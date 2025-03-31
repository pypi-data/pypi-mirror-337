#from .initializer import initialize_environment

# 在包加载时自动调用初始化函数
#initialize_environment()
import os
import sys
import clr
from YJKAPI._APIData import *
from YJKAPI._DataFuncApplication import *
from YJKAPI._CsToYjk import * 
from YJKAPI._MiddleTrans import * 
from YJKAPI._YJKIPC import * 

DEFAULT_STATE='NDepend'
# 获取当前状态
state = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_STATE

# 获取当前 __init__.py 文件所在的目录
current_directory = os.path.dirname(os.path.abspath(__file__))

# 加载DLL路径
if(state=='Depend'):
    dll_path=os.path.join(current_directory, "DLLs","Depend")
    dll_path_yapi = os.path.join(dll_path,"YAPIData.dll")
    dll_path_yjkapi = os.path.join(dll_path,"YJKAPI.dll")
else:
    dll_path=os.path.join(current_directory, "DLLs","NDepend")
    dll_path_yapi = os.path.join(dll_path,"YAPIData.dll")
    dll_path_yjkapi = os.path.join(dll_path,"YJKAPI.dll")
os.environ["PATH"]+= os.pathsep + dll_path

# 加载 DLL
clr.AddReference(dll_path_yapi)
clr.AddReference(dll_path_yjkapi)

# 导入命名空间
from DataFuncApplication import *
from CsToYjk import *
from APIData import *
from MiddleTrans import *
from YJKIPC import *

print("Environment initialized successfully.")

# # 初始化逻辑
# def initialize_environment():
#     global _initialized
#     if _initialized:
#         return  # 如果已经初始化过，直接返回
    
#     _initialized = True  # 标记为已初始化
    
#     current_directory = os.getcwd()  # 获取当前目录
#     dll_path_yapi = os.path.join(current_directory, "DLLs", "YAPIData.dll")
#     dll_path_yjkapi = os.path.join(current_directory, "DLLs", "YJKAPI.dll")
    
#     # 加载 DLL
#     clr.AddReference(dll_path_yapi)
#     clr.AddReference(dll_path_yjkapi)
    
#     # 导入命名空间
#     from DataFuncApplication import *
#     from CsToYjk import *
    
#     print("Environment initialized successfully.")

# # 在导入包时自动调用初始化函数
# initialize_environment()