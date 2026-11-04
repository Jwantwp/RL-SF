import json
import os
import pandas as pd
import re
import shutil
import argparse
import csv
import yaml
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from tqdm import tqdm

# def cal_metrics(df,file_name,model_name,explain_text):

#     labels = []
#     preds = []

#     for i in range(len(df)):
#         pred = str(df.loc[i,"pred_processed"]).lower()
#         label = str(df.loc[i,"Label"]).lower()
#         labels.append(label)
#         preds.append(pred)

#         print('pred: {}, label: {}'.format(pred, label))

#     acc = accuracy_score(labels, preds)
#     f1 = f1_score(labels, preds, average='macro')
#     prec = precision_score(labels, preds, average='macro')
#     rec = recall_score(labels, preds, average='macro')

#     weighted_f1 = f1_score(labels, preds, average='weighted')
#     weighted_prec = precision_score(labels, preds, average='weighted')

#     results_dict = {
#         'ACC': round(acc * 100, 2),
#         'F1': round(f1 * 100, 2),
#         'Precision': round(prec * 100, 2),
#         'Recall': round(rec * 100, 2),
#         'WF1': round(weighted_f1 * 100, 2),
#         'WP': round(weighted_prec * 100, 2),
#         'explain_type': file_name,
#         'model_type':model_name,
#         'explain_text':explain_text,
#     }

#     return results_dict


def cal_metrics(df, file_name, model_name, explain_text):
    labels = []
    preds = []

    for i in range(len(df)):
        # 保持你原有的预处理逻辑（转小写、去空格）
        pred = str(df.loc[i, "pred_processed"]).lower().strip()
        label = str(df.loc[i, "Label"]).lower().strip()
        
        labels.append(label)
        preds.append(pred)

    # --- 修改重点开始 ---

    # 1. 定义正类标签为字符串 'positive'
    target_pos_label = 'positive' 

    # 2. 计算指标时，传入 pos_label=target_pos_label
    # 注意：二分类通常关注正类的表现，所以这里不再使用 average='macro'，而是直接计算正类指标
    f1 = f1_score(labels, preds, pos_label=target_pos_label, zero_division=0)
    prec = precision_score(labels, preds, pos_label=target_pos_label, zero_division=0)
    rec = recall_score(labels, preds, pos_label=target_pos_label, zero_division=0)

    # 3. 准确率不需要 pos_label
    acc = accuracy_score(labels, preds)

    # 4. 如果你依然需要 weighted/macro 指标（用于对比），它们会自动处理字符串标签，不需要改
    f1_weighted = f1_score(labels, preds, average='weighted', zero_division=0)
    prec_weighted = precision_score(labels, preds, average='weighted', zero_division=0)

    # --- 修改重点结束 ---

    results_dict = {
        'ACC': round(acc * 100, 2),
        'F1': round(f1 * 100, 2),          # 这里现在是 'positive' 类的 F1
        'Precision': round(prec * 100, 2), # 这里现在是 'positive' 类的 Precision
        'Recall': round(rec * 100, 2),     # 这里现在是 'positive' 类的 Recall
        'WF1': round(f1_weighted * 100, 2),
        'WP': round(prec_weighted * 100, 2),
        'explain_type': file_name,
        'model_type': model_name,
        'explain_text': explain_text,
    }

    return results_dict










def save_results(file_path, results_dict):

    if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        ori = []
        ori.append(results_dict.values())
        df1 = pd.DataFrame(ori, columns = list(results_dict.keys()))
        df1.to_csv(file_path, index = False)
    else:
        df1 = pd.read_csv(file_path)
        new = pd.DataFrame(results_dict, index=[1])
        df1 = pd.concat([df1, new], ignore_index=True)
        df1.to_csv(file_path,index=False)
    
    data_diagram = pd.read_csv(file_path)
    
    print('test_results', data_diagram)

if __name__ == '__main__':

    



    save_results_path = "/home/<USER>/<USER>/RL-SF/Eval/result.csv"
  
    path = "/home/<USER>/<USER>/RL-SF/ms-swift/examples/bash/Infer/result/Qwen3-VL-8B-Instruct/infer_result/20260428-030013.jsonl"
    
    
    
    last_level = os.path.basename(path)
    file_name =last_level.replace(".jsonl", "")
    pres=[]
    true=[]
    with open(path, 'r', encoding='utf-8') as json_file:
        # 这行代码只能处理单个大 JSON 对象或列表
        for row in json_file:
            row=json.loads(row)
            # row=dict(row)
            # print("==",row)
            # pres.append(row["response"].split("\n\ndialogue act:")[-1].replace("dialogue act:", "").replace("\n", "").strip())
            # true.append(row["labels"].replace("dialogue act:", "").strip())
            pres.append(row["response"].replace("sentiment:","").strip())
            true.append(row["labels"].replace("sentiment:", "").strip())

        df = pd.DataFrame({'pred_processed': pres, 'Label': true})
        results = cal_metrics(df,file_name,'Qwen3-VL','MOSI-Zero-Shot')
        save_results(f"{save_results_path}", results)

