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


def combinedStatsTask2():

    combinedDf = pd.read_csv('combined_closePosition.csv')

    totalTrades = len(combinedDf)
    uniqueDays = len(combinedDf['Date'].unique())
    averageTrades = totalTrades/ uniqueDays
    totalPnl = combinedDf['Pnl'].sum()
    profitTrades = (combinedDf['Pnl'] > 0).sum()
    lossTrades = (combinedDf['Pnl'] <= 0).sum()

    with open('combined_stats.txt', 'w') as file:
        file.write(f"Total trades: {totalTrades}\n")
        file.write(f"Unique days: {uniqueDays}\n")
        file.write(f"Average trades: {int(averageTrades)}\n")
        file.write(f"Total Pnl: {int(totalPnl)}\n")
        file.write(f"Profit trades: {profitTrades}\n")
        file.write(f"Loss trades: {lossTrades}\n")


# combinedPositionTask1()
combinedStatsTask2()

