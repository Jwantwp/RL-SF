#!/bin/bash
# ================================================================
# PIWM Stage-1 用户状态推断 — Qwen2.5-VL-7B-Instruct LoRA 微调
# ================================================================
# 数据集: stage1_user_intent.jsonl (197 条, 帧全部可用)
# 划分:   train=137 / val=19 / test=41  (7:1:2, seed=42)
# 模型:   Qwen2.5-VL-7B-Instruct
# 框架:   ms-swift (swift sft)
# ================================================================
# 超参数选择依据:
#   - 训练集 137 条，极小样本微调，需重点防过拟合
#   - 单卡 V100-32GB，无需 DeepSpeed
#   - 7B 模型 + LoRA，学习率 1e-5 保守设置
#   - freeze_vit/aligner 仅训练语言模型 LoRA 参数
#   - batch_size=1, grad_accum=4, 有效 batch=4
#     137/4 ≈ 34 steps/epoch，eval 每 epoch 一次
#   - 20 epochs 充分学习小数据集，观察 val loss 选最优 checkpoint
# ================================================================

# ==================== 路径配置 ====================

# 数据路径（已完成划分）
TRAIN_DATASET="/home/<USER>/<USER>/SX/W_M/Data_Pro/data/splits/stage1_train.jsonl"
VAL_DATASET="/home/<USER>/<USER>/SX/W_M/Data_Pro/data/splits/stage1_val.jsonl"

# 模型路径
BASE_MODEL_PATH="./llm_checkpoints/Qwen2.5-VL-7B-Instruct"

# 训练输出目录
OUTPUT_DIR="./SFT/piwm/piwm_stage1_qwen2_5_vl_7b"

# ==================== 训练配置 ====================

# 模型与模板
TEMPLATE="qwen2_5_vl"
TORCH_DTYPE="bfloat16"

# LoRA 配置
TUNER_TYPE="lora"
LORA_RANK=16
LORA_ALPHA=32
TARGET_MODULES="all-linear"

# 优化器配置
LEARNING_RATE="1e-5"
NUM_TRAIN_EPOCHS=20
PER_DEVICE_TRAIN_BATCH_SIZE=1
PER_DEVICE_EVAL_BATCH_SIZE=1
GRADIENT_ACCUMULATION_STEPS=4
WARMUP_RATIO=0.1
MAX_LENGTH=8192

# 正则化与稳定性
GRADIENT_CHECKPOINTING=true
VIT_GRADIENT_CHECKPOINTING=true
FREEZE_VIT=true
FREEZE_ALIGNER=true
PADDING_FREE=false

# 日志与保存
# 137 样本 / 1 卡 / batch 1 / accum 4 = ~34 steps/epoch
# eval/save 每 34 steps ≈ 每 epoch 一次，便于观察 val loss 曲线
EVAL_STEPS=34
SAVE_STEPS=34
LOGGING_STEPS=2
SAVE_TOTAL_LIMIT=5

# 数据加载
DATASET_NUM_PROC=2
DATALOADER_NUM_WORKERS=2

# GPU 配置（单卡 V100-32GB）
DEVICE_IDS="2"
NPROC_PER_NODE=1

# ==================== 开始训练 ====================

START_TIME=$(date +"%Y-%m-%d-%H-%M-%S")

echo "=========================================="
echo "PIWM Stage-1 SFT — Qwen2.5-VL-7B-Instruct LoRA"
echo "=========================================="
echo "开始时间:   $START_TIME"
echo "------------------------------------------"
echo "模型:       $BASE_MODEL_PATH"
echo "模板:       $TEMPLATE"
echo "训练集:     $TRAIN_DATASET (137 条)"
echo "验证集:     $VAL_DATASET (19 条)"
echo "输出目录:   $OUTPUT_DIR"
echo "------------------------------------------"
echo "GPU:        $DEVICE_IDS ($NPROC_PER_NODE 卡 V100-32GB)"
echo "Epochs:     $NUM_TRAIN_EPOCHS"
echo "Batch:      $PER_DEVICE_TRAIN_BATCH_SIZE/device × $GRADIENT_ACCUMULATION_STEPS accum = 有效 batch $((NPROC_PER_NODE * PER_DEVICE_TRAIN_BATCH_SIZE * GRADIENT_ACCUMULATION_STEPS))"
echo "LR:         $LEARNING_RATE"
echo "LoRA:       rank=$LORA_RANK, alpha=$LORA_ALPHA, target=$TARGET_MODULES"
echo "Freeze:     ViT=$FREEZE_VIT, Aligner=$FREEZE_ALIGNER"
echo "Max Length: $MAX_LENGTH"
echo "Eval/Save:  每 $EVAL_STEPS steps (~每 epoch)"
echo "=========================================="

# 导出 GPU 环境变量
export CUDA_VISIBLE_DEVICES=$DEVICE_IDS

# 执行 Swift 训练命令
# 注意: 单卡训练不使用 DeepSpeed
PYTORCH_CUDA_ALLOC_CONF='expandable_segments:True' \
IMAGE_MAX_TOKEN_NUM=1024 \
VIDEO_MAX_TOKEN_NUM=128 \
FPS_MAX_FRAMES=4 \
NPROC_PER_NODE=$NPROC_PER_NODE \
swift sft \
    --model "$BASE_MODEL_PATH" \
    --template "$TEMPLATE" \
    --dataset "$TRAIN_DATASET" \
    --val_dataset "$VAL_DATASET" \
    --tuner_type "$TUNER_TYPE" \
    --torch_dtype "$TORCH_DTYPE" \
    --output_dir "$OUTPUT_DIR" \
    --num_train_epochs "$NUM_TRAIN_EPOCHS" \
    --per_device_train_batch_size "$PER_DEVICE_TRAIN_BATCH_SIZE" \
    --per_device_eval_batch_size "$PER_DEVICE_EVAL_BATCH_SIZE" \
    --padding_free "$PADDING_FREE" \
    --learning_rate "$LEARNING_RATE" \
    --lora_rank "$LORA_RANK" \
    --lora_alpha "$LORA_ALPHA" \
    --target_modules "$TARGET_MODULES" \
    --freeze_vit "$FREEZE_VIT" \
    --freeze_aligner "$FREEZE_ALIGNER" \
    --gradient_checkpointing "$GRADIENT_CHECKPOINTING" \
    --vit_gradient_checkpointing "$VIT_GRADIENT_CHECKPOINTING" \
    --gradient_accumulation_steps "$GRADIENT_ACCUMULATION_STEPS" \
    --eval_steps "$EVAL_STEPS" \
    --save_steps "$SAVE_STEPS" \
    --save_total_limit "$SAVE_TOTAL_LIMIT" \
    --logging_steps "$LOGGING_STEPS" \
    --max_length "$MAX_LENGTH" \
    --warmup_ratio "$WARMUP_RATIO" \
    --dataset_num_proc "$DATASET_NUM_PROC" \
    --dataloader_num_workers "$DATALOADER_NUM_WORKERS"

TRAIN_END_TIME=$(date +"%Y-%m-%d-%H-%M-%S")

echo ""
echo "=========================================="
echo "训练完成"
echo "=========================================="
echo "开始时间: $START_TIME"
echo "结束时间: $TRAIN_END_TIME"
echo "输出目录: $OUTPUT_DIR"
echo "=========================================="
