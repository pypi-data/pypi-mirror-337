import os
from ase.io import read
from atomorph.converter.core.converter import StructureConverter

def test_fixed_atoms():
    """测试固定指定原子的功能"""
    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # 读取测试文件
    input_path = os.path.join(data_dir, 'test_multi_sort.cif')
    output_path = os.path.join(data_dir, 'test_fixed_atoms.vasp')
    
    # 创建转换器实例
    converter = StructureConverter()
    
    # 设置固定原子（固定第一个Fe原子和第一个Cu原子）
    fixed_atoms = [0, 2]  # Fe1和Cu1的索引
    constraints = {"fixed_atoms": fixed_atoms}
    
    # 执行转换
    converter.convert(
        input_path=input_path,
        output_path=output_path,
        input_format='cif',
        output_format='vasp',
        sort_order="descending",
        constraints=constraints
    )
    
    # 读取结果并验证
    atoms = read(output_path)
    assert atoms.constraints is not None, "没有找到约束"
    assert len(atoms.constraints) == 1, "约束数量不正确"
    assert len(atoms.constraints[0].index) == 2, "固定原子数量不正确"
    print("\n固定原子测试通过！")

def test_fixed_elements():
    """测试固定指定元素的功能"""
    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    
    # 读取测试文件
    input_path = os.path.join(data_dir, 'test_multi_sort.cif')
    output_path = os.path.join(data_dir, 'test_fixed_elements.vasp')
    
    # 创建转换器实例
    converter = StructureConverter()
    
    # 设置固定元素（固定所有的Fe和Cu原子）
    constraints = {"fixed_elements": ["Fe", "Cu"]}
    
    # 执行转换
    converter.convert(
        input_path=input_path,
        output_path=output_path,
        input_format='cif',
        output_format='vasp',
        sort_order="descending",
        constraints=constraints
    )
    
    # 读取结果并验证
    atoms = read(output_path)
    assert atoms.constraints is not None, "没有找到约束"
    assert len(atoms.constraints) == 1, "约束数量不正确"
    # Fe有2个原子，Cu有3个原子，总共应该固定5个原子
    assert len(atoms.constraints[0].index) == 5, "固定原子数量不正确"
    print("\n固定元素测试通过！")

def test_fixed_layers():
    """测试固定指定层的功能"""
    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    
    # 读取测试文件
    input_path = os.path.join(data_dir, 'test_multi_sort.cif')
    output_path = os.path.join(data_dir, 'test_fixed_layers.vasp')
    
    # 创建转换器实例
    converter = StructureConverter()
    
    # 设置固定层（固定最底层和最顶层）
    constraints = {
        "fixed_layers": [0, 9],  # 固定第一层和最后一层
        "layer_thickness": 1.0  # 层厚度为1.0埃
    }
    
    # 执行转换
    converter.convert(
        input_path=input_path,
        output_path=output_path,
        input_format='cif',
        output_format='vasp',
        sort_order="descending",
        constraints=constraints
    )
    
    # 读取结果并验证
    atoms = read(output_path)
    assert atoms.constraints is not None, "没有找到约束"
    assert len(atoms.constraints) == 1, "约束数量不正确"
    print("\n固定层测试通过！")

def test_combined_constraints():
    """测试组合约束的功能"""
    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    
    # 读取测试文件
    input_path = os.path.join(data_dir, 'test_multi_sort.cif')
    output_path = os.path.join(data_dir, 'test_combined_constraints.vasp')
    
    # 创建转换器实例
    converter = StructureConverter()
    
    # 设置组合约束（固定指定原子、指定元素和指定层）
    constraints = {
        "fixed_atoms": [0, 2],  # 固定第一个Fe原子和第一个Cu原子
        "fixed_elements": ["Ag"],  # 固定所有的Ag原子
        "fixed_layers": [0],  # 固定最底层
        "layer_thickness": 1.0  # 层厚度为1.0埃
    }
    
    # 执行转换
    converter.convert(
        input_path=input_path,
        output_path=output_path,
        input_format='cif',
        output_format='vasp',
        sort_order="descending",
        constraints=constraints
    )
    
    # 读取结果并验证
    atoms = read(output_path)
    assert atoms.constraints is not None, "没有找到约束"
    assert len(atoms.constraints) == 1, "约束数量不正确"
    
    # 读取VASP文件内容并检查选择性动力学标记
    with open(output_path, 'r') as f:
        content = f.readlines()
    
    # 检查是否包含"Selective dynamics"行
    assert any("Selective dynamics" in line for line in content), "没有找到选择性动力学标记"
    
    # 检查固定原子的标记
    fixed_count = sum(1 for line in content if "F F F" in line)
    assert fixed_count > 0, "没有找到固定原子的标记"
    print("\n组合约束测试通过！")

if __name__ == '__main__':
    print("开始测试所有约束功能...")
    test_fixed_atoms()
    test_fixed_elements()
    test_fixed_layers()
    test_combined_constraints()
    print("\n所有约束功能测试完成！") 