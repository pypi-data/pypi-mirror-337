import pandas as pd
import requests
from unittest import mock
from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from io import StringIO

from data.models import ETFDetails, ETFPrice, ETFTopHolding, ETFSectorWeighting, ETFAssetAllocation
from data.management.commands.fetch_etfs_data import Command


class TestETFDataCommand(TestCase):
    """Test cases for fetch_etfs_data command"""

    def setUp(self):
        """Set up test data and mocks"""
        # Create test ETF
        self.test_etf = ETFDetails.objects.create(
            symbol="TEST",
            name="Test ETF",
            provider="Test Provider",
            asset_class="Equity",
            total_assets=1000000,
            ter=0.05,
            pe_ratio=20.5,
            beta=1.1
        )
        
        # Sample data for mocking
        self.sample_etf_csv_data = pd.DataFrame({
            'Symbol': ['SPY', 'QQQ'],
            'ETF Name': ['SPDR S&P 500 ETF', 'Invesco QQQ Trust'],
            'Asset Class': ['Equity', 'Equity'],
            'Total Assets ': [300000000000, 150000000000],
            'Inception': ['1993-01-22', '1999-03-10'],
            'ER': [0.09, 0.2],
            'P/E Ratio': [22.5, 30.2],
            'Beta': [1.0, 1.2]
        })
        
        self.sample_price_data = pd.DataFrame({
            'Open': [400.5, 401.2, 399.8],
            'High': [405.1, 402.6, 401.3],
            'Low': [398.2, 399.7, 396.5],
            'Close': [401.2, 400.8, 398.7],
            'Volume': [75000000, 68000000, 82000000]
        }, index=pd.date_range('2023-01-01', periods=3))
        
        # Mock fund data structure
        class MockFundsData:
            def __init__(self):
                self.top_holdings = pd.DataFrame({
                    'Name': ['Apple Inc', 'Microsoft Corp'],
                    'Percentage': [0.075, 0.067]
                }, index=['AAPL', 'MSFT'])
                
                self.sector_weightings = {
                    'Technology': 0.28,
                    'Financial Services': 0.15,
                    'Healthcare': 0.12
                }
                
                self.asset_classes = {
                    'Equity': 0.95,
                    'Cash': 0.05
                }
        
        self.mock_funds_data = MockFundsData()

    @mock.patch('data.management.commands.fetch_etfs_data.os.path.exists')
    @mock.patch('data.management.commands.fetch_etfs_data.os.listdir')
    @mock.patch('pandas.read_csv')
    def test_import_etfs_from_file(self, mock_read_csv, mock_listdir, mock_exists):
        """Test importing ETF data from CSV files"""
        # Setup mocks
        mock_exists.return_value = True
        mock_listdir.return_value = ['etfs_test.csv']
        mock_read_csv.return_value = self.sample_etf_csv_data
        
        # Run command
        out = StringIO()
        call_command('fetch_etfs_data', '--etfs-only', stdout=out)
        
        # Verify results
        self.assertIn("ETF population complete", out.getvalue())
        
        # Check database records
        self.assertEqual(ETFDetails.objects.count(), 3)  # Our test_etf + 2 from CSV
        spy = ETFDetails.objects.get(symbol='SPY')
        self.assertEqual(spy.name, 'SPDR S&P 500 ETF')
        self.assertEqual(spy.ter, 0.09)

    @mock.patch('yfinance.Ticker')
    def test_update_etf_prices(self, mock_ticker):
        """Test updating ETF prices"""
        # Setup mock
        mock_ticker_instance = mock.MagicMock()
        mock_ticker_instance.history.return_value = self.sample_price_data
        mock_ticker.return_value = mock_ticker_instance
        
        # Run command
        out = StringIO()
        call_command('fetch_etfs_data', '--prices-only', stdout=out)
        
        # Verify results
        self.assertIn("ETF population complete", out.getvalue())
        
        # Check database records
        prices = ETFPrice.objects.filter(etf=self.test_etf)
        self.assertEqual(prices.count(), 3)
        
        # Verify last_price_date was updated
        self.test_etf.refresh_from_db()
        expected_date = self.sample_price_data.index[-1].date()
        self.assertEqual(self.test_etf.last_price_date, expected_date)

    @mock.patch('yfinance.Ticker')
    def test_validate_price_data(self, mock_ticker):
        """Test price data validation"""
        cmd = Command()
        
        # Create data with invalid values
        invalid_data = pd.DataFrame({
            'Open': [400.5, -10.2, 399.8],  # Negative price
            'High': [405.1, 402.6, 401.3],
            'Low': [398.2, 405.7, 396.5],   # Low > High
            'Close': [401.2, 400.8, 398.7],
            'Volume': [75000000, 68000000, 82000000]
        }, index=pd.date_range('2023-01-01', periods=3))
        
        # Validate data
        valid_df = cmd.validate_price_data(invalid_data, "TEST")
        
        # Should have filtered out the invalid rows
        self.assertEqual(len(valid_df), 1)

    @mock.patch('yfinance.Ticker')
    def test_update_additional_data(self, mock_ticker):
        """Test updating additional ETF data (holdings, sectors, allocations)"""
        # Setup mock
        mock_ticker.return_value.funds_data = self.mock_funds_data
        
        # Run command
        out = StringIO()
        call_command('fetch_etfs_data', '--additional-only', stdout=out)
        
        # Verify results
        self.assertIn("ETF population complete", out.getvalue())
        
        # Check database records
        holdings = ETFTopHolding.objects.filter(etf=self.test_etf)
        self.assertEqual(holdings.count(), 2)
        self.assertTrue(holdings.filter(symbol='AAPL').exists())
        
        sectors = ETFSectorWeighting.objects.filter(etf=self.test_etf)
        self.assertEqual(sectors.count(), 3)
        tech_sector = sectors.get(sector='Technology')
        self.assertEqual(tech_sector.weighting_percent, 28.0)
        
        allocations = ETFAssetAllocation.objects.filter(etf=self.test_etf)
        self.assertEqual(allocations.count(), 2)
        equity_alloc = allocations.get(allocation='Equity')
        self.assertEqual(equity_alloc.allocation_percent, 95.0)

    @mock.patch('pandas.read_csv')
    def test_specific_symbol_filter(self, mock_read_csv):
        """Test filtering by specific symbols"""
        mock_read_csv.return_value = self.sample_etf_csv_data
        
        # Run command with specific symbol
        out = StringIO()
        call_command('fetch_etfs_data', '--etfs-only', '--symbols=SPY', stdout=out)
        
        # Verify only SPY was processed
        self.assertIn("Processing only these symbols: SPY", out.getvalue())
        # Our test_etf + only SPY from the CSV
        self.assertEqual(ETFDetails.objects.filter(symbol='QQQ').count(), 0)
        self.assertEqual(ETFDetails.objects.filter(symbol='SPY').count(), 1)

    @mock.patch('data.management.commands.fetch_etfs_data.requests.Session')
    def test_http_session_setup(self, mock_session):
        """Test HTTP session setup with retry mechanism"""
        cmd = Command()
        cmd._setup_http_session()
        
        # Verify session was configured
        self.assertTrue(mock_session.called)
        mount_calls = mock_session.return_value.mount.call_args_list
        self.assertEqual(len(mount_calls), 2)
        self.assertIn("http://", mount_calls[0][0][0])
        self.assertIn("https://", mount_calls[1][0][0])

    @mock.patch('yfinance.Ticker')
    def test_fetch_etf_prices_error_handling(self, mock_ticker):
        """Test error handling in fetch_etf_prices method"""
        # Make the ticker raise an exception
        mock_ticker.side_effect = requests.exceptions.RequestException("API Error")
        
        cmd = Command()
        
        # This should retry and eventually fail
        with self.assertRaises(requests.exceptions.RequestException):
            cmd.fetch_etf_prices(self.test_etf)
        
        # Check the stats were updated correctly
        self.assertEqual(cmd.stats.api_failures, 1)

    def test_command_error_handling(self):
        """Test overall command error handling"""
        with mock.patch.object(Command, '_import_etfs_from_files', 
                              side_effect=Exception("Test error")):
            with self.assertRaises(CommandError):
                call_command('fetch_etfs_data')

    @mock.patch('time.sleep')
    @mock.patch('yfinance.Ticker')
    def test_batch_processing(self, mock_ticker, mock_sleep):
        """Test batch processing of ETFs"""
        # Create multiple test ETFs
        for i in range(5):
            ETFDetails.objects.create(
                symbol=f"TEST{i}",
                name=f"Test ETF {i}",
                provider="Test Provider"
            )
        
        mock_ticker_instance = mock.MagicMock()
        mock_ticker_instance.history.return_value = self.sample_price_data
        mock_ticker.return_value = mock_ticker_instance
        
        # Run command with small batch size
        with mock.patch('data.management.commands.fetch_etfs_data.CONFIG', 
                       {'max_threads': 2, 'batch_size': 3, 'pause_seconds': 1,
                        'retry_attempts': 3, 'retry_backoff': 1, 
                        'connection_timeout': 5, 'db_batch_size': 100}):
            out = StringIO()
            call_command('fetch_etfs_data', '--prices-only', stdout=out)
            
        # Verify batching worked
        self.assertTrue(mock_sleep.called)
        output = out.getvalue()
        self.assertIn("Processing batch 1/2", output)
        self.assertIn("Processing batch 2/2", output)
