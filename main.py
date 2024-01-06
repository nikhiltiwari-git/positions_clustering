import os
import pandas as pd

def combinedPositionTask1():

    path = "./SampleData/SampleData"
    
    dfs = []
    for file in os.listdir(path):
        if 'closePosition' in file:
            filePath = os.path.join(path, file)
            df = pd.read_csv(filePath, usecols=['Key', 'ExitTime', 'Symbol', 'EntryPrice', 'Quantity', 'Pnl'])
            df['Date'] = pd.to_datetime(df['ExitTime']).dt.date
            dfs.append(df)

    combinedDf = pd.concat(dfs, ignore_index=True)
    combinedDf.to_csv('combined_closePosition.csv', index=False)

combinedPositionTask1()

