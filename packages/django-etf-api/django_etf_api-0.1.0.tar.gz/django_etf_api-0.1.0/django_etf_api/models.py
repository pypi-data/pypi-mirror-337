from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class ETFDetails(models.Model):
    """
    Model representing exchange-traded fund (ETF) details including key metrics and identifiers.
    """
    PROVIDER_CHOICES = [
        ("Allianz", "Allianz"),
        ("American Century", "American Century"),
        ("ARK", "ARK"),
        ("Capital Group", "Capital Group"),
        ("Digital Currency Group", "Digital Currency Group"),
        ("Dimensional", "Dimensional"),
        ("Direxion", "Direxion"),
        ("Exchange Traded Concepts", "Exchange Traded Concepts"),
        ("Fidelity", "Fidelity"),
        ("Franklin Templeton", "Franklin Templeton"),
        ("GraniteShares", "GraniteShares"),
        ("Innovator", "Innovator"),
        ("Invesco", "Invesco"),
        ("iShares", "iShares"),
        ("Janus Henderson", "Janus Henderson"),
        ("JPMorgan", "JPMorgan"),
        ("Mirae Asset", "Mirae Asset"),
        ("Morgan Stanley", "Morgan Stanley"),
        ("New York Life", "New York Life"),
        ("ProShares", "ProShares"),
        ("Rafferty", "Rafferty"),
        ("Schwab", "Schwab"),
        ("SPDR", "SPDR"),
        ("SS&C", "SS&C"),
        ("Toroso", "Toroso"),
        ("VanEck", "VanEck"),
        ("Vanguard", "Vanguard"),
        ("WisdomTree", "WisdomTree"),
        ("Xtrackers", "Xtrackers"),
        ("YieldMax", "YieldMax"),
    ]

    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES, blank=True, null=True)
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=200)
    asset_class = models.CharField(max_length=12, blank=True, null=True)
    total_assets = models.CharField(max_length=100, blank=True, null=True)
    inception = models.CharField(max_length=10, blank=True, null=True)
    ter = models.CharField(max_length=50, blank=True, null=True)
    pe_ratio = models.FloatField(blank=True, null=True)
    beta = models.FloatField(blank=True, null=True)
    last_price_date = models.DateField(blank=True, null=True)  # Track last price date separately
    last_updated = models.DateField(auto_now=True)  # Automatically update on save
    
    class Meta:
        verbose_name = "ETF Detail"
        verbose_name_plural = "ETF Details"
        indexes = [
            models.Index(fields=['symbol']),
            models.Index(fields=['provider']),
        ]
    
    def __str__(self):
        return f"{self.symbol} - {self.name}"


class ETFPrice(models.Model):
    """
    Historical price data for ETFs including OHLCV values.
    """
    etf = models.ForeignKey(ETFDetails, on_delete=models.CASCADE, related_name='prices')
    date = models.DateField(db_index=True)  # Add index for frequent date filtering
    open = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    close = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()
    
    class Meta:
        unique_together = ('etf', 'date')
        ordering = ['-date']
        verbose_name = "ETF Price"
        verbose_name_plural = "ETF Prices"
    
    def __str__(self):
        return f"{self.etf.symbol} - {self.date} - ${self.close}"


class ETFAssetAllocation(models.Model):
    """
    Asset allocation breakdown for ETFs showing distribution across asset classes.
    """
    etf = models.ForeignKey(ETFDetails, on_delete=models.CASCADE, related_name="asset_allocations")
    allocation = models.CharField(max_length=100)
    allocation_percent = models.DecimalField(
        max_digits=6, 
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )

    class Meta:
        unique_together = ("etf", "allocation")
        verbose_name = "ETF Asset Allocation"
        verbose_name_plural = "ETF Asset Allocations"
        ordering = ['-allocation_percent']  # Show highest allocations first

    def __str__(self):
        return f"{self.etf.symbol} - {self.allocation}: {self.allocation_percent:.2f}%"
    
    @property
    def formatted_percent(self):
        """Return weighting percent formatted with 2 decimal places and % symbol"""
        return f"{self.allocation_percent:.2f}%"


class ETFTopHolding(models.Model):
    """
    Top holdings for ETFs showing their largest individual positions.
    """
    etf = models.ForeignKey(ETFDetails, on_delete=models.CASCADE, related_name="top_holdings")
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=255)
    holding_percent = models.DecimalField(
        max_digits=6, 
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )

    class Meta:
        unique_together = ("etf", "symbol")
        ordering = ["-holding_percent"]
        verbose_name = "ETF Top Holding"
        verbose_name_plural = "ETF Top Holdings"

    def __str__(self):
        return f"{self.etf.symbol} - {self.name} ({self.symbol}): {self.holding_percent:.2f}%"
    
    @property
    def formatted_percent(self):
        """Return holding percent formatted with 2 decimal places and % symbol"""
        return f"{self.holding_percent:.2f}%"


class ETFSectorWeighting(models.Model):
    """
    Sector allocation breakdown for ETFs showing distribution across market sectors.
    """
    etf = models.ForeignKey(ETFDetails, on_delete=models.CASCADE, related_name="sector_weightings")
    sector = models.CharField(max_length=100)
    weighting_percent = models.DecimalField(
        max_digits=6, 
        decimal_places=4,
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))]
    )

    class Meta:
        unique_together = ("etf", "sector")
        verbose_name = "ETF Sector Weighting"
        verbose_name_plural = "ETF Sector Weightings"
        ordering = ['-weighting_percent']

    def __str__(self):
        return f"{self.etf.symbol} - {self.sector}: {self.weighting_percent:.2f}%"
    
    @property
    def formatted_percent(self):
        """Return weighting percent formatted with 2 decimal places and % symbol"""
        return f"{self.weighting_percent:.2f}%"


class ETFTechnicalIndicator(models.Model):
    """
    Technical indicators for ETFs including moving averages, oscillators, and volatility metrics.
    """
    etf = models.ForeignKey(ETFDetails, on_delete=models.CASCADE, related_name='technical_indicators')
    date = models.DateField(db_index=True)
    
    # Moving Averages
    sma_5 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sma_10 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sma_20 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sma_50 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sma_200 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Exponential Moving Averages
    ema_12 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ema_26 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # MACD
    macd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    macd_signal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    macd_histogram = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Bollinger Bands
    bb_upper = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bb_middle = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bb_lower = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Oscillators and other indicators
    rsi_14 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stoch_k = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stoch_d = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    atr_14 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    obv = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        unique_together = ('etf', 'date')
        ordering = ['-date']
        verbose_name = "ETF Technical Indicator"
        verbose_name_plural = "ETF Technical Indicators"
        indexes = [
            models.Index(fields=['etf', 'date']),
        ]
    
    def __str__(self):
        return f"{self.etf.symbol} - {self.date} - Technical Indicators"


class ETFSignal(models.Model):
    """
    Trading signals for ETFs based on technical analysis with confidence levels and reasoning.
    """
    SIGNAL_TYPES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
        ('HOLD', 'Hold'),
        ('STRONG_BUY', 'Strong Buy'),
        ('STRONG_SELL', 'Strong Sell'),
    ]
    
    SIGNAL_SOURCES = [
        ('SMA_CROSS', 'SMA Crossover'),
        ('MACD', 'MACD'),
        ('RSI', 'RSI'),
        ('BB', 'Bollinger Bands'),
        ('STOCH', 'Stochastic'),
        ('MULTI', 'Multiple Indicators'),
    ]
    
    etf = models.ForeignKey(ETFDetails, on_delete=models.CASCADE, related_name='signals')
    date = models.DateField(db_index=True)
    signal_type = models.CharField(max_length=20, choices=SIGNAL_TYPES)
    signal_source = models.CharField(max_length=20, choices=SIGNAL_SOURCES)
    confidence = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0')), MaxValueValidator(Decimal('100'))],
        help_text="Confidence level from 0-100%"
    )
    description = models.TextField(help_text="Description of the signal and reasoning")
    indicator = models.ForeignKey(
        ETFTechnicalIndicator, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='generated_signals'
    )
    
    class Meta:
        ordering = ['-date', '-confidence']
        verbose_name = "ETF Signal"
        verbose_name_plural = "ETF Signals"
        indexes = [
            models.Index(fields=['etf', 'date']),
            models.Index(fields=['signal_type']),
        ]
    
    def __str__(self):
        return f"{self.etf.symbol} - {self.date} - {self.signal_type} ({self.confidence:.2f}%)"
        
    @property
    def get_confidence_display(self):
        """Return formatted confidence percentage"""
        return f"{self.confidence:.2f}%"