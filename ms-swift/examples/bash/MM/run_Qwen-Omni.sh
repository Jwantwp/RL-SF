# #!/bin/bash

# # 定义根目录变量
# # 假设 Qwen3-VL 文件夹在当前脚本的同级目录
# ROOT_DIR="./MiniCPM"
# ZERO_SHOT_DIR="$ROOT_DIR/Zero-Shot"
# Few-shot_DIR="$ROOT_DIR/Few-Shot"
# SFT_DIR="$ROOT_DIR/SFT"



# # 检查根目录是否存在
# if [ ! -d "$ROOT_DIR" ]; then
#     echo "错误：找不到根目录 $ROOT_DIR，请确认脚本位置是否正确。"
#     exit 1
# fi

# echo ">>> 🚀 开始执行所有任务..."

# # -----------------------------------------------------------
# # 步骤 1: 进入 SFT/MIntRec 并执行
# # -----------------------------------------------------------
# echo ">>> [1/1] 正在处理 SFT/MIntRec..."
# TARGET_1="$ZERO_SHOT_DIR/MIntRec"

# if [ -d "$TARGET_1" ]; then
#     cd "$TARGET_1" || exit 1
#     echo "    当前目录: $(pwd)"
    
#     # 执行该目录下的所有 .sh 文件
#     for script in *.sh; do
#         if [ -f "$script" ]; then
#             echo "    执行脚本: $script"
#             bash "$script"
#         fi
#     done
# else
#     echo "    警告: 目录 $TARGET_1 不存在"
# fi

# # -----------------------------------------------------------
# # 步骤 2: 进入 SFT/MIntRec2.0 并执行
# # -----------------------------------------------------------
# echo ">>> [1/2] 正在处理 SFT/MIntRec2.0..."
# TARGET_2="$ZERO_SHOT_DIR/MIntRec2.0"

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
# echo ">>> [2/1] 正在处理 Qwen3-VL/MIntRec2.0 (与SFT同级)..."
# TARGET_3="$Few-shot_DIR/MIntRec"
# if [ -d "$Few-shot_DIR" ]; then
#     cd "$TARGET_3" || exit 1
#     echo "    当前目录: $(pwd)"
    
#     # 执行该目录下的所有 .sh 文件
#     for script in *.sh; do
#         if [ -f "$script" ]; then
#             echo "    执行脚本: $script"
#             bash "$script"
#         fi
#     done
# else
#     echo "    警告: 目录 $Few-shot_DIR 不存在"
# fi


# echo ">>> [2/2] 正在处理 Qwen3-VL/MIntRec2.0 (与SFT同级)..."
# TARGET_4="$Few-shot_DIR/MIntRec2.0"
# if [ -d "$Few-shot_DIR" ]; then
#     cd "$TARGET_4" || exit 1
#     echo "    当前目录: $(pwd)"

#     # 执行该目录下的所有 .sh 文件
#     for script in *.sh; do
#         if [ -f "$script" ]; then
#             echo "    执行脚本: $script"
#             bash "$script"
#         fi
#     done
# else
#     echo "    警告: 目录 $Few-shot_DIR 不存在"
# fi


# echo ">>> [3/1] 正在处理 SFT/MIntRec2.0..."
# TARGET_5="$SFT_DIR/MIntRec"
# if [ -d "$TARGET_5" ]; then
#     cd "$TARGET_5" || exit 1
#     echo "    当前目录: $(pwd)"
    
#     # 执行该目录下的所有 .sh 文件
#     for script in *.sh; do
#         if [ -f "$script" ]; then
#             echo "    执行脚本: $script"
#             bash "$script"
#         fi
#     done
# else
#     echo "    警告: 目录 $TARGET_5 不存在"
# fi

# echo ">>> [3/2] 正在处理 SFT/MIntRec2.0..."
# TARGET_6="$SFT_DIR/MIntRec2.0"
# if [ -d "$TARGET_6" ]; then
#     cd "$TARGET_6" || exit 1
#     echo "    当前目录: $(pwd)"

#     # 执行该目录下的所有 .sh 文件
#     for script in *.sh; do
#         if [ -f "$script" ]; then
#             echo "    执行脚本: $script"
#             bash "$script"
#         fi
#     done
# else
#     echo "    警告: 目录 $SFT_DIR 不存在"
# fi


# echo ">>> ✅ 所有任务执行完毕！"




#!/bin/bash

# 1. 【核心修复】记录脚本启动时的目录
INITIAL_DIR="$(pwd)"

# 定义根目录变量 (相对路径保持不变)
ROOT_DIR="./Qwen3-8B"
# ZERO_SHOT_DIR="$ROOT_DIR/Zero-Shot"
# Few-shot_DIR="$ROOT_DIR/Few-Shot"
SFT_DIR="$ROOT_DIR/SFT"

# # 检查根目录是否存在
# if [ ! -d "$ROOT_DIR" ]; then
#     echo "错误：找不到根目录 $ROOT_DIR，请确认脚本位置是否正确。"
#     exit 1
# fi

# echo ">>> 🚀 开始执行所有任务..."

# # -----------------------------------------------------------
# # 步骤 1: Zero-Shot / MIntRec
# # -----------------------------------------------------------
# echo ">>> [1/1] 正在处理 Zero-Shot/MIntRec..."
# TARGET_1="$ZERO_SHOT_DIR/MIntRec"

# if [ -d "$TARGET_1" ]; then
#     cd "$TARGET_1" || exit 1
#     echo "    当前目录: $(pwd)"
    
#     for script in *.sh; do
#         if [ -f "$script" ]; then
#             echo "    执行脚本: $script"
#             bash "$script"
#         fi
#     done
# else
#     echo "    警告: 目录 $TARGET_1 不存在"
# fi

# # 🛑 关键：回到初始目录，重置相对路径基准
# cd "$INITIAL_DIR"

# # -----------------------------------------------------------
# # 步骤 2: Zero-Shot / MIntRec2.0
# # -----------------------------------------------------------
# echo ">>> [1/2] 正在处理 Zero-Shot/MIntRec2.0..."
# TARGET_2="$ZERO_SHOT_DIR/MIntRec2.0"

# if [ -d "$TARGET_2" ]; then
#     cd "$TARGET_2" || exit 1
#     echo "    当前目录: $(pwd)"
    
#     for script in *.sh; do
#         if [ -f "$script" ]; then
#             echo "    执行脚本: $script"
#             bash "$script"
#         fi
#     done
# else
#     echo "    警告: 目录 $TARGET_2 不存在"
# fi

# # 🛑 关键：回到初始目录
# cd "$INITIAL_DIR"

# # -----------------------------------------------------------
# # 步骤 3: Few-Shot / MIntRec
# # -----------------------------------------------------------
# echo ">>> [2/1] 正在处理 Few-Shot/MIntRec..."
# TARGET_3="$Few-shot_DIR/MIntRec"

# if [ -d "$TARGET_3" ]; then
#     cd "$TARGET_3" || exit 1
#     echo "    当前目录: $(pwd)"
    
#     for script in *.sh; do
#         if [ -f "$script" ]; then
#             echo "    执行脚本: $script"
#             bash "$script"
#         fi
#     done
# else
#     echo "    警告: 目录 $TARGET_3 不存在"
# fi

# # 🛑 关键：回到初始目录
# cd "$INITIAL_DIR"

# # -----------------------------------------------------------
# # 步骤 4: Few-Shot / MIntRec2.0
# # -----------------------------------------------------------
# echo ">>> [2/2] 正在处理 Few-Shot/MIntRec2.0..."
# TARGET_4="$Few-shot_DIR/MIntRec2.0"

# if [ -d "$TARGET_4" ]; then
#     cd "$TARGET_4" || exit 1
#     echo "    当前目录: $(pwd)"

#     for script in *.sh; do
#         if [ -f "$script" ]; then
#             echo "    执行脚本: $script"
#             bash "$script"
#         fi
#     done
# else
#     echo "    警告: 目录 $TARGET_4 不存在"
# fi

# 🛑 关键：回到初始目录
cd "$INITIAL_DIR"

# -----------------------------------------------------------
# 步骤 5: SFT / MIntRec
# -----------------------------------------------------------
echo ">>> [3/1] 正在处理 SFT/MIntRec..."
TARGET_5="$SFT_DIR/MIntRec2.0"

if [ -d "$TARGET_5" ]; then
    cd "$TARGET_5" || exit 1
    echo "    当前目录: $(pwd)"
    
    for script in *.sh; do
        if [ -f "$script" ]; then
            echo "    执行脚本: $script"
            bash "$script"
        fi
    done
else
    echo "    警告: 目录 $TARGET_5 不存在"
fi
echo ">>> [3/1] 正在处理 SFT/MIntRec..."
TARGET_5="$SFT_DIR/MIntRec"

if [ -d "$TARGET_5" ]; then
    cd "$TARGET_5" || exit 1
    echo "    当前目录: $(pwd)"
    
    for script in *.sh; do
        if [ -f "$script" ]; then
            echo "    执行脚本: $script"
            bash "$script"
        fi
    done
else
    echo "    警告: 目录 $TARGET_5 不存在"
fi
# # 🛑 关键：回到初始目录
# cd "$INITIAL_DIR"

# # ------------------------------------------------