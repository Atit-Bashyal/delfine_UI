import datetime as dt
import pathlib
import pandas as pd

# Load data
class loadData:
    def __init__(self) -> None:
        self.options = {}
        self.data = {}
        self.dataAll = {}
        self.datemin = dt.date(dt.MAXYEAR, 1, 1)  # Give max date to min to compare
        self.datemax = dt.date(dt.MINYEAR, 12, 31)  # Give min date to max to compare

    def _appendData(self, key, data):
        self.data[key] = data
        self.options[key] = data.columns

        for column in data.columns:
            self.dataAll[f'{key}-{column}'] = data[column]

        datemin = self.data[key].index.min().date()
        datemax = self.data[key].index.max().date()
        if self.datemin > datemin:
            self.datemin = datemin
        if self.datemax < datemax:
            self.datemax = datemax

    def loadDataFromFile(self, filePath, index_col=0, sep=','):
        filePath = pathlib.Path(filePath)
        fileName = filePath.stem
        df = pd.read_csv(filePath, index_col=index_col, parse_dates=True, sep=sep)
        df = df.sort_index()
        self._appendData(fileName, df)
        return df

    def loadDataFromDir(self, dirPath, index_col=None, sep=None):
        dirPath = pathlib.Path(dirPath)
        files = list(dirPath.iterdir())
        
        if index_col is None:
            index_col = [0] * len(files)

        if sep is None:
            sep = [","] * len(files)

        df_dict = {}
        for i, file in enumerate(files):
            fileName = file.stem
            df_dict[fileName] = self.loadDataFromFile(file, index_col=index_col[i])
        return df_dict

    def getDataKeys(self):
        return list(self.dataAll.keys())

    def getDataValues(self):
        return list(self.dataAll.values)

    def getDateLimit(self):
        return self.datemin, self.datemax