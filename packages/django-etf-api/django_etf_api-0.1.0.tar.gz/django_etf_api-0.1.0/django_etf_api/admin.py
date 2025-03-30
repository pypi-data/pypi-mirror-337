from django.contrib import admin
from django.utils.html import format_html
from .models import (
    ETFDetails, ETFPrice, ETFAssetAllocation, 
    ETFTopHolding, ETFSectorWeighting, 
    ETFTechnicalIndicator, ETFSignal
)


class ETFPriceInline(admin.TabularInline):
    model = ETFPrice
    extra = 0
    max_num = 5
    fields = ('date', 'open', 'high', 'low', 'close', 'volume')


class ETFTopHoldingInline(admin.TabularInline):
    model = ETFTopHolding
    extra = 0
    max_num = 10
    fields = ('symbol', 'name', 'holding_percent')


class ETFSectorWeightingInline(admin.TabularInline):
    model = ETFSectorWeighting
    extra = 0
    fields = ('sector', 'weighting_percent')


@admin.register(ETFDetails)
class ETFAdmin(admin.ModelAdmin):
    list_display = ("provider", "symbol", "name", "asset_class", "ter", "last_updated")
    list_filter = ("provider", "asset_class")
    search_fields = ("symbol", "name")
    readonly_fields = ("last_updated",)
    fieldsets = (
        ('Basic Information', {
            'fields': ('symbol', 'name', 'provider', 'asset_class')
        }),
        ('Financial Details', {
            'fields': ('total_assets', 'inception', 'ter', 'pe_ratio', 'beta', 'last_updated')
        }),
    )
    inlines = [ETFTopHoldingInline, ETFSectorWeightingInline]


@admin.register(ETFPrice)
class ETFPriceAdmin(admin.ModelAdmin):
    list_display = ("etf", "date", "display_close", "display_change", "volume")
    list_filter = ("etf__provider", "date")
    search_fields = ("etf__symbol", "etf__name")
    date_hierarchy = 'date'
    readonly_fields = ('display_change',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('etf')

    def display_close(self, obj):
        return f"${obj.close}"
    display_close.short_description = "Close Price"

    def display_change(self, obj):
        """
        Calculate and display the daily price change percentage.
        Returns formatted change with color coding: green for positive, red for negative.
        """
        try:
            # Get the previous day's price record for the same ETF
            prev_day = ETFPrice.objects.filter(
                etf=obj.etf,
                date__lt=obj.date
            ).order_by('-date').first()
            
            if not prev_day:
                return "-"
                
            # Calculate percentage change
            change_pct = ((obj.close - prev_day.close) / prev_day.close) * 100
            
            # Format with color: green for positive, red for negative
            color = "#44ff44" if change_pct >= 0 else "#ff4444"
            formatted_change = f"{change_pct:.2f}%"
            
            return format_html('<span style="color: {};">{}</span>', color, formatted_change)
        except Exception:
            return "-"
    display_change.short_description = "Daily Change"


@admin.register(ETFAssetAllocation)
class ETFAssetAllocationAdmin(admin.ModelAdmin):
    list_display = ("etf", "allocation", "formatted_percent")
    list_filter = ("etf__provider", "etf")
    search_fields = ("etf__symbol", "allocation")
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('etf')


@admin.register(ETFTopHolding)
class ETFTopHoldingAdmin(admin.ModelAdmin):
    list_display = ("etf", "symbol", "name", "formatted_percent")
    list_filter = ("etf__provider", "etf")
    search_fields = ("etf__symbol", "symbol", "name")
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('etf')


@admin.register(ETFSectorWeighting)
class ETFSectorWeightingAdmin(admin.ModelAdmin):
    list_display = ("etf", "sector", "formatted_percent")
    list_filter = ("etf__provider", "sector", "etf")
    search_fields = ("etf__symbol", "sector")
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('etf')


@admin.register(ETFTechnicalIndicator)
class ETFTechnicalIndicatorAdmin(admin.ModelAdmin):
    list_display = ("etf", "date", "sma_20", "rsi_14")
    list_filter = ("etf", "date")
    search_fields = ("etf__symbol",)
    date_hierarchy = 'date'
    fieldsets = (
        ('ETF Information', {
            'fields': ('etf', 'date')
        }),
        ('Moving Averages', {
            'classes': ('collapse',),
            'fields': ('sma_5', 'sma_10', 'sma_20', 'sma_50', 'sma_200', 'ema_12', 'ema_26'),
        }),
        ('MACD', {
            'classes': ('collapse',),
            'fields': ('macd', 'macd_signal', 'macd_histogram'),
        }),
        ('Bollinger Bands', {
            'classes': ('collapse',),
            'fields': ('bb_upper', 'bb_middle', 'bb_lower'),
        }),
        ('Oscillators', {
            'classes': ('collapse',),
            'fields': ('rsi_14', 'stoch_k', 'stoch_d', 'atr_14', 'obv'),
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('etf')


@admin.register(ETFSignal)
class ETFSignalAdmin(admin.ModelAdmin):
    list_display = ("etf", "date", "signal_type", "signal_source", "confidence_display", "has_description")
    list_filter = ("signal_type", "signal_source", "date")
    search_fields = ("etf__symbol", "etf__name", "description")
    date_hierarchy = "date"
    raw_id_fields = ("etf", "indicator")
    readonly_fields = ("confidence_display",)
    
    def confidence_display(self, obj):
        """Format confidence with percentage sign and color"""
        confidence = obj.confidence
        color = "#ff4444" if confidence < 50 else "#44ff44"
        # Format the number before passing it to format_html
        formatted_value = f"{float(confidence):.2f}%"
        return format_html('<span style="color: {};">{}</span>', color, formatted_value)
    confidence_display.short_description = "Confidence"
    confidence_display.admin_order_field = "confidence"
    
    def has_description(self, obj):
        """Check if description is present"""
        return bool(obj.description)
    has_description.boolean = True
    has_description.short_description = "Has Details"
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('etf')