# #!/bin/bash


# # --packing true \
# # ================= 基础配置 =================

# # 模型配置列表
# MODEL_NAMES=("Qwen3-VL-8B-Instruct")

#  # 模型模板映射
# declare -A TEMPLATES
# TEMPLATES["Qwen3-VL-8B-Instruct"]="qwen3_vl"



# # Conda 环境名称映射
# declare -A ENV_NAMES
# ENV_NAMES["Qwen3-VL-8B-Instruct"]="sf-sft"

# # 设备映射
# declare -A MODEL_DEVICES
# MODEL_DEVICES["Qwen3-VL-8B-Instruct"]="2"

# declare -A task_map
# task_map['Mutimodal Intent Recognition']='Mutimodal Intent Recognition'

# # ================= 开始训练循环 =================

# # export MASTER_PORT=

# START_TIME=$(date +"%Y-%m-%d-%H-%M-%S")
# echo "=========================================="
# echo "Script Start Time: $START_TIME"
# echo "=========================================="

# for MODEL_NAME in "${MODEL_NAMES[@]}"; do
#     # 基础模型路径 (Swift 支持 HF 模型名，也可写本地路径)
#     BASE_MODEL_PATH="./SFT/MIntRec2.0/v1-20260310-022314/checkpoint-3000"
    
#     DEVICE_IDS="${MODEL_DEVICES[$MODEL_NAME]}"
#     ENV_NAME="${ENV_NAMES[$MODEL_NAME]}"
#     TEMPLATE="${TEMPLATES[$MODEL_NAME]}"

#     for dataset_key in "${!task_map[@]}"; do
#         TASK_NAME="${task_map[$dataset_key]}"
        
#         TIMESTAMP=$(date +"%Y-%m-%d-%H-%M-%S")
#         # 定义输出目录，保持风格一致
#         MODEL_PATH="./SFT/MIntRec"
        
#         echo "------------------------------------------"
#         echo "[$(date)] Start training: $TASK_NAME"
#         echo "模型名称: $MODEL_NAME"
#         echo "使用显卡id: $DEVICE_IDS"
#         echo "环境名称: $ENV_NAME"
#         echo "输出路径: $MODEL_PATH"
#         echo "------------------------------------------"
#         # 导出显卡环境变量
#         export CUDA_VISIBLE_DEVICES=$DEVICE_IDS



#         # 执行 Swift 训练命令 (保持原有参数不变，仅替换输出目录变量)
#         PYTORCH_ALLOC_CONF='expandable_segments:True' \
#         IMAGE_MAX_TOKEN_NUM=1024 \
#         VIDEO_MAX_TOKEN_NUM=128 \
#         FPS_MAX_FRAMES=16 \
#         NPROC_PER_NODE=1 \
#         swift infer \
#             --adapters ./SFT/MiniCPM-V-4_5/MIntRec2.0/v0-20260314-081917/checkpoint-3000 \
#             --val_dataset /home/<USER>/<USER>/RL-SF/ms-swift/swift/Data/MIntRec2.0/test_MIntRec2.0.jsonl \
#             --max_new_tokens 2048 \
#             --temperature 0 \
#             --load_data_args true
#     done
# done

# END_TIME=$(date +"%Y-%m-%d-%H-%M-%S")
# echo "=========================================="
# echo "Script End Time: $END_TIME"
# echo "Start Time: $START_TIME"
# echo "=========================================="
#!/bin/bash

# ================= 基础配置 =================

# 模型配置列表
MODEL_NAMES=("Qwen3-VL-8B-Instruct")

# 模型模板映射
declare -A TEMPLATES
TEMPLATES["Qwen3-VL-8B-Instruct"]="qwen3_vl"

# Conda 环境名称映射
declare -A ENV_NAMES
ENV_NAMES["Qwen3-VL-8B-Instruct"]="sf-sft"

# 设备映射 (注意：值必须加引号)
declare -A MODEL_DEVICES
MODEL_DEVICES["Qwen3-VL-8B-Instruct"]="0"

declare -A task_map
task_map['Mutimodal Intent Recognition']='Mutimodal Intent Recognition'

# ================= 开始训练循环 =================
# /home/<USER>/<USER>/RL-SF/Data_Format/test_MIntRec2.0_3shot_seed42.jsonl


START_TIME=$(date +"%Y-%m-%d-%H-%M-%S")
echo "=========================================="
echo "Script Start Time: $START_TIME"
echo "=========================================="

for MODEL_NAME in "${MODEL_NAMES[@]}"; do
    # 基础模型路径
    BASE_MODEL_PATH="./SFT/MIntRec/v0-20260309-084815/checkpoint-900"
    
    DEVICE_IDS="${MODEL_DEVICES[$MODEL_NAME]}"
    ENV_NAME="${ENV_NAMES[$MODEL_NAME]}"
    TEMPLATE="${TEMPLATES[$MODEL_NAME]}"

    # 导出显卡环境变量
    export CUDA_VISIBLE_DEVICES=$DEVICE_IDS

    for dataset_key in "${!task_map[@]}"; do
        TASK_NAME="${task_map[$dataset_key]}"
        
        # 定义输出目录
        MODEL_PATH="./SFT/MIntRec"
        
        echo "------------------------------------------"
        echo "[$(date)] Start processing Task: $TASK_NAME"
        echo "模型名称: $MODEL_NAME"
        echo "使用显卡id: $DEVICE_IDS"
        echo "------------------------------------------"

        # --- 修改部分开始 ---
        # 定义初始温度
        TEMPERATURE=0.0
        
        # 随机种子循环
        for SEED in 0 1 2 3 4; do
            TIMESTAMP=$(date +"%Y-%m-%d-%H-%M-%S")
            
            echo "====== 开始种子 $SEED 的实验 (温度: $TEMPERATURE) ======"
            
            # 执行 Swift 推理命令
            PYTORCH_ALLOC_CONF='expandable_segments:True' \
            IMAGE_MAX_TOKEN_NUM=1024 \
            VIDEO_MAX_TOKEN_NUM=128 \
            FPS_MAX_FRAMES=16 \
            NPROC_PER_NODE=1 \
            swift infer \
                --model ./llm_checkpoints/MiniCPM-V-4_5-8B \
                --val_dataset /home/<USER>/<USER>/RL-SF/Data_Format/test_MIntRec2.0_3shot_seed42.jsonl \
                --seed $SEED \
                --max_new_tokens 2048 \
                --temperature $TEMPERATURE
                
            echo "====== 种子 $SEED 执行完毕 ======"

            # 温度增加 0.05 (使用 bc 进行浮点运算)
            TEMPERATURE=$(echo "$TEMPERATURE + 0.05" | bc)
        done
        # --- 修改部分结束 ---

    done
done

END_TIME=$(date +"%Y-%m-%d-%H-%M-%S")
echo "=========================================="
echo "Script End Time: $END_TIME"
echo "Start Time: $START_TIME"
echo "=========================================="