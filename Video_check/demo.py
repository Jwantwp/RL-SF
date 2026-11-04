import os
import cv2
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# ================= 配置区域 =================
INPUT_VIDEO_DIR = "./AnnoMi/video"      # 你的原始视频文件夹路径
OUTPUT_VIDEO_DIR = "./AnnoMi/video_fix"  # 最终输出的新目录
MAX_WORKERS = 8                                  # FFmpeg 修复时的并发线程数
# ============================================

# 确保输出目录存在
# os.makedirs(OUTPUT_VIDEO_DIR, exist_ok=True)

# 常见视频格式后缀
VIDEO_EXTS = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.ts', '.m4v')

def is_video_valid(video_path, num_samples=5):
    """检测视频文件是否底层损坏（完全保留你原有的 OpenCV 抽帧检测逻辑）"""
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

        # 抽帧检测视频中间和末尾是否能正常读取
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

def fix_video_task(video_path):
    """FFmpeg 修复任务函数"""
    filename = os.path.basename(video_path)
    output_path = os.path.join(OUTPUT_VIDEO_DIR, filename)
    
    # 如果输出目录已经存在该文件（可能之前修复过），直接返回成功
    if os.path.exists(output_path):
        return True, output_path
        
    # 使用 FFmpeg 强制修复并重新编码
    cmd = [
        "ffmpeg", "-y", "-err_detect", "ignore_err",
        "-i", video_path,
        "-c:v", "libx264", "-preset", "superfast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k", 
        output_path
    ]
    
    try:
        # 屏蔽 FFmpeg 的大量控制台输出，保持界面整洁
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, timeout=300)
        return True, output_path
    except subprocess.CalledProcessError:
        return False, output_path
    except subprocess.TimeoutExpired:
        return False, output_path

def main():
    print(f"[{'='*50}]")
    print("🚀 开始自动化视频检测、修复与归档")
    print(f"[{'='*50}]\n")

    # 1. 收集所有视频文件
    video_files = []
    for root, _, files in os.walk(INPUT_VIDEO_DIR):
        for file in files:
            if file.lower().endswith(VIDEO_EXTS):
                video_files.append(os.path.join(root, file))
    
    if not video_files:
        print(f"❌ 在目录 '{INPUT_VIDEO_DIR}' 中未找到任何视频文件！")
        return

    print(f"📂 共找到 {len(video_files)} 个视频文件，开始处理...\n")

    healthy_videos = []
    broken_videos = []

    # 2. 阶段一：使用 OpenCV 扫描检测视频完整性
    print("▶ 阶段一：使用 OpenCV 抽帧检测视频底层完整性")
    for video_path in tqdm(video_files, desc="Scanning"):
        if is_video_valid(video_path):
            healthy_videos.append(video_path)
        else:
            broken_videos.append(video_path)

    print(f"  -> 原生健康视频: {len(healthy_videos)} 个")
    print(f"  -> 发现损坏/异常视频: {len(broken_videos)} 个\n")

    # 3. 阶段二：处理视频（健康的复制，损坏的修复）
    final_success_count = 0

    # 3.1 先把健康的视频直接复制到新目录
    if healthy_videos:
        print("▶ 阶段二-A：复制健康视频到新目录")
        for video_path in tqdm(healthy_videos, desc="Copying"):
            filename = os.path.basename(video_path)
            dst_path = os.path.join(OUTPUT_VIDEO_DIR, filename)
            # 避免重名覆盖
            if not os.path.exists(dst_path):
                shutil.copy2(video_path, dst_path)
        print(f"  -> 健康视频复制完成！\n")
        final_success_count += len(healthy_videos)

    # 3.2 多线程抢救损坏的视频
    if broken_videos:
        print("▶ 阶段二-B：启动 FFmpeg 强制抢救机制")
        rescued_count = 0
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            # 使用 tqdm 包装并发任务以显示进度
            results = list(tqdm(executor.map(fix_video_task, broken_videos), total=len(broken_videos), desc="Fixing"))
            
        for success, _ in results:
            if success:
                rescued_count += 1
                
        print(f"  -> 抢救成功: {rescued_count} 个")
        print(f"  -> 彻底报废无法挽救: {len(broken_videos) - rescued_count} 个\n")
        final_success_count += rescued_count
    else:
        print("▶ 阶段二-B：没有发现损坏视频，跳过抢救环节\n")

    # 4. 打印最终报告
    print(f"[{'='*50}]")
    print("✅ 处理完成！最终报告：")
    print(f"原始视频总数   : {len(video_files)} 个")
    print(f"原生健康视频   : {len(healthy_videos)} 个 (已复制)")
    print(f"成功抢救视频   : {final_success_count - len(healthy_videos)} 个 (已修复)")
    print(f"彻底报废视频   : {len(video_files) - final_success_count} 个")
    print(f"最终可用总数   : {final_success_count} 个")
    print(f"\n所有可用视频已统一存放于: {OUTPUT_VIDEO_DIR}")
    print(f"[{'='*50}]")

if __name__ == "__main__":
    main()