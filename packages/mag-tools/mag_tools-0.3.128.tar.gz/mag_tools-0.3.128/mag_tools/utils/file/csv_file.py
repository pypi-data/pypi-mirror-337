from dataclasses import dataclass, field

import numpy as np
import pandas as pd


@dataclass
class CsvFile:
    file_path: str = field(metadata={'description': 'CSV文件路径'})

    def process(self, target_columns: int= 1) -> tuple[np.ndarray, np.ndarray]:
        """
        :param target_columns: 目标值的列数
        """
        df = pd.read_csv(self.file_path)

        inputs = df.iloc[:, :-target_columns].values  # 选择所有列，排除最后N列
        targets = df.iloc[:, -target_columns].values  # 选择最后N列作为目标值

        inputs = np.array(inputs)
        targets = np.array(targets)

        return inputs, targets