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
# MODEL_DEVICES["Qwen3-VL-8B-Instruct"]="0"

# declare -A task_map
# task_map['Mutimodal Intent Recognition']='Mutimodal Intent Recognition'

# # ================= 开始训练循环 =================



# START_TIME=$(date +"%Y-%m-%d-%H-%M-%S")
# echo "=========================================="
# echo "Script Start Time: $START_TIME"
# echo "=========================================="
# os.environ['FPS_MAX_FRAMES'] = '4'
# os.environ['FPS_MIN_FRAMES'] = '0'
# for MODEL_NAME in "${MODEL_NAMES[@]}"; do
#     # 基础模型路径 (Swift 支持 HF 模型名，也可写本地路径)
#     BASE_MODEL_PATH="./llm_checkpoints/Qwen3-VL-8B-Instruct"
    
#     DEVICE_IDS="${MODEL_DEVICES[$MODEL_NAME]}"
#     ENV_NAME="${ENV_NAMES[$MODEL_NAME]}"
#     TEMPLATE="${TEMPLATES[$MODEL_NAME]}"

#     for dataset_key in "${!task_map[@]}"; do
#         TASK_NAME="${task_map[$dataset_key]}"
        
#         TIMESTAMP=$(date +"%Y-%m-%d-%H-%M-%S")
#         # 定义输出目录，保持风格一致
#         MODEL_PATH="./SFT/Qwen3-VL_Instruct/Anno-Client-CoT"
        
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
#         PYTORCH_CUDA_ALLOC_CONF='expandable_segments:True' \
#         IMAGE_MAX_TOKEN_NUM=1024 \
#         VIDEO_MAX_TOKEN_NUM=64 \
#         FPS_MAX_FRAMES=8 \
#         FPS_MIN_FRAME=0 \
#         NPROC_PER_NODE=1 \
#         swift sft \
#             --model $BASE_MODEL_PATH \
#             --template $TEMPLATE \
#             --dataset /home/<USER>/<USER>/RL-SF/Data_Format/CoT/annomi_client_train_clean.json \
#             --val_dataset /home/<USER>/<USER>/RL-SF/Data_Format/CoT/annomi_client_dev_clean.json \
#             --tuner_type lora \
#             --torch_dtype bfloat16 \
#             --output_dir $MODEL_PATH \
#             --num_train_epochs 4 \
#             --per_device_train_batch_size 2 \
#             --per_device_eval_batch_size 2 \
#             --padding_free false \
#             --learning_rate 2e-5 \
#             --lora_rank 16 \
#             --lora_alpha 32 \
#             --target_modules all-linear \
#             --freeze_vit true \
#             --freeze_aligner true \
#             --gradient_checkpointing true \
#             --vit_gradient_checkpointing false \
#             --gradient_accumulation_steps 2 \
#             --eval_steps 100 \
#             --save_steps 100 \
#             --logging_steps 5 \
#             --max_length 8192 \
#             --warmup_ratio 0.1 \
#             --deepspeed zero2 \
#             --dataset_num_proc 4 \
#             --dataloader_num_workers 4
#     done
# done

# END_TIME=$(date +"%Y-%m-%d-%H-%M-%S")
# echo "=========================================="
# echo "Script End Time: $END_TIME"
# echo "Start Time: $START_TIME"
# echo "=========================================="
#!/bin/bash


# --packing true \
# ================= 基础配置 =================

# 模型配置列表
MODEL_NAMES=("MiniCPM-V-4_5")

 # 模型模板映射
declare -A TEMPLATES
TEMPLATES["MiniCPM-V-4_5"]="minicpmv4_5"



# Conda 环境名称映射
declare -A ENV_NAMES
ENV_NAMES["MiniCPM-V-4_5"]="sf-sft"

# 设备映射
declare -A MODEL_DEVICES
MODEL_DEVICES["MiniCPM-V-4_5"]="1,2"

declare -A task_map
task_map['Mutimodal Intent Recognition']='Mutimodal Intent Recognition'



# ================= 开始训练循环 =================
START_TIME=$(date +"%Y-%m-%d-%H-%M-%S")
echo "=========================================="
echo "Script Start Time: $START_TIME"
echo "=========================================="

for MODEL_NAME in "${MODEL_NAMES[@]}"; do
    # 基础模型路径 (Swift 支持 HF 模型名，也可写本地路径)
    BASE_MODEL_PATH="./llm_checkpoints/MiniCPM-V-4_5-8B"
    
    DEVICE_IDS="${MODEL_DEVICES[$MODEL_NAME]}"
    ENV_NAME="${ENV_NAMES[$MODEL_NAME]}"
    TEMPLATE="${TEMPLATES[$MODEL_NAME]}"

    for dataset_key in "${!task_map[@]}"; do
        TASK_NAME="${task_map[$dataset_key]}"
        
        TIMESTAMP=$(date +"%Y-%m-%d-%H-%M-%S")

        # 定义输出目录，保持风格一致
        MODEL_PATH="./SFT/MiniCPM-V-4_5/AnnoMi-CoT"
        
        echo "------------------------------------------"
        echo "[$(date)] Start training: $TASK_NAME"
        echo "模型名称: $MODEL_NAME"
        echo "使用显卡id: $DEVICE_IDS"
        echo "环境名称: $ENV_NAME"
        echo "输出路径: $MODEL_PATH"
        echo "------------------------------------------"

        # 导出显卡环境变量
        export CUDA_VISIBLE_DEVICES=$DEVICE_IDS



        # 执行 Swift 训练命令 (保持原有参数不变，仅替换输出目录变量)
        PYTORCH_CUDA_ALLOC_CONF='expandable_segments:True' \
        IMAGE_MAX_TOKEN_NUM=512 \
        VIDEO_MAX_TOKEN_NUM=64 \
        FPS_MAX_FRAMES=8 \
        NPROC_PER_NODE=2 \
        swift sft \
            --model $BASE_MODEL_PATH \
            --model_type minicpmv4_5 \
            --template $TEMPLATE \
            --enable_thinking false \
            --dataset /home/<USER>/<USER>/RL-SF/Data_Format/CoT/annomi_client_train_clean.json \
            --val_dataset /home/<USER>/<USER>/RL-SF/Data_Format/CoT/annomi_client_dev_clean.json \
            --tuner_type lora \
            --torch_dtype bfloat16 \
            --output_dir $MODEL_PATH \
            --num_train_epochs 3 \
            --per_device_train_batch_size 1 \
            --per_device_eval_batch_size 1 \
            --padding_free false \
            --learning_rate 2e-5 \
            --lora_rank 16 \
            --lora_alpha 32 \
            --target_modules all-linear \
            --freeze_vit true \
            --freeze_aligner true \
            --gradient_checkpointing true \
            --vit_gradient_checkpointing false \
            --gradient_accumulation_steps 1 \
            --eval_steps 600 \
            --save_steps 600 \
            --logging_steps 5 \
            --max_length 8192 \
            --warmup_ratio 0.1 \
            --dataset_num_proc 4 \
            --dataloader_num_workers 4
    done
done

END_TIME=$(date +"%Y-%m-%d-%H-%M-%S")
echo "=========================================="
echo "Script End Time: $END_TIME"
echo "Start Time: $START_TIME"
echo "=========================================="
