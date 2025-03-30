from django.db.models import Max
from tabulate import tabulate
from data.models import (
    ETFDetails, ETFPrice, ETFTopHolding, ETFSectorWeighting, 
    ETFAssetAllocation, ETFTechnicalIndicator, ETFSignal
)
from data.management.commands.utils.base_command import PortfolioBaseCommand

class Command(PortfolioBaseCommand):
    """Django command to display comprehensive ETF information with colorized output."""
    
    help = "Displays ETF information including price, holdings, sectors, and asset allocations"
    
    def __init__(self, *args, **kwargs):
        super().__init__(command_name="print_etf_data", *args, **kwargs)
        self.table_format = "grid"  # Default table format
        # ANSI color codes
        self.RED = "\033[91m"
        self.LIGHT_BLUE = "\033[38;5;75m"
        self.RESET = "\033[0m"
    
    def add_arguments(self, parser):
        parser.add_argument("symbol", type=str, help="ETF symbol to display data for (e.g., VOO, EEM)")
        parser.add_argument("--table-format", type=str, choices=[
            "plain", "simple", "github", "grid", "fancy_grid", 
            "pipe", "orgtbl", "jira", "presto", "pretty"
        ], default="grid", help="Table format style (default: grid)")
    
    def handle(self, *args, **kwargs):
        # Extract command arguments
        symbol = kwargs.get("symbol")
        self.table_format = kwargs.get("table_format")
        
        if not symbol:
            self.error("Symbol argument is required!")
            return
        
        # Get ETF data based on symbol
        etf = self._get_etf(symbol)
        
        if not etf:
            self.error(f"No ETF found with symbol '{symbol}'!")
            return
        
        # Display information for the ETF
        self._display_etf_info(etf)
        
        self.success("Data display complete!")
    
    def _get_etf(self, symbol):
        """Fetch ETF based on symbol."""
        self.info(f"Fetching data for ETF: {symbol.upper()}...\n")
        try:
            return ETFDetails.objects.get(symbol__iexact=symbol)  # Case-insensitive match
        except ETFDetails.DoesNotExist:
            return None
    
    def _colorize_headers(self, data):
        """Apply light red color to column headers (first row) of tables."""
        if not data or len(data) <= 1:
            return data
            
        # Create a copy to avoid modifying the original data
        colored_data = data.copy()
        
        # Color each column header in the first row
        if isinstance(colored_data[0], list):
            colored_data[0] = [f"{self.LIGHT_BLUE}{header}{self.RESET}" for header in colored_data[0]]
        
        return colored_data
    
    def _display_etf_info(self, etf):
        """Display comprehensive information for a single ETF."""
        # Create a centered header with the ETF symbol and name
        header = f" ETF: {etf.symbol} - {etf.name} "
        divider = "=" * 80
        
        self.info(divider)
        self.info(header.center(80))
        self.info(divider + "\n")
        
        # Display ETF metadata
        metadata = [
            ["Provider", etf.provider or "N/A"],
            ["Asset Class", etf.asset_class or "N/A"],
            ["Total Assets", etf.total_assets or "N/A"],
            ["Inception", etf.inception or "N/A"],
            ["Expense Ratio", etf.ter or "N/A"],
            ["P/E Ratio", f"{etf.pe_ratio:.2f}" if etf.pe_ratio else "N/A"],
            ["Beta", f"{etf.beta:.4f}" if etf.beta else "N/A"],
            ["Last Updated", etf.last_updated.strftime("%Y-%m-%d") if etf.last_updated else "N/A"]
        ]
        
        self.info(f"{self.RED}FUND INFORMATION{self.RESET}")
        self.info(tabulate(metadata, tablefmt=self.table_format))
        self.info("")  # Empty line for separation
        
        # Display each data section
        sections = [
            ("PRICE INFORMATION", self._get_price_data(etf)),
            ("ASSET ALLOCATIONS", self._get_asset_allocation(etf)),
            ("TOP HOLDINGS", self._get_top_holdings(etf)),
            ("SECTOR WEIGHTINGS", self._get_sector_weightings(etf)),
            ("TECHNICAL INDICATORS", self._get_technical_indicators(etf)),
            ("TRADING SIGNALS", self._get_signals(etf))
        ]
        
        for title, data in sections:
            if data:
                self.info(f"{self.RED}{title}{self.RESET}")
                # Apply color to headers if data has multiple rows
                colored_data = self._colorize_headers(data) if len(data) > 1 else data
                self.info(tabulate(colored_data, headers="firstrow" if len(data) > 1 else None, 
                                 tablefmt=self.table_format))
                self.info("")  # Empty line for separation
        
        self.info("-" * 80 + "\n")
    
    def _get_price_data(self, etf):
        """Get latest price data for the ETF."""
        latest_price = ETFPrice.objects.filter(etf=etf).order_by('-date').first()
        
        if not latest_price:
            self.warning("No price data available")
            return None
        
        return [
            ["Date", latest_price.date],
            ["Open", f"${latest_price.open:.2f}"],
            ["High", f"${latest_price.high:.2f}"],
            ["Low", f"${latest_price.low:.2f}"],
            ["Close", f"${latest_price.close:.2f}"],
            ["Volume", f"{latest_price.volume:,}"]
        ]
    
    def _get_asset_allocation(self, etf):
        """Get asset allocation data for the ETF."""
        allocations = ETFAssetAllocation.objects.filter(etf=etf).order_by('-allocation_percent')
        
        if not allocations:
            self.warning("No asset allocation data available")
            return None
        
        data = [["Allocation", "Weight"]]
        for allocation in allocations:
            data.append([
                allocation.allocation,
                f"{allocation.allocation_percent:.2f}%"
            ])
        
        return data
    
    def _get_top_holdings(self, etf):
        """Get top holdings data for the ETF."""
        holdings = ETFTopHolding.objects.filter(etf=etf).order_by('-holding_percent')
        
        if not holdings:
            self.warning("No holdings data available")
            return None
        
        data = [["Symbol", "Name", "Weight"]]
        for holding in holdings:
            # Truncate long names for better display
            name = holding.name
            if len(name) > 30:
                name = name[:27] + "..."
            
            data.append([
                holding.symbol,
                name,
                f"{holding.holding_percent:.2f}%"
            ])
        
        return data
    
    def _get_sector_weightings(self, etf):
        """Get sector weightings data for the ETF."""
        sectors = ETFSectorWeighting.objects.filter(etf=etf).order_by('-weighting_percent')
        
        if not sectors:
            self.warning("No sector weighting data available")
            return None
        
        data = [["Sector", "Weight"]]
        for sector in sectors:
            data.append([
                sector.sector,
                f"{sector.weighting_percent:.2f}%"
            ])
        
        return data

    def _get_technical_indicators(self, etf):
        """Get latest technical indicators data for the ETF."""
        latest_indicators = ETFTechnicalIndicator.objects.filter(etf=etf).order_by('-date').first()
        
        if not latest_indicators:
            self.warning("No technical indicators available")
            return None
        
        # Create data rows for indicators, grouping by type
        data = [
            ["Date", latest_indicators.date],
            ["", ""],  # Separator
            ["MOVING AVERAGES", ""],
            ["SMA (5-day)", f"${latest_indicators.sma_5:.2f}" if latest_indicators.sma_5 else "N/A"],
            ["SMA (10-day)", f"${latest_indicators.sma_10:.2f}" if latest_indicators.sma_10 else "N/A"],
            ["SMA (20-day)", f"${latest_indicators.sma_20:.2f}" if latest_indicators.sma_20 else "N/A"],
            ["SMA (50-day)", f"${latest_indicators.sma_50:.2f}" if latest_indicators.sma_50 else "N/A"],
            ["SMA (200-day)", f"${latest_indicators.sma_200:.2f}" if latest_indicators.sma_200 else "N/A"],
            ["EMA (12-day)", f"${latest_indicators.ema_12:.2f}" if latest_indicators.ema_12 else "N/A"],
            ["EMA (26-day)", f"${latest_indicators.ema_26:.2f}" if latest_indicators.ema_26 else "N/A"],
            ["", ""],  # Separator
            ["MACD", ""],
            ["MACD Line", f"{latest_indicators.macd:.4f}" if latest_indicators.macd else "N/A"],
            ["Signal Line", f"{latest_indicators.macd_signal:.4f}" if latest_indicators.macd_signal else "N/A"],
            ["Histogram", f"{latest_indicators.macd_histogram:.4f}" if latest_indicators.macd_histogram else "N/A"],
            ["", ""],  # Separator
            ["BOLLINGER BANDS", ""],
            ["Upper Band", f"${latest_indicators.bb_upper:.2f}" if latest_indicators.bb_upper else "N/A"],
            ["Middle Band", f"${latest_indicators.bb_middle:.2f}" if latest_indicators.bb_middle else "N/A"],
            ["Lower Band", f"${latest_indicators.bb_lower:.2f}" if latest_indicators.bb_lower else "N/A"],
            ["", ""],  # Separator
            ["OSCILLATORS", ""],
            ["RSI (14-day)", f"{latest_indicators.rsi_14:.2f}" if latest_indicators.rsi_14 else "N/A"],
            ["Stochastic %K", f"{latest_indicators.stoch_k:.2f}" if latest_indicators.stoch_k else "N/A"],
            ["Stochastic %D", f"{latest_indicators.stoch_d:.2f}" if latest_indicators.stoch_d else "N/A"],
            ["ATR (14-day)", f"{latest_indicators.atr_14:.4f}" if latest_indicators.atr_14 else "N/A"],
            ["", ""],  # Separator
            ["VOLUME", ""],
            ["On-Balance Volume", f"{latest_indicators.obv:,}" if latest_indicators.obv is not None else "N/A"]
        ]
        
        return data

    def _get_signals(self, etf):
        """Get latest trading signals for the ETF."""
        # Get the latest date with signals
        latest_date = ETFSignal.objects.filter(etf=etf).aggregate(latest=Max('date'))['latest']
        
        if not latest_date:
            self.warning("No trading signals available")
            return None
        
        # Get all signals from the latest date
        signals = ETFSignal.objects.filter(etf=etf, date=latest_date).order_by('-confidence')
        
        if not signals:
            return None
        
        data = [["Signal Type", "Source", "Confidence", "Description"]]
        
        for signal in signals:
            # Format the signal type with color indicators (if using color terminal)
            signal_type = signal.get_signal_type_display()
            confidence = f"{signal.confidence:.1f}%"
            
            # Truncate long descriptions
            desc = signal.description
            if len(desc) > 50:
                desc = desc[:47] + "..."
                
            data.append([
                signal_type,
                signal.get_signal_source_display(),
                confidence,
                desc
            ])
        
        return data