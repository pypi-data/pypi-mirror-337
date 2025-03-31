# AdaptivePixelizer

[![PyPI version](https://badge.fury.io/py/grid-pixelator.svg)](https://badge.fury.io/py/grid-pixelator) <!-- 公開後に確認 -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AdaptivePixelizer** is a simple GUI tool to pixelate images by averaging colors within a user-defined grid. It's designed for easily converting high-resolution pixel art or photos into a low-resolution, dot-art style.

<!-- ![Screenshot](path/to/your/screenshot.png) --> <!-- GitHub等に画像を置いてパスを指定 -->

## Features

*   **Interactive Grid Editing:** Manually add, delete, and move grid lines directly on the image using mouse clicks and drags.
    *   Shift + Left Click: Add vertical line
    *   Shift + Right Click: Add horizontal line
    *   Ctrl + Click: Delete line under cursor
    *   Drag line: Move line
    *   Delete/Backspace: Delete line under cursor
*   **Zoom and Pan:** Easily navigate large images. (Mouse wheel, Alt+Drag)
*   **Multiple Color Averaging Methods:** Choose between Average, Median, or Mode color calculation for pixelation.
*   **Real-time Preview:** See the pixelated result instantly (can be toggled on/off).
*   **Undo/Redo:** Supports undo/redo for grid modifications.
*   **Simple Interface:** Lightweight and easy to use.

## Installation

You can install AdaptivePixelizer using pip:

pip install grid-pixelator

**Optional Dependencies:**

For potentially faster median color calculation, NumPy is recommended:

pip install grid-pixelator[numpy]
# or just "pip install numpy" separately

## Usage

1.  Launch the application by typing the following command in your terminal:

    grid-pixelator

2.  Click "画像ファイルを開く" (Open Image File) to load an image.
3.  Adjust the grid lines on the left panel (original image):
    *   Use the initial grid spinboxes, or
    *   Use Shift+Click, Ctrl+Click, Drag, or Delete/Backspace key as described in Features.
4.  Select the desired color calculation method (Average, Median, Mode).
5.  The pixelated preview will update automatically on the right panel (if "プレビュー自動更新" is checked). Click "プレビュー更新 / 実行" to manually update.
6.  Once satisfied, save the processed image using "ファイル" > "名前を付けて保存...".

## Requirements

*   Python 3.8 or later
*   PyQt6
*   Pillow
*   NumPy (Optional, recommended for Median calculation)
*   OS: Primarily tested on macOS, should work on Windows/Linux.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing / Issues

<!-- If you find any bugs or have suggestions, please open an issue on the [GitHub Issues page](link/to/your/github/issues) (if available). -->