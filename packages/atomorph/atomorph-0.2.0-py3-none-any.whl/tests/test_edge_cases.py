import os
import sys
from pathlib import Path
from ase.io import read, write
from atomorph.converter.core.converter import StructureConverter

def setup_test_environment():
    """设置测试环境"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    return current_dir, data_dir

def test_empty_structure():
    """测试空结构处理"""
    print("\n=== 测试空结构处理 ===")
    current_dir, data_dir = setup_test_environment()
    converter = StructureConverter()
    
    # 创建一个空的结构文件
    input_path = os.path.join(data_dir, 'test_empty.cif')
    output_path = os.path.join(data_dir, 'test_empty.vasp')
    
    try:
        # 创建一个包含晶格参数但没有原子的结构
        with open(input_path, 'w') as f:
            f.write("data_empty\n")
            f.write("_cell_length_a 1.0\n")
            f.write("_cell_length_b 1.0\n")
            f.write("_cell_length_c 1.0\n")
            f.write("_cell_angle_alpha 90.0\n")
            f.write("_cell_angle_beta 90.0\n")
            f.write("_cell_angle_gamma 90.0\n")
            f.write("loop_\n")
            f.write("_atom_site_label\n")
            f.write("_atom_site_type_symbol\n")
            f.write("_atom_site_fract_x\n")
            f.write("_atom_site_fract_y\n")
            f.write("_atom_site_fract_z\n")
        
        converter.convert(
            input_path=input_path,
            output_path=output_path,
            input_format='cif',
            output_format='vasp'
        )
        print("✗ 空结构处理失败：应该抛出异常")
    except ValueError as e:
        print(f"✓ 空结构处理成功：捕获到预期的异常 - {str(e)}")

def test_large_file():
    """测试大文件处理"""
    print("\n=== 测试大文件处理 ===")
    current_dir, data_dir = setup_test_environment()
    converter = StructureConverter()
    
    # 创建一个超过大小限制的文件
    input_path = os.path.join(data_dir, 'test_large.cif')
    output_path = os.path.join(data_dir, 'test_large.vasp')
    
    try:
        # 创建一个超过100MB的文件
        with open(input_path, 'w') as f:
            # 写入大量重复的结构数据
            for _ in range(1000000):
                f.write("data_large\n")
                f.write("_cell_length_a 1.0\n")
                f.write("_cell_length_b 1.0\n")
                f.write("_cell_length_c 1.0\n")
                f.write("_cell_angle_alpha 90.0\n")
                f.write("_cell_angle_beta 90.0\n")
                f.write("_cell_angle_gamma 90.0\n")
                f.write("loop_\n")
                f.write("_atom_site_label\n")
                f.write("_atom_site_type_symbol\n")
                f.write("_atom_site_fract_x\n")
                f.write("_atom_site_fract_y\n")
                f.write("_atom_site_fract_z\n")
                f.write("Fe1 Fe 0.0 0.0 0.0\n")
        
        converter.convert(
            input_path=input_path,
            output_path=output_path,
            input_format='cif',
            output_format='vasp'
        )
        print("✗ 大文件处理失败：应该抛出异常")
    except ValueError as e:
        print(f"✓ 大文件处理成功：捕获到预期的异常 - {str(e)}")

def test_special_characters():
    """测试特殊字符处理"""
    print("\n=== 测试特殊字符处理 ===")
    current_dir, data_dir = setup_test_environment()
    converter = StructureConverter()
    
    # 创建一个包含特殊字符的文件
    input_path = os.path.join(data_dir, 'test_special.cif')
    output_path = os.path.join(data_dir, 'test_special.vasp')
    
    try:
        # 创建一个包含特殊字符的结构文件
        with open(input_path, 'w') as f:
            f.write("data_special\n")
            f.write("_cell_length_a 1.0\n")
            f.write("_cell_length_b 1.0\n")
            f.write("_cell_length_c 1.0\n")
            f.write("_cell_angle_alpha 90.0\n")
            f.write("_cell_angle_beta 90.0\n")
            f.write("_cell_angle_gamma 90.0\n")
            f.write("loop_\n")
            f.write("_atom_site_label\n")
            f.write("_atom_site_type_symbol\n")
            f.write("_atom_site_fract_x\n")
            f.write("_atom_site_fract_y\n")
            f.write("_atom_site_fract_z\n")
            f.write("Fe1@#$ Fe 0.0 0.0 0.0\n")
        
        converter.convert(
            input_path=input_path,
            output_path=output_path,
            input_format='cif',
            output_format='vasp'
        )
        print("✓ 特殊字符处理成功")
    except Exception as e:
        print(f"✗ 特殊字符处理失败：{str(e)}")

def test_parallel_processing():
    """测试并行处理功能"""
    print("\n=== 测试并行处理功能 ===")
    current_dir, data_dir = setup_test_environment()
    converter = StructureConverter()
    
    # 创建一个多帧结构文件
    input_path = os.path.join(data_dir, 'test_parallel.cif')
    output_path = os.path.join(data_dir, 'test_parallel.vasp')
    
    try:
        # 创建一个包含多帧的结构文件
        with open(input_path, 'w') as f:
            for i in range(10):  # 创建10帧
                f.write(f"data_frame_{i}\n")
                f.write("_cell_length_a 1.0\n")
                f.write("_cell_length_b 1.0\n")
                f.write("_cell_length_c 1.0\n")
                f.write("_cell_angle_alpha 90.0\n")
                f.write("_cell_angle_beta 90.0\n")
                f.write("_cell_angle_gamma 90.0\n")
                f.write("loop_\n")
                f.write("_atom_site_label\n")
                f.write("_atom_site_type_symbol\n")
                f.write("_atom_site_fract_x\n")
                f.write("_atom_site_fract_y\n")
                f.write("_atom_site_fract_z\n")
                f.write(f"Fe1 Fe {i*0.1} 0.0 0.0\n")
        
        # 测试并行处理
        converter.convert(
            input_path=input_path,
            output_path=output_path,
            input_format='cif',
            output_format='vasp',
            parallel=True
        )
        print("✓ 并行处理成功")
    except Exception as e:
        print(f"✗ 并行处理失败：{str(e)}")

def test_error_handling():
    """测试错误处理"""
    print("\n=== 测试错误处理 ===")
    current_dir, data_dir = setup_test_environment()
    converter = StructureConverter()
    
    # 创建一个错误的结构文件
    input_path = os.path.join(data_dir, 'test_error.cif')
    output_path = os.path.join(data_dir, 'test_error.vasp')
    
    try:
        # 创建一个包含错误信息的结构文件
        with open(input_path, 'w') as f:
            f.write("data_error\n")
            f.write("_cell_length_a invalid\n")
        
        converter.convert(
            input_path=input_path,
            output_path=output_path,
            input_format='cif',
            output_format='vasp'
        )
        print("✗ 错误处理失败：应该抛出异常")
    except ValueError as e:
        print(f"✓ 错误处理成功：捕获到预期的异常 - {str(e)}")

def main():
    """主测试函数"""
    print("开始运行边界情况测试...")
    
    # 运行所有测试
    test_empty_structure()
    test_large_file()
    test_special_characters()
    test_parallel_processing()
    test_error_handling()
    
    print("\n边界情况测试完成！")

if __name__ == '__main__':
    main() 