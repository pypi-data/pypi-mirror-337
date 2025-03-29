import os
from ase.io import read
from atomorph.converter.core.converter import StructureConverter

def test_multi_atom_sorting():
    """测试多原子多元素类型的排序功能"""
    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 创建测试目录
    data_dir = os.path.join(current_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # 读取测试文件
    input_path = os.path.join(data_dir, 'test_multi_sort.cif')
    output_path = os.path.join(data_dir, 'test_multi_sort.vasp')
    
    # 创建转换器实例
    converter = StructureConverter()
    
    # 打印默认元素顺序
    print("\n默认元素顺序：")
    for element in ['Fe', 'Cu', 'Ag', 'Pt', 'Au']:
        idx = converter.DEFAULT_ELEMENT_ORDER.index(element)
        print(f"{element}: {idx}")
    
    # 读取输入文件中的原子顺序
    atoms = read(input_path)
    print("\n输入文件中的原子顺序：", atoms.get_chemical_symbols())
    
    # 测试降序排序
    print("\n测试降序排序：")
    converter.convert(
        input_path=input_path,
        output_path=output_path,
        input_format='cif',
        output_format='vasp',
        sort_order="descending"
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
    
    # 测试升序排序
    print("\n测试升序排序：")
    converter.convert(
        input_path=input_path,
        output_path=output_path,
        input_format='cif',
        output_format='vasp',
        sort_order="ascending"
    )
    
    # 直接读取VASP文件内容
    with open(output_path, 'r') as f:
        content = f.readlines()
    
    # 检查第一行（元素顺序）
    elements = content[0].strip().split()
    print("\nVASP文件中的元素顺序：", elements)
    
    # 验证排序是否正确（按照周期表顺序升序：Fe < Cu < Ag < Pt < Au）
    expected_order = ['Fe', 'Cu', 'Ag', 'Pt', 'Au']
    assert elements == expected_order, f"排序错误！期望顺序：{expected_order}，实际顺序：{elements}"
    
    # 验证原子数量是否正确
    atom_counts = [int(x) for x in content[6].strip().split()]
    expected_counts = [2, 3, 2, 1, 2]  # Fe:2, Cu:3, Ag:2, Pt:1, Au:2
    assert atom_counts == expected_counts, f"原子数量错误！期望数量：{expected_counts}，实际数量：{atom_counts}"
    
    print("\n测试通过！多原子多元素类型的排序功能正常工作。")

if __name__ == '__main__':
    test_multi_atom_sorting() 