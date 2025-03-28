#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Atomorph Core Converter
"""

import os
import warnings
from pathlib import Path
from typing import Dict, List, Optional, Union
import ase.io
from ase import Atoms
import sys
from ase.io import read, write
from ase.constraints import FixAtoms
import numpy as np
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial

# Filter out ASE spacegroup warnings
warnings.filterwarnings("ignore", category=UserWarning, module="ase.spacegroup.spacegroup")

class StructureConverter:
    """原子结构文件格式转换器"""
    
    # 默认元素顺序（按元素周期表顺序）
    DEFAULT_ELEMENT_ORDER = [
        "H", "He",
        "Li", "Be", "B", "C", "N", "O", "F", "Ne",
        "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar",
        "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr",
        "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe",
        "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu",
        "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn",
        "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr",
        "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"
    ]

    def __init__(self):
        """初始化转换器"""
        self.single_frame_only_formats = ["vasp"]
        self.format_mapping = {
            "xyz": "extxyz",  # Map xyz to extxyz
            "extxyz": "extxyz"
        }
        self.element_order = self.DEFAULT_ELEMENT_ORDER
        self.sort_order = "ascending"  # 默认升序排序
        self.MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
        self.MAX_WORKERS = os.cpu_count() or 4  # 使用CPU核心数或默认4个线程
    
    def _check_file_size(self, file_path):
        """检查文件大小是否超过限制"""
        file_size = os.path.getsize(file_path)
        if file_size > self.MAX_FILE_SIZE:
            raise ValueError(f"文件大小 ({file_size/1024/1024:.2f}MB) 超过限制 ({self.MAX_FILE_SIZE/1024/1024:.2f}MB)")

    def _show_progress(self, total, desc="处理中"):
        """显示进度条"""
        return tqdm(total=total, desc=desc, unit="帧")

    def _process_frame(self, frame, output_path, constraints):
        """处理单个结构帧"""
        try:
            self._write_vasp(frame, output_path, constraints)
            return True, output_path
        except Exception as e:
            return False, str(e)

    def convert(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        input_format: Optional[str] = None,
        output_format: Optional[str] = None,
        mode: Optional[str] = None,
        frame: Optional[int] = None,
        element_mapping: Optional[Dict[str, str]] = None,
        constraints: Optional[Dict[str, Union[List[int], bool]]] = None,
        element_order: Optional[List[str]] = None,
        sort_order: str = "ascending",
        parallel: bool = True,
        multi_frame: bool = False
    ) -> None:
        """
        转换原子结构文件格式
        
        Args:
            input_path: 输入文件路径
            output_path: 输出文件路径
            input_format: 输入文件格式
            output_format: 输出文件格式
            mode: 转换模式，'single'或'multi'
            frame: 要转换的帧索引
            element_mapping: 元素映射字典
            constraints: 原子约束配置
            element_order: 元素排序顺序列表，如果为None则使用默认顺序
            sort_order: 排序顺序，"ascending"（升序）或"descending"（降序）
            parallel: 是否并行处理
            multi_frame: 是否为多帧处理模式
        """
        try:
            # 检查文件大小
            self._check_file_size(input_path)
            
            # 设置元素排序顺序
            if element_order is not None:
                self.element_order = element_order
            
            # 设置排序顺序
            self.sort_order = sort_order
            
            # Convert paths to Path objects
            input_path = Path(input_path)
            output_path = Path(output_path)
            
            # Auto-detect file format
            if input_format is None:
                input_format = input_path.suffix[1:]
            if output_format is None:
                output_format = output_path.suffix[1:]
            
            # Map file formats
            input_format = self.format_mapping.get(input_format, input_format)
            output_format = self.format_mapping.get(output_format, output_format)
            
            # Auto-detect mode
            if mode is None:
                mode = "multi" if multi_frame else "single"
            
            # Validate mode
            self._validate_mode(mode, output_format)
            
            # Read structures
            structures = self._read_structures(input_path, input_format, frame)
            
            # Apply element mapping
            if element_mapping:
                structures = self._apply_element_mapping(structures, element_mapping)
            
            # 在排序之前应用所有约束
            if constraints:
                # 应用固定原子约束
                if "fixed_atoms" in constraints:
                    structures = self._apply_fixed_atoms(structures, constraints["fixed_atoms"])
                
                # 应用固定元素约束
                if "fixed_elements" in constraints:
                    structures = self._apply_fixed_elements(structures, constraints["fixed_elements"])
                
                # 应用固定层约束
                if "fixed_layers" in constraints:
                    layer_thickness = constraints.get("layer_thickness", 1.0)
                    structures = self._apply_fixed_layers(structures, constraints["fixed_layers"], layer_thickness)
            
            # Handle output
            if output_format == "vasp":
                # 对于VASP格式，使用自定义的写入函数
                if mode == "single":
                    self._write_vasp(structures[0], output_path, constraints)
                else:
                    # 创建输出目录
                    output_path.mkdir(parents=True, exist_ok=True)
                    if parallel:
                        # 并行处理多帧
                        print(f"使用{self.MAX_WORKERS}个线程并行处理...")
                        with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
                            # 创建任务列表
                            futures = []
                            for i, structure in enumerate(structures):
                                frame_output = output_path / f"frame_{i+1}.vasp"
                                future = executor.submit(self._process_frame, structure, frame_output, constraints)
                                futures.append(future)
                            
                            # 使用进度条显示处理进度
                            with self._show_progress(len(futures), "并行处理多帧结构") as pbar:
                                for future in as_completed(futures):
                                    success, result = future.result()
                                    if not success:
                                        print(f"警告：处理失败 - {result}")
                                    pbar.update(1)
                    else:
                        # 串行处理多帧
                        with self._show_progress(len(structures), "处理多帧结构") as pbar:
                            for i, structure in enumerate(structures):
                                frame_output = output_path / f"frame_{i+1}.vasp"
                                self._write_vasp(structure, frame_output, constraints)
                                pbar.update(1)
            else:
                # 对于其他格式，使用ASE的写入函数
                if mode == "single":
                    ase.io.write(output_path, structures[0], format=output_format)
                else:
                    if output_format in self.single_frame_only_formats:
                        # 创建输出目录
                        output_path.mkdir(parents=True, exist_ok=True)
                        for i, structure in enumerate(structures):
                            frame_path = output_path / f"frame_{i+1}.{output_format}"
                            ase.io.write(frame_path, structure, format=output_format)
                    else:
                        ase.io.write(output_path, structures, format=output_format)
            
            print(f"转换完成！输出文件：{output_path}")
            
        except Exception as e:
            raise ValueError(f"转换失败：{str(e)}")
    
    def _detect_mode(self, input_path: Path, input_format: str) -> str:
        """Detect conversion mode"""
        try:
            structures = ase.io.read(input_path, format=input_format, index=":")
            return "multi" if len(structures) > 1 else "single"
        except Exception:
            return "single"
    
    def _validate_mode(self, mode: str, output_format: str) -> None:
        """Validate conversion mode"""
        if mode == "multi" and output_format in self.single_frame_only_formats:
            if isinstance(output_format, str) and Path(output_format).suffix:
                raise ValueError(f"Output format {output_format} does not support multi-frame structures. Please choose another output format or use single-frame mode.")
    
    def _read_structures(
        self,
        input_path: Path,
        input_format: str,
        frame: Optional[int] = None,
    ) -> List[Atoms]:
        """Read structures"""
        try:
            if frame is not None:
                structures = [ase.io.read(input_path, format=input_format, index=frame-1)]
            else:
                try:
                    # Try to read all frames
                    structures = ase.io.read(input_path, format=input_format, index=":")
                except Exception:
                    # If failed, try to read single frame
                    structures = [ase.io.read(input_path, format=input_format)]
                
                if not isinstance(structures, list):
                    structures = [structures]
            
            # Ensure all structures have lattice
            for structure in structures:
                if structure.cell.rank < 3:
                    # Set default lattice
                    structure.set_cell([10.0, 10.0, 10.0])
                    structure.center()
            
            return structures
        except Exception as e:
            raise ValueError(f"Failed to read file: {str(e)}")
    
    def _apply_element_mapping(
        self,
        structures: List[Atoms],
        element_mapping: Dict[str, str],
    ) -> List[Atoms]:
        """Apply element mapping"""
        for structure in structures:
            symbols = structure.get_chemical_symbols()
            for i, symbol in enumerate(symbols):
                if symbol in element_mapping:
                    symbols[i] = element_mapping[symbol]
            structure.set_chemical_symbols(symbols)
        return structures
    
    def _apply_fixed_atoms(
        self,
        structures: List[Atoms],
        fixed_atoms: List[int],
    ) -> List[Atoms]:
        """Apply fixed atoms"""
        from ase.constraints import FixAtoms
        
        for structure in structures:
            constraint = FixAtoms(indices=fixed_atoms)
            structure.set_constraint(constraint)
        
        return structures
    
    def _apply_fixed_elements(
        self,
        structures: List[Atoms],
        fixed_elements: List[str],
    ) -> List[Atoms]:
        """应用固定元素约束"""
        from ase.constraints import FixAtoms
        
        for structure in structures:
            # 找到所有匹配元素的原子索引
            fixed_indices = []
            symbols = structure.get_chemical_symbols()
            for i, symbol in enumerate(symbols):
                if symbol in fixed_elements:
                    fixed_indices.append(i)
            
            # 应用约束
            if fixed_indices:
                constraint = FixAtoms(indices=fixed_indices)
                structure.set_constraint(constraint)
        
        return structures
    
    def _apply_fixed_layers(
        self,
        structures: List[Atoms],
        fixed_layers: List[int],
        layer_thickness: float = 1.0,
    ) -> List[Atoms]:
        """应用固定层约束"""
        from ase.constraints import FixAtoms
        
        for structure in structures:
            # 获取原子的z坐标
            positions = structure.get_positions()
            z_coords = positions[:, 2]
            min_z = min(z_coords)
            max_z = max(z_coords)
            
            # 计算层数
            n_layers = int((max_z - min_z) / layer_thickness) + 1
            
            # 找到所有在指定层中的原子索引
            fixed_indices = []
            for layer in fixed_layers:
                if 0 <= layer < n_layers:
                    layer_min = min_z + layer * layer_thickness
                    layer_max = layer_min + layer_thickness
                    for i, z in enumerate(z_coords):
                        if layer_min <= z < layer_max:
                            fixed_indices.append(i)
            
            # 应用约束
            if fixed_indices:
                constraint = FixAtoms(indices=fixed_indices)
                structure.set_constraint(constraint)
        
        return structures
    
    def _handle_output(
        self,
        structures: List[Atoms],
        output_path: Path,
        output_format: str,
        mode: str = "single",
    ) -> None:
        """Handle output"""
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if mode == "single":
                # Single frame mode: write directly to file
                if structures:
                    ase.io.write(output_path, structures[0], format=output_format)
            else:
                # Multi-frame mode: choose write method based on format
                if output_format in self.single_frame_only_formats:
                    # Formats not supporting multi-frame: create directory and write separately
                    output_path.mkdir(parents=True, exist_ok=True)
                    for i, structure in enumerate(structures):
                        frame_path = output_path / f"frame_{i+1}.{output_format}"
                        ase.io.write(frame_path, structure, format=output_format)
                else:
                    # Formats supporting multi-frame: write directly
                    ase.io.write(output_path, structures, format=output_format)
        except Exception as e:
            raise ValueError(f"Failed to write file: {str(e)}")

    def _write_vasp(self, atoms, output_path, constraints=None):
        """将结构写入VASP格式文件"""
        # 检查结构是否为空
        if len(atoms) == 0:
            raise ValueError("结构为空，无法写入VASP文件")
            
        # 获取晶格参数
        cell = atoms.get_cell()
        if cell is None or len(cell) == 0:
            raise ValueError("晶格参数为空，无法写入VASP文件")
            
        # 获取原子位置
        positions = atoms.get_positions()
        if positions is None or len(positions) == 0:
            raise ValueError("原子位置为空，无法写入VASP文件")
            
        # 获取元素信息
        symbols = atoms.get_chemical_symbols()
        if not symbols:
            raise ValueError("元素信息为空，无法写入VASP文件")
            
        # 获取元素排序参数
        sort_order = getattr(self, 'sort_order', 'ascending')
        element_order = getattr(self, 'element_order', None)
        
        # 创建元素到周期表位置的映射
        element_positions = {}
        for symbol in symbols:
            if symbol not in element_positions:
                if element_order and symbol in element_order:
                    element_positions[symbol] = element_order.index(symbol)
                else:
                    element_positions[symbol] = self._get_element_position(symbol)
        
        # 根据排序方式对元素进行排序
        reverse = sort_order == "descending"
        sorted_elements = sorted(set(symbols), key=lambda x: element_positions[x], reverse=reverse)
        
        # 重新排列原子
        new_indices = []
        for element in sorted_elements:
            new_indices.extend([i for i, s in enumerate(symbols) if s == element])
        
        # 重新排列原子
        atoms = atoms[new_indices]
        
        # 获取约束信息
        fixed_atoms = []
        if constraints:
            if "fixed_atoms" in constraints:
                fixed_atoms.extend(constraints["fixed_atoms"])
            if "fixed_elements" in constraints:
                for element in constraints["fixed_elements"]:
                    fixed_atoms.extend([i for i, s in enumerate(symbols) if s == element])
            if "fixed_layers" in constraints:
                layer_thickness = constraints.get("layer_thickness", 1.0)
                z_coords = positions[:, 2]
                min_z, max_z = z_coords.min(), z_coords.max()
                num_layers = int((max_z - min_z) / layer_thickness) + 1
                
                for layer in constraints["fixed_layers"]:
                    if 0 <= layer < num_layers:
                        layer_min = min_z + layer * layer_thickness
                        layer_max = layer_min + layer_thickness
                        layer_atoms = [i for i, z in enumerate(z_coords) 
                                     if layer_min <= z < layer_max]
                        fixed_atoms.extend(layer_atoms)
        
        # 写入VASP格式文件
        with open(output_path, 'w') as f:
            # 写入注释行
            f.write("Converted by Atomorph\n")
            
            # 写入缩放因子
            f.write("1.0\n")
            
            # 写入晶格参数
            for row in cell:
                f.write(f"{row[0]:.6f} {row[1]:.6f} {row[2]:.6f}\n")
            
            # 写入元素符号
            unique_symbols = []
            symbol_counts = []
            for symbol in sorted_elements:
                if symbol not in unique_symbols:
                    unique_symbols.append(symbol)
                    symbol_counts.append(symbols.count(symbol))
            
            f.write(" ".join(unique_symbols) + "\n")
            f.write(" ".join(map(str, symbol_counts)) + "\n")
            
            # 如果有固定原子，添加Selective dynamics标记
            if fixed_atoms:
                f.write("Selective dynamics\n")
            
            # 写入坐标类型
            f.write("Cartesian\n")
            
            # 写入原子坐标
            for i, (symbol, pos) in enumerate(zip(atoms.get_chemical_symbols(), atoms.get_positions())):
                # 确定原子是否被固定
                is_fixed = i in fixed_atoms
                # 写入坐标和固定标记
                f.write(f"{pos[0]:.6f} {pos[1]:.6f} {pos[2]:.6f} "
                       f"{'F F F' if is_fixed else 'T T T'} {symbol}\n")