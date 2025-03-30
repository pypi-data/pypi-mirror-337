import pandas as pd
import numpy as np
from decimal import Decimal
from datetime import datetime, timedelta
from django.test import TestCase
from django.core.management import call_command
from io import StringIO

from data.models import ETFDetails, ETFPrice, ETFTechnicalIndicator
from data.management.commands.calculate_indicators import Command


class CalculateIndicatorsTest(TestCase):
    """Test suite for the calculate_indicators management command"""

    def setUp(self):
        """Set up test data"""
        # Create test ETF
        self.etf = ETFDetails.objects.create(
            symbol='TEST',
            name='Test ETF',
            description='A test ETF',
            category='Equity',
            family='Test Family',
            expense_ratio=Decimal('0.10')
        )
        
        # Create 300 days of price data for sufficient lookback periods
        base_date = datetime.now().date() - timedelta(days=300)
        prices = []
        
        for i in range(300):
            current_date = base_date + timedelta(days=i)
            # Generate some realistic price movement
            base_price = 100 + i * 0.1  # Slight uptrend
            noise = np.random.normal(0, 1)  # Random noise
            
            prices.append(ETFPrice(
                etf=self.etf,
                date=current_date,
                open=Decimal(str(base_price + noise)),
                high=Decimal(str(base_price + noise + 0.5)),
                low=Decimal(str(base_price + noise - 0.5)),
                close=Decimal(str(base_price + noise + 0.1)),
                volume=int(1000000 + np.random.normal(0, 50000))
            ))
        
        ETFPrice.objects.bulk_create(prices)

    def test_handle_specific_symbol(self):
        """Test processing a specific ETF symbol"""
        out = StringIO()
        call_command('calculate_indicators', symbol='TEST', stdout=out)
        
        # Verify indicators were created
        indicators = ETFTechnicalIndicator.objects.filter(etf=self.etf)
        self.assertGreater(indicators.count(), 0)
        self.assertIn(f"Processing TEST", out.getvalue())
        self.assertIn(f"Completed processing for TEST", out.getvalue())

    def test_handle_all_symbols(self):
        """Test processing all ETF symbols"""
        # Create another ETF
        etf2 = ETFDetails.objects.create(
            symbol='TST2',
            name='Test ETF 2',
            description='Another test ETF',
            category='Fixed Income',
            family='Test Family',
            expense_ratio=Decimal('0.15')
        )
        
        # Create price data for the second ETF
        base_date = datetime.now().date() - timedelta(days=300)
        prices = []
        
        for i in range(300):
            current_date = base_date + timedelta(days=i)
            base_price = 50 + i * 0.05  # Different price trend
            noise = np.random.normal(0, 0.5)
            
            prices.append(ETFPrice(
                etf=etf2,
                date=current_date,
                open=Decimal(str(base_price + noise)),
                high=Decimal(str(base_price + noise + 0.25)),
                low=Decimal(str(base_price + noise - 0.25)),
                close=Decimal(str(base_price + noise + 0.05)),
                volume=int(500000 + np.random.normal(0, 25000))
            ))
        
        ETFPrice.objects.bulk_create(prices)
        
        out = StringIO()
        call_command('calculate_indicators', stdout=out)
        
        # Verify indicators were created for both ETFs
        indicators1 = ETFTechnicalIndicator.objects.filter(etf=self.etf)
        indicators2 = ETFTechnicalIndicator.objects.filter(etf=etf2)
        
        self.assertGreater(indicators1.count(), 0)
        self.assertGreater(indicators2.count(), 0)
        self.assertIn("All ETFs processed successfully", out.getvalue())

    def test_handle_days_parameter(self):
        """Test processing with specific days parameter"""
        out = StringIO()
        call_command('calculate_indicators', symbol='TEST', days=30, stdout=out)
        
        # Verify cutoff date message
        self.assertIn("processing 30 days + 250 days lookback", out.getvalue())
        
        # Verify indicators were created
        indicators = ETFTechnicalIndicator.objects.filter(etf=self.etf)
        self.assertGreater(indicators.count(), 0)

    def test_calculate_indicators(self):
        """Test indicator calculation logic"""
        command = Command()
        
        # Create a simple DataFrame to test
        dates = [datetime.now().date() - timedelta(days=i) for i in range(250, 0, -1)]
        prices = np.linspace(100, 150, 250)  # Linear price increase
        volumes = np.random.randint(100000, 1000000, 250)  # Random volumes
        
        df = pd.DataFrame({
            'date': dates,
            'open': prices - 0.5,
            'high': prices + 1.0,
            'low': prices - 1.0,
            'close': prices,
            'volume': volumes
        })
        
        # Delete any existing indicators
        ETFTechnicalIndicator.objects.filter(etf=self.etf).delete()
        
        # Calculate indicators
        command._calculate_indicators(self.etf, df)
        
        # Verify indicators were created
        indicators = ETFTechnicalIndicator.objects.filter(etf=self.etf)
        self.assertGreater(indicators.count(), 0)
        
        # Check specific indicators for the most recent date
        latest = indicators.order_by('-date').first()
        self.assertIsNotNone(latest)
        
        # The SMA-5 should be close to the average of the last 5 prices
        expected_sma5 = sum(prices[-5:]) / 5
        self.assertAlmostEqual(float(latest.sma_5), expected_sma5, places=1)
        
        # Verify RSI is in the correct range
        self.assertTrue(0 <= float(latest.rsi_14) <= 100)
        
        # For an uptrend, RSI should be high
        self.assertGreater(float(latest.rsi_14), 50)

    def test_insufficient_price_data(self):
        """Test behavior when there's not enough price data"""
        # Create ETF with insufficient data
        etf_no_data = ETFDetails.objects.create(
            symbol='NODT',
            name='No Data ETF',
            description='ETF with insufficient data',
            category='Equity',
            family='Test',
            expense_ratio=Decimal('0.10')
        )
        
        # Create only 10 days of data (less than the 250 required)
        base_date = datetime.now().date() - timedelta(days=10)
        prices = []
        
        for i in range(10):
            current_date = base_date + timedelta(days=i)
            prices.append(ETFPrice(
                etf=etf_no_data,
                date=current_date,
                open=Decimal('100.0'),
                high=Decimal('101.0'),
                low=Decimal('99.0'),
                close=Decimal('100.5'),
                volume=1000000
            ))
        
        ETFPrice.objects.bulk_create(prices)
        
        out = StringIO()
        call_command('calculate_indicators', symbol='NODT', stdout=out)
        
        # Verify warning message
        self.assertIn("Not enough price data for NODT", out.getvalue())
        
        # Verify no indicators were created
        indicators = ETFTechnicalIndicator.objects.filter(etf=etf_no_data)
        self.assertEqual(indicators.count(), 0)
