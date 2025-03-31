# src/grid_pixelator/image_utils.py
import traceback
from collections import Counter

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    print("Warning: NumPy not found. Median calculation will be slower.")

from PIL import Image
from PyQt6.QtGui import QImage, QPixmap

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
    # print("Warning: Pillow-PIL (ImageQt) not found. Pillow to QImage conversion might be less efficient for some formats.") # 起動時のメッセージはmain側で

# === 色計算関数 ===

def calculate_average_color(region, output_mode):
    """指定領域の平均色を計算"""
    try:
        target_mode_calc = 'RGBA'
        if region.mode != target_mode_calc:
            region_calc = region.convert(target_mode_calc)
        else:
            region_calc = region

        pixels = list(region_calc.getdata())
        num_pixels = len(pixels)
        if not pixels or num_pixels == 0: return None

        sum_r, sum_g, sum_b, sum_a = 0, 0, 0, 0
        for p in pixels:
            sum_r += p[0]; sum_g += p[1]; sum_b += p[2]; sum_a += p[3]

        avg_r = int(sum_r / num_pixels); avg_g = int(sum_g / num_pixels)
        avg_b = int(sum_b / num_pixels); avg_a = int(sum_a / num_pixels)

        return (avg_r, avg_g, avg_b, avg_a) if output_mode == 'RGBA' else (avg_r, avg_g, avg_b)
    except Exception as e:
        print(f"Average color calculation error: {e}")
        return None

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
            if pixels.size == 0: return None
            median_values = np.median(pixels.reshape(-1, 4), axis=0)
            med_r, med_g, med_b, med_a = map(int, median_values)
        else:
            pixels = list(region_calc.getdata())
            if not pixels: return None
            num_pixels = len(pixels)
            r, g, b, a = [], [], [], []
            for p in pixels: r.append(p[0]); g.append(p[1]); b.append(p[2]); a.append(p[3])
            r.sort(); g.sort(); b.sort(); a.sort()
            mid = num_pixels // 2
            med_r, med_g, med_b, med_a = r[mid], g[mid], b[mid], a[mid]

        return (med_r, med_g, med_b, med_a) if output_mode == 'RGBA' else (med_r, med_g, med_b)
    except Exception as e:
        print(f"Median color calculation error: {e}")
        return None

def calculate_mode_color(region, output_mode):
    """指定領域の最頻色を計算"""
    try:
        target_mode_calc = 'RGBA'
        if region.mode != target_mode_calc:
            region_calc = region.convert(target_mode_calc)
        else:
            region_calc = region

        pixels = list(region_calc.getdata())
        if not pixels: return None
        count = Counter(pixels)
        if not count: return None
        mode_color_rgba = count.most_common(1)[0][0]

        return mode_color_rgba if output_mode == 'RGBA' else mode_color_rgba[:3]
    except Exception as e:
        print(f"Mode color calculation error: {e}")
        return None

# === Pillow <=> QImage/QPixmap 変換関数 ===

def pillow_to_qimage(pillow_img):
    """Pillow ImageをQImageに変換 (InteractiveImageLabel用, bytesPerLine指定)"""
    try:
        if pillow_img.mode not in ('RGB', 'RGBA'):
            pillow_img_conv = pillow_img.convert('RGBA')
            image_format = QImage.Format.Format_RGBA8888
            bytes_per_pixel = 4
        elif pillow_img.mode == 'RGB':
            pillow_img_conv = pillow_img
            image_format = QImage.Format.Format_RGB888
            bytes_per_pixel = 3
        else: # RGBA
            pillow_img_conv = pillow_img
            image_format = QImage.Format.Format_RGBA8888
            bytes_per_pixel = 4

        data = pillow_img_conv.tobytes("raw", pillow_img_conv.mode)
        width = pillow_img_conv.width
        height = pillow_img_conv.height
        bytes_per_line = width * bytes_per_pixel
        qimage = QImage(data, width, height, bytes_per_line, image_format)

        # RGB888の場合、rgbSwapped() は通常不要 (PillowのRGBとQtのRGB888は通常一致)
        # if image_format == QImage.Format.Format_RGB888:
        #     qimage = qimage.rgbSwapped()

        return qimage.copy()

    except Exception as e:
        print(f"Error converting Pillow to QImage (mode: {pillow_img.mode}): {e}\n{traceback.format_exc()}")
        if IMAGEQT_AVAILABLE:
            try:
                print("Falling back to ImageQt conversion.")
                if pillow_img.mode != 'RGBA':
                    pillow_img_rgba = pillow_img.convert('RGBA')
                else:
                    pillow_img_rgba = pillow_img
                img_qt_obj = ImageQt(pillow_img_rgba)
                if isinstance(img_qt_obj, QImage):
                    return img_qt_obj.copy()
                else:
                    pixmap = QPixmap.fromImage(img_qt_obj)
                    return pixmap.toImage().copy()
            except Exception as e_imgqt:
                print(f"Fallback ImageQt conversion failed: {e_imgqt}")
                return None
        return None

def pillow_to_qimage_for_display(pillow_img):
    """表示用にPillow画像をQImageに変換するヘルパー (PixelatorWindow用)"""
    # この関数は InteractiveImageLabel のものとほぼ同じロジックで良い場合が多い
    # 必要であれば右側表示用に特化した変換（例：常にRGBAにするなど）をここに実装
    # 今回は pillow_to_qimage と同じ実装を流用
    # ただし、エラー時の ImageQt フォールバックは簡略化しても良いかもしれない

    try:
        # 基本的に pillow_to_qimage と同じロジックを使用
        if pillow_img.mode not in ('RGB', 'RGBA'):
            pillow_img_conv = pillow_img.convert('RGBA')
            image_format = QImage.Format.Format_RGBA8888
            bytes_per_pixel = 4
        elif pillow_img.mode == 'RGB':
            pillow_img_conv = pillow_img
            image_format = QImage.Format.Format_RGB888
            bytes_per_pixel = 3
        else: # RGBA
            pillow_img_conv = pillow_img
            image_format = QImage.Format.Format_RGBA8888
            bytes_per_pixel = 4

        data = pillow_img_conv.tobytes("raw", pillow_img_conv.mode)
        width = pillow_img_conv.width
        height = pillow_img_conv.height
        bytes_per_line = width * bytes_per_pixel
        qimage = QImage(data, width, height, bytes_per_line, image_format)

        # if image_format == QImage.Format.Format_RGB888:
        #     qimage = qimage.rgbSwapped()

        return qimage.copy()

    except Exception as e:
        # 右側表示用のエラーメッセージ
        print(f"Display conversion error (pillow_to_qimage_for_display, mode: {pillow_img.mode}): {e}")
        # ImageQtフォールバック (シンプル版)
        if IMAGEQT_AVAILABLE:
             try:
                 return ImageQt(pillow_img.convert('RGBA')).copy() # ImageQtはRGBA推奨
             except Exception as e_imgqt:
                 print(f"Fallback ImageQt conversion for display failed: {e_imgqt}")
                 return None
        return None