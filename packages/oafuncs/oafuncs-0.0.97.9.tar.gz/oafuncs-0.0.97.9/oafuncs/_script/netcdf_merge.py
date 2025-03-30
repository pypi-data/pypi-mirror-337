#!/usr/bin/env python
# coding=utf-8
"""
Author: Liu Kun && 16031215@qq.com
Date: 2025-03-30 11:16:29
LastEditors: Liu Kun && 16031215@qq.com
LastEditTime: 2025-03-30 11:16:31
FilePath: \\Python\\My_Funcs\\OAFuncs\\oafuncs\\_script\\netcdf_merge.py
Description:
EditPlatform: vscode
ComputerInfo: XPS 15 9510
SystemInfo: Windows 11
Python Version: 3.12
"""

import logging
import os
from typing import Dict, List, Union

import numpy as np
import xarray as xr
from dask.diagnostics import ProgressBar

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def merge(file_list: Union[str, List[str]], var_name: Union[str, List[str], None] = None, dim_name: str = "time", target_filename: str = "merged.nc", chunk_config: Dict = {"time": 1000}, compression: Union[bool, Dict] = True, sanity_check: bool = True, overwrite: bool = True, parallel: bool = True) -> None:
    """
    终极版NetCDF合并函数

    Parameters:
        file_list: 文件路径列表或单个文件路径
        var_name: 需要合并的变量（单个变量名/变量列表/None表示全部）
        dim_name: 合并维度，默认为'time'
        target_filename: 输出文件路径
        chunk_config: Dask分块配置，如{"time": 1000}
        compression: 压缩配置（True启用默认压缩，或自定义编码字典）
        sanity_check: 是否执行数据完整性校验
        overwrite: 是否覆盖已存在文件
        parallel: 是否启用并行处理

    Example:
        merge(["data1.nc", "data2.nc"],
             var_name=["temp", "salt"],
             target_filename="result.nc",
             chunk_config={"time": 500})
    """
    # ------------------------ 参数预处理 ------------------------#
    file_list = _validate_and_preprocess_inputs(file_list, target_filename, overwrite)
    all_vars, var_names = _determine_variables(file_list, var_name)
    static_vars = _identify_static_vars(file_list[0], var_names, dim_name)

    # 估计处理所需的内存
    _estimate_memory_usage(file_list, var_names, chunk_config)

    # ------------------------ 数据校验阶段 ------------------------#
    if sanity_check:
        _perform_sanity_checks(file_list, var_names, dim_name, static_vars)

    # ------------------------ 核心合并逻辑 ------------------------#
    with xr.set_options(keep_attrs=True):  # 保留元数据属性
        # 动态变量合并
        merged_ds = xr.open_mfdataset(
            file_list,
            combine="nested",
            concat_dim=dim_name,
            data_vars=[var for var in var_names if var not in static_vars],
            chunks=chunk_config,
            parallel=parallel,
            preprocess=lambda ds: ds[var_names],  # 仅加载目标变量
        )

        # 静态变量处理
        if static_vars:
            with xr.open_dataset(file_list[0], chunks=chunk_config) as ref_ds:
                merged_ds = merged_ds.assign({var: ref_ds[var] for var in static_vars})

    # ------------------------ 时间维度处理 ------------------------#
    if dim_name == "time":
        merged_ds = _process_time_dimension(merged_ds)

    # ------------------------ 文件输出 ------------------------#
    encoding = _generate_encoding_config(merged_ds, compression)
    _write_to_netcdf(merged_ds, target_filename, encoding)


# ------------------------ 辅助函数 ------------------------#
def _validate_and_preprocess_inputs(file_list: Union[str, List[str]], target_filename: str, overwrite: bool) -> List[str]:
    """输入参数校验与预处理"""
    if not file_list:
        raise ValueError("文件列表不能为空")

    file_list = [file_list] if isinstance(file_list, str) else file_list
    for f in file_list:
        if not os.path.exists(f):
            raise FileNotFoundError(f"输入文件不存在: {f}")

    target_dir = os.path.dirname(os.path.abspath(target_filename))
    os.makedirs(target_dir, exist_ok=True)

    if os.path.exists(target_filename):
        if overwrite:
            logger.warning(f"覆盖已存在文件: {target_filename}")
            os.remove(target_filename)
        else:
            raise FileExistsError(f"目标文件已存在: {target_filename}")

    return file_list


def _determine_variables(file_list: List[str], var_name: Union[str, List[str], None]) -> tuple:
    """确定需要处理的变量列表"""
    with xr.open_dataset(file_list[0]) as ds:
        all_vars = list(ds.data_vars.keys())

    if var_name is None:
        return all_vars, all_vars
    elif isinstance(var_name, str):
        if var_name not in all_vars:
            raise ValueError(f"无效变量名: {var_name}")
        return all_vars, [var_name]
    elif isinstance(var_name, list):
        if not var_name:  # 处理空列表情况
            logger.warning("提供了空的变量列表，将使用所有变量")
            return all_vars, all_vars
        invalid_vars = set(var_name) - set(all_vars)
        if invalid_vars:
            raise ValueError(f"无效变量名: {invalid_vars}")
        return all_vars, var_name
    else:
        raise TypeError("var_name参数类型必须是str/list/None")


def _identify_static_vars(sample_file: str, var_names: List[str], dim_name: str) -> List[str]:
    """识别静态变量"""
    with xr.open_dataset(sample_file) as ds:
        return [var for var in var_names if dim_name not in ds[var].dims]


def _perform_sanity_checks(file_list: List[str], var_names: List[str], dim_name: str, static_vars: List[str]) -> None:
    """执行数据完整性校验"""
    logger.info("正在执行数据完整性校验...")

    # 静态变量一致性检查
    with xr.open_dataset(file_list[0]) as ref_ds:
        for var in static_vars:
            ref = ref_ds[var]
            for f in file_list[1:]:
                with xr.open_dataset(f) as ds:
                    if not ref.equals(ds[var]):
                        raise ValueError(f"静态变量 {var} 不一致\n参考文件: {file_list[0]}\n问题文件: {f}")

    # 动态变量维度检查
    dim_sizes = {}
    for f in file_list:
        with xr.open_dataset(f) as ds:
            for var in var_names:
                if var not in static_vars:
                    dims = ds[var].dims
                    if dim_name not in dims:
                        raise ValueError(f"变量 {var} 在文件 {f} 中缺少合并维度 {dim_name}")
                    dim_sizes.setdefault(var, []).append(ds[var].sizes[dim_name])

    # 检查维度连续性
    for var, sizes in dim_sizes.items():
        if len(set(sizes[1:])) > 1:
            raise ValueError(f"变量 {var} 的 {dim_name} 维度长度不一致: {sizes}")


def _process_time_dimension(ds: xr.Dataset) -> xr.Dataset:
    """时间维度特殊处理"""
    if "time" not in ds.dims:
        return ds

    # 排序并去重
    ds = ds.sortby("time")
    # 找到唯一时间戳的索引
    _, index = np.unique(ds["time"], return_index=True)
    # 无需再次排序索引，因为我们需要保持时间的原始顺序
    return ds.isel(time=index)


def _generate_encoding_config(ds: xr.Dataset, compression: Union[bool, Dict]) -> Dict:
    """生成压缩编码配置"""
    if not compression:
        return {}

    # 默认压缩设置基础
    def _get_default_encoding(var):
        return {"zlib": True, "complevel": 3, "dtype": "float32" if ds[var].dtype == "float64" else ds[var].dtype}

    # 处理自定义压缩配置
    encoding = {}
    if isinstance(compression, dict):
        for var in ds.data_vars:
            encoding[var] = _get_default_encoding(var)
            encoding[var].update(compression.get(var, {}))  # 使用 dict.update() 合并字典
    else:
        for var in ds.data_vars:
            encoding[var] = _get_default_encoding(var)

    return encoding


def _write_to_netcdf(ds: xr.Dataset, filename: str, encoding: Dict) -> None:
    """改进后的安全写入NetCDF文件"""
    logger.info("开始写入文件...")
    unlimited_dims = [dim for dim in ds.dims if ds[dim].encoding.get("unlimited", False)]

    delayed = ds.to_netcdf(filename, encoding=encoding, compute=False, unlimited_dims=unlimited_dims)

    try:
        with ProgressBar():
            delayed.compute()

        logger.info(f"合并完成 → {filename}")
        logger.info(f"文件大小: {os.path.getsize(filename) / 1e9:.2f}GB")
    except MemoryError as e:
        _handle_write_error(filename, "内存不足，无法完成文件写入。请尝试调整chunk_config参数减少内存使用", e)
    except Exception as e:
        _handle_write_error(filename, f"写入文件失败: {str(e)}", e)


def _handle_write_error(filename: str, message: str, exception: Exception) -> None:
    """统一处理写入文件的异常"""
    logger.error(message)
    if os.path.exists(filename):
        os.remove(filename)
    raise exception


def _estimate_memory_usage(file_list: List[str], var_names: List[str], chunk_config: Dict) -> None:
    """改进内存使用量估算"""
    try:
        total_size = 0
        sample_file = file_list[0]
        with xr.open_dataset(sample_file) as ds:
            for var in var_names:
                if var in ds:
                    # 考虑变量的维度大小
                    var_size = np.prod([ds[var].sizes[dim] for dim in ds[var].dims]) * ds[var].dtype.itemsize
                    total_size += var_size * len(file_list)

        # 估算Dask处理时的内存使用量 (通常是原始数据的2-3倍)
        estimated_memory = total_size * 3

        if estimated_memory > 8e9:
            logger.warning(f"预计内存使用可能较高 (约 {estimated_memory / 1e9:.1f}GB)。如果遇到内存问题，请调整chunk_config参数: {chunk_config}")
    except Exception as e:
        logger.debug(f"内存估计失败: {str(e)}")


if __name__ == "__main__":
    # 示例文件列表（请替换为实际文件路径）
    sample_files = ["data/file1.nc", "data/file2.nc", "data/file3.nc"]

    # 示例1: 基础用法 - 合并全部变量
    print("\n" + "=" * 40)
    print("示例1: 合并所有变量（默认配置）")
    merge(file_list=sample_files, target_filename="merged_all_vars.nc")

    # 示例2: 合并指定变量
    print("\n" + "=" * 40)
    print("示例2: 合并指定变量（温度、盐度）")
    merge(
        file_list=sample_files,
        var_name=["temperature", "salinity"],
        target_filename="merged_selected_vars.nc",
        chunk_config={"time": 500},  # 更保守的内存分配
    )

    # 示例3: 自定义压缩配置
    print("\n" + "=" * 40)
    print("示例3: 自定义压缩参数")
    merge(file_list=sample_files, var_name="chlorophyll", compression={"chlorophyll": {"zlib": True, "complevel": 5, "dtype": "float32"}}, target_filename="merged_compressed.nc")

    # 示例4: 处理大型数据集
    print("\n" + "=" * 40)
    print("示例4: 大文件分块策略")
    merge(file_list=sample_files, chunk_config={"time": 2000, "lat": 100, "lon": 100}, target_filename="merged_large_dataset.nc", parallel=True)

    # 示例5: 时间维度特殊处理
    print("\n" + "=" * 40)
    print("示例5: 时间维度排序去重")
    merge(
        file_list=sample_files,
        dim_name="time",
        target_filename="merged_time_processed.nc",
        sanity_check=True,  # 强制数据校验
    )

    # 示例6: 覆盖已存在文件
    print("\n" + "=" * 40)
    print("示例6: 强制覆盖现有文件")
    try:
        merge(
            file_list=sample_files,
            target_filename="merged_all_vars.nc",  # 与示例1相同文件名
            overwrite=True,  # 显式启用覆盖
        )
    except FileExistsError as e:
        print(f"捕获预期外异常: {str(e)}")

    # 示例7: 禁用并行处理
    print("\n" + "=" * 40)
    print("示例7: 单线程模式运行")
    merge(file_list=sample_files, target_filename="merged_single_thread.nc", parallel=False)

    # 示例8: 处理特殊维度
    print("\n" + "=" * 40)
    print("示例8: 按深度维度合并")
    merge(file_list=sample_files, dim_name="depth", var_name=["density", "oxygen"], target_filename="merged_by_depth.nc")

    # 示例9: 混合变量类型处理
    print("\n" + "=" * 40)
    print("示例9: 混合静态/动态变量")
    merge(
        file_list=sample_files,
        var_name=["bathymetry", "temperature"],  # bathymetry为静态变量
        target_filename="merged_mixed_vars.nc",
        sanity_check=True,  # 验证静态变量一致性
    )

    # 示例10: 完整配置演示
    print("\n" + "=" * 40)
    print("示例10: 全参数配置演示")
    merge(
        file_list=sample_files,
        var_name=None,  # 所有变量
        dim_name="time",
        target_filename="merged_full_config.nc",
        chunk_config={"time": 1000, "lat": 500, "lon": 500},
        compression={"temperature": {"complevel": 4}, "salinity": {"zlib": False}},
        sanity_check=True,
        overwrite=True,
        parallel=True,
    )
