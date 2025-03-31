# src/adaptive_pixelizer/image_utils.py
# このファイルは変更の必要はありません。
import traceback
from collections import Counter

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    # print("Warning: NumPy not found. Median calculation will be slower.") # main_windowで表示

from PIL import Image
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QBuffer, QByteArray, QIODevice # 代替変換用

# Pillow 10.0.0以降ではImage.Resampling.NEARESTを使用
# それ以前の場合は Image.NEAREST
try:
    NEAREST_NEIGHBOR = Image.Resampling.NEAREST
except AttributeError:
    NEAREST_NEIGHBOR = Image.NEAREST

# Pillow-PIL (ImageQt) のインポートを試みる
try:
    from PIL.ImageQt import ImageQt
    IMAGEQT_AVAILABLE = True
except ImportError:
    IMAGEQT_AVAILABLE = False
    # print("Warning: Pillow-PIL (ImageQt) not found. Pillow to QImage conversion might be less efficient for some formats.") # main_windowで表示

# === 色計算関数 ===


def calculate_average_color(region, output_mode):
    """指定領域の平均色を計算"""
    try:
        # 計算は常にRGBAで行う
        target_mode_calc = 'RGBA'
        if region.mode != target_mode_calc:
            region_calc = region.convert(target_mode_calc)
        else:
            region_calc = region

        pixels = list(region_calc.getdata())
        num_pixels = len(pixels)
        if not pixels or num_pixels == 0:
            # 空の領域の場合、完全透明を返すように変更
            return (0, 0, 0, 0) # RGBAで返す

        sum_r, sum_g, sum_b, sum_a = 0, 0, 0, 0
        for p in pixels:
            # pが期待通り4要素のタプルか確認 (Pillowのgetdataの挙動依存)
            if len(p) == 4:
                sum_r += p[0]; sum_g += p[1]; sum_b += p[2]; sum_a += p[3]
            elif len(p) == 3: # RGBの場合 (RGBA変換がうまくいかなかった場合のフォールバック?)
                 sum_r += p[0]; sum_g += p[1]; sum_b += p[2]; sum_a += 255 # アルファは不透明と仮定
            # 他の形式 (L, LAなど) はconvert('RGBA')でカバーされるはず

        avg_r = int(sum_r / num_pixels); avg_g = int(sum_g / num_pixels)
        avg_b = int(sum_b / num_pixels); avg_a = int(sum_a / num_pixels)

        return (avg_r, avg_g, avg_b, avg_a) # RGBAタプルで返す
    except Exception as e:
        print(f"Average color calculation error: {e}\n{traceback.format_exc()}")
        # エラー時もNoneではなくデフォルト色を返す方が安全かも
        return (128, 128, 128, 255) # RGBAで返す


def calculate_median_color(region, output_mode):
    """指定領域の中央値を計算 (NumPy利用を試みる)"""
    global NUMPY_AVAILABLE
    try:
        target_mode_calc = 'RGBA'
        if region.mode != target_mode_calc:
            region_calc = region.convert(target_mode_calc)
        else:
            region_calc = region

        if NUMPY_AVAILABLE:
            pixels = np.array(region_calc)
            if pixels.size == 0: return (0, 0, 0, 0) # RGBAで返す
            # RGBA画像であることを確認 (shapeが (h, w, 4) になるはず)
            if pixels.ndim == 3 and pixels.shape[2] == 4:
                # NaNを無視して中央値を計算（完全透明ピクセルなどがある場合）
                # median_values = np.nanmedian(pixels.reshape(-1, 4).astype(float), axis=0) # astype(float)が必要かも
                # 単純なmedianで問題ないことが多い
                median_values = np.median(pixels.reshape(-1, 4), axis=0)
                med_r, med_g, med_b, med_a = map(int, median_values)
            else: # グレースケールやRGBなど予期しない形式の場合
                 print(f"Warning: Unexpected image shape in median calculation: {pixels.shape}. Trying fallback.")
                 # NumPyなしロジックへフォールバック
                 NUMPY_AVAILABLE = False # 一時的に無効化して再試行
                 return calculate_median_color(region, output_mode)

        else: # NumPyがない場合
            pixels = list(region_calc.getdata())
            if not pixels:
                return (0, 0, 0, 0) # RGBAで返す
            num_pixels = len(pixels)
            r, g, b, a = [], [], [], []
            valid_pixels = 0
            for p in pixels:
                if len(p) == 4:
                    r.append(p[0]); g.append(p[1]); b.append(p[2]); a.append(p[3])
                    valid_pixels += 1
                elif len(p) == 3: # RGBフォールバック
                    r.append(p[0]); g.append(p[1]); b.append(p[2]); a.append(255)
                    valid_pixels += 1
            if valid_pixels == 0: # 有効なピクセルがなかった場合
                return (0, 0, 0, 0) # RGBAで返す

            r.sort(); g.sort(); b.sort(); a.sort()
            mid = valid_pixels // 2
            # midがリストの範囲内か確認
            if mid < len(r):
                med_r, med_g, med_b, med_a = r[mid], g[mid], b[mid], a[mid]
            elif valid_pixels > 0: # ピクセル数が1などのエッジケース
                med_r, med_g, med_b, med_a = r[0], g[0], b[0], a[0]
            else: # このケースは起こらないはずだが念のため
                return (0, 0, 0, 0)


        return (med_r, med_g, med_b, med_a) # RGBAタプルで返す
    except Exception as e:
        print(f"Median color calculation error: {e}\n{traceback.format_exc()}")
        return (128, 128, 128, 255) # RGBAで返す


def calculate_mode_color(region, output_mode):
    """指定領域の最頻色を計算"""
    try:
        target_mode_calc = 'RGBA'
        if region.mode != target_mode_calc:
            region_calc = region.convert(target_mode_calc)
        else:
            region_calc = region

        pixels = list(region_calc.getdata())
        if not pixels:
            return (0, 0, 0, 0) # RGBAで返す

        # CounterはRGBAタプルに対して正しく動作する
        count = Counter(pixels)
        if not count:
            return (0, 0, 0, 0) # RGBAで返す

        # most_common(1) は [(element, count)] のリストを返す
        mode_color_rgba = count.most_common(1)[0][0]

        # mode_color_rgbaが期待通りタプルか確認
        if isinstance(mode_color_rgba, tuple) and len(mode_color_rgba) == 4:
            return mode_color_rgba
        elif isinstance(mode_color_rgba, tuple) and len(mode_color_rgba) == 3: # RGBの場合
            return mode_color_rgba + (255,) # アルファ追加 (RGBA)
        else:
             print(f"Warning: Unexpected mode color format: {mode_color_rgba}")
             # 不正な形式ならエラー色
             return (255, 0, 255, 255) # RGBAで返す

    except Exception as e:
        print(f"Mode color calculation error: {e}\n{traceback.format_exc()}")
        return (128, 128, 128, 255) # RGBAで返す

# === Pillow <=> QImage/QPixmap 変換関数 ===

def pillow_to_qimage(pillow_img):
    """Pillow ImageをQImageに変換 (InteractiveImageLabel用, bytesPerLine指定)"""
    global IMAGEQT_AVAILABLE # グローバル変数を参照
    try:
        # 優先: ImageQt が利用可能ならそれを使う (より多くのフォーマットに対応する可能性がある)
        if IMAGEQT_AVAILABLE:
            try:
                # ImageQtもRGBAを推奨
                target_mode = 'RGBA'
                if pillow_img.mode != target_mode:
                    pillow_img_conv = pillow_img.convert(target_mode)
                else:
                    pillow_img_conv = pillow_img

                # ImageQtオブジェクトを作成
                img_qt_obj = ImageQt(pillow_img_conv)

                # ImageQtオブジェクトが直接QImageを返すか確認
                if isinstance(img_qt_obj, QImage):
                    return img_qt_obj.copy()
                else:
                    # QPixmapに変換してからQImageに変換 (古いPillow/ImageQtバージョン用)
                    pixmap = QPixmap.fromImage(img_qt_obj)
                    return pixmap.toImage().copy()

            except Exception as e_imgqt:
                print(f"ImageQt conversion failed: {e_imgqt}. Falling back to manual conversion.")
                IMAGEQT_AVAILABLE = False # ImageQtでの変換に失敗したら以降は使わない

        # フォールバック: 手動での変換 (RGBA/RGBのみ対応)
        target_mode = 'RGBA' # 基本的にRGBAでQImageを作る
        bytes_per_pixel = 4
        qt_format = QImage.Format.Format_RGBA8888

        if pillow_img.mode == 'RGB':
            target_mode = 'RGB'
            bytes_per_pixel = 3
            qt_format = QImage.Format.Format_RGB888
            pillow_img_conv = pillow_img # 変換不要
        elif pillow_img.mode != 'RGBA':
            # RGBAでもRGBでもない場合、RGBAに変換
            try:
                pillow_img_conv = pillow_img.convert('RGBA')
            except Exception as convert_err:
                 print(f"Error converting image to RGBA: {convert_err}")
                 return None # 変換できない場合はNoneを返す
        else:
            pillow_img_conv = pillow_img # RGBAなので変換不要

        data = pillow_img_conv.tobytes("raw", target_mode)
        width = pillow_img_conv.width
        height = pillow_img_conv.height
        bytes_per_line = width * bytes_per_pixel
        qimage = QImage(data, width, height, bytes_per_line, qt_format)

        # データのコピーを作成して返すのが安全
        return qimage.copy()

    except Exception as e:
        print(f"Error converting Pillow to QImage (mode: {pillow_img.mode}): {e}\n{traceback.format_exc()}")
        # さらなるフォールバック: QBuffer経由での変換を試みる (PNG形式に依存)
        try:
            print("Falling back to QBuffer conversion (via PNG).")
            buffer = QBuffer()
            buffer.open(QIODevice.OpenModeFlag.ReadWrite)
            # Pillow画像をPNG形式でメモリ上のバッファに保存
            pillow_img.save(buffer, "PNG")
            buffer.seek(0)
            qimage = QImage()
            # QImageがバッファからPNGを読み込む
            if qimage.loadFromData(buffer.data(), "PNG"):
                 return qimage.copy() # 成功したらコピーを返す
            else:
                 print("QBuffer conversion failed.")
                 return None
        except Exception as e_buffer:
             print(f"QBuffer conversion fallback failed: {e_buffer}")
             return None


def pillow_to_qimage_for_display(pillow_img):
    """表示用にPillow画像をQImageに変換するヘルパー (PixelatorWindow用)"""
    # InteractiveImageLabelと同じ変換ロジックを使用
    return pillow_to_qimage(pillow_img)