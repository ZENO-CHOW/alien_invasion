# About alien_invasion

这是一个基于 Pygame 的小游戏，依赖由 [uv](https://docs.astral.sh/uv/) 管理。

安装项目依赖：

```bash
uv sync
```

运行游戏：

```bash
uv run python alien_invasion.py
```

打包 Windows 应用：

```bash
uv sync --dev
uv run pyinstaller --clean --noconfirm alien_invasion.spec
```

生成的应用位于 `dist/alien_invasion.exe`。打包配置会自动包含 `images` 目录，
应用从任意工作目录启动时都能正确找到图片资源。
