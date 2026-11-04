import json
import os
import csv



def pro_text(text):
    marker = "### Final Label:"
    if marker in text:
        result = text.split(marker)[-1].strip()
        return result
    else:
        return text.strip()





base_path="/home/<USER>/<USER>/RL-SF/Eval/Pro_Infer/CoT-Qwen3-VL"
files=os.listdir(base_path)
for file in files:
    file_path=os.path.join(base_path, file)
    if os.path.isdir(file_path):
        continue
    
    file=file.replace(".jsonl", "")
    csv_file=f"{file}.csv"
    csv_file_open=open(csv_file, 'w', encoding='utf-8')
    csv_writer=csv.writer(csv_file_open)
    header=['video_name', 'pre','true']
    csv_writer.writerow(header)
    

    True_files=f"/home/<USER>/<USER>/ACL/tsv/{file}/all.tsv"
    True_labes=[]
    file_name=[]
    tsv_file=open(True_files, 'r', encoding='utf-8')
    reader=csv.reader(tsv_file,delimiter='\t')
    for row in reader:
        True_labes.append(row[2])
        file_name.append(row[0])
    




    with open(file_path, 'r', encoding='utf-8') as f:
        lines=f.readlines()
        for line in lines:
            data=json.loads(line)
            response=data['response']
            pro_result=pro_text(response)
            video_path=data['videos'][0]
            video_name=os.path.basename(video_path)
            index=file_name.index(video_name)
            true_lable=True_labes[index]
            csv_writer.writerow([video_name, pro_result,true_lable])
            
            