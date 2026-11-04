python Zero-shot.py \
  --model_name ./llm_checkpoints/Qwen3-8B \
  --input_jsonl /home/<USER>/<USER>/RL-SF/ms-swift/examples/bash/MM/Qwen3-8B/Data/test_MIntRec2.0.jsonl \
  --output_dir MIntRec2.0-zero_shot_csv \
  --device cuda:0