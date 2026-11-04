#!/bin/bash

# 模型配置列表
MODEL_NAMES=("InternVL-3.5-Instruct")


 # 模型模板映射
declare -A TEMPLATES
TEMPLATES["InternVL-3.5-Instruct"]="internvl3_5"



# Conda 环境名称映射
declare -A ENV_NAMES
ENV_NAMES["InternVL-3.5-Instruct"]="sf-sft"


# 设备映射
declare -A MODEL_DEVICES
MODEL_DEVICES["InternVL-3.5-Instruct"]="0"



declare -A task_map
task_map['Mutimodal Sentiment Analysis']='Mutimodal Sentiment Analysis'


# ================= 开始训练循环 =================

START_TIME=$(date +"%Y-%m-%d-%H-%M-%S")
echo "=========================================="
echo "Script Start Time: $START_TIME"
echo "=========================================="
export MASTER_PORT=29504
for MODEL_NAME in "${MODEL_NAMES[@]}"; do
    # 基础模型路径 (Swift 支持 HF 模型名，也可写本地路径)
    BASE_MODEL_PATH="./llm_checkpoints/InternVL3_5-8B-Instruct"
    
    DEVICE_IDS="${MODEL_DEVICES[$MODEL_NAME]}"
    ENV_NAME="${ENV_NAMES[$MODEL_NAME]}"
    TEMPLATE="${TEMPLATES[$MODEL_NAME]}"

    for dataset_key in "${!task_map[@]}"; do
        TASK_NAME="${task_map[$dataset_key]}"
        
        TIMESTAMP=$(date +"%Y-%m-%d-%H-%M-%S")
        # 定义输出目录，保持风格一致
        MODEL_PATH="./SFT/InternVL/MOSI-CoT"


        
        echo "------------------------------------------"
        echo "[$(date)] Start training: $TASK_NAME"
        echo "模型名称: $MODEL_NAME"
        echo "使用显卡id: $DEVICE_IDS"
        echo "环境名称: $ENV_NAME"
        echo "输出路径: $MODEL_PATH"
        echo "------------------------------------------"
        # 导出显卡环境变量
        export CUDA_VISIBLE_DEVICES=$DEVICE_IDS

        #// "attn_implementation": "flash_attention_2",

        # 执行 Swift 训练命令 (保持原有参数不变，仅替换输出目录变量)
        PYTORCH_CUDA_ALLOC_CONF='expandable_segments:True' \
        IMAGE_MAX_TOKEN_NUM=1024 \
        VIDEO_MAX_TOKEN_NUM=128 \
        FPS_MAX_FRAMES=8 \
        NPROC_PER_NODE=1 \
        swift sft \
            --model $BASE_MODEL_PATH \
            --template $TEMPLATE \
            --dataset /home/<USER>/<USER>/RL-SF/Data_Format/CoT/mosi_train.json \
            --val_dataset /home/<USER>/<USER>/RL-SF/Data_Format/CoT/mosi_dev.json \
            --tuner_type lora \
            --output_dir $MODEL_PATH \
            --num_train_epochs 4 \
            --per_device_train_batch_size 2 \
            --per_device_eval_batch_size 2 \
            --padding_free false \
            --learning_rate 5e-5 \
            --lora_rank 8 \
            --lora_alpha 32 \
            --target_modules all-linear \
            --freeze_vit true \
            --freeze_aligner true \
            --gradient_checkpointing true \
            --vit_gradient_checkpointing false \
            --gradient_accumulation_steps 2 \
            --eval_steps 100 \
            --save_steps 100 \
            --logging_steps 5 \
            --max_length 8192 \
            --warmup_ratio 0.1 \
            --deepspeed zero2 \
            --dataset_num_proc 4 \
            --dataloader_num_workers 4
    done
done

END_TIME=$(date +"%Y-%m-%d-%H-%M-%S")
echo "=========================================="
echo "Script End Time: $END_TIME"
echo "Start Time: $START_TIME"
echo "=========================================="
