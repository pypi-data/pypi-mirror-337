from django.db import transaction
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from decimal import Decimal

from .utils.base_command import PortfolioBaseCommand
from ...models import ETFDetails, ETFPrice, ETFTechnicalIndicator

class Command(PortfolioBaseCommand):
    help = 'Calculate technical indicators for ETFs based on price data'

    def __init__(self):
        super().__init__('calculate_indicators')

    def add_arguments(self, parser):
        parser.add_argument('--symbol', type=str, help='Specific ETF symbol to process')
        parser.add_argument('--days', type=int, default=365, help='Number of days to calculate (default: 365)')

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
        
        self.info(f"Processing {etfs.count()} ETFs...")
        
        # Set the cutoff date
        cutoff_date = datetime.now().date() - timedelta(days=days_to_process + 250)  # Extra days for lookback periods
        self.info(f"Using cutoff date: {cutoff_date} (processing {days_to_process} days + 250 days lookback)")
        
        for etf in etfs:
            self.info(f"Processing {etf.symbol}...")
            
            # Get price data for this ETF
            prices = ETFPrice.objects.filter(etf=etf, date__gte=cutoff_date).order_by('date')
            
            if prices.count() < 250:
                self.warning(f"Not enough price data for {etf.symbol}. Skipping.")
                continue
            
            # Convert to pandas DataFrame for easier calculation
            price_data = list(prices.values('date', 'open', 'high', 'low', 'close', 'volume'))
            
            # Convert Decimal to float for calculations
            for row in price_data:
                for field in ['open', 'high', 'low', 'close']:
                    row[field] = float(row[field])
            
            df = pd.DataFrame(price_data)
            
            if df.empty:
                continue
                
            # Calculate indicators
            self._calculate_indicators(etf, df)
            
            self.success(f"Completed processing for {etf.symbol}")
        
        self.success("All ETFs processed successfully")
    
    def _calculate_indicators(self, etf, df):
        """Calculate all technical indicators for an ETF"""
        # Ensure data is sorted by date
        df = df.sort_values('date')
        
        # Calculate Simple Moving Averages
        for window in [5, 10, 20, 50, 200]:
            df[f'sma_{window}'] = df['close'].rolling(window=window).mean()
        
        # Calculate Exponential Moving Averages
        df['ema_12'] = df['close'].ewm(span=12, adjust=False).mean()
        df['ema_26'] = df['close'].ewm(span=26, adjust=False).mean()
        
        # Calculate MACD
        df['macd'] = df['ema_12'] - df['ema_26']
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        df['macd_histogram'] = df['macd'] - df['macd_signal']
        
        # Calculate Bollinger Bands
        df['bb_middle'] = df['sma_20']
        rolling_std = df['close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + (rolling_std * 2)
        df['bb_lower'] = df['bb_middle'] - (rolling_std * 2)
        
        # Calculate RSI
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        
        # Avoid division by zero
        rs = gain / loss.replace(0, np.finfo(float).eps)
        df['rsi_14'] = 100 - (100 / (1 + rs))
        
        # Calculate Stochastic Oscillator
        period = 14
        low_min = df['low'].rolling(window=period).min()
        high_max = df['high'].rolling(window=period).max()
        
        # Avoid division by zero
        high_low_diff = high_max - low_min
        high_low_diff = high_low_diff.replace(0, np.finfo(float).eps)
        
        df['stoch_k'] = 100 * ((df['close'] - low_min) / high_low_diff)
        df['stoch_d'] = df['stoch_k'].rolling(window=3).mean()
        
        # Calculate ATR
        df['tr'] = np.maximum(
            np.maximum(
                df['high'] - df['low'],  # Current high - current low
                abs(df['high'] - df['close'].shift())  # Current high - previous close
            ),
            abs(df['low'] - df['close'].shift())  # Current low - previous close
        )
        df['atr_14'] = df['tr'].rolling(window=14).mean()
        
        # Calculate On-Balance Volume (fixed implementation)
        df['obv'] = np.nan
        df.loc[1, 'obv'] = df.loc[1, 'volume']  # Initialize first OBV value
        
        for i in range(2, len(df)):
            if df.loc[i, 'close'] > df.loc[i-1, 'close']:
                df.loc[i, 'obv'] = df.loc[i-1, 'obv'] + df.loc[i, 'volume']
            elif df.loc[i, 'close'] < df.loc[i-1, 'close']:
                df.loc[i, 'obv'] = df.loc[i-1, 'obv'] - df.loc[i, 'volume']
            else:
                df.loc[i, 'obv'] = df.loc[i-1, 'obv']
        
        # Save indicators to database
        self._save_indicators(etf, df)
    
    @transaction.atomic
    def _save_indicators(self, etf, df):
        """Save calculated indicators to the database"""
        # Delete existing indicators for this ETF
        ETFTechnicalIndicator.objects.filter(etf=etf).delete()
        
        # Create new indicator objects
        indicators = []
        for _, row in df.iterrows():
            # Skip rows with NaN values that would be at the beginning of the dataset
            if pd.isna(row['sma_200']) or pd.isna(row['rsi_14']) or pd.isna(row['obv']):
                continue
                
            indicator = ETFTechnicalIndicator(
                etf=etf,
                date=row['date'],
                sma_5=Decimal(str(row['sma_5'])),
                sma_10=Decimal(str(row['sma_10'])),
                sma_20=Decimal(str(row['sma_20'])),
                sma_50=Decimal(str(row['sma_50'])),
                sma_200=Decimal(str(row['sma_200'])),
                ema_12=Decimal(str(row['ema_12'])),
                ema_26=Decimal(str(row['ema_26'])),
                macd=Decimal(str(row['macd'])),
                macd_signal=Decimal(str(row['macd_signal'])),
                macd_histogram=Decimal(str(row['macd_histogram'])),
                bb_upper=Decimal(str(row['bb_upper'])),
                bb_middle=Decimal(str(row['bb_middle'])),
                bb_lower=Decimal(str(row['bb_lower'])),
                rsi_14=Decimal(str(row['rsi_14'])),
                stoch_k=Decimal(str(row['stoch_k'])),
                stoch_d=Decimal(str(row['stoch_d'])),
                atr_14=Decimal(str(row['atr_14'])),
                obv=int(row['obv'])
            )
            indicators.append(indicator)
        
        # Bulk create for efficiency
        ETFTechnicalIndicator.objects.bulk_create(indicators)
        self.info(f"Created {len(indicators)} indicator records for {etf.symbol}")