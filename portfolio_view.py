# portfolio_view.py

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from asset_data import AssetData
from typing import List

def get_portfolio_df(assets: List[AssetData]) -> pd.DataFrame:
    return pd.DataFrame([{
        "Name": asset.name,
        "Symbol": asset.symbol,
        "Currency": asset.currency,
        "Shares": asset.shares,
        "Price": asset.price,
        "Fx": asset.fx_rate,
        "Value (THB)": asset.value_thb,
        "Class": asset.asset_class,
        "assumed MDD": asset.mdd,
        "MDD": asset.mdd,            #for debug table

        "Weight": asset.weight,
        
        "Rebound": asset.rebound,
        "CAGR": asset.cagr,
        "Offset Yield": asset.dividend_yield_offset,

        "Inverse MDD": asset.mdd_inverse,
        "Target in Class": asset.target_in_class,
        "Target": asset.target,
        "MDD Contribution": asset.mdd_contribution,
        
        "Drift": asset.drift,
        "%Drift": asset.drift_relative,
        "Position": asset.position_size,
    
        "52w high": asset.high_52w,
        "52w low": asset.low_52w,
        "Years low": asset.low_years,
        "52w drop": asset.drop_52w,
        "52w gain": asset.gain_52w,
        "Years gain": asset.gain_years,
        "Price Signal": asset.price_signal,
        
        "PE": asset.pe_ratio,
        "PE p25": asset.pe_p25,
        "PE p75": asset.pe_p75,
        "PE Signal": asset.pe_signal,
        
        "Yield": asset.dividend_yield,
        "Yield Signal": asset.dividend_yield_signal,
    } for asset in assets])

def show_portfolio_table(portfolio_df: pd.DataFrame):
    show_cols = ["Name", "Currency", "Shares", "Price", "Fx", "Value (THB)", "Weight"]
    format_dict = {
        "Shares": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "Price": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "Fx": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "Value (THB)": lambda x: f"{x:,.0f}" if x != 0.0 else "-",
        "Weight": lambda x: f"{x * 100:.1f}%" if x is not None else "-",
    }
    st.dataframe(portfolio_df[show_cols].style.format(format_dict))

def show_google_sheet_data_table(portfolio_df: pd.DataFrame):
    show_cols = ["Name", "Symbol", "Currency", "Shares", "Price", "Fx", "Class", "assumed MDD", "52w high", "52w low", "Years low", "PE", "PE p25", "PE p75", "Yield"]
    format_dict = {
        "Shares": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "Price": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "assumed MDD": lambda x: f"{x * 100:.0f}%" if x not in [None, 0.0] else "-",
        "Fx": lambda x: f"{x:,.2f}" if x != 0.0 else "-",
        "52w high": lambda x: f"{x:,.2f}" if x else "-",
        "52w low": lambda x: f"{x:,.2f}" if x else "-",
        "Years low": lambda x: f"{x:,.2f}" if x else "-",
        "PE": lambda x: f"{x:,.2f}" if pd.notnull(x) and x != 0.0 else "-",
        "PE p25": lambda x: f"{x:,.2f}" if pd.notnull(x) and x != 0.0 else "-",
        "PE p75": lambda x: f"{x:,.2f}" if pd.notnull(x) and x != 0.0 else "-",
        "Yield": lambda x: f"{x * 100:.2f}%" if x not in [None, 0.0] else "-",
    }
    st.dataframe(portfolio_df[show_cols].style.format(format_dict))

def show_allocation_pie_chart(portfolio_df: pd.DataFrame, total_thb: float):
    chart_df = portfolio_df[["Name", "Value (THB)"]].copy()
    chart_df["weight (%)"] = (chart_df["Value (THB)"] / total_thb * 100).round(2)
    chart_df = chart_df[chart_df["weight (%)"] >= 1]

    fig, ax = plt.subplots()
    chart_df.set_index("Name")["weight (%)"].plot.pie(
        autopct="%1.0f%%",
        figsize=(5, 5),
        ylabel="",
        ax=ax
    )
    st.pyplot(fig)
