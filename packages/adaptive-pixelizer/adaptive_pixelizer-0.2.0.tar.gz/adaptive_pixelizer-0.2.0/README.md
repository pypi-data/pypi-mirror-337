# README.md
# adaptive-pixelizer

[![PyPI version](https://badge.fury.io/py/adaptive-pixelizer.svg)](https://badge.fury.io/py/adaptive-pixelizer) <!-- 公開後に確認 -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**adaptive-pixelizer** is a simple GUI tool to pixelate images by averaging colors within a user-defined grid. It's designed for easily converting high-resolution pixel art or photos into a low-resolution, dot-art style with interactive editing capabilities.

<!-- ![Screenshot](path/to/your/screenshot.png) --> <!-- GitHub等に画像を置いてパスを指定 -->

## Features

*   **Three-Step Workflow:**
    1.  **Initial Grid Setup:** Define the initial grid size and color calculation method.
    2.  **Interactive Grid Editing:** Manually add, delete, and move grid lines directly on the image.
    3.  **Color Editing:** Select and edit the colors of the generated pixels.
*   **Grid Editing Operations:**
    *   Shift + Left Click: Add vertical line
    *   Shift + Right Click: Add horizontal line
    *   Ctrl + Click: Delete line under cursor
    *   Drag line: Move line
    *   Delete/Backspace: Delete line under cursor
*   **Color Editing Operations (Step 3):**
    *   Click: Select/deselect individual pixel.
    *   Shift + Click: Select/deselect all pixels of the same color.
    *   Drag: Select/deselect pixels within the dragged area.
    *   Click outside pixels: Deselect all pixels.
    *   Edit Button / Menu: Change the color of selected pixels.
*   **Zoom and Pan:** Easily navigate large images (Mouse wheel, Alt+Drag).
*   **Multiple Color Calculation Methods:** Choose between Average, Median, or Mode for pixelation.
*   **Real-time Preview:** See the pixelated result instantly (can be toggled on/off for grid editing).
*   **Undo/Redo:** Supports undo/redo for grid modifications and color edits (including selection state).
*   **Simple Interface:** Lightweight and easy to use.

## Installation

You can install adaptive-pixelizer using pip:

```bash
pip install adaptive-pixelizer
```

**Optional Dependencies:**

For potentially faster median color calculation, NumPy is recommended:

```bash
pip install adaptive-pixelizer[numpy]
# or just "pip install numpy" separately
```

## Usage

1.  Launch the application by typing the following command in your terminal:

    ```bash
    adaptive-pixelizer
    ```

2.  **Step 1: Initial Grid**
    *   Click "画像ファイルを開く" (Open Image File) to load an image.
    *   Adjust the initial grid size using the spinboxes ("横", "縦").
    *   Select the color calculation method ("平均", "中央値", "最頻色").
    *   The preview updates automatically (if "プレビュー自動更新" is checked). Click "プレビュー更新" for manual update.
    *   Click "グリッド編集へ進む →" to proceed.

3.  **Step 2: Grid Editing**
    *   Edit the grid lines on the left panel (original image) using the operations described in Features.
    *   You can change the color calculation method here as well.
    *   The preview updates based on the grid changes.
    *   Click "色編集へ進む →" to finalize the grid and proceed.
    *   Click "← 初期グリッドに戻る" to discard grid edits and return to Step 1.

4.  **Step 3: Color Editing**
    *   Select pixels on the left panel (now showing pixelated blocks) using the color editing operations.
    *   Click "選択ピクセルを編集..." to open the color dialog and change the color of the selected pixels.
    *   Undo/Redo works for color changes and restores the selection state before the change.
    *   Click "← グリッド編集に戻る" to discard color edits and return to Step 2.

5.  **Saving:**
    *   Once satisfied with the result (usually after Step 3), save the processed image using "ファイル" > "名前を付けて保存...".

## Requirements

*   Python 3.8 or later
*   PyQt6 >= 6.4
*   Pillow >= 9.0
*   NumPy (Optional, >= 1.20 recommended for Median calculation)
*   OS: Primarily tested on macOS, should work on Windows/Linux.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing / Issues

<!-- If you find any bugs or have suggestions, please open an issue on the [GitHub Issues page](link/to/your/github/issues) (if available). -->