from datetime import date, datetime
from decimal import Decimal
from io import StringIO
from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.core.management import call_command

from data.models import (
    ETFDetails, ETFPrice, ETFTopHolding, ETFSectorWeighting, 
    ETFAssetAllocation, ETFTechnicalIndicator, ETFSignal
)
from data.management.commands.print_etf_data import Command


class PrintETFDataCommandTest(TestCase):
    """Test cases for the print_etf_data management command."""
    
    def setUp(self):
        """Set up test data for ETF display."""
        # Create a sample ETF
        self.etf = ETFDetails.objects.create(
            symbol="TEST",
            name="Test ETF",
            provider="Vanguard",
            asset_class="Equity",
            total_assets="$100M",
            inception="2020-01-01",
            ter="0.05%",
            pe_ratio=20.5,
            beta=1.1,
            last_updated=datetime.now()
        )
        
        # Create sample price data
        self.price = ETFPrice.objects.create(
            etf=self.etf,
            date=date.today(),
            open=Decimal("100.00"),
            high=Decimal("105.00"),
            low=Decimal("99.00"),
            close=Decimal("103.50"),
            volume=1000000
        )
        
        # Create sample asset allocations
        ETFAssetAllocation.objects.create(
            etf=self.etf,
            allocation="US Equity",
            allocation_percent=Decimal("70.0")
        )
        ETFAssetAllocation.objects.create(
            etf=self.etf,
            allocation="International Equity",
            allocation_percent=Decimal("30.0")
        )
        
        # Create sample top holdings
        ETFTopHolding.objects.create(
            etf=self.etf,
            symbol="AAPL",
            name="Apple Inc",
            holding_percent=Decimal("10.5")
        )
        ETFTopHolding.objects.create(
            etf=self.etf,
            symbol="MSFT",
            name="Microsoft Corporation",
            holding_percent=Decimal("8.2")
        )
        
        # Create sample sector weightings
        ETFSectorWeighting.objects.create(
            etf=self.etf,
            sector="Technology",
            weighting_percent=Decimal("45.0")
        )
        ETFSectorWeighting.objects.create(
            etf=self.etf,
            sector="Healthcare",
            weighting_percent=Decimal("20.0")
        )
        
        # Create sample technical indicators
        self.indicator = ETFTechnicalIndicator.objects.create(
            etf=self.etf,
            date=date.today(),
            sma_5=Decimal("102.50"),
            sma_10=Decimal("101.75"),
            sma_20=Decimal("100.80"),
            sma_50=Decimal("98.50"),
            sma_200=Decimal("95.00"),
            ema_12=Decimal("102.00"),
            ema_26=Decimal("100.50"),
            macd=Decimal("1.50"),
            macd_signal=Decimal("1.20"),
            macd_histogram=Decimal("0.30"),
            bb_upper=Decimal("105.00"),
            bb_middle=Decimal("100.80"),
            bb_lower=Decimal("96.60"),
            rsi_14=Decimal("65.5"),
            stoch_k=Decimal("75.0"),
            stoch_d=Decimal("70.0"),
            atr_14=Decimal("2.50"),
            obv=500000
        )
        
        # Create sample signals
        ETFSignal.objects.create(
            etf=self.etf,
            date=date.today(),
            signal_type="BUY",
            signal_source="RSI",
            confidence=Decimal("75.0"),
            description="RSI bouncing from oversold territory",
            indicator=self.indicator
        )
        ETFSignal.objects.create(
            etf=self.etf,
            date=date.today(),
            signal_type="SELL",
            signal_source="MACD",
            confidence=Decimal("65.0"),
            description="MACD crossing below signal line",
            indicator=self.indicator
        )
        
        # Create the command instance
        self.command = Command()
    
    def test_get_etf_success(self):
        """Test successful ETF retrieval by symbol."""
        # Test case-insensitive matching
        etf = self.command._get_etf("test")
        self.assertIsNotNone(etf)
        self.assertEqual(etf.symbol, "TEST")
        self.assertEqual(etf.name, "Test ETF")
    
    def test_get_etf_not_found(self):
        """Test ETF retrieval with non-existent symbol."""
        etf = self.command._get_etf("NONEXISTENT")
        self.assertIsNone(etf)
    
    def test_get_price_data(self):
        """Test retrieving price data for an ETF."""
        price_data = self.command._get_price_data(self.etf)
        self.assertIsNotNone(price_data)
        self.assertEqual(len(price_data), 6)  # 6 rows of price info
        
        # Check specific data fields
        self.assertEqual(price_data[1][0], "Open")
        self.assertEqual(price_data[4][0], "Close")
        self.assertEqual(price_data[4][1], "$103.50")
    
    def test_get_asset_allocation(self):
        """Test retrieving asset allocation data."""
        allocation_data = self.command._get_asset_allocation(self.etf)
        self.assertIsNotNone(allocation_data)
        self.assertEqual(len(allocation_data), 3)  # Header row + 2 allocations
        
        # Header row
        self.assertEqual(allocation_data[0][0], "Allocation")
        self.assertEqual(allocation_data[0][1], "Weight")
        
        # Check that allocations are ordered by percentage (descending)
        self.assertEqual(allocation_data[1][0], "US Equity")
        self.assertEqual(allocation_data[1][1], "70.00%")
    
    def test_get_top_holdings(self):
        """Test retrieving top holdings data."""
        holdings_data = self.command._get_top_holdings(self.etf)
        self.assertIsNotNone(holdings_data)
        self.assertEqual(len(holdings_data), 3)  # Header row + 2 holdings
        
        # Check data format
        self.assertEqual(holdings_data[1][0], "AAPL")
        self.assertEqual(holdings_data[1][2], "10.50%")
    
    def test_get_sector_weightings(self):
        """Test retrieving sector weighting data."""
        sector_data = self.command._get_sector_weightings(self.etf)
        self.assertIsNotNone(sector_data)
        self.assertEqual(len(sector_data), 3)  # Header row + 2 sectors
        
        # Check ordering by weight
        self.assertEqual(sector_data[1][0], "Technology")
        self.assertEqual(sector_data[1][1], "45.00%")
    
    def test_get_technical_indicators(self):
        """Test retrieving technical indicators data."""
        indicators_data = self.command._get_technical_indicators(self.etf)
        self.assertIsNotNone(indicators_data)
        
        # Check SMA values
        sma5_row = [row for row in indicators_data if row[0] == "SMA (5-day)"][0]
        self.assertEqual(sma5_row[1], "$102.50")
        
        # Check RSI values
        rsi_row = [row for row in indicators_data if row[0] == "RSI (14-day)"][0]
        self.assertEqual(rsi_row[1], "65.50")
    
    def test_get_signals(self):
        """Test retrieving trading signals data."""
        signals_data = self.command._get_signals(self.etf)
        self.assertIsNotNone(signals_data)
        self.assertEqual(len(signals_data), 3)  # Header row + 2 signals
        
        # Check signal types
        signal_types = [row[0] for row in signals_data[1:]]
        self.assertIn("Buy", signal_types)
        self.assertIn("Sell", signal_types)
    
    def test_colorize_headers(self):
        """Test colorizing table headers."""
        test_data = [
            ["Header1", "Header2", "Header3"],
            ["Value1", "Value2", "Value3"]
        ]
        
        colored_data = self.command._colorize_headers(test_data)
        
        # Check that color codes were added to headers
        for header in colored_data[0]:
            self.assertIn("\033[", header)
            self.assertIn("\033[0m", header)
        
        # Check that values were not modified
        self.assertEqual(colored_data[1], test_data[1])
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_command_output_success(self, mock_stdout):
        """Test command output with a valid ETF symbol."""
        call_command('print_etf_data', 'TEST', table_format='plain')
        output = mock_stdout.getvalue()
        
        # Check for key sections in the output
        self.assertIn("ETF: TEST - Test ETF", output)
        self.assertIn("FUND INFORMATION", output)
        self.assertIn("PRICE INFORMATION", output)
        self.assertIn("ASSET ALLOCATIONS", output)
        self.assertIn("TOP HOLDINGS", output)
        self.assertIn("SECTOR WEIGHTINGS", output)
        self.assertIn("TECHNICAL INDICATORS", output)
        self.assertIn("TRADING SIGNALS", output)
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_command_invalid_symbol(self, mock_stdout):
        """Test command handling of an invalid ETF symbol."""
        call_command('print_etf_data', 'INVALID', table_format='plain')
        output = mock_stdout.getvalue()
        
        self.assertIn("No ETF found with symbol 'INVALID'", output)
    
    def test_handle_missing_data(self):
        """Test handling of ETFs with missing data sections."""
        # Create ETF with minimal data
        minimal_etf = ETFDetails.objects.create(
            symbol="MIN",
            name="Minimal ETF"
        )
        
        # Test each data retrieval method with minimal ETF
        self.assertIsNone(self.command._get_price_data(minimal_etf))
        self.assertIsNone(self.command._get_asset_allocation(minimal_etf))
        self.assertIsNone(self.command._get_top_holdings(minimal_etf))
        self.assertIsNone(self.command._get_sector_weightings(minimal_etf))
        self.assertIsNone(self.command._get_technical_indicators(minimal_etf))
        self.assertIsNone(self.command._get_signals(minimal_etf))
    
    @patch.object(Command, '_display_etf_info')
    def test_display_etf_info_called(self, mock_display):
        """Test that the _display_etf_info method is called correctly."""
        with patch.object(Command, '_get_etf', return_value=self.etf):
            call_command('print_etf_data', 'TEST')
            mock_display.assert_called_once_with(self.etf)
