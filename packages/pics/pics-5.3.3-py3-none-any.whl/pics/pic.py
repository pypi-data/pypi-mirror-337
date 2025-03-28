import os
from PIL import Image
import shutil


def cut_picture_by_size(pic_path: str, limit_size: float = 3):
    """
    让图片的重量变小，以接近limit_size。
    图变大没有意义，可以通过指定为png，compress_level=0 实现变很大，但没法变小且清晰度并没有提升
    """
    pic_folder = os.path.dirname(pic_path)
    pic_name = pic_path.rsplit(os.sep)[-1][:pic_path.rindex('.')]
    output_file = os.path.join(pic_folder, f'{pic_name}-{limit_size}.jpg')

    try:
        pic_opened = Image.open(pic_path)
    except FileNotFoundError as e:
        print("异常：文件没找到 %s" % e)
        return
    except Exception:
        raise TypeError("异常：此文件打不开或有问题 %s" % pic_path)

    jpg_ = pic_opened
    quality = 100

    # 小图变大无意义
    if os.path.getsize(pic_path) < limit_size * 1024 * 1024:
        shutil.copy(pic_path, output_file)
        return output_file
    ct = 0
    while True:
        ct += 1
        if ct > 30:
            break
        pic_size = os.path.getsize(output_file)
        if pic_size > limit_size * 1024 * 1024:
            quality -= 2
            jpg_.convert('RGB').save(output_file, quality=quality)
        else:
            break
    return output_file


def cut_picture_by_dimension(pic_path: str, size_list: list = [[1440, 2560]], limit_size: float = 3):
    """
    输入一张任意比例的图片，裁切成指定大小的图片。嵌套列表以应对多尺寸情况。
    """
    pic_folder = os.path.dirname(pic_path)
    pic_name = pic_path.rsplit(os.sep)[-1][:pic_path.rindex('.')]
    for once in size_list:
        width, high = int(once[0]), int(once[1])
        output_file = os.path.join(pic_folder, f'{pic_name}-{width}x{high}.jpg')

        try:
            pic_opened = Image.open(pic_path)
            pic_opened.convert('RGB')
        except FileNotFoundError as e:
            print("异常：文件没找到 %s" % e)
            continue
        except Exception:
            raise TypeError("异常：此文件打不开或有问题 %s" % pic_path)

        jpg_ = __crop__(pic_opened, width, high)
        if not jpg_:
            print("该图片资源有有误%s" % output_file)
            continue
        else:
            jpg_.convert('RGB').save(output_file, quality=100)
        if limit_size:
            quality = 100
            while True:
                pic_size = os.path.getsize(output_file)
                if pic_size > limit_size * 1024 * 1024:
                    quality -= 2
                    jpg_.convert('RGB').save(output_file, quality=quality)
                else:
                    break
        return output_file


def __crop__(pic_image, nx=None, ny=None):
    """
    剪裁图片，小图切大，大图切小。
    """
    try:
        x, y = pic_image.size
    except AttributeError:
        return None

    k = x / y
    nk = nx / ny
    if k > nk:  # 切两边
        x_left = (x / 2) - (y * nk / 2)
        x_right = (x / 2) + (y * nk / 2)
        region = (x_left, 0, x_right, y)  # 对角线两点坐标的合集
        pic_image = pic_image.crop(region)
    else:  # 切上下
        y_top = (y / 2) - (x / nk / 2)
        y_bottom = (y / 2) + (x / nk / 2)
        region = (0, y_top, x, y_bottom)
        pic_image = pic_image.crop(region)
    return pic_image.resize((nx, ny), Image.Resampling.LANCZOS)
