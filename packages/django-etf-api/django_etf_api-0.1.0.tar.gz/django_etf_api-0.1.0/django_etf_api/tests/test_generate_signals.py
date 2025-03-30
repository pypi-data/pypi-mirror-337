from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import patch, MagicMock
import pandas as pd
from django.test import TestCase
from django.core.management import call_command
from io import StringIO

from data.models import ETFDetails, ETFTechnicalIndicator, ETFSignal, ETFPrice
from data.management.commands.generate_signals import Command as GenerateSignalsCommand


class GenerateSignalsCommandTest(TestCase):
    """Test suite for the generate_signals management command."""

    def setUp(self):
        """Set up test data before each test."""
        # Create test ETF
        self.etf = ETFDetails.objects.create(
            symbol="TEST",
            name="Test ETF",
            asset_class="Equity"
        )
        
        # Create dates for the test data
        self.today = datetime.now().date()
        self.dates = [(self.today - timedelta(days=i)) for i in range(10)]
        
        # Create technical indicators
        self._create_test_indicators()
        
        # Create price data
        self._create_test_prices()
        
    def _create_test_indicators(self):
        """Create test technical indicators."""
        indicators = []
        for i, date in enumerate(self.dates):
            # Create indicators with values that will trigger different signals
            indicators.append(
                ETFTechnicalIndicator(
                    etf=self.etf,
                    date=date,
                    sma_5=Decimal(105 + i),
                    sma_20=Decimal(100 + i),
                    sma_50=Decimal(100 + (i*0.5)),  # Crosses SMA 200 at i=6
                    sma_200=Decimal(103),
                    rsi_14=Decimal(40 + i*5),  # Goes from 40 to 85 (crosses overbought)
                    macd=Decimal(-0.5 + i*0.2),  # Crosses signal around i=5
                    macd_signal=Decimal(0.5),
                    bb_upper=Decimal(110 + i),
                    bb_middle=Decimal(100 + i),
                    bb_lower=Decimal(90 + i),
                    stoch_k=Decimal(30 + i*7),  # Goes from 30 to 93 (crosses overbought)
                    stoch_d=Decimal(50)
                )
            )
        ETFTechnicalIndicator.objects.bulk_create(indicators)

    def _create_test_prices(self):
        """Create test price data."""
        prices = []
        for i, date in enumerate(self.dates):
            prices.append(
                ETFPrice(
                    etf=self.etf,
                    date=date,
                    open=Decimal(100 + i),
                    high=Decimal(105 + i),
                    low=Decimal(95 + i),
                    close=Decimal(102 + i),
                    volume=1000 * (i + 1)
                )
            )
        ETFPrice.objects.bulk_create(prices)
    
    def test_command_execution(self):
        """Test basic command execution."""
        # Redirect stdout to capture output
        out = StringIO()
        call_command('generate_signals', stdout=out)
        
        # Check output for expected message
        self.assertIn("All ETFs processed successfully", out.getvalue())
        
        # Verify signals were created
        signals = ETFSignal.objects.filter(etf=self.etf)
        self.assertTrue(signals.exists())

    def test_specific_symbol(self):
        """Test processing a specific ETF symbol."""
        out = StringIO()
        call_command('generate_signals', symbol='TEST', stdout=out)
        
        self.assertIn("Generating signals for 1 ETFs", out.getvalue())
        self.assertIn("Completed signal generation for TEST", out.getvalue())

    def test_invalid_symbol(self):
        """Test with non-existent ETF symbol."""
        out = StringIO()
        err = StringIO()
        call_command('generate_signals', symbol='NONEXISTENT', stdout=out, stderr=err)
        
        self.assertIn("No ETF found with symbol NONEXISTENT", err.getvalue())

    def test_days_parameter(self):
        """Test the days parameter."""
        out = StringIO()
        call_command('generate_signals', days=5, stdout=out)
        
        five_days_ago = datetime.now().date() - timedelta(days=5)
        self.assertIn(f"Using cutoff date: {five_days_ago}", out.getvalue())

    def test_generate_signals_function(self):
        """Test the _generate_signals method directly."""
        command = GenerateSignalsCommand()
        
        # Get indicators to pass to the function
        indicators = ETFTechnicalIndicator.objects.filter(etf=self.etf)
        
        # Create DataFrame that would be passed to _generate_signals
        df_values = list(indicators.values())
        df = pd.DataFrame(df_values)
        
        # Get price data and merge
        prices = ETFPrice.objects.filter(
            etf=self.etf, 
            date__in=[ind.date for ind in indicators]
        ).values('date', 'close')
        
        price_df = pd.DataFrame(list(prices))
        df = pd.merge(df, price_df, on='date', how='inner')
        
        # Call the function
        command._generate_signals(self.etf, df, indicators)
        
        # Verify signals were created
        signals = ETFSignal.objects.filter(etf=self.etf)
        self.assertTrue(signals.exists())
        
        # Check for specific signal types that should be generated based on our test data
        signal_types = set(signals.values_list('signal_source', flat=True))
        self.assertIn('RSI', signal_types)  # RSI crosses above 70
        self.assertIn('MACD', signal_types)  # MACD crosses signal line

    @patch('data.management.commands.generate_signals.ETFTechnicalIndicator.objects.filter')
    def test_not_enough_indicators(self, mock_filter):
        """Test case when there are not enough indicators."""
        mock_filter.return_value.order_by.return_value = MagicMock(count=lambda: 3)
        
        out = StringIO()
        err = StringIO()
        call_command('generate_signals', symbol='TEST', stdout=out, stderr=err)
        
        self.assertIn("Not enough indicator data for TEST", err.getvalue())

    @patch('data.management.commands.generate_signals.ETFPrice.objects.filter')
    def test_no_matching_prices(self, mock_filter):
        """Test case when there are no matching prices."""
        mock_filter.return_value.values.return_value = []
        
        out = StringIO()
        err = StringIO()
        call_command('generate_signals', symbol='TEST', stdout=out, stderr=err)
        
        self.assertIn("No matching price data for TEST", err.getvalue())

    def test_signal_types_and_sources(self):
        """Test that different signal types and sources are generated."""
        # Run the command
        call_command('generate_signals', symbol='TEST')
        
        # Get all signals
        signals = ETFSignal.objects.filter(etf=self.etf)
        
        # Check signal types
        signal_types = set(signals.values_list('signal_type', flat=True))
        expected_types = {'BUY', 'SELL', 'STRONG_BUY', 'STRONG_SELL'}
        self.assertTrue(any(t in signal_types for t in expected_types))
        
        # Check signal sources
        signal_sources = set(signals.values_list('signal_source', flat=True))
        expected_sources = {'SMA_CROSS', 'MACD', 'RSI', 'BB', 'STOCH', 'MULTI'}
        self.assertTrue(any(s in signal_sources for s in expected_sources))
        
    def test_atomic_transaction(self):
        """Test that signal generation is atomic."""
        # First run to create some signals
        call_command('generate_signals', symbol='TEST')
        
        # Count the signals
        initial_count = ETFSignal.objects.count()
        self.assertTrue(initial_count > 0)
        
        # Run again - should replace the signals, not add to them
        call_command('generate_signals', symbol='TEST')
        
        # Count should be the same (or very similar)
        new_count = ETFSignal.objects.count()
        self.assertEqual(initial_count, new_count)
