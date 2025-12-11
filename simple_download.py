from huggingface_hub import snapshot_download
import os

print("Downloading microsoft/speecht5_tts...")
try:
    snapshot_download(
        repo_id="microsoft/speecht5_tts",
        local_dir="./models/speecht5_tts",
        local_dir_use_symlinks=False
    )
    print("✓ microsoft/speecht5_tts downloaded successfully!")
except Exception as e:
    print(f"Download failed: {e}")

print("Downloading microsoft/speecht5_hifigan...")
try:
    snapshot_download(
        repo_id="microsoft/speecht5_hifigan", 
        local_dir="./models/speecht5_hifigan",
        local_dir_use_symlinks=False
    )
    print("✓ microsoft/speecht5_hifigan downloaded successfully!")
except Exception as e:
    print(f"Download failed: {e}")

print("All models downloaded!")