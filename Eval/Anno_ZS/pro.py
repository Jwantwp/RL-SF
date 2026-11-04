import os
import json
import numpy as np
from tqdm import tqdm
import csv



# 读取jsonl文件


labels=['neutral', 'change', 'sustain']




def pre_str(strs):
    jie_duan_str=strs[-20:]
    pre=[i for i in labels if i in jie_duan_str]
    if len(pre)==1:
        return pre[0]
    else:
        return jie_duan_str
def read_jsonl(file_path):
    data = []
    # 获得文件名
    file_name = os.path.basename(file_path)
    name=file_name.split(".")[0]
    csv_files=f"{name}.csv"
    csv_file_open=open(csv_files, 'w', encoding='utf-8')
    csv_writer=csv.writer(csv_file_open)
    csv_writer.writerow(["answer", "label"])


    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:

            # data.append(json.loads(line))
            item=json.loads(line)

            pre=item["response"].lower()
            true=item["labels"].lower()

            pre_pre=pre_str(pre)
            true_pre=pre_str(true)
            csv_writer.writerow([pre_pre, true_pre])



read_jsonl("/home/<USER>/<USER>/RL-SF/Eval/Anno_ZS/Source/Qwen3-VL.jsonl")






















