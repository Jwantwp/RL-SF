import os
import subprocess
from pathlib import Path

# ================= 配置区域 =================
# 定义源视频目录和目标音频目录的映射关系
# 格式: "视频源路径": "音频保存路径"
PATH_MAP = {
    "./data/Intent_Data/MIntRec/video": 
    "./data/Intent_Data/MIntRec/audio",
    
    "./data/Intent_Data/MIntRec2.0/video": 
    "./data/Intent_Data/MIntRec2.0/audio"
}

# 支持的音频格式 (ffmpeg 输出格式)
AUDIO_FORMAT = "wav" 
# 采样率 (可选，设置为 None 则保持原采样率，常用 16000 或 44100)
SAMPLE_RATE = 16000 
# ===========================================

def extract_audio(video_path, output_path):
    """
    使用 ffmpeg 提取音频
    """
    # 构建 ffmpeg 命令
    # -i: 输入文件
    # -vn: 禁止视频录制 (只提取音频)
    # -ar: 设置采样率
    # -ac: 设置音频通道数 (1为单声道，2为立体声，这里设为2)
    # -y: 覆盖输出文件而不询问
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vn",
        "-ar", str(SAMPLE_RATE),
        "-ac", "2",
        "-y",
        output_path
    ]
    
    try:
        # 禁止输出 ffmpeg 的日志到控制台以保持整洁，如果需要调试可去掉 capture_output
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ 提取失败: {e.stderr.decode()}")
        return False

def process_directory(video_dir, audio_dir):
    # 支持的视频扩展名
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.m4v')
    
    # 确保目标目录存在
    os.makedirs(audio_dir, exist_ok=True)
    
    # 获取目录下所有文件
    files = [f for f in os.listdir(video_dir) if os.path.isfile(os.path.join(video_dir, f))]
    video_files = [f for f in files if f.lower().endswith(video_extensions)]
    
    print(f"\n📂 正在处理目录: {video_dir}")
    print(f"🔍 发现 {len(video_files)} 个视频文件...")
    
    success_count = 0
    fail_count = 0
    
    for video_name in video_files:
        video_full_path = os.path.join(video_dir, video_name)
        
        # 生成输出文件名: 将扩展名替换为 .wav (或配置的格式)
        output_filename = os.path.splitext(video_name)[0] + f".{AUDIO_FORMAT}"
        audio_full_path = os.path.join(audio_dir, output_filename)
        
        print(f"   🔄 处理中: {video_name} ...", end="")
        
        if extract_audio(video_full_path, audio_full_path):
            print(" ✅ 成功")
            success_count += 1
        else:
            print(" ❌ 失败")
            fail_count += 1
            
    print(f"📊 本组完成: 成功 {success_count}, 失败 {fail_count}")

def main():
    print("🚀 开始批量提取音频...")
    
    for video_dir, audio_dir in PATH_MAP.items():
        if os.path.exists(video_dir):
            process_directory(video_dir, audio_dir)
        else:
            print(f"⚠️ 警告: 目录不存在 - {video_dir}")
            
    print("\n🎉 所有任务处理完毕！")

if __name__ == "__main__":
    main()