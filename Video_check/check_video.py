import os
import json
import cv2
import subprocess
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# ================= 配置区域 =================
INPUT_JSON = "/data/data/annomi_client_test.json"               # 原始输入的数据集
OUTPUT_JSON = "/data/data/annomi_client_test_clean.json"        # 最终输出的数据集
RESCUED_DIR = "/data/video/AnnoMi/fixed_videos/" # 修复后视频的存放目录
MAX_WORKERS = 8                                  # FFmpeg 修复时的并发线程数
# ============================================

os.makedirs(RESCUED_DIR, exist_ok=True)

def is_video_valid(video_path, num_samples=5):
    """检测视频文件是否底层损坏（抽帧测试）"""
    if not os.path.exists(video_path):
        return False
        
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return False
            
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames <= 0:
            cap.release()
            return False

        step = max(1, total_frames // num_samples)
        for frame_idx in range(0, total_frames, step):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, _ = cap.read()
            if not ret:
                cap.release()
                return False
                
        if total_frames > 3:
            cap.set(cv2.CAP_PROP_POS_FRAMES, total_frames - 2)
            ret, _ = cap.read()
            if not ret:
                cap.release()
                return False

        cap.release()
        return True
    except Exception:
        return False

def fix_video_task(item):
    """FFmpeg 修复任务函数"""
    video_path = item["videos"][0]
    filename = os.path.basename(video_path)
    output_path = os.path.join(RESCUED_DIR, filename)
    
    # 如果已经修复过，直接返回成功并更新路径
    if os.path.exists(output_path):
        item["videos"] = [output_path]
        return True, item
        
    cmd = [
        "ffmpeg", "-y", "-err_detect", "ignore_err",
        "-i", video_path,
        "-c:v", "libx264", "-preset", "superfast", "-crf", "23",
        "-c:a", "copy", 
        output_path
    ]
    
    try:
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        # 修复成功，更新 item 中的视频路径为新路径
        item["videos"] = [output_path]
        return True, item
    except subprocess.CalledProcessError:
        # 彻底修复失败
        return False, item

def main():
    print(f"[{'='*40}]")
    print("🚀 开始端到端自动化数据集清洗与修复")
    print(f"[{'='*40}]\n")

    # 1. 读取原始数据
    with open(INPUT_JSON, 'r', encoding='utf-8') as f:
        dataset = json.load(f)
    print(f"加载原始数据: {len(dataset)} 条\n")

    good_items = []
    bad_items = []
    missing_files = 0

    # 2. 阶段一：扫描检测
    print("▶ 阶段一：扫描视频底层完整性")
    for item in tqdm(dataset, desc="Scanning"):
        videos = item.get("videos", [])
        if not videos:
            continue
            
        video_path = videos[0]
        if not os.path.exists(video_path):
            missing_files += 1
            continue

        if is_video_valid(video_path):
            good_items.append(item)
        else:
            bad_items.append(item)

    print(f"  -> 发现原生健康数据: {len(good_items)} 条")
    print(f"  -> 发现底层损坏异常: {len(bad_items)} 条")
    if missing_files > 0:
        print(f"  -> 警告：文件丢失 {missing_files} 条\n")

    # 3. 阶段二：多线程抢救异常视频
    rescued_items = []
    failed_to_rescue = 0

    if bad_items:
        print("\n▶ 阶段二：启动 FFmpeg 强制抢救机制")
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # 使用 tqdm 包装并发任务以显示进度
            results = list(tqdm(executor.map(fix_video_task, bad_items), total=len(bad_items), desc="Fixing"))
            
        for success, updated_item in results:
            if success:
                rescued_items.append(updated_item)
            else:
                failed_to_rescue += 1
                
        print(f"  -> 抢救成功并更新路径: {len(rescued_items)} 条")
        print(f"  -> 彻底报废无法挽救: {failed_to_rescue} 条\n")
    else:
        print("\n▶ 阶段二：没有发现损坏视频，跳过抢救环节\n")

    # 4. 阶段三：合并与输出
    print("▶ 阶段三：合并最终可用数据集")
    final_dataset = good_items + rescued_items
    
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(final_dataset, f, indent=2, ensure_ascii=False)

    # 5. 打印最终报告
    print(f"\n[{'='*40}]")
    print("✅ 处理完成！最终数据报告：")
    print(f"原始数据总量 : {len(dataset)} 条")
    print(f"原生完美数据 : {len(good_items)} 条")
    print(f"成功抢救数据 : {len(rescued_items)} 条")
    print(f"废弃数据总计 : {failed_to_rescue + missing_files} 条 (含损坏及丢失)")
    print(f"最终可用总量 : {len(final_dataset)} 条")
    print(f"\n请将 ms-swift 训练集的路径指向: {OUTPUT_JSON}")
    print(f"[{'='*40}]")

if __name__ == "__main__":
    main()