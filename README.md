# tban-cat

一个流畅的 TrueColor 终端 GIF 播放器，灵感来自 nyancat。

## 功能特性

- 在终端中以 ANSI TrueColor 方式渲染 GIF 动画
- 支持半块（half-block）和实心块（solid-block）两种渲染模式
- 实时 FPS 显示
- 支持音乐播放（MP3）
- 自动裁剪 GIF 透明边距
- 支持 Floyd-Steinberg 抖动算法
- 平滑缩放和锯齿缩放模式
- 自适应终端窗口大小
- 支持窗口模式和终端模式

## 安装

### 前置依赖

- Python 3.10+
- Pillow (PIL)

### 使用 pip 安装

```bash
pip install .
```

### 开发模式安装

```bash
pip install -e .
```

### 可选依赖（音乐播放）

- Windows: PowerShell（内置）
- macOS: afplay（内置）
- Linux: ffplay, mpv, mpg123, cvlc 或 play

## 使用方法

### 基本用法

```bash
tban-cat
```

### 命令行参数

```
--window          在独立窗口中运行（默认）
--terminal        在终端模式下运行
--gif PATH        GIF 文件路径（默认：./cat.gif）
--fps             显示实时 FPS
--dither          启用 Floyd-Steinberg 抖动
--dither-levels N 抖动颜色级别（2-256，默认：32）
--margin-rows N   动画上下空白行数（默认：0）
--scale FLOAT     动画缩放比例（0.1-2.0，默认：1.0）
--no-trim         保留 GIF 透明边距
--alpha-threshold N 透明像素阈值（0-255，默认：128）
--half-block      使用高分辨率半块渲染
--smooth          使用抗锯齿缩放
--music PATH      MP3 音乐文件路径（默认：./music.mp3）
--no-music        禁用音乐播放
--no-alt-screen   不使用备用屏幕缓冲区
```

### 示例

```bash
# 使用自定义 GIF 并显示 FPS
tban-cat --gif myanimation.gif --fps

# 使用半块渲染模式和抗锯齿缩放
tban-cat --half-block --smooth

# 禁用音乐并在终端模式运行
tban-cat --terminal --no-music
```

## 项目结构

```
salary-cat/
├── main.py          # 主程序入口
├── gif_loader.py    # GIF 加载和处理模块
├── renderer.py      # 终端渲染模块
├── audio_player.py  # 音频播放模块
├── window_main.py   # 窗口模式入口
├── cat.gif          # 默认 GIF 文件
├── cat.GIF          # 备用 GIF 文件
├── maltese.gif      # 额外 GIF 文件
├── music.mp3        # 默认音乐文件
├── requirements.txt # 依赖列表
└── pyproject.toml   # 项目配置
```

## 核心模块说明

### main.py
主程序入口，处理命令行参数解析、帧预渲染、动画循环和事件处理。

### gif_loader.py
负责 GIF 文件加载、帧裁剪、尺寸适配和颜色抖动处理。

### renderer.py
实现终端渲染逻辑，支持半块和实心块两种渲染模式，处理屏幕组合和绘制更新。

### audio_player.py
跨平台音频播放模块，支持 Windows、macOS 和 Linux。

## 技术实现

### 渲染原理

1. **半块渲染**：使用 Unicode 字符 `▀` 和 `▄`，每个字符可以显示上下两种颜色，实现更高分辨率的视觉效果。
2. **实心块渲染**：使用 Unicode 字符 `█`，每个字符显示单一颜色。
3. **颜色缓存**：避免重复生成 ANSI 颜色代码，提升性能。
4. **增量更新**：只更新变化的行，减少终端输出量。

### 帧处理流程

1. 加载 GIF 文件，提取所有帧
2. 裁剪透明边距（可选）
3. 根据终端尺寸计算目标大小
4. 缩放并应用抖动（可选）
5. 预渲染为 ANSI 字符序列
6. 循环播放，根据帧延迟控制帧率

## 终端要求

- 支持 TrueColor（24-bit 颜色）
- 支持 Unicode 字符
- 推荐终端：Windows Terminal、iTerm2、GNOME Terminal

## 许可证

Apache-2.0 License

## 作者

tban-cat contributors
