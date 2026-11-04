#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
import csv
import random
import argparse
from typing import Optional, Dict, Any, List

import numpy as np
import torch
from tqdm import tqdm
from modelscope import AutoModelForCausalLM, AutoTokenizer


LABELS = [
    "Complain", "Praise", "Apologise", "Thank", "Criticize",
    "Agree", "Taunt", "Flaunt", "Joke", "Oppose",
    "Comfort", "Care", "Inform", "Advise", "Arrange",
    "Introduce", "Leave", "Prevent", "Greet", "Ask for help"
]
LABEL_MAP = {x.lower(): x for x in LABELS}


def set_all_seeds(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)

    if hasattr(torch.backends, "cudnn"):
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def extract_label(text: str) -> Optional[str]:
    if text is None:
        return None

    text = str(text).strip()
    if not text:
        return None

    # 优先匹配 "intent: xxx"
    match = re.search(r"intent\s*:\s*(.+)", text, flags=re.IGNORECASE | re.DOTALL)
    candidate = match.group(1).strip() if match else text

    candidate = candidate.splitlines()[0].strip()
    candidate = candidate.strip(" \t\r\n'\"`[](){}")
    candidate = re.sub(r"\s+", " ", candidate)
    candidate_lower = candidate.lower()

    if candidate_lower in LABEL_MAP:
        return LABEL_MAP[candidate_lower]

    for label in LABELS:
        if candidate_lower.startswith(label.lower()):
            return label

    lower_text = text.lower()
    hits = [label for label in LABELS if label.lower() in lower_text]
    if len(hits) == 1:
        return hits[0]

    return None


def move_to_device(batch: Dict[str, torch.Tensor], device: str) -> Dict[str, torch.Tensor]:
    return {k: v.to(device) for k, v in batch.items()}


def build_zero_shot_input_and_gold(item: Dict[str, Any]) -> (List[Dict[str, str]], str):
    """
    Zero-shot 格式：
    {
      "messages": [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "intent: Inform"}
      ]
    }
    """
    if "messages" not in item or not isinstance(item["messages"], list):
        raise ValueError("样本缺少 messages 字段，或 messages 不是 list")

    messages = item["messages"]
    if len(messages) < 2:
        raise ValueError("Zero-shot 样本至少需要 2 条消息")

    if messages[-1].get("role") != "assistant":
        raise ValueError("Zero-shot 样本最后一条必须是 assistant，作为 gold")

    input_messages = messages[:-1]
    gold_answer = str(messages[-1].get("content", "")).strip()
    return input_messages, gold_answer


def apply_chat_template_safe(tokenizer, messages: List[Dict[str, str]]) -> str:
    try:
        return tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False
        )
    except TypeError:
        return tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )


def generate_one(
    model,
    tokenizer,
    messages: List[Dict[str, str]],
    device: str,
    max_new_tokens: int,
    greedy: bool,
    temperature: float,
    top_p: float,
) -> str:
    text = apply_chat_template_safe(tokenizer, messages)
    model_inputs = tokenizer(text, return_tensors="pt")
    model_inputs = move_to_device(model_inputs, device)

    gen_kwargs = {
        "max_new_tokens": max_new_tokens,
        "do_sample": not greedy,
        "pad_token_id": tokenizer.pad_token_id if tokenizer.pad_token_id is not None else tokenizer.eos_token_id,
        "eos_token_id": tokenizer.eos_token_id,
    }

    if not greedy:
        gen_kwargs["temperature"] = temperature
        gen_kwargs["top_p"] = top_p

    with torch.inference_mode():
        generated_ids = model.generate(**model_inputs, **gen_kwargs)

    new_token_ids = generated_ids[0][model_inputs["input_ids"].shape[1]:]
    output_text = tokenizer.decode(new_token_ids, skip_special_tokens=True).strip()
    return output_text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_name", type=str, required=True)
    parser.add_argument("--input_jsonl", type=str, required=True)
    parser.add_argument("--output_dir", type=str, required=True)
    parser.add_argument("--device", type=str, default="cuda:0")
    parser.add_argument("--id_field", type=str, default="id", help="样本 id 字段名；若不存在则自动用行号")
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2, 3, 4])
    parser.add_argument("--max_new_tokens", type=int, default=16)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top_p", type=float, default=0.8)
    parser.add_argument("--greedy", action="store_true", help="贪心解码；若开启，不同 seed 基本不会影响结果")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)

    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        torch_dtype="auto",
        device_map={"": args.device}
    )
    model.eval()

    for seed in args.seeds:
        print(f"\n========== Zero-shot | seed={seed} ==========")
        set_all_seeds(seed)

        output_csv = os.path.join(args.output_dir, f"zero_shot_seed_{seed}.csv")

        total = 0
        correct = 0
        invalid = 0

        with open(args.input_jsonl, "r", encoding="utf-8") as fin, \
             open(output_csv, "w", encoding="utf-8-sig", newline="") as fout:

            writer = csv.writer(fout)
            writer.writerow(["id", "gold", "pred"])

            for idx, line in enumerate(tqdm(fin, desc=f"seed={seed}"), start=1):
                line = line.strip()
                if not line:
                    continue

                try:
                    item = json.loads(line)
                    sample_id = item.get(args.id_field, idx)

                    input_messages, gold_answer = build_zero_shot_input_and_gold(item)

                    prediction_raw = generate_one(
                        model=model,
                        tokenizer=tokenizer,
                        messages=input_messages,
                        device=args.device,
                        max_new_tokens=args.max_new_tokens,
                        greedy=args.greedy,
                        temperature=args.temperature,
                        top_p=args.top_p,
                    )

                    gold_label = extract_label(gold_answer)
                    pred_label = extract_label(prediction_raw)

                    if pred_label is None:
                        pred_label = ""

                    writer.writerow([sample_id, gold_label or "", pred_label])

                    total += 1
                    if gold_label == pred_label:
                        correct += 1
                    if pred_label == "":
                        invalid += 1

                except Exception as e:
                    print(f"[seed={seed}] line {idx} error: {e}")

        acc = correct / total if total > 0 else 0.0
        print(f"seed={seed} | total={total} | correct={correct} | invalid={invalid} | acc={acc:.4f}")
        print(f"saved to: {output_csv}")


if __name__ == "__main__":
    main()