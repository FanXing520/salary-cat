from __future__ import annotations

import argparse
import sys
import time
import threading
from pathlib import Path

import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk, ImageSequence

from audio_player import AudioPlayer


LOVE_MESSAGE = "我真的特别爱你"


def load_gif_frames(path: str | Path) -> list[tuple[Image.Image, float]]:
    frames = []
    with Image.open(path) as image:
        for frame in ImageSequence.Iterator(image):
            duration_ms = frame.info.get("duration", image.info.get("duration", 100))
            duration = max(float(duration_ms) / 1000.0, 0.02)
            frames.append((frame.convert("RGBA").copy(), duration))
    return frames


def crop_to_content(frames: list[tuple[Image.Image, float]]) -> list[tuple[Image.Image, float]]:
    if not frames:
        return frames
    
    boxes = [frame[0].getchannel("A").getbbox() for frame in frames]
    boxes = [box for box in boxes if box is not None]
    
    if not boxes:
        return frames
    
    left = min(box[0] for box in boxes)
    top = min(box[1] for box in boxes)
    right = max(box[2] for box in boxes)
    bottom = max(box[3] for box in boxes)
    
    return [
        (frame[0].crop((left, top, right, bottom)), frame[1])
        for frame in frames
    ]


class CatWindow:
    def __init__(self, gif_path: Path, music_path: Path | None, scale: float = 2.0):
        self.root = tk.Tk()
        self.root.title("Salary Cat")
        
        self.gif_path = gif_path
        self.music_path = music_path
        self.scale = scale
        
        self.frames = load_gif_frames(gif_path)
        self.frames = crop_to_content(self.frames)
        
        self.current_frame = 0
        self.is_running = True
        self.audio_player = None
        
        self.setup_ui()
        self.start_animation()
        
        if music_path and music_path.exists():
            self.start_audio()
    
    def setup_ui(self):
        # 获取原始GIF尺寸
        if self.frames:
            original_width, original_height = self.frames[0][0].size
            new_width = int(original_width * self.scale)
            new_height = int(original_height * self.scale)
        else:
            new_width, new_height = 400, 300
        
        # 创建画布
        self.canvas = tk.Canvas(self.root, width=new_width, height=new_height, bg="#1a1a1a")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 创建标签显示消息
        self.message_label = ttk.Label(
            self.root, 
            text=LOVE_MESSAGE,
            font=("Microsoft YaHei", 16, "bold"),
            foreground="#ff69b4",
            background="#1a1a1a"
        )
        self.message_label.pack(pady=10)
        
        # 设置窗口大小
        self.root.geometry(f"{new_width}x{new_height + 60}")
        self.root.resizable(True, True)
        
        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def start_animation(self):
        def animate():
            while self.is_running:
                if self.frames:
                    frame_img, duration = self.frames[self.current_frame]
                    
                    # 调整大小
                    original_width, original_height = frame_img.size
                    new_width = int(original_width * self.scale)
                    new_height = int(original_height * self.scale)
                    resized = frame_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # 转换为Tkinter图像
                    self.tk_img = ImageTk.PhotoImage(resized)
                    
                    # 更新画布
                    self.canvas.delete("all")
                    self.canvas.config(width=new_width, height=new_height)
                    self.canvas.create_image(0, 0, image=self.tk_img, anchor=tk.NW)
                    
                    # 更新窗口大小
                    self.root.geometry(f"{new_width}x{new_height + 60}")
                    
                    self.current_frame = (self.current_frame + 1) % len(self.frames)
                    
                    # 控制帧率
                    time.sleep(duration)
                else:
                    time.sleep(0.1)
        
        self.animation_thread = threading.Thread(target=animate, daemon=True)
        self.animation_thread.start()
    
    def start_audio(self):
        def play_audio():
            self.audio_player = AudioPlayer(self.music_path)
            self.audio_player.start()
        
        self.audio_thread = threading.Thread(target=play_audio, daemon=True)
        self.audio_thread.start()
    
    def on_close(self):
        self.is_running = False
        if self.audio_player:
            self.audio_player.stop()
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render cat.gif as a window animation."
    )
    parser.add_argument(
        "--gif",
        default="cat.gif",
        help="GIF path. Defaults to ./cat.gif.",
    )
    parser.add_argument(
        "--scale",
        type=float,
        default=2.0,
        help="Animation scale from 0.1 to 2.0. Default: 1.0.",
    )
    parser.add_argument(
        "--music",
        default="music.mp3",
        help="MP3 file to play when the animation starts. Default: ./music.mp3.",
    )
    parser.add_argument(
        "--no-music",
        action="store_true",
        help="Disable music playback.",
    )
    return parser.parse_args()


def resolve_path(path: str, default_name: str) -> Path:
    requested = Path(path)
    if requested.exists():
        return requested
    
    for candidate in (Path.cwd() / default_name, Path(__file__).parent / default_name):
        if candidate.exists():
            return candidate
    
    return requested


def run() -> int:
    args = parse_args()
    
    gif_path = resolve_path(args.gif, "cat.gif")
    
    music_path = None
    if not args.no_music:
        music_path = resolve_path(args.music, "music.mp3")
        if not music_path.exists():
            music_path = None
    
    try:
        app = CatWindow(gif_path, music_path, scale=args.scale)
        app.run()
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(run())