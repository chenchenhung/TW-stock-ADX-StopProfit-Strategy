# TW-stock-ADX-StopProfit-Strategy
Trading Strategy Using ADX, Moving Average Crossover, and Bollinger Bands with Trailing Take-Profit
Overview
This repository contains a Python implementation of an enhanced ADX trading strategy that integrates a trailing take-profit mechanism. The strategy dynamically adapts to market conditions based on the Average Directional Index (ADX) and utilizes different approaches for trending and ranging markets.

Strategy Logic
1. Trend-Following (Moving Average Crossover) – When ADX > 25
If the market is strongly trending, a moving average crossover strategy is used.
A 20-day short-term moving average is compared with a 50-day long-term moving average to generate trading signals:
Buy (+1) when the short MA crosses above the long MA.
Sell (-1) when the short MA crosses below the long MA.

2️. Mean Reversion (Bollinger Bands) – When ADX < 20
If the market is ranging, a Bollinger Bands mean reversion strategy is applied:
Buy (+1) when the price nears the lower Bollinger Band.
Sell (-1) when the price nears the upper Bollinger Band.
New Feature: Trailing Take-Profit
If the price crosses the middle Bollinger Band, the stop-loss is moved to the midpoint between the entry price and the middle band, locking in potential profits while allowing for further upside.

3️. Supports Long and Short Positions
This strategy is designed for futures trading, allowing for both long and short positions.
It computes daily returns and cumulative returns over a 25-year period (2000-2025).

Features
1.Data Source: Fetches Taiwan Stock Index (^TWII) data from Yahoo Finance using yfinance.
2.echnical Indicator Calculations: Implements ADX, Moving Averages, and Bollinger Bands.
3.Dynamic Strategy Selection: Automatically switches between trend-following and mean reversion strategies based on ADX values.
4.railing Take-Profit Mechanism: Uses a dynamic stop-loss update when the price crosses the middle Bollinger Band.
5.Performance Simulation: Computes daily and cumulative returns for strategy evaluation.
6.Visualization: Generates plots showing price movements, technical indicators, trade signals, and cumulative returns.

Requirements
Ensure you have the following dependencies installed:
Python 3.x
pandas
numpy
matplotlib
yfinance

Tek Details:
1. ADX Indicator
The 14-day ADX (Average Directional Index) is used to measure trend strength:
ADX > 25 → Trending Market → Use Moving Average Crossover Strategy.
ADX < 20 → Ranging Market → Use Bollinger Bands with Trailing Take-Profit.
2. Moving Average Crossover Strategy
Uses 20-day short-term MA and 50-day long-term MA:
Buy (+1) when short MA crosses above long MA.
Sell (-1) when short MA crosses below long MA.
3. Bollinger Bands with Trailing Take-Profit
Uses Bollinger Bands (20-day moving average ± 2 standard deviations):
Buy (+1) when price nears the lower Bollinger Band.
Sell (-1) when price nears the upper Bollinger Band.
If price crosses the middle band, the stop-loss is moved to the midpoint between the entry price and the middle band.
4. Trading Signal Selection
ADX Indicator	Strategy Used
ADX > 25	Moving Average Crossover
ADX < 20	Bollinger Bands (with trailing take-profit)
20 ≤ ADX ≤ 25	Hold Previous Position

Conclusion

This enhanced ADX strategy adapts to both trending and ranging markets, while introducing a trailing take-profit feature to optimize profits.
1. Trending Market → Moving Average Crossover
2. Ranging Market → Bollinger Bands with Trailing Take-Profit
3. Adaptive Stop-Loss to Secure Profits
4. Fully Automated Trading Strategy with Performance Tracking

Best Use Cases
✔ Taiwan Stock Index Futures & ETF Trading (e.g., 0050.TW)
✔ Mid-term trend trading & mean reversion strategies
✔ Can be adapted to other markets (US indices, crypto, etc.)

Disclaimer
This project is for educational and research purposes only and does not constitute financial advice. Trading involves risks, and past performance does not guarantee future results.

此份文件有使用OpenAI潤色

