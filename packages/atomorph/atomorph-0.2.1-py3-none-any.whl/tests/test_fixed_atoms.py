import os
from ase.io import read
from atomorph.converter.core.converter import StructureConverter

def test_fixed_atoms_before_sorting():
    """测试固定原子功能在排序之前应用"""
    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 创建测试目录
    data_dir = os.path.join(current_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # 读取测试文件
    input_path = os.path.join(data_dir, 'test_multi_sort.cif')
    output_path = os.path.join(data_dir, 'test_fixed_atoms.vasp')
    
    # 创建转换器实例
    converter = StructureConverter()
    
    # 读取输入文件中的原子顺序
    atoms = read(input_path)
    print("\n输入文件中的原子顺序：", atoms.get_chemical_symbols())
    
    # 设置固定原子（固定第一个Fe原子和第一个Cu原子）
    fixed_atoms = [0, 2]  # Fe1和Cu1的索引
    constraints = {"fixed_atoms": fixed_atoms}
    
    # 测试降序排序
    print("\n测试降序排序（带固定原子）：")
    converter.convert(
        input_path=input_path,
        output_path=output_path,
        input_format='cif',
        output_format='vasp',
        sort_order="descending",
        constraints=constraints
    )
    
    # 直接读取VASP文件内容
    print("\nVASP文件内容：")
    with open(output_path, 'r') as f:
        content = f.readlines()
        print("".join(content))
    
    # 检查第一行（元素顺序）
    elements = content[0].strip().split()
    print("\nVASP文件中的元素顺序：", elements)
    
    # 验证排序是否正确（按照周期表顺序降序：Au > Pt > Ag > Cu > Fe）
    expected_order = ['Au', 'Pt', 'Ag', 'Cu', 'Fe']
    assert elements == expected_order, f"排序错误！期望顺序：{expected_order}，实际顺序：{elements}"
    
    # 验证原子数量是否正确
    atom_counts = [int(x) for x in content[6].strip().split()]
    expected_counts = [2, 1, 2, 3, 2]  # Au:2, Pt:1, Ag:2, Cu:3, Fe:2
    assert atom_counts == expected_counts, f"原子数量错误！期望数量：{expected_counts}，实际数量：{atom_counts}"
    
    # 验证固定原子约束是否正确应用
    # 在排序后的结构中，第一个Fe原子应该在最后两个位置，第一个Cu原子应该在中间位置
    symbols = atoms.get_chemical_symbols()
    fixed_symbols = [symbols[i] for i in fixed_atoms]
    print("\n固定原子的元素：", fixed_symbols)
    
    # 读取排序后的结构
    sorted_atoms = read(output_path)
    sorted_symbols = sorted_atoms.get_chemical_symbols()
    print("\n排序后的原子顺序：", sorted_symbols)
    
    # 验证固定原子的约束是否保持
    constraints = sorted_atoms.constraints
    assert constraints is not None, "没有找到约束"
    assert len(constraints) == 1, "约束数量不正确"
    constraint = constraints[0]
    print("\n固定原子的索引：", constraint.index)
    
    print("\n测试通过！固定原子功能在排序之前正确应用。")

if __name__ == '__main__':
    test_fixed_atoms_before_sorting() 