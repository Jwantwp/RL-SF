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

def cal_metrics(df,file_name,model_name,explain_text):

    labels = []
    preds = []

    for i in range(len(df)):
        pred = str(df.loc[i,"pred_processed"]).lower()
        label = str(df.loc[i,"Label"]).lower()
        labels.append(label)
        preds.append(pred)

        print('pred: {}, label: {}'.format(pred, label))

    acc = accuracy_score(labels, preds)
    f1 = f1_score(labels, preds, average='macro')
    prec = precision_score(labels, preds, average='macro')
    rec = recall_score(labels, preds, average='macro')

    weighted_f1 = f1_score(labels, preds, average='weighted')
    weighted_prec = precision_score(labels, preds, average='weighted')

    results_dict = {
        'ACC': round(acc * 100, 2),
        'F1': round(f1 * 100, 2),
        'Precision': round(prec * 100, 2),
        'Recall': round(rec * 100, 2),
        'WF1': round(weighted_f1 * 100, 2),
        'WP': round(weighted_prec * 100, 2),
        'explain_type': file_name,
        'model_type':model_name,
        'explain_text':explain_text,
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

    



    save_results_path = "/home/<USER>/<USER>/RL-SF/ms-swift/examples/bash/MM/Result/result.csv"
    
    base_path="/home/<USER>/<USER>/RL-SF/ms-swift/examples/bash/MM/Result"
    Models=["Qwen3-VL","Qwen3-8B"]
    for model in Models:
        model_path=os.path.join(base_path,model)
        Datasets=os.listdir(model_path)
        for dataset in Datasets:
            dataset_path=os.path.join(model_path,dataset)
            
            if dataset == "MIntRec":
                true=[]
                true_path="/home/<USER>/<USER>/RL-SF/ms-swift/examples/bash/MM/Result/Qwen3-VL/MIntRec/Zero-shot/20260331-061643.jsonl"
                with open(true_path, 'r', encoding='utf-8') as json_file:
                    for row in json_file:
                        row=json.loads(row)
                        true_labels=row["labels"].replace("intent:", "").strip()
                        true.append(true_labels)
            elif dataset == "MIntRec2.0":
                true=[]
                true_path="/home/<USER>/<USER>/RL-SF/ms-swift/examples/bash/MM/Result/Qwen3-VL/MIntRec2.0/Zero-shot/20260331-070545.jsonl"
                with open(true_path, 'r', encoding='utf-8') as json_file:
                    for row in json_file:
                        row=json.loads(row)
                        true_labels=row["labels"].replace("intent:", "").strip()
                        true.append(true_labels)
            
            
            explain_types=os.listdir(dataset_path)
            for explain_type in explain_types:
                type_path=os.path.join(dataset_path,explain_type)
                jsonl_files=os.listdir(type_path)
                for jsonl_file in jsonl_files:
                    if jsonl_file.endswith(".jsonl"):
                        file_path=os.path.join(type_path,jsonl_file)
                        last_level = os.path.basename(file_path)
                        file_name =last_level.replace(".jsonl", "")
                        pres=[]
                        true=[]
                        with open(file_path, 'r', encoding='utf-8') as json_file:
                            # 这行代码只能处理单个大 JSON 对象或列表
                            for row in json_file:
                                row=json.loads(row)
                                # row=dict(row)
                                # print("==",row)

                                # pres.append(row["response"].split("\n\ndialogue act:")[-1].replace("dialogue act:", "").replace("\n", "").strip())
                                # true.append(row["labels"].replace("dialogue act:", "").strip())
                                pres.append(row["response"].replace("intent:","").strip())
                                # true.append(row["labels"].replace("sentiment:", "").strip())

                            df = pd.DataFrame({'pred_processed': pres, 'Label': true})
                            results = cal_metrics(df,file_name,model,explain_type)
                            save_results(f"{save_results_path}", results)
    
    
    
    # path = "/home/<USER>/<USER>/RL-SF/Eval/Pro_Infer/InternVL/MOSI.jsonl"
    
    
    
    # last_level = os.path.basename(path)
    # file_name =last_level.replace(".jsonl", "")
    # pres=[]
    # true=[]
    # with open(path, 'r', encoding='utf-8') as json_file:
    #     # 这行代码只能处理单个大 JSON 对象或列表
    #     for row in json_file:
    #         row=json.loads(row)
    #         # row=dict(row)
    #         # print("==",row)

    #         # pres.append(row["response"].split("\n\ndialogue act:")[-1].replace("dialogue act:", "").replace("\n", "").strip())
    #         # true.append(row["labels"].replace("dialogue act:", "").strip())
    #         pres.append(row["response"].replace("sentiment:","").strip())
    #         true.append(row["labels"].replace("sentiment:", "").strip())

    #     df = pd.DataFrame({'pred_processed': pres, 'Label': true})
    #     results = cal_metrics(df,file_name,'InternVL','MOSI-SFT')
    #     save_results(f"{save_results_path}", results)

