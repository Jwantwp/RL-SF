# Since `output/vx-xxx/checkpoint-xxx` is trained by swift and contains an `args.json` file,
# there is no need to explicitly set `--model`, `--system`, etc., as they will be automatically read.
swift export \
    --adapters ./SFT/Study_3/MIntRec2.0/v0-20260409-142945/checkpoint-2000 \
    --merge_lora true
