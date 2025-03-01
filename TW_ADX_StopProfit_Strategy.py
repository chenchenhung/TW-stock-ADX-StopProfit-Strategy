# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# ----------------------------
# 下載台股指數期貨數據 (以台股加權指數 ^TWII)
# ----------------------------
df = pd.read_csv("taiwan_stock_data.csv")
# ----------------------------
# ADX 計算函數 (14日週期)
# ----------------------------
def compute_adx(data, n=14):
    df = data.copy()
    df['H-L'] = df['High'] - df['Low']
    df['H-PC'] = abs(df['High'] - df['Close'].shift(1))
    df['L-PC'] = abs(df['Low'] - df['Close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)

    df['UpMove'] = df['High'] - df['High'].shift(1)
    df['DownMove'] = df['Low'].shift(1) - df['Low']
    df['+DM'] = np.where((df['UpMove'] > df['DownMove']) & (df['UpMove'] > 0), df['UpMove'], 0)
    df['-DM'] = np.where((df['DownMove'] > df['UpMove']) & (df['DownMove'] > 0), df['DownMove'], 0)

    df['TR_s'] = df['TR'].rolling(window=n).sum()
    df['+DM_s'] = df['+DM'].rolling(window=n).sum()
    df['-DM_s'] = df['-DM'].rolling(window=n).sum()

    df['+DI'] = 100 * (df['+DM_s'] / df['TR_s'])
    df['-DI'] = 100 * (df['-DM_s'] / df['TR_s'])

    df['DX'] = 100 * abs(df['+DI'] - df['-DI']) / (df['+DI'] + df['-DI'])
    df['ADX'] = df['DX'].rolling(window=n).mean()

    df.drop(['H-L', 'H-PC', 'L-PC', 'TR', 'UpMove', 'DownMove', '+DM', '-DM', 'TR_s', '+DM_s', '-DM_s', '+DI', '-DI', 'DX'], axis=1, inplace=True)
    return df

df = compute_adx(df, n=14)

# ----------------------------
# 均線交叉策略 (ADX > 25 時適用)
# ----------------------------
df['MA_short'] = df['Close'].rolling(window=20).mean()
df['MA_long'] = df['Close'].rolling(window=50).mean()
df['trend_signal'] = np.where(df['MA_short'] > df['MA_long'], 1, -1)

# ----------------------------
# 布林通道策略 (ADX < 20 時適用)
# ----------------------------
window_bb = 20
df['BB_middle'] = df['Close'].rolling(window=window_bb).mean()
df['BB_std'] = df['Close'].rolling(window=window_bb).std()
df['BB_upper'] = df['BB_middle'] + 2 * df['BB_std']
df['BB_lower'] = df['BB_middle'] - 2 * df['BB_std']

df['bollinger_signal'] = 0
df.loc[df['Close'] <= df['BB_lower'], 'bollinger_signal'] = 1
df.loc[df['Close'] >= df['BB_upper'], 'bollinger_signal'] = -1

# 設定移動止損線
df['stop_loss'] = np.nan
position = 0
entry_price = 0

for i in range(1, len(df)):
    signal = df['bollinger_signal'].iloc[i]

    if position == 0 and signal != 0:
        position = signal
        entry_price = df['Close'].iloc[i]

    elif position != 0:
        if position == 1 and df['Close'].iloc[i] >= df['BB_middle'].iloc[i]:  # 多頭突破中軌
            df.at[df.index[i], 'stop_loss'] = (entry_price + df['BB_middle'].iloc[i]) / 2
        elif position == -1 and df['Close'].iloc[i] <= df['BB_middle'].iloc[i]:  # 空頭跌破中軌
            df.at[df.index[i], 'stop_loss'] = (entry_price + df['BB_middle'].iloc[i]) / 2

df['stop_loss'].fillna(method='ffill', inplace=True)

# ----------------------------
# 結合兩種策略
# ----------------------------
df['final_signal'] = np.nan
df.loc[df['ADX'] > 25, 'final_signal'] = df.loc[df['ADX'] > 25, 'trend_signal']
df.loc[df['ADX'] < 20, 'final_signal'] = df.loc[df['ADX'] < 20, 'bollinger_signal']

df['final_signal'].ffill(inplace=True)
df['final_signal'].fillna(0, inplace=True)

df['final_position'] = df['final_signal']

# ----------------------------
# **修正對齊錯誤**
# ----------------------------
df['daily_return'] = df['Close'].pct_change()

# 確保對齊 `final_position.shift(1)` 和 `daily_return`
final_position_shifted, daily_return_aligned = df['final_position'].shift(1).align(df['daily_return'], axis=0, copy=False)

# 修正計算策略報酬率的問題
df['strategy_return'] = final_position_shifted.mul(daily_return_aligned, fill_value=0)
df['cumulative_return'] = (1 + df['strategy_return']).cumprod() - 1

# ----------------------------
# 繪製結果
# ----------------------------
plt.figure(figsize=(14,8))

ax1 = plt.subplot(2,1,1)
plt.plot(df.index, df['Close'], label='Close Price', color='black', alpha=0.7)
plt.plot(df.index, df['MA_short'], label='MA Short (20)', color='blue', alpha=0.6)
plt.plot(df.index, df['MA_long'], label='MA Long (50)', color='red', alpha=0.6)
plt.plot(df.index, df['BB_upper'], linestyle='--', color='magenta', alpha=0.6)
plt.plot(df.index, df['BB_middle'], linestyle='--', color='grey', alpha=0.6)
plt.plot(df.index, df['BB_lower'], linestyle='--', color='green', alpha=0.6)
plt.title('TW index')
plt.ylabel('Price')
plt.legend()
plt.grid(True)

ax2 = plt.subplot(2,1,2)
plt.plot(df.index, df['cumulative_return']*100, label='Cumulative Return', color='blue')
plt.title('Total Return in %')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()