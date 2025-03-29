import os
from ase.io import read, write
from atomorph.converter.core.converter import StructureConverter

def test_atom_sorting():
    """测试原子排序功能"""
    # 获取当前文件的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 创建测试目录
    data_dir = os.path.join(current_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # 读取测试文件
    input_path = os.path.join(data_dir, 'test_sort.cif')
    output_path = os.path.join(data_dir, 'test_sort.vasp')
    
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
    
    # 执行转换（使用降序排序）
    converter.convert(
        input_path=input_path,
        output_path=output_path,
        input_format='cif',
        output_format='vasp',
        sort_order="descending"  # 使用降序排序
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
    
    print("\n测试通过！原子已按照周期表顺序正确排序。")

if __name__ == '__main__':
    test_atom_sorting() 