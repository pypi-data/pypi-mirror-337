from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from datetime import date, timedelta
from decimal import Decimal

from ..models import ETFDetails, ETFPrice, ETFAssetAllocation, ETFTopHolding, ETFSectorWeighting, ETFTechnicalIndicator, ETFSignal

"""ETF Model Tests"""

class ETFDetailsModelTest(TestCase):
    """Test cases for the ETFDetails model."""
    
    def setUp(self):
        """Create sample ETF details for testing."""
        self.etf = ETFDetails.objects.create(
            provider="Vanguard",
            symbol="VTI",
            name="Vanguard Total Stock Market ETF",
            asset_class="Equity",
            total_assets="$300B",
            inception="2001-05-24",
            ter="0.03%",
            pe_ratio=22.5,
            beta=1.02,
            last_price_date=date.today() - timedelta(days=1)
        )
    
    def test_etf_creation(self):
        """Test ETFDetails instance creation with valid data."""
        self.assertEqual(self.etf.symbol, "VTI")
        self.assertEqual(self.etf.name, "Vanguard Total Stock Market ETF")
        self.assertEqual(self.etf.provider, "Vanguard")
        self.assertEqual(str(self.etf), "VTI - Vanguard Total Stock Market ETF")
    
    def test_unique_symbol_constraint(self):
        """Test that ETF symbols must be unique."""
        with self.assertRaises(IntegrityError):
            ETFDetails.objects.create(
                symbol="VTI",  # Duplicate symbol
                name="Duplicate ETF"
            )
    
    def test_provider_choices(self):
        """Test that provider must be one of the predefined choices."""
        self.etf.provider = "Invalid Provider"
        with self.assertRaises(ValidationError):
            self.etf.full_clean()


class ETFPriceModelTest(TestCase):
    """Test cases for the ETFPrice model."""
    
    def setUp(self):
        """Create sample ETF and price data for testing."""
        self.etf = ETFDetails.objects.create(
            symbol="SPY",
            name="SPDR S&P 500 ETF Trust"
        )
        self.price = ETFPrice.objects.create(
            etf=self.etf,
            date=date.today() - timedelta(days=1),
            open=Decimal('450.25'),
            high=Decimal('453.75'),
            low=Decimal('448.50'),
            close=Decimal('452.10'),
            volume=65000000
        )
    
    def test_price_creation(self):
        """Test ETFPrice instance creation with valid data."""
        self.assertEqual(self.price.etf, self.etf)
        self.assertEqual(self.price.close, Decimal('452.10'))
        self.assertEqual(str(self.price), f"SPY - {date.today() - timedelta(days=1)} - $452.10")
    
    def test_unique_etf_date_constraint(self):
        """Test that ETF price entries must have unique date per ETF."""
        with self.assertRaises(IntegrityError):
            ETFPrice.objects.create(
                etf=self.etf,
                date=date.today() - timedelta(days=1),  # Same date as existing
                open=Decimal('451.00'),
                high=Decimal('455.00'),
                low=Decimal('450.00'),
                close=Decimal('454.00'),
                volume=70000000
            )


class ETFAssetAllocationModelTest(TestCase):
    """Test cases for the ETFAssetAllocation model."""
    
    def setUp(self):
        """Create sample ETF and asset allocation data for testing."""
        self.etf = ETFDetails.objects.create(
            symbol="VXUS",
            name="Vanguard Total International Stock ETF"
        )
        self.allocation = ETFAssetAllocation.objects.create(
            etf=self.etf,
            allocation="International Equity",
            allocation_percent=Decimal('95.5')
        )
    
    def test_allocation_creation(self):
        """Test ETFAssetAllocation instance creation with valid data."""
        self.assertEqual(self.allocation.etf, self.etf)
        self.assertEqual(self.allocation.allocation, "International Equity")
        self.assertEqual(self.allocation.allocation_percent, Decimal('95.5'))
    
    def test_formatted_percent_property(self):
        """Test the formatted_percent property."""
        self.assertEqual(self.allocation.formatted_percent, "95.50%")
    
    def test_allocation_percent_validation(self):
        """Test that allocation percentage must be between 0 and 100."""
        with self.assertRaises(ValidationError):
            invalid_allocation = ETFAssetAllocation(
                etf=self.etf,
                allocation="Over Allocation",
                allocation_percent=Decimal('101')  # Over 100%
            )
            invalid_allocation.full_clean()


class ETFTopHoldingModelTest(TestCase):
    """Test cases for the ETFTopHolding model."""
    
    def setUp(self):
        """Create sample ETF and top holding data for testing."""
        self.etf = ETFDetails.objects.create(
            symbol="QQQ",
            name="Invesco QQQ Trust Series 1"
        )
        self.holding = ETFTopHolding.objects.create(
            etf=self.etf,
            symbol="AAPL",
            name="Apple Inc.",
            holding_percent=Decimal('12.5')
        )
    
    def test_holding_creation(self):
        """Test ETFTopHolding instance creation with valid data."""
        self.assertEqual(self.holding.etf, self.etf)
        self.assertEqual(self.holding.symbol, "AAPL")
        self.assertEqual(self.holding.name, "Apple Inc.")
        self.assertEqual(self.holding.holding_percent, Decimal('12.5'))
    
    def test_formatted_percent_property(self):
        """Test the formatted_percent property."""
        self.assertEqual(self.holding.formatted_percent, "12.50%")
    
    def test_unique_etf_symbol_constraint(self):
        """Test that top holdings must have unique symbols per ETF."""
        with self.assertRaises(IntegrityError):
            ETFTopHolding.objects.create(
                etf=self.etf,
                symbol="AAPL",  # Duplicate symbol for this ETF
                name="Apple Inc. Duplicate",
                holding_percent=Decimal('10.0')
            )


class ETFSectorWeightingModelTest(TestCase):
    """Test cases for the ETFSectorWeighting model."""
    
    def setUp(self):
        """Create sample ETF and sector weighting data for testing."""
        self.etf = ETFDetails.objects.create(
            symbol="XLK",
            name="Technology Select Sector SPDR Fund"
        )
        self.sector = ETFSectorWeighting.objects.create(
            etf=self.etf,
            sector="Information Technology",
            weighting_percent=Decimal('85.75')
        )
    
    def test_sector_weighting_creation(self):
        """Test ETFSectorWeighting instance creation with valid data."""
        self.assertEqual(self.sector.etf, self.etf)
        self.assertEqual(self.sector.sector, "Information Technology")
        self.assertEqual(self.sector.weighting_percent, Decimal('85.75'))
    
    def test_formatted_percent_property(self):
        """Test the formatted_percent property."""
        self.assertEqual(self.sector.formatted_percent, "85.75%")


class ETFTechnicalIndicatorModelTest(TestCase):
    """Test cases for the ETFTechnicalIndicator model."""
    
    def setUp(self):
        """Create sample ETF and technical indicators data for testing."""
        self.etf = ETFDetails.objects.create(
            symbol="IWM",
            name="iShares Russell 2000 ETF"
        )
        self.indicator = ETFTechnicalIndicator.objects.create(
            etf=self.etf,
            date=date.today() - timedelta(days=1),
            sma_5=Decimal('185.25'),
            sma_10=Decimal('183.50'),
            sma_20=Decimal('180.75'),
            rsi_14=Decimal('65.5'),
            macd=Decimal('2.35'),
            macd_signal=Decimal('1.75'),
            macd_histogram=Decimal('0.60')
        )
    
    def test_technical_indicator_creation(self):
        """Test ETFTechnicalIndicator instance creation with valid data."""
        self.assertEqual(self.indicator.etf, self.etf)
        self.assertEqual(self.indicator.sma_5, Decimal('185.25'))
        self.assertEqual(self.indicator.rsi_14, Decimal('65.5'))
    
    def test_unique_etf_date_constraint(self):
        """Test that technical indicators must have unique dates per ETF."""
        with self.assertRaises(IntegrityError):
            ETFTechnicalIndicator.objects.create(
                etf=self.etf,
                date=date.today() - timedelta(days=1),  # Same date
                sma_5=Decimal('186.00')
            )


class ETFSignalModelTest(TestCase):
    """Test cases for the ETFSignal model."""
    
    def setUp(self):
        """Create sample ETF, technical indicators, and signals for testing."""
        self.etf = ETFDetails.objects.create(
            symbol="EEM",
            name="iShares MSCI Emerging Markets ETF"
        )
        
        self.indicator = ETFTechnicalIndicator.objects.create(
            etf=self.etf,
            date=date.today() - timedelta(days=1),
            sma_5=Decimal('40.25'),
            sma_20=Decimal('39.50'),
            rsi_14=Decimal('72.5')
        )
        
        self.signal = ETFSignal.objects.create(
            etf=self.etf,
            date=date.today() - timedelta(days=1),
            signal_type='BUY',
            signal_source='RSI',
            confidence=Decimal('85.5'),
            description="RSI moving up from oversold territory",
            indicator=self.indicator
        )
    
    def test_signal_creation(self):
        """Test ETFSignal instance creation with valid data."""
        self.assertEqual(self.signal.etf, self.etf)
        self.assertEqual(self.signal.signal_type, 'BUY')
        self.assertEqual(self.signal.signal_source, 'RSI')
        self.assertEqual(self.signal.confidence, Decimal('85.5'))
        self.assertEqual(self.signal.indicator, self.indicator)
    
    def test_get_confidence_display(self):
        """Test the get_confidence_display property."""
        self.assertEqual(self.signal.get_confidence_display, "85.50%")
    
    def test_confidence_validation(self):
        """Test that confidence must be between 0 and 100."""
        with self.assertRaises(ValidationError):
            invalid_signal = ETFSignal(
                etf=self.etf,
                date=date.today(),
                signal_type='SELL',
                signal_source='MACD',
                confidence=Decimal('101.5'),  # Over 100%
                description="Invalid confidence level"
            )
            invalid_signal.full_clean()
