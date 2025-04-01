from setuptools import setup, find_packages

setup(
    name="feon_dynamic",
    version="1.0.0",
    packages=find_packages(),
    package_data={
        'feon_dynamic': [
            'data/K_dict.pkl',
            'data/positions.xlsx'
        ]
    },
    install_requires=[
        'numpy>=1.18',
        'scipy>=1.4',
        'pandas>=1.0',
        'openpyxl'  # 用于读取Excel文件
    ]
) 