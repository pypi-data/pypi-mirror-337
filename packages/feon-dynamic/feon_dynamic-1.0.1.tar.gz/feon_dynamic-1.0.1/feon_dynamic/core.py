import numpy as np
import scipy.linalg as sl
import pandas as pd
import os
import pickle
from scipy.io import loadmat, savemat
import gzip

class VibrationAnalyzer:
    def __init__(self):
        """初始化分析器，自动加载内置数据"""
        self.K_dict = self._load_default_kdict()
        self.position_df = self._load_default_positions()
    
    def _load_default_kdict(self):
        """加载内置刚度矩阵字典"""
        data_path = os.path.join(
            os.path.dirname(__file__), 
            'data/K_dict.pkl'
        )
        
        # 优先尝试加载压缩文件
        gz_path = data_path + '.gz'
        if os.path.exists(gz_path):
            with gzip.open(gz_path, 'rb') as f:
                return pickle.load(f)
        
        # 原始加载方式保持不变
        with open(data_path, 'rb') as f:
            return pickle.load(f)
    
    def _load_default_positions(self):
        """加载内置位置数据"""
        data_path = os.path.join(
            os.path.dirname(__file__),
            'data/positions.xlsx'
        )
        return pd.read_excel(data_path, names=['单元编号', 'A位置', 'Iy位置', 'Iz位置'])
    

    def analyze(self, K, M):
        """
        执行完整振动分析流程
        
        参数:
        K (numpy.ndarray): 刚度矩阵
        M (numpy.ndarray): 质量矩阵
        
        返回:
        tuple: (特征值数组, 修改后的振型矩阵)
        """
        # 计算特征值和振型
        eigenvalues, eigenvectors = sl.eigh(K, M)
        
        # 损伤检测
        damage_result = self._detect_damage(K)
        
        # 添加损伤标记
        marked_eigenvectors = self._add_damage_markers(eigenvectors, damage_result)
        
        return eigenvalues, marked_eigenvectors
    
    def _detect_damage(self, KD, threshold=0.01):
        """损伤检测核心逻辑"""
        damage_report = {}
        
        for _, row in self.position_df.iterrows():
            elem = row['单元编号']
            damage_report.setdefault(elem, {'A': None, 'Iy': None, 'Iz': None})
            
            # 检查A分量
            if pd.notna(row['A位置']):
                i, j = self._parse_position(row['A位置'])
                actual = KD[i,j]
                if not (1 - threshold <= actual <= 1 + threshold):
                    damage_report[elem]['A'] = 1 - actual
            
            # 检查Iy分量（对应I1）
            if pd.notna(row['Iy位置']):
                i, j = self._parse_position(row['Iy位置'])
                actual = KD[i,j]
                if not (1 - threshold <= actual <= 1 + threshold):
                    damage_report[elem]['Iy'] = 1 - actual
            
            # 检查Iz分量（对应I2）
            if pd.notna(row['Iz位置']):
                i, j = self._parse_position(row['Iz位置'])
                actual = KD[i,j]
                if not (1 - threshold <= actual <= 1 + threshold):
                    damage_report[elem]['Iz'] = 1 - actual
        
        return self._format_damage_result(damage_report)
    
    def _parse_position(self, pos_str):
        """解析位置字符串为坐标"""
        pos = list(map(int, str(pos_str).split(',')))
        return pos[0]-1, pos[1]-1  # 转换为0-based索引
    
    def _format_damage_result(self, raw_data):
        """格式化损伤结果"""
        return {
            elem: (
                raw_data[elem]['A'] or 0.0,
                raw_data[elem]['Iy'] or 0.0,
                raw_data[elem]['Iz'] or 0.0
            )
            for elem in raw_data if any(raw_data[elem].values())
        }
    
    def _add_damage_markers(self, matrix, damage_result):
        """添加损伤标记到振型矩阵"""
        matrix = self._add_damage_position(matrix, damage_result)
        matrix = self._add_damage_degree(matrix, damage_result)
        return matrix
    
    def _add_damage_position(self, matrix, damage_result):
        """在矩阵第7列添加损伤位置信息"""
        DISPLAY_INDICES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        damaged_units = sorted(damage_result.keys())
        
        processed_count = 0
        for i, unit in enumerate(damaged_units[:10]):
            if i >= len(DISPLAY_INDICES):
                break
            
            row_idx = DISPLAY_INDICES[i]
            original = matrix[row_idx, 6]
            sign = np.sign(original)
            abs_val = abs(original)
            
            int_part = int(abs_val)
            decimal_str = f"{abs_val:.6f}".split('.')[1]
            new_decimal = f"{unit:03d}{decimal_str[3:]}"
            
            matrix[row_idx, 6] = sign * float(f"{int_part}.{new_decimal}")
            processed_count += 1
        
        # 添加结束标记233
        if processed_count < len(DISPLAY_INDICES):
            row_idx = DISPLAY_INDICES[processed_count]
            original = matrix[row_idx, 6]
            sign = np.sign(original)
            abs_val = abs(original)
            
            int_part = int(abs_val)
            decimal_str = f"{abs_val:.6f}".split('.')[1]
            new_decimal = f"233{decimal_str[3:]}"
            
            matrix[row_idx, 6] = sign * float(f"{int_part}.{new_decimal}")
        
        return matrix
    
    def _add_damage_degree(self, matrix, damage_result):
        """在矩阵第8列添加损伤程度信息"""
        DISPLAY_INDICES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        damaged_units = sorted(damage_result.keys())
        
        for i, unit in enumerate(damaged_units[:10]):
            if i >= len(DISPLAY_INDICES):
                break
            
            row_idx = DISPLAY_INDICES[i]
            original = matrix[row_idx, 7]
            sign = np.sign(original)
            abs_val = abs(original)
            
            int_part = int(abs_val)
            a, iy, iz = damage_result[unit]
            decimal_str = f"{a*100:02.0f}{iy*100:02.0f}{iz*100:02.0f}"
            
            matrix[row_idx, 7] = sign * float(f"{int_part}.{decimal_str}")
        
        return matrix 