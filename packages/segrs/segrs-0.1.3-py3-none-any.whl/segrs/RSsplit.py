import rasterio
from rasterio.windows import Window
import os
from tqdm import tqdm


def crop_tif(input_path, output_dir="output", tile_size=512, overlap=0, keep_size=False, name = "tile"):
    """
    此函数用于将一个大的 TIF 影像裁剪成多个小的瓦片。

    参数:
    input_path (str): 输入的大 TIF 影像的文件路径。
    output_dir (str, 可选): 裁剪后小瓦片的输出目录，默认为 "output"。
    tile_size (int, 可选): 每个小瓦片的尺寸，默认为 512。
    overlap (float, 可选): 小瓦片之间的重叠率，范围是 0 到 1，默认为 0。
    keep_size (bool, 可选): 是否只保留尺寸为 tile_size x tile_size 的瓦片，默认为 False。
    name (str, 可选): 输出小瓦片文件名的前缀，默认为 "tile"。

    返回:
    无
    """
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    overlap_pixels = int(tile_size * overlap)

    with rasterio.open(input_path) as src:
        width = src.width
        height = src.height
        print(f"tile size: {tile_size}, overlap: {overlap_pixels}, keep_size: {keep_size}")
        
        col_index = 0
        for col in tqdm(range(0, width, tile_size - overlap_pixels),desc=f"Crop tif file {input_path}"):
            row_index = 0
            for row in range(0, height, tile_size - overlap_pixels):
                # 确保窗口不超出影像边界
                window_width = min(tile_size, width - col)
                window_height = min(tile_size, height - row)

                if keep_size and (window_width != tile_size or window_height != tile_size):
                    continue

                window = Window(col, row, window_width, window_height)
                transform = src.window_transform(window)

                # 读取窗口内的数据
                data = src.read(window=window)

                # 定义输出文件路径，使用行列编号
                output_filename = os.path.join(output_dir, f"{name}_{col_index + 1}_{row_index + 1}.tif")

                # 创建输出文件
                profile = src.profile
                profile.update(
                    width=window_width,
                    height=window_height,
                    transform=transform
                )

                with rasterio.open(output_filename, 'w', **profile) as dst:
                    dst.write(data)

                row_index += 1
            col_index += 1
    