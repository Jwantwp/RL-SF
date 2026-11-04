#!/bin/bash

# 定义要执行的三个脚本文件的路径
# 请确保将这些路径替换为你实际的脚本路径
SCRIPT1="/home/<USER>/<USER>/RL-SF/ms-swift/examples/bash/MM/Qwen3-8B/Code/MIntRec-Zero-shot.sh"
SCRIPT2="/home/<USER>/<USER>/RL-SF/ms-swift/examples/bash/MM/Qwen3-8B/Code/MIntRec2.0-Zero-shot.sh"


SCRIPT3="/home/<USER>/<USER>/RL-SF/ms-swift/examples/bash/MM/Qwen3-8B/Code/MIntRec-Few-shot.sh"

SCRIPT4="/home/<USER>/<USER>/RL-SF/ms-swift/examples/bash/MM/Qwen3-8B/Code/MIntRec2.0-Few-shot.sh"



echo "开始执行任务..."

# 执行第一个脚本
echo "正在执行: $SCRIPT1"
if bash "$SCRIPT1"; then
    echo "$SCRIPT1 执行成功，等待 15 秒..."
    sleep 15
else
    echo "$SCRIPT1 执行失败，停止后续任务。"
    exit 1
fi

# 执行第二个脚本
echo "正在执行: $SCRIPT2"
if bash "$SCRIPT2"; then
    echo "$SCRIPT2 执行成功，等待 15 秒..."
    sleep 15
else
    echo "$SCRIPT2 执行失败，停止后续任务。"
    exit 1
fi

# 执行第二个脚本
echo "正在执行: $SCRIPT3"
if bash "$SCRIPT3"; then
    echo "$SCRIPT3 执行成功，等待 15 秒..."
    sleep 15
else
    echo "$SCRIPT3 执行失败，停止后续任务。"
    exit 1
fi

# 执行第二个脚本
echo "正在执行: $SCRIPT4"
if bash "$SCRIPT4"; then
    echo "$SCRIPT4 执行成功，等待 15 秒..."
    sleep 15
else
    echo "$SCRIPT4 执行失败，停止后续任务。"
    exit 1
fi

