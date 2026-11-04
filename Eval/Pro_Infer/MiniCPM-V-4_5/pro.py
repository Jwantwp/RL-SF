# import csv

# import json

# path = "/home/<USER>/<USER>/RL-SF/Eval/Pro_Infer/MiniCPM-V-4_5/source_file"



# jsonl_files=os.listdir(path)


# for file in jsonl_files:
#     file_path=os.path.join(path,file)

#     last_level = os.path.basename(file_path)
#     file_name =last_level.replace(".jsonl", "")
#     pres=[]
#     true=[]
#     with open(path, 'r', encoding='utf-8') as json_file:
#         # 这行代码只能处理单个大 JSON 对象或列表
#         for row in json_file:
#             row=json.loads(row)
#             pres.append(row["response"].split("\n\n")[-1].strip())
#             true.append(row["labels"].strip())
            
            
import os
import csv
import json

# 定义源文件目录路径
path = "/home/<USER>/<USER>/RL-SF/ms-swift/examples/bash/Infer/Zero-Shot-MIniCPM/MOSI/result/MiniCPM-V-4_5-8B/infer_result"

# 获取目录下所有文件
files = os.listdir(path)

for file in files:
    # 只处理 .jsonl 后缀的文件
    if not file.endswith(".jsonl"):
        continue

    file_path = os.path.join(path, file)
    
    # 生成输出 CSV 的文件名 (例如: data.jsonl -> data.csv)
    output_filename = file.replace(".jsonl", ".csv")
    output_path = os.path.join(path, output_filename)

    pres = []
    trues = []

    print(f"正在处理文件: {file} ...")

    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            for line in json_file:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                    
                    # 提取 response 的最后一部分 (根据 \n\n 分割)
                    # 防止 response 为空导致报错
                    response_text = row.get("response", "")
                    pre_value = response_text.split("\n\n")[-1].strip()
                    
                    # 提取 labels
                    true_value = row.get("labels", "").strip()

                    pres.append(pre_value)
                    trues.append(true_value)
                except json.JSONDecodeError:
                    print(f"警告: 跳过无效 JSON 行 in {file}")
                except KeyError as e:
                    print(f"警告: 缺少键 {e} in {file}, 跳过该行")

        # 写入 CSV 文件
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # 写入表头
            writer.writerow(['pre', 'true'])
            
            # 写入数据，使用 zip 将两个列表配对
            for p, t in zip(pres, trues):
                writer.writerow([p, t])
        
        print(f"成功保存至: {output_path} (共 {len(pres)} 条数据)")

    except Exception as e:
        print(f"处理文件 {file} 时发生错误: {e}")

print("所有文件处理完成。")