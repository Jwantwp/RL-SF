# from modelscope import AutoModelForCausalLM, AutoTokenizer

# model_name = "./llm_checkpoints/Qwen3-8B"

# # load the tokenizer and the model
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(
#     model_name,
#     torch_dtype="auto",
#     device_map="cuda:2"
# )

# # prepare the model input
# prompt = "Give me a short introduction to large language model."
# messages = [
#     {"role": "user", "content": prompt}
# ]
# text = tokenizer.apply_chat_template(
#     messages,
#     tokenize=False,
#     add_generation_prompt=True,
#     enable_thinking=False # Switches between thinking and non-thinking modes. Default is True.
# )
# model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

# # conduct text completion
# generated_ids = model.generate(
#     **model_inputs,
#     max_new_tokens=32768
# )
# output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist() 

# # parsing thinking content
# try:
#     # rindex finding 151668 (</think>)
#     index = len(output_ids) - output_ids[::-1].index(151668)
# except ValueError:
#     index = 0

# # thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
# content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

# print("thinking content:", thinking_content)
# print("content:", content)













import os
import json
import random
import numpy as np
import torch
from tqdm import tqdm
from modelscope import AutoModelForCausalLM, AutoTokenizer

model_name = "./llm_checkpoints/Qwen3-8B"
input_jsonl = "input.jsonl"
output_dir = "outputs_by_seed"
os.makedirs(output_dir, exist_ok=True)

# 你要跑的 5 个随机种子
seeds = [0, 1, 2, 3, 4]

# 生成参数
MAX_NEW_TOKENS = 1024   # 你原来是 32768，通常太大了，按需要改
TEMPERATURE = 0.7
TOP_P = 0.8

def set_all_seeds(seed: int):
    """设置所有常见随机种子"""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

def build_messages(item: dict):
    """
    根据 jsonl 每行内容构造 messages
    优先使用 messages 字段，否则使用 prompt/question/input 字段
    """
    if "messages" in item and isinstance(item["messages"], list):
        return item["messages"]

    prompt = item.get("prompt") or item.get("question") or item.get("input")
    if prompt is None:
        raise ValueError(
            "每行 JSON 必须包含 'messages' 或 'prompt'/'question'/'input' 字段之一"
        )
    return [{"role": "user", "content": prompt}]

def parse_output(tokenizer, output_ids):
    """
    解析 thinking_content 和最终 content
    如果没有 </think>，则 thinking_content 为空，content 为全部输出
    """
    try:
        # 151668 是 </think> 的 token id（你原代码里就是这么写的）
        index = len(output_ids) - output_ids[::-1].index(151668)
        thinking_content = tokenizer.decode(
            output_ids[:index], skip_special_tokens=True
        ).strip("\n")
        content = tokenizer.decode(
            output_ids[index:], skip_special_tokens=True
        ).strip("\n")
    except ValueError:
        thinking_content = ""
        content = tokenizer.decode(
            output_ids, skip_special_tokens=True
        ).strip("\n")

    return thinking_content, content

# 1) 加载 tokenizer 和 model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="cuda:2"
)
model.eval()

# 2) 依次跑 5 个 seed
for seed in seeds:
    output_jsonl = os.path.join(output_dir, f"result_seed_{seed}.jsonl")
    print(f"\n===== Running seed = {seed} =====")
    print(f"Output file: {output_jsonl}")

    with open(input_jsonl, "r", encoding="utf-8") as fin, \
         open(output_jsonl, "w", encoding="utf-8") as fout:

        for line_idx, line in enumerate(tqdm(fin, desc=f"seed={seed}"), start=1):
            line = line.strip()
            if not line:
                continue

            item = json.loads(line)

            try:
                messages = build_messages(item)

                text = tokenizer.apply_chat_template(
                    messages,
                    tokenize=False,
                    add_generation_prompt=True,
                    enable_thinking=False  # 如果要思维链可改成 True
                )

                model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

                # 这里设置 seed。这样每条样本在同一个 seed 下都是可复现的
                set_all_seeds(seed)

                with torch.no_grad():
                    generated_ids = model.generate(
                        **model_inputs,
                        max_new_tokens=MAX_NEW_TOKENS,
                        do_sample=True,        # 非常重要：要让 seed 生效，必须开启采样
                        temperature=TEMPERATURE,
                        top_p=TOP_P,
                    )

                output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
                thinking_content, content = parse_output(tokenizer, output_ids)

                result = {
                    **item,
                    "seed": seed,
                    "thinking_content": thinking_content,
                    "content": content,
                }

                fout.write(json.dumps(result, ensure_ascii=False) + "\n")

            except Exception as e:
                error_item = {
                    **item,
                    "seed": seed,
                    "error": str(e),
                    "line_idx": line_idx,
                }
                fout.write(json.dumps(error_item, ensure_ascii=False) + "\n")