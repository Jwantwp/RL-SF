# import csv
# import os
# import json




# import json
# import os
# # ['greeting', 'question', 'answer', 'statement-opinion', 'statement-non-opinion', 'apology',
# #                          'command', 'agreement', 'disagreement', 'acknowledge', 'backchannel', 'others']
# # ['greeting', 'question', 'answer', 'statement-opinion', 'statement-non-opinion', 'apology',
# #                          'command', 'agreement', 'disagreement', 'acknowledge', 'backchannel', 'others']

# # f"You are presented with a video in which the speaker says: i definitely will buy it Based on the text, video, and audio content, what is the sentiment of this speaker?\nThe candidate labels for sentiment are: {labels}. Respond in the format: 'sentiment: [label]'. Only one label should be provided."
# # prompt = f"<video>You are presented with a video in which the speaker says: {row[1]}  Based on the text, video, and audio content, what is the dialogue act of this speaker?\nThe candidate labels for dialogue act are: {labels}. Respond in the format: 'dialogue act: [label]'. Only one label should be provided."
            

# label_map={
#     'MIntRec':'[Complain, Praise, Apologise, Thank, Criticize, Agree, Taunt, Flaunt, Joke, Oppose, Comfort, Care, Inform, Advise, Arrange, Introduce, Leave, Prevent, Greet, Ask for help]',
#     'MIntRec2.0':'[Acknowledge, Advise, Agree, Apologise, Arrange, Ask for help, Asking for opinions, Care, Comfort, Complain, Confirm, Criticize, Doubt, Emphasize, Explain, Flaunt, Greet, Inform, Introduce, Invite, Joke, Leave, Oppose, Plan, Praise, Prevent, Refuse, Taunt, Thank, Warn]',
# }

# label_map={
#     'MIntRec':'[Complain, Praise, Apologise, Thank, Criticize, Agree, Taunt, Flaunt, Joke, Oppose, Comfort, Care, Inform, Advise, Arrange, Introduce, Leave, Prevent, Greet, Ask for help]',
#     'MIntRec2.0':'[Acknowledge, Advise, Agree, Apologise, Arrange, Ask for help, Asking for opinions, Care, Comfort, Complain, Confirm, Criticize, Doubt, Emphasize, Explain, Flaunt, Greet, Inform, Introduce, Invite, Joke, Leave, Oppose, Plan, Praise, Prevent, Refuse, Taunt, Thank, Warn]',
# }


# def load_swift_data(file_name,Dataset):
    
#     tsv_file = os.path.join(base_path, file_name)
#     # 加载jsonl文件
#     new_name=file_name.split(".")[0]
#     labels=label_map[Dataset]
    
#     new_jsonl_file = open(f"{new_name}_{Dataset}.jsonl", 'w', encoding='utf-8')
#     with open(tsv_file, 'r', encoding='utf-8') as f:
#         print(f"加载文件: {tsv_file}")
#         # 逐行读取tsv文件
#         csv_reader = csv.reader(f, delimiter='\t')
#         next(csv_reader)
#         for row in csv_reader:
#             video_path = f"./data/Intent_Data/MIntRec2.0/video/{row[0]}"
#             audio_path = f"./data/Intent_Data/MIntRec2.0/audio/{row[0].split('.')[0]}.wav"
#             prompt = f"<video><audio>You are presented with a video in which the speaker says: {row[1]} ased on the text, video, and audio content, what is the intent of this speaker?\nThe candidate labels for intent are:  {labels}. Respond in the format: 'intent: [label]'. Only one label should be provided."
#             answer = f"intent: {row[2].strip()}"

#             item = {}
#             item["messages"] = []
#             item["messages"].append({"role": "user", "content": f"{prompt}"})
#             item["messages"].append({"role": "assistant", "content": f"{answer}"})
            
            
#             item["videos"] = []
#             item["videos"].append(video_path)
#             item["audios"] = []
#             item["audios"].append(audio_path)
 
            
#             json.dump(item, new_jsonl_file, ensure_ascii=False)
#             new_jsonl_file.write('\n')
    

# base_path = "/home/<USER>/<USER>/ACL/tsv/MIntRec2.0"
# file_names = ['train.tsv', 'test.tsv', 'dev.tsv']
# for file_name in file_names:
#     load_swift_data(file_name,'MIntRec2.0')
#     print(f"处理完成: {file_name}")




# # import os
# # import csv
# # import json
# # import random
# # from typing import List, Dict


# # label_map = {
# #     'MIntRec': '[Complain, Praise, Apologise, Thank, Criticize, Agree, Taunt, Flaunt, Joke, Oppose, Comfort, Care, Inform, Advise, Arrange, Introduce, Leave, Prevent, Greet, Ask for help]',
# #     'MIntRec2.0': '[Acknowledge, Advise, Agree, Apologise, Arrange, Ask for help, Asking for opinions, Care, Comfort, Complain, Confirm, Criticize, Doubt, Emphasize, Explain, Flaunt, Greet, Inform, Introduce, Invite, Joke, Leave, Oppose, Plan, Praise, Prevent, Refuse, Taunt, Thank, Warn]',
# # }

# # # 这里按你的实际视频路径修改
# # video_root_map = {
# #     'MIntRec': './data/Intent_Data/MIntRec/video',
# #     'MIntRec2.0': './data/Intent_Data/MIntRec2.0/video',
# # }


# # def build_prompt(utterance: str, dataset: str) -> str:
# #     labels = label_map[dataset]
# #     prompt = (
# #         f"<video>You are presented with a video in which the speaker says: {utterance} "
# #         f"Based on the text, video, and audio content, what is the intent of this speaker?\n"
# #         f"The candidate labels for intent are: {labels}. "
# #         f"Respond in the format: 'intent: [label]'. Only one label should be provided."
# #     )
# #     return prompt


# # def load_tsv_examples(base_path: str, file_name: str, dataset: str) -> List[Dict]:
# #     tsv_file = os.path.join(base_path, file_name)
# #     video_root = video_root_map[dataset]

# #     examples = []
# #     with open(tsv_file, 'r', encoding='utf-8') as f:
# #         print(f"加载文件: {tsv_file}")
# #         csv_reader = csv.reader(f, delimiter='\t')
# #         next(csv_reader, None)  # 跳过表头

# #         for line_idx, row in enumerate(csv_reader, start=2):
# #             if len(row) < 3:
# #                 print(f"[Warning] 第 {line_idx} 行字段不足，已跳过: {row}")
# #                 continue

# #             video_name = row[0].strip()
# #             utterance = row[1].strip()
# #             label = row[2].strip()

# #             video_path = os.path.join(video_root, video_name)
# #             prompt = build_prompt(utterance, dataset)
# #             answer = f"intent: {label}"

# #             examples.append({
# #                 "video_path": video_path,
# #                 "prompt": prompt,
# #                 "answer": answer,
# #                 "label": label,
# #                 "utterance": utterance,
# #                 "video_name": video_name,
# #             })

# #     return examples


# # def write_standard_jsonl(examples: List[Dict], output_file: str) -> None:
# #     """用于 train/dev，保持原来的单轮监督格式"""
# #     with open(output_file, 'w', encoding='utf-8') as fout:
# #         for ex in examples:
# #             item = {
# #                 "messages": [
# #                     {"role": "user", "content": ex["prompt"]},
# #                     {"role": "assistant", "content": ex["answer"]}
# #                 ],
# #                 "videos": [ex["video_path"]]
# #             }
# #             json.dump(item, fout, ensure_ascii=False)
# #             fout.write('\n')

# #     print(f"写入完成: {output_file}")


# # def sample_unique_support_indices(
# #     train_size: int,
# #     num_shots: int,
# #     rng: random.Random,
# #     used_combinations: set,
# #     max_try: int = 1000
# # ) -> tuple:
# #     """
# #     为每个测试样本尽量采样不同的 few-shot 支持集。
# #     这里用“有序tuple”做唯一性约束，所以顺序不同也算不同 prompt。
# #     """
# #     if train_size < num_shots:
# #         raise ValueError(f"训练样本数量不足，无法采样 {num_shots}-shot。当前 train_size={train_size}")

# #     for _ in range(max_try):
# #         indices = tuple(rng.sample(range(train_size), num_shots))
# #         if indices not in used_combinations:
# #             used_combinations.add(indices)
# #             return indices

# #     # 如果组合太多次都撞了，就直接返回一个随机结果
# #     return tuple(rng.sample(range(train_size), num_shots))


# # def write_test_jsonl_with_fewshot(
# #     test_examples: List[Dict],
# #     train_examples: List[Dict],
# #     output_file: str,
# #     num_shots: int = 3,
# #     seed: int = 42
# # ) -> None:
# #     """
# #     为 test 集构造 few-shot 推理格式：
# #     [train-example-1 user]
# #     [train-example-1 assistant]
# #     [train-example-2 user]
# #     [train-example-2 assistant]
# #     [train-example-3 user]
# #     [train-example-3 assistant]
# #     [test user]
# #     videos 按照所有 <video> 出现顺序排列
# #     """
# #     rng = random.Random(seed)
# #     used_combinations = set()

# #     with open(output_file, 'w', encoding='utf-8') as fout:
# #         for test_idx, test_ex in enumerate(test_examples):
# #             support_indices = sample_unique_support_indices(
# #                 train_size=len(train_examples),
# #                 num_shots=num_shots,
# #                 rng=rng,
# #                 used_combinations=used_combinations
# #             )

# #             item = {
# #                 "messages": [],
# #                 "videos": [],
# #                 # 这个字段用于后续评测；如果你的框架不允许额外字段，可以删掉
# #                 "gold_answer": test_ex["answer"]
# #             }

# #             # 加入 few-shot 的 train 样例
# #             for s_idx in support_indices:
# #                 support_ex = train_examples[s_idx]
# #                 item["messages"].append({
# #                     "role": "user",
# #                     "content": support_ex["prompt"]
# #                 })
# #                 item["messages"].append({
# #                     "role": "assistant",
# #                     "content": support_ex["answer"]
# #                 })
# #                 item["videos"].append(support_ex["video_path"])

# #             # 最后加入当前 test query（不放答案，留给模型推理）
# #             item["messages"].append({
# #                 "role": "user",
# #                 "content": test_ex["prompt"]
# #             })
# #             item["videos"].append(test_ex["video_path"])

# #             json.dump(item, fout, ensure_ascii=False)
# #             fout.write('\n')

# #     print(f"写入完成: {output_file}")


# # if __name__ == "__main__":
# #     dataset = "MIntRec2.0"
# #     base_path = "/home/<USER>/<USER>/ACL/tsv/MIntRec2.0"

# #     random_seed = 42
# #     num_shots = 3

# #     # 读取数据
# #     train_examples = load_tsv_examples(base_path, "train.tsv", dataset)
# #     dev_examples = load_tsv_examples(base_path, "dev.tsv", dataset)
# #     test_examples = load_tsv_examples(base_path, "test.tsv", dataset)

# #     # 1) train/dev 保持原始单样本监督格式
# #     write_standard_jsonl(train_examples, f"train_{dataset}.jsonl")
# #     write_standard_jsonl(dev_examples, f"dev_{dataset}.jsonl")

# #     # 2) test 构造成 3-shot few-shot 推理格式
# #     write_test_jsonl_with_fewshot(
# #         test_examples=test_examples,
# #         train_examples=train_examples,
# #         output_file=f"test_{dataset}_{num_shots}shot_seed{random_seed}.jsonl",
# #         num_shots=num_shots,
# #         seed=random_seed
# #     )

# #     print("全部处理完成。")



import os
import csv
import json
import random
from typing import List, Dict

# ================= 配置区域 =================
# 数据集选择 ('MIntRec' 或 'MIntRec2.0')
DATASET_NAME = "MIntRec"

# TSV 文件所在路径
BASE_PATH = "/home/<USER>/<USER>/ACL/tsv/MIntRec"

# 数据根目录 (视频和音频)
# 注意：新代码逻辑强制使用了 MIntRec 的路径结构，这里保持一致
DATA_ROOT = "./data/Intent_Data/MIntRec"
VIDEO_ROOT = os.path.join(DATA_ROOT, "video")
AUDIO_ROOT = os.path.join(DATA_ROOT, "audio")

# 随机种子
RANDOM_SEED = 42
NUM_SHOTS = 3
# ===========================================

label_map = {
    'MIntRec': '[Complain, Praise, Apologise, Thank, Criticize, Agree, Taunt, Flaunt, Joke, Oppose, Comfort, Care, Inform, Advise, Arrange, Introduce, Leave, Prevent, Greet, Ask for help]',
    'MIntRec2.0': '[Acknowledge, Advise, Agree, Apologise, Arrange, Ask for help, Asking for opinions, Care, Comfort, Complain, Confirm, Criticize, Doubt, Emphasize, Explain, Flaunt, Greet, Inform, Introduce, Invite, Joke, Leave, Oppose, Plan, Praise, Prevent, Refuse, Taunt, Thank, Warn]',
}


def build_prompt(utterance: str, dataset: str) -> str:
    """构建包含视频和音频标签的 Prompt"""
    labels = label_map[dataset]
    # 增加了 <audio> 标签，修正了原代码中 "ased" 的拼写错误为 "Based"
    prompt = (
        f"<video><audio>You are presented with a video in which the speaker says: {utterance} "
        f"Based on the text, video, and audio content, what is the intent of this speaker?\n"
        f"The candidate labels for intent are: {labels}. "
        f"Respond in the format: 'intent: [label]'. Only one label should be provided."
    )
    return prompt


def load_tsv_examples(file_name: str, dataset: str) -> List[Dict]:
    """加载 TSV 文件并构建包含视频和音频路径的样本列表"""
    tsv_file = os.path.join(BASE_PATH, file_name)
    
    examples = []
    with open(tsv_file, 'r', encoding='utf-8') as f:
        print(f"加载文件: {tsv_file}")
        csv_reader = csv.reader(f, delimiter='\t')
        next(csv_reader, None)  # 跳过表头

        for line_idx, row in enumerate(csv_reader, start=2):
            if len(row) < 3:
                print(f"[Warning] 第 {line_idx} 行字段不足，已跳过: {row}")
                continue

            video_name = row[0].strip()
            utterance = row[1].strip()
            label = row[2].strip()

            # 构建视频和音频的绝对路径
            video_path = os.path.join(VIDEO_ROOT, video_name)
            # 假设音频文件名与视频名相同，但后缀为 .wav
            audio_name = f"{video_name.split('.')[0]}.wav"
            audio_path = os.path.join(AUDIO_ROOT, audio_name)

            prompt = build_prompt(utterance, dataset)
            answer = f"intent: {label}"

            examples.append({
                "video_path": video_path,
                "audio_path": audio_path,
                "prompt": prompt,
                "answer": answer,
                "label": label,
                "utterance": utterance,
                "video_name": video_name,
            })

    return examples


def write_standard_jsonl(examples: List[Dict], output_file: str) -> None:
    """用于 train/dev，保持单轮监督格式，包含 videos 和 audios 字段"""
    with open(output_file, 'w', encoding='utf-8') as fout:
        for ex in examples:
            item = {
                "messages": [
                    {"role": "user", "content": ex["prompt"]},
                    {"role": "assistant", "content": ex["answer"]}
                ],
                "videos": [ex["video_path"]],
                "audios": [ex["audio_path"]]  # 新增音频字段
            }
            json.dump(item, fout, ensure_ascii=False)
            fout.write('\n')

    print(f"写入完成: {output_file}")


def sample_unique_support_indices(
    train_size: int,
    num_shots: int,
    rng: random.Random,
    used_combinations: set,
    max_try: int = 1000
) -> tuple:
    """采样 few-shot 支持集索引"""
    if train_size < num_shots:
        raise ValueError(f"训练样本数量不足，无法采样 {num_shots}-shot。当前 train_size={train_size}")

    for _ in range(max_try):
        indices = tuple(rng.sample(range(train_size), num_shots))
        if indices not in used_combinations:
            used_combinations.add(indices)
            return indices

    return tuple(rng.sample(range(train_size), num_shots))


def write_test_jsonl_with_fewshot(
    test_examples: List[Dict],
    train_examples: List[Dict],
    output_file: str,
    num_shots: int = 3,
    seed: int = 42
) -> None:
    """
    为 test 集构造 few-shot 推理格式。
    包含视频和音频的多模态输入。
    """
    rng = random.Random(seed)
    used_combinations = set()

    with open(output_file, 'w', encoding='utf-8') as fout:
        for test_idx, test_ex in enumerate(test_examples):
            support_indices = sample_unique_support_indices(
                train_size=len(train_examples),
                num_shots=num_shots,
                rng=rng,
                used_combinations=used_combinations
            )

            item = {
                "messages": [],
                "videos": [],
                "audios": [],
                "gold_answer": test_ex["answer"] # 用于后续评测
            }

            # 加入 few-shot 的 train 样例
            for s_idx in support_indices:
                support_ex = train_examples[s_idx]
                item["messages"].append({"role": "user", "content": support_ex["prompt"]})
                item["messages"].append({"role": "assistant", "content": support_ex["answer"]})
                
                item["videos"].append(support_ex["video_path"])
                item["audios"].append(support_ex["audio_path"])

            # 最后加入当前 test query
            item["messages"].append({"role": "user", "content": test_ex["prompt"]})
            item["videos"].append(test_ex["video_path"])
            item["audios"].append(test_ex["audio_path"])

            json.dump(item, fout, ensure_ascii=False)
            fout.write('\n')

    print(f"写入完成: {output_file}")


if __name__ == "__main__":
    # 1) 读取数据
    train_examples = load_tsv_examples("train.tsv", DATASET_NAME)
    dev_examples = load_tsv_examples("dev.tsv", DATASET_NAME)
    test_examples = load_tsv_examples("test.tsv", DATASET_NAME)

    # 2) 处理 train/dev (标准监督微调格式)
    write_standard_jsonl(train_examples, f"train_{DATASET_NAME}.jsonl")
    write_standard_jsonl(dev_examples, f"dev_{DATASET_NAME}.jsonl")

    # 3) 处理 test (Few-shot 推理格式)
    write_test_jsonl_with_fewshot(
        test_examples=test_examples,
        train_examples=train_examples,
        output_file=f"test_{DATASET_NAME}_{NUM_SHOTS}shot_seed{RANDOM_SEED}.jsonl",
        num_shots=NUM_SHOTS,
        seed=RANDOM_SEED
    )

    print("全部处理完成。")