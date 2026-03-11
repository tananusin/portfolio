# fetch_data.py
from typing import List
from asset_data import AssetData
from fetch_yfinance import get_price, get_fx_to_thb, get_52_week_high, get_52_week_low, get_trailing_pe, get_trailing_dividend_yield

def enrich_asset(asset: AssetData) -> AssetData:
    """
    Fetch price and fx_rate for an asset and compute its values.
    """
    # FX rate
    if asset.currency == 'THB':
        asset.fx_rate = 1
    else:
        asset.fx_rate = get_fx_to_thb(asset.currency)

    # Price handling
    if asset.symbol == 'CASH':
        asset.price = 1
    elif asset.symbol == 'BOND':
        pass  # Use user-assigned value
    elif asset.symbol == 'FUNDTH':
        pass  # Use user-assigned value
    else:
        asset.price = get_price(asset.symbol)
        asset.high_52w = get_52_week_high(asset.symbol)
        asset.low_52w = get_52_week_low(asset.symbol)
        asset.pe_ratio = get_trailing_pe(asset.symbol)
        asset.dividend_yield = get_trailing_dividend_yield(asset.symbol)

    return asset


def assign_weights(assets: List[AssetData], total_value: float):
    for asset in assets:
        if asset.value_thb is not None and total_value > 0:
            asset.weight = asset.value_thb / total_value
