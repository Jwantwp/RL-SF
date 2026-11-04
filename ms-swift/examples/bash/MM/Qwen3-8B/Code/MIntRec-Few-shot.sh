python Few-shot.py \
  --model_name ./llm_checkpoints/Qwen3-8B \
  --input_jsonl /home/<USER>/<USER>/RL-SF/ms-swift/examples/bash/MM/Qwen3-8B/Data/test_MIntRec_3shot_seed42.jsonl \
  --output_dir MIntRec-few_shot_csv \
  --device cuda:0