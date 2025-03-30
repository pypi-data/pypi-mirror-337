from django.db import transaction
from datetime import datetime, timedelta
import pandas as pd

from .utils.base_command import PortfolioBaseCommand
from ...models import ETFDetails, ETFTechnicalIndicator, ETFSignal, ETFPrice

class Command(PortfolioBaseCommand):
    help = 'Generate trading signals based on technical indicators'
    
    def __init__(self):
        super().__init__('generate_signals')

    def add_arguments(self, parser):
        parser.add_argument('--symbol', type=str, help='Specific ETF symbol to process')
        parser.add_argument('--days', type=int, default=250, help='Number of recent days to generate signals for')

    def handle(self, *args, **options):
        symbol = options.get('symbol')
        days_to_process = options.get('days')
        
        # Get ETFs to process
        if symbol:
            etfs = ETFDetails.objects.filter(symbol=symbol)
            if not etfs.exists():
                self.error(f"No ETF found with symbol {symbol}")
                return
        else:
            etfs = ETFDetails.objects.all()
        
        self.info(f"Generating signals for {etfs.count()} ETFs...")
        
        # Set the cutoff date
        cutoff_date = datetime.now().date() - timedelta(days=days_to_process)
        self.info(f"Using cutoff date: {cutoff_date} (processing {days_to_process} days)")
        
        for etf in etfs:
            self.info(f"Processing {etf.symbol}...")
            
            # Get technical indicators for this ETF
            indicators = ETFTechnicalIndicator.objects.filter(
                etf=etf, 
                date__gte=cutoff_date
            ).order_by('date')
            
            if indicators.count() < 5:
                self.warning(f"Not enough indicator data for {etf.symbol}. Skipping.")
                continue
            
            # Convert indicators to pandas DataFrame
            df = pd.DataFrame(list(indicators.values()))
            
            if df.empty:
                continue
            
            # Get matching price data for the same date range
            prices = ETFPrice.objects.filter(
                etf=etf,
                date__in=df['date'].tolist()
            ).values('date', 'close')
            
            # Create price dataframe and merge with indicators
            price_df = pd.DataFrame(list(prices))
            
            # Check if we have price data
            if price_df.empty:
                self.warning(f"No matching price data for {etf.symbol}. Skipping.")
                continue
                
            # Merge price data with indicators on the date field
            df = pd.merge(df, price_df, on='date', how='inner')
            
            # Ensure we still have enough data after the merge
            if len(df) < 5:
                self.warning(f"Not enough data after merging prices for {etf.symbol}. Skipping.")
                continue
                
            # Generate signals
            self._generate_signals(etf, df, indicators)
            
            self.success(f"Completed signal generation for {etf.symbol}")
        
        self.success("All ETFs processed successfully")
    
    @transaction.atomic
    def _generate_signals(self, etf, df, indicators):
        """Generate trading signals based on technical indicators"""
        # Delete existing signals in the date range
        min_date = df['date'].min()
        ETFSignal.objects.filter(etf=etf, date__gte=min_date).delete()
        
        # Sort DataFrame by date to ensure correct order
        df = df.sort_values('date')
        
        # Create a dictionary to map dates to indicator objects for easier lookup
        indicator_dict = {ind.date: ind for ind in indicators}
        
        signals = []
        
        # Iterate through each day of indicator data (except the first few)
        for i in range(5, len(df)):
            row = df.iloc[i]
            date = row['date']
            
            # Get the corresponding indicator object
            if date not in indicator_dict:
                continue
            indicator = indicator_dict[date]
            
            # Check for SMA crossovers (Golden Cross / Death Cross)
            if df.iloc[i-1]['sma_50'] < df.iloc[i-1]['sma_200'] and row['sma_50'] > row['sma_200']:
                # Golden Cross - bullish
                signals.append(ETFSignal(
                    etf=etf,
                    date=date,
                    signal_type='STRONG_BUY',
                    signal_source='SMA_CROSS',
                    confidence=85.0,
                    description=f"Golden Cross: 50-day SMA crossed above 200-day SMA. Strong bullish signal.",
                    indicator=indicator
                ))
            
            elif df.iloc[i-1]['sma_50'] > df.iloc[i-1]['sma_200'] and row['sma_50'] < row['sma_200']:
                # Death Cross - bearish
                signals.append(ETFSignal(
                    etf=etf,
                    date=date,
                    signal_type='STRONG_SELL',
                    signal_source='SMA_CROSS',
                    confidence=85.0,
                    description=f"Death Cross: 50-day SMA crossed below 200-day SMA. Strong bearish signal.",
                    indicator=indicator
                ))
            
            # Check MACD signals
            if df.iloc[i-1]['macd'] < df.iloc[i-1]['macd_signal'] and row['macd'] > row['macd_signal']:
                signals.append(ETFSignal(
                    etf=etf,
                    date=date,
                    signal_type='BUY',
                    signal_source='MACD',
                    confidence=75.0,
                    description=f"MACD crossed above signal line. Bullish momentum signal.",
                    indicator=indicator
                ))
            
            elif df.iloc[i-1]['macd'] > df.iloc[i-1]['macd_signal'] and row['macd'] < row['macd_signal']:
                signals.append(ETFSignal(
                    etf=etf,
                    date=date,
                    signal_type='SELL',
                    signal_source='MACD',
                    confidence=75.0,
                    description=f"MACD crossed below signal line. Bearish momentum signal.",
                    indicator=indicator
                ))
            
            # RSI signals (oversold/overbought)
            if row['rsi_14'] < 30:
                signals.append(ETFSignal(
                    etf=etf,
                    date=date,
                    signal_type='BUY',
                    signal_source='RSI',
                    confidence=70.0,
                    description=f"RSI below 30 indicates oversold conditions. Potential buy signal.",
                    indicator=indicator
                ))
            
            elif row['rsi_14'] > 70:
                signals.append(ETFSignal(
                    etf=etf,
                    date=date,
                    signal_type='SELL',
                    signal_source='RSI',
                    confidence=70.0,
                    description=f"RSI above 70 indicates overbought conditions. Potential sell signal.",
                    indicator=indicator
                ))
            
            # Bollinger Band signals
            close_price = float(row['close'])  # Convert Decimal to float
            if close_price < float(row['bb_lower']):
                signals.append(ETFSignal(
                    etf=etf,
                    date=date,
                    signal_type='BUY',
                    signal_source='BB',
                    confidence=65.0,
                    description=f"Price below lower Bollinger Band. Potential buy signal on mean reversion.",
                    indicator=indicator
                ))
            
            elif close_price > float(row['bb_upper']):
                signals.append(ETFSignal(
                    etf=etf,
                    date=date,
                    signal_type='SELL',
                    signal_source='BB',
                    confidence=65.0,
                    description=f"Price above upper Bollinger Band. Potential sell signal on mean reversion.",
                    indicator=indicator
                ))
            
            # Stochastic signals
            if df.iloc[i-1]['stoch_k'] < 20 and row['stoch_k'] > 20 and row['stoch_k'] > row['stoch_d']:
                signals.append(ETFSignal(
                    etf=etf,
                    date=date,
                    signal_type='BUY',
                    signal_source='STOCH',
                    confidence=60.0,
                    description=f"Stochastic K-line crossed above 20 from below and above D-line. Bullish signal.",
                    indicator=indicator
                ))
            
            elif df.iloc[i-1]['stoch_k'] > 80 and row['stoch_k'] < 80 and row['stoch_k'] < row['stoch_d']:
                signals.append(ETFSignal(
                    etf=etf,
                    date=date,
                    signal_type='SELL',
                    signal_source='STOCH',
                    confidence=60.0,
                    description=f"Stochastic K-line crossed below 80 from above and below D-line. Bearish signal.",
                    indicator=indicator
                ))
            
            # Multi-indicator consensus (when multiple indicators align)
            bullish_count = 0
            bearish_count = 0
            
            # Count bullish signals
            if row['sma_5'] > row['sma_20']: bullish_count += 1
            if row['macd'] > row['macd_signal']: bullish_count += 1
            if 30 < row['rsi_14'] < 50: bullish_count += 1
            if row['stoch_k'] > row['stoch_d'] and row['stoch_k'] < 50: bullish_count += 1
            
            # Count bearish signals
            if row['sma_5'] < row['sma_20']: bearish_count += 1
            if row['macd'] < row['macd_signal']: bearish_count += 1
            if 50 < row['rsi_14'] < 70: bearish_count += 1
            if row['stoch_k'] < row['stoch_d'] and row['stoch_k'] > 50: bearish_count += 1
            
            # Generate consensus signals if at least 3 indicators align
            if bullish_count >= 3 and bearish_count == 0:
                signals.append(ETFSignal(
                    etf=etf,
                    date=date,
                    signal_type='BUY',
                    signal_source='MULTI',
                    confidence=80.0,
                    description=f"Multiple indicators showing bullish signals. Consider buying.",
                    indicator=indicator
                ))
            
            elif bearish_count >= 3 and bullish_count == 0:
                signals.append(ETFSignal(
                    etf=etf,
                    date=date,
                    signal_type='SELL',
                    signal_source='MULTI',
                    confidence=80.0,
                    description=f"Multiple indicators showing bearish signals. Consider selling.",
                    indicator=indicator
                ))
        
        # Bulk create for efficiency
        ETFSignal.objects.bulk_create(signals)
        self.info(f"Created {len(signals)} signals for {etf.symbol}")