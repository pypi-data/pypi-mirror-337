"""
Financial ratio analysis module for XBRL data.

This module provides a comprehensive set of financial ratio calculations
for analyzing company performance, efficiency, and financial health.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
import pandas as pd

@dataclass
class RatioResult:
    """Container for ratio calculation results with metadata."""
    value: float
    components: Dict[str, float]
    period: str
    
    def __repr__(self) -> str:
        return f"{self.value:.2f} ({self.period})"

class FinancialRatios:
    """Calculate and analyze financial ratios from XBRL data."""
    
    def __init__(self, xbrl):
        """Initialize with an XBRL instance."""
        self.xbrl = xbrl
        self._balance_sheet = None
        self._income_stmt = None
        self._cash_flow = None
        
    def _get_value(self, concept: str, statement_type: str = "BalanceSheet") -> Optional[float]:
        """Safely extract a numeric value for a concept."""
        try:
            df = self.xbrl.to_dataframe(statement_type)
            value = df[df['concept'] == concept]['value'].iloc[0]
            return float(value) if pd.notnull(value) else None
        except (KeyError, IndexError, ValueError):
            return None
            
    def liquidity_ratios(self) -> Dict[str, RatioResult]:
        """Calculate liquidity ratios.
        
        Returns:
            Dict containing:
            - current_ratio
            - quick_ratio
            - cash_ratio
            - working_capital
        """
        current_assets = self._get_value("us-gaap_AssetsCurrent")
        current_liab = self._get_value("us-gaap_LiabilitiesCurrent")
        cash = self._get_value("us-gaap_CashAndCashEquivalentsAtCarryingValue")
        inventory = self._get_value("us-gaap_InventoryNet")
        receivables = self._get_value("us-gaap_AccountsReceivableNetCurrent")
        
        if not all([current_assets, current_liab]):
            return {}
            
        period = self.xbrl.reporting_periods()[0]
        
        results = {}
        
        # Current Ratio
        assert current_assets is not None and current_liab is not None  # Help type checker
        results['current_ratio'] = RatioResult(
            value=current_assets / current_liab,
            components={
                'current_assets': current_assets,
                'current_liabilities': current_liab
            },
            period=period
        )
        
        # Quick Ratio
        if all([inventory, receivables]):
            assert inventory is not None  # Help type checker
            quick_assets = current_assets - inventory
            assert current_liab is not None  # Help type checker
            results['quick_ratio'] = RatioResult(
                value=quick_assets / current_liab,
                components={
                    'quick_assets': quick_assets,
                    'current_liabilities': current_liab
                },
                period=period
            )
            
        # Cash Ratio
        if cash:
            assert cash is not None  # Help type checker
            assert current_liab is not None  # Help type checker
            results['cash_ratio'] = RatioResult(
                value=cash / current_liab,
                components={
                    'cash': cash,
                    'current_liabilities': current_liab
                },
                period=period
            )
            
        # Working Capital
        assert current_assets is not None and current_liab is not None  # Help type checker
        results['working_capital'] = RatioResult(
            value=current_assets - current_liab,
            components={
                'current_assets': current_assets,
                'current_liabilities': current_liab
            },
            period=period
        )
        
        return results
        
    def profitability_ratios(self) -> Dict[str, RatioResult]:
        """Calculate profitability ratios.
        
        Returns:
            Dict containing:
            - gross_margin
            - operating_margin
            - net_margin
            - return_on_assets
            - return_on_equity
        """
        revenue = self._get_value("us-gaap_Revenues", "IncomeStatement")
        gross_profit = self._get_value("us-gaap_GrossProfit", "IncomeStatement")
        operating_income = self._get_value("us-gaap_OperatingIncomeLoss", "IncomeStatement")
        net_income = self._get_value("us-gaap_NetIncomeLoss", "IncomeStatement")
        total_assets = self._get_value("us-gaap_Assets")
        total_equity = self._get_value("us-gaap_StockholdersEquity")
        
        if not revenue:
            return {}
            
        period = self.xbrl.reporting_periods()[0]
        results = {}
        
        # Margin Ratios
        if gross_profit:
            assert gross_profit is not None and revenue is not None  # Help type checker
            results['gross_margin'] = RatioResult(
                value=gross_profit / revenue,
                components={
                    'gross_profit': gross_profit,
                    'revenue': revenue
                },
                period=period
            )
            
        if operating_income:
            assert operating_income is not None and revenue is not None  # Help type checker
            results['operating_margin'] = RatioResult(
                value=operating_income / revenue,
                components={
                    'operating_income': operating_income,
                    'revenue': revenue
                },
                period=period
            )
            
        if net_income:
            assert net_income is not None and revenue is not None  # Help type checker
            results['net_margin'] = RatioResult(
                value=net_income / revenue,
                components={
                    'net_income': net_income,
                    'revenue': revenue
                },
                period=period
            )
            
        # Return Ratios
        if all([net_income, total_assets]):
            assert net_income is not None and total_assets is not None  # Help type checker
            results['return_on_assets'] = RatioResult(
                value=net_income / total_assets,
                components={
                    'net_income': net_income,
                    'total_assets': total_assets
                },
                period=period
            )
            
        if all([net_income, total_equity]):
            assert net_income is not None and total_equity is not None  # Help type checker
            results['return_on_equity'] = RatioResult(
                value=net_income / total_equity,
                components={
                    'net_income': net_income,
                    'total_equity': total_equity
                },
                period=period
            )
            
        return results
        
    def efficiency_ratios(self) -> Dict[str, RatioResult]:
        """Calculate efficiency ratios.
        
        Returns:
            Dict containing:
            - asset_turnover
            - inventory_turnover
            - receivables_turnover
            - days_sales_outstanding
        """
        revenue = self._get_value("us-gaap_Revenues", "IncomeStatement")
        total_assets = self._get_value("us-gaap_Assets")
        inventory = self._get_value("us-gaap_InventoryNet")
        cogs = self._get_value("us-gaap_CostOfGoodsAndServicesSold", "IncomeStatement")
        receivables = self._get_value("us-gaap_AccountsReceivableNetCurrent")
        
        period = self.xbrl.reporting_periods()[0]
        results = {}
        
        # Asset Turnover
        if all([revenue, total_assets]):
            assert revenue is not None and total_assets is not None  # Help type checker
            results['asset_turnover'] = RatioResult(
                value=revenue / total_assets,
                components={
                    'revenue': revenue,
                    'total_assets': total_assets
                },
                period=period
            )
            
        # Inventory Turnover
        if all([cogs, inventory]):
            assert cogs is not None and inventory is not None  # Help type checker
            results['inventory_turnover'] = RatioResult(
                value=cogs / inventory,
                components={
                    'cogs': cogs,
                    'inventory': inventory
                },
                period=period
            )
            
        # Receivables Turnover
        if all([revenue, receivables]):
            assert revenue is not None and receivables is not None  # Help type checker
            turnover = revenue / receivables
            results['receivables_turnover'] = RatioResult(
                value=turnover,
                components={
                    'revenue': revenue,
                    'receivables': receivables
                },
                period=period
            )
            
            # Days Sales Outstanding
            assert turnover is not None  # Help type checker
            results['days_sales_outstanding'] = RatioResult(
                value=365 / turnover,
                components={
                    'receivables_turnover': turnover
                },
                period=period
            )
            
        return results
        
    def leverage_ratios(self) -> Dict[str, RatioResult]:
        """Calculate leverage ratios.
        
        Returns:
            Dict containing:
            - debt_to_equity
            - debt_to_assets
            - interest_coverage
            - equity_multiplier
        """
        total_debt = self._get_value("us-gaap_LongTermDebtNoncurrent")
        total_equity = self._get_value("us-gaap_StockholdersEquity")
        total_assets = self._get_value("us-gaap_Assets")
        operating_income = self._get_value("us-gaap_OperatingIncomeLoss", "IncomeStatement")
        interest_expense = self._get_value("us-gaap_InterestExpense", "IncomeStatement")
        
        period = self.xbrl.reporting_periods()[0]
        results = {}
        
        # Debt to Equity
        if all([total_debt, total_equity]):
            assert total_debt is not None and total_equity is not None  # Help type checker
            results['debt_to_equity'] = RatioResult(
                value=total_debt / total_equity,
                components={
                    'total_debt': total_debt,
                    'total_equity': total_equity
                },
                period=period
            )
            
        # Debt to Assets
        if all([total_debt, total_assets]):
            assert total_debt is not None and total_assets is not None  # Help type checker
            results['debt_to_assets'] = RatioResult(
                value=total_debt / total_assets,
                components={
                    'total_debt': total_debt,
                    'total_assets': total_assets
                },
                period=period
            )
            
        # Interest Coverage
        if all([operating_income, interest_expense]) and interest_expense != 0:
            assert operating_income is not None and interest_expense is not None  # Help type checker
            results['interest_coverage'] = RatioResult(
                value=operating_income / interest_expense,
                components={
                    'operating_income': operating_income,
                    'interest_expense': interest_expense
                },
                period=period
            )
            
        # Equity Multiplier
        if all([total_assets, total_equity]):
            assert total_assets is not None and total_equity is not None  # Help type checker
            results['equity_multiplier'] = RatioResult(
                value=total_assets / total_equity,
                components={
                    'total_assets': total_assets,
                    'total_equity': total_equity
                },
                period=period
            )
            
        return results
        
    def calculate_all(self) -> Dict[str, Dict[str, RatioResult]]:
        """Calculate all available financial ratios."""
        return {
            'liquidity': self.liquidity_ratios(),
            'profitability': self.profitability_ratios(),
            'efficiency': self.efficiency_ratios(),
            'leverage': self.leverage_ratios()
        }