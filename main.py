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


def combinedWinningLosingTask3():

    combinedDf = pd.read_csv('combined_closePosition.csv')

    combinedDf['ExitTime'] = pd.to_datetime(combinedDf['ExitTime'])
    combinedDf = combinedDf.sort_values('ExitTime')

    winningStreaks = []
    losingStreaks = []
    currentStreak = []
    totalPnl = 0
    streakType = None

    for index, row in combinedDf.iterrows():

        if row['Pnl'] > 0:
            if streakType != 'winning':
                if streakType == 'losing':
                    losingStreaks.append({'type': streakType, 'totalPnl': totalPnl, 'streak': currentStreak})
                currentStreak = []
                totalPnl = 0 
                streakType = 'winning'

            currentStreak.append(row)
            totalPnl += row['Pnl']

        elif row['Pnl'] <= 0:
            if streakType != 'losing':
                if streakType == 'winning':
                    winningStreaks.append({'type': streakType, 'totalPnl': totalPnl, 'streak': currentStreak})
                currentStreak = []
                totalPnl = 0
                streakType = 'losing'

            currentStreak.append(row)
            totalPnl += row['Pnl']

    if currentStreak:
        if streakType == 'winning':
            winningStreaks.append({'type': streakType, 'totalPnl': totalPnl, 'streak': currentStreak})
        else:
            losingStreaks.append({'type': streakType, 'totalPnl': totalPnl, 'streak': currentStreak})


    n = int(input("Enter n: "))

    losingStreaks = sorted(losingStreaks, key=lambda x: x['totalPnl'])
    winningStreaks = sorted(winningStreaks, key=lambda x: x['totalPnl'], reverse=True)

    with open('combined_winning_losing.txt', 'w') as file:
        for i in range(n):
            file.write(f"Winning Streak {i+1}:  ")
            file.write(f"{len(winningStreaks[i]['streak'])} Trades  ")
            file.write(f"{min(trade['ExitTime'] for trade in winningStreaks[i]['streak']).strftime('%Y-%m-%d')} to ")
            file.write(f"{max(trade['ExitTime'] for trade in winningStreaks[i]['streak']).strftime('%Y-%m-%d')}  ")
            file.write(f"Total Pnl: {int(winningStreaks[i]['totalPnl'])}\n")
        file.write("\n")
        
        for i in range(n):
            file.write(f"Losing Streak {i+1}:  ")
            file.write(f"{len(losingStreaks[i]['streak'])} Trades  ")
            file.write(f"{min(trade['ExitTime'] for trade in losingStreaks[i]['streak']).strftime('%Y-%m-%d')} to ")
            file.write(f"{max(trade['ExitTime'] for trade in losingStreaks[i]['streak']).strftime('%Y-%m-%d')}  ")
            file.write(f"Total Pnl: {int(losingStreaks[i]['totalPnl'])}\n")
            


# combinedPositionTask1()
# combinedStatsTask2()
combinedWinningLosingTask3()

