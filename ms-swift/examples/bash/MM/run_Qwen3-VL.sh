# #!/bin/bash

# # 定义根目录变量
# # 假设 Qwen3-VL 文件夹在当前脚本的同级目录
# ROOT_DIR="./Qwen3-VL"
# SFT_DIR="$ROOT_DIR/SFT"
# ROOT_MIntRec2_DIR="$ROOT_DIR/MIntRec2.0"

# # 检查根目录是否存在
# if [ ! -d "$ROOT_DIR" ]; then
#     echo "错误：找不到根目录 $ROOT_DIR，请确认脚本位置是否正确。"
#     exit 1
# fi

# echo ">>> 🚀 开始执行所有任务..."

# # -----------------------------------------------------------
# # 步骤 1: 进入 SFT/MIntRec 并执行
# # -----------------------------------------------------------
# echo ">>> [1/3] 正在处理 SFT/MIntRec..."
# TARGET_1="$SFT_DIR/MIntRec"

# if [ -d "$TARGET_1" ]; then
#     cd "$TARGET_1" || exit 1
#     echo "    当前目录: $(pwd)"
    
#     # 执行该目录下的所有 .sh 文件
#     for script in *.sh; do
#         # if [ -f "$script" ]; then
#         #     echo "    执行脚本: $script"
#         #     bash "$script"
#         # fi
#     done
# else
#     echo "    警告: 目录 $TARGET_1 不存在"
# fi

# # -----------------------------------------------------------
# # 步骤 2: 进入 SFT/MIntRec2.0 并执行
# # -----------------------------------------------------------
# echo ">>> [2/3] 正在处理 SFT/MIntRec2.0..."
# TARGET_2="$SFT_DIR/MIntRec2.0"

# if [ -d "$TARGET_2" ]; then
#     cd "$TARGET_2" || exit 1
#     echo "    当前目录: $(pwd)"
    
#     # 执行该目录下的所有 .sh 文件
#     for script in *.sh; do
#         if [ -f "$script" ]; then
#             echo "    执行脚本: $script"
#             bash "$script"
#         fi
#     done
# else
#     echo "    警告: 目录 $TARGET_2 不存在"
# fi

# # -----------------------------------------------------------
# # 步骤 3: 进入与 SFT 同级的 MIntRec2.0 并执行
# # -----------------------------------------------------------
# echo ">>> [3/3] 正在处理 Qwen3-VL/MIntRec2.0 (与SFT同级)..."

# if [ -d "$ROOT_MIntRec2_DIR" ]; then
#     cd "$ROOT_MIntRec2_DIR" || exit 1
#     echo "    当前目录: $(pwd)"
    
#     # 执行该目录下的所有 .sh 文件
#     for script in *.sh; do
#         if [ -f "$script" ]; then
#             echo "    执行脚本: $script"
#             bash "$script"
#         fi
#     done
# else
#     echo "    警告: 目录 $ROOT_MIntRec2_DIR 不存在"
# fi

# echo ">>> ✅ 所有任务执行完毕！"




#!/bin/bash

# 1. 记录脚本刚开始执行时的目录（作为基准点）
START_DIR="$(pwd)"

# 定义根目录变量 (相对路径)
ROOT_DIR="./Qwen3-VL"
SFT_DIR="$ROOT_DIR/SFT"
ROOT_MIntRec2_DIR="$ROOT_DIR/MIntRec2.0"

# 检查根目录是否存在
if [ ! -d "$ROOT_DIR" ]; then
    echo "错误：找不到根目录 $ROOT_DIR，请确认脚本位置是否正确。"
    exit 1
fi

echo ">>> 🚀 开始执行所有任务..."

# -----------------------------------------------------------
# 步骤 1: 进入 SFT/MIntRec 并执行
# -----------------------------------------------------------
echo ">>> [1/3] 正在处理 SFT/MIntRec..."
TARGET_1="$SFT_DIR/MIntRec"

if [ -d "$TARGET_1" ]; then
    cd "$TARGET_1" || exit 1
    echo "    当前目录: $(pwd)"
    
#     # 执行该目录下的所有 .sh 文件
#     for script in *.sh; do
#         if [ -f "$script" ]; then
#             echo "    执行脚本: $script"
#             bash "$script"
#         fi
#     done
# else
#     echo "    警告: 目录 $TARGET_1 不存在"
fi

# -----------------------------------------------------------
# 🛑 关键修复：回到初始目录，确保下一步的相对路径有效
# -----------------------------------------------------------
cd "$START_DIR" 

# -----------------------------------------------------------
# 步骤 2: 进入 SFT/MIntRec2.0 并执行
# -----------------------------------------------------------
echo ">>> [2/3] 正在处理 SFT/MIntRec2.0..."
TARGET_2="$SFT_DIR/MIntRec2.0"

if [ -d "$TARGET_2" ]; then
    cd "$TARGET_2" || exit 1
    echo "    当前目录: $(pwd)"
    
    # 执行该目录下的所有 .sh 文件
    for script in *.sh; do
        if [ -f "$script" ]; then
            echo "    执行脚本: $script"
            bash "$script"
        fi
    done
else
    echo "    警告: 目录 $TARGET_2 不存在"
fi

# -----------------------------------------------------------
# 🛑 关键修复：再次回到初始目录
# -----------------------------------------------------------
cd "$START_DIR"

# -----------------------------------------------------------
# 步骤 3: 进入与 SFT 同级的 MIntRec2.0 并执行
# -----------------------------------------------------------
echo ">>> [3/3] 正在处理 Qwen3-VL/MIntRec2.0 (与SFT同级)..."

if [ -d "$ROOT_MIntRec2_DIR" ]; then
    cd "$ROOT_MIntRec2_DIR" || exit 1
    echo "    当前目录: $(pwd)"
    
    # 执行该目录下的所有 .sh 文件
    for script in *.sh; do
        if [ -f "$script" ]; then
            echo "    执行脚本: $script"
            bash "$script"
        fi
    done
else
    echo "    警告: 目录 $ROOT_MIntRec2_DIR 不存在"
fi

echo ">>> ✅ 所有任务执行完毕！"