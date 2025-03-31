'''
Author: Wangzhibo && ttbylzb11@gmail.com
Date: 2025-03-31 15:21:24
LastEditors: Wanzhiboo && ttbylzb11@gmail.com
LastEditTime: 2025-03-31 17:04:49
FilePath: /上传segrs/segrs/RSmerge.py
Description: 

Copyright (c) 2025 by ttbylzb11@gmail.com, All Rights Reserved. 
'''
import rasterio
import os
import numpy as np
from tqdm import tqdm

def merge_tiles(input_dir, output_path, tile_size=512, overlap=0, name="tile"):
    """
    此函数用于将指定目录下的多个小图（瓦片）合并成一个大图。

    参数:
    input_dir (str): 包含小图文件的目录路径。
    output_path (str): 合并后大图的输出文件路径。
    tile_size (int, 可选): 每个小图的尺寸（默认值为 512）。
    overlap (float, 可选): 小图之间的重叠率，范围为 0 到 1（默认值为 0）。
    name (str, 可选): 小图文件名的前缀（默认值为 "tile"）。

    返回:
    无
    """
    # 获取所有小图文件名
    tile_files = [f for f in os.listdir(input_dir) if f.startswith(name) and f.endswith('.tif')]

    # 计算最大行列编号
    max_col = 0
    max_row = 0
    for tile_file in tile_files:
        parts = tile_file.split('.')[0].split('_')
        col = int(parts[-2])
        row = int(parts[-1])
        if col > max_col:
            max_col = col
        if row > max_row:
            max_row = row

    # 计算大图的宽度和高度
    overlap_pixels = int(tile_size * overlap)
    width = (max_col - 1) * (tile_size - overlap_pixels) + tile_size
    height = (max_row - 1) * (tile_size - overlap_pixels) + tile_size

    # 读取第一个小图，获取元数据
    first_tile_path = os.path.join(input_dir, tile_files[0])
    with rasterio.open(first_tile_path) as src:
        profile = src.profile
        num_bands = src.count
        first_transform = src.transform

    new_transform = rasterio.Affine(first_transform.a, first_transform.b, first_transform.c,
                                    first_transform.d, first_transform.e, first_transform.f)

    # 更新元数据以适应大图
    profile.update(
        width=width,
        height=height,
        transform=new_transform
    )

    # 创建一个空的数组来存储大图数据
    big_image = np.zeros((num_bands, height, width), dtype=profile['dtype'])

    # 遍历每个小图并将其数据合并到大图中
    for tile_file in tqdm(tile_files,desc="Merge tif file"):
        parts = tile_file.split('.')[0].split('_')
        col = int(parts[-2]) - 1
        row = int(parts[-1]) - 1

        tile_path = os.path.join(input_dir, tile_file)
        with rasterio.open(tile_path) as src:
            tile_data = src.read()
            col_offset = col * (tile_size - overlap_pixels)
            row_offset = row * (tile_size - overlap_pixels)
            big_image[:, row_offset:row_offset + tile_size, col_offset:col_offset + tile_size] = tile_data

    # 将合并后的数据写入大图文件
    with rasterio.open(output_path, 'w', **profile) as dst:
        dst.write(big_image)
    