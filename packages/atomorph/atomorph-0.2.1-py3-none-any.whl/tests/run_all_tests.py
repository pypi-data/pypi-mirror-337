import os
import sys
from pathlib import Path
from ase.io import read, write
from atomorph.converter.core.converter import StructureConverter

def setup_test_environment():
    """设置测试环境"""
    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    return current_dir, data_dir

def test_basic_conversion():
    """测试基础文件格式转换功能"""
    print("\n=== 测试基础文件格式转换 ===")
    current_dir, data_dir = setup_test_environment()
    converter = StructureConverter()
    
    # 测试CIF -> VASP转换
    input_path = os.path.join(data_dir, 'test_multi_sort.cif')
    output_path = os.path.join(data_dir, 'test_basic_convert.vasp')
    
    try:
        converter.convert(
            input_path=input_path,
            output_path=output_path,
            input_format='cif',
            output_format='vasp'
        )
        print("✓ CIF -> VASP 转换成功")
    except Exception as e:
        print(f"✗ CIF -> VASP 转换失败: {str(e)}")
    
    # 测试VASP -> CIF转换
    input_path = output_path
    output_path = os.path.join(data_dir, 'test_basic_convert_back.cif')
    
    try:
        converter.convert(
            input_path=input_path,
            output_path=output_path,
            input_format='vasp',
            output_format='cif'
        )
        print("✓ VASP -> CIF 转换成功")
    except Exception as e:
        print(f"✗ VASP -> CIF 转换失败: {str(e)}")

def test_sorting():
    """测试元素排序功能"""
    print("\n=== 测试元素排序功能 ===")
    current_dir, data_dir = setup_test_environment()
    converter = StructureConverter()
    
    # 测试升序排序
    input_path = os.path.join(data_dir, 'test_multi_sort.cif')
    output_path = os.path.join(data_dir, 'test_ascending.vasp')
    
    try:
        converter.convert(
            input_path=input_path,
            output_path=output_path,
            input_format='cif',
            output_format='vasp',
            sort_order="ascending"
        )
        print("✓ 升序排序成功")
    except Exception as e:
        print(f"✗ 升序排序失败: {str(e)}")
    
    # 测试降序排序
    output_path = os.path.join(data_dir, 'test_descending.vasp')
    
    try:
        converter.convert(
            input_path=input_path,
            output_path=output_path,
            input_format='cif',
            output_format='vasp',
            sort_order="descending"
        )
        print("✓ 降序排序成功")
    except Exception as e:
        print(f"✗ 降序排序失败: {str(e)}")
    
    # 测试自定义元素顺序
    custom_order = ["Au", "Pt", "Ag", "Cu", "Fe"]
    output_path = os.path.join(data_dir, 'test_custom_order.vasp')
    
    try:
        converter.convert(
            input_path=input_path,
            output_path=output_path,
            input_format='cif',
            output_format='vasp',
            element_order=custom_order
        )
        print("✓ 自定义元素顺序成功")
    except Exception as e:
        print(f"✗ 自定义元素顺序失败: {str(e)}")

def test_constraints():
    """测试约束功能"""
    print("\n=== 测试约束功能 ===")
    current_dir, data_dir = setup_test_environment()
    converter = StructureConverter()
    
    # 测试固定原子
    input_path = os.path.join(data_dir, 'test_multi_sort.cif')
    output_path = os.path.join(data_dir, 'test_fixed_atoms.vasp')
    
    try:
        converter.convert(
            input_path=input_path,
            output_path=output_path,
            input_format='cif',
            output_format='vasp',
            constraints={"fixed_atoms": [0, 2]}
        )
        print("✓ 固定原子成功")
    except Exception as e:
        print(f"✗ 固定原子失败: {str(e)}")
    
    # 测试固定元素
    output_path = os.path.join(data_dir, 'test_fixed_elements.vasp')
    
    try:
        converter.convert(
            input_path=input_path,
            output_path=output_path,
            input_format='cif',
            output_format='vasp',
            constraints={"fixed_elements": ["Fe", "Cu"]}
        )
        print("✓ 固定元素成功")
    except Exception as e:
        print(f"✗ 固定元素失败: {str(e)}")
    
    # 测试固定层
    output_path = os.path.join(data_dir, 'test_fixed_layers.vasp')
    
    try:
        converter.convert(
            input_path=input_path,
            output_path=output_path,
            input_format='cif',
            output_format='vasp',
            constraints={
                "fixed_layers": [0, 9],
                "layer_thickness": 1.0
            }
        )
        print("✓ 固定层成功")
    except Exception as e:
        print(f"✗ 固定层失败: {str(e)}")
    
    # 测试组合约束
    output_path = os.path.join(data_dir, 'test_combined_constraints.vasp')
    
    try:
        converter.convert(
            input_path=input_path,
            output_path=output_path,
            input_format='cif',
            output_format='vasp',
            constraints={
                "fixed_atoms": [0, 2],
                "fixed_elements": ["Ag"],
                "fixed_layers": [0],
                "layer_thickness": 1.0
            }
        )
        print("✓ 组合约束成功")
    except Exception as e:
        print(f"✗ 组合约束失败: {str(e)}")

def test_edge_cases():
    """测试边界情况"""
    print("\n=== 测试边界情况 ===")
    current_dir, data_dir = setup_test_environment()
    converter = StructureConverter()
    
    # 测试空结构
    input_path = os.path.join(data_dir, 'test_empty.cif')
    output_path = os.path.join(data_dir, 'test_empty.vasp')
    
    try:
        # 创建一个空的结构文件
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
        print("✓ 空结构处理成功")
    except Exception as e:
        print(f"✗ 空结构处理失败: {str(e)}")
    
    # 测试错误处理
    input_path = os.path.join(data_dir, 'test_error.cif')
    output_path = os.path.join(data_dir, 'test_error.vasp')
    
    try:
        # 创建一个错误的结构文件
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
    except Exception as e:
        print(f"✓ 错误处理成功：捕获到预期的异常 - {str(e)}")

def main():
    """主测试函数"""
    print("开始运行Atomorph软件包测试...")
    
    # 运行所有测试
    test_basic_conversion()
    test_sorting()
    test_constraints()
    test_edge_cases()
    
    print("\n测试完成！")

if __name__ == '__main__':
    main() 