#!/usr/bin/env python3
"""Author the deterministic Daloopa fixture catalog (widgets plus baked data).

The Bench Daloopa fixture mirrors the data surface consumed by the Daloopa
Claude plugin skills (https://github.com/daloopa/daloopa-plugin-claude):
company discovery, series discovery, fundamentals with per-datapoint citation
ids, operating KPIs, segment breakdowns, management guidance, consensus
estimates, SEC document search, and daily stock prices. Unlike the Stark
catalog (imported from a demo repo, then baked), Daloopa has no widgets.json
source, so this script authors the catalog and bakes the data in one pass.
"""

from __future__ import annotations

import json
import random
from datetime import date, timedelta
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[2]
DEFAULT_DATA_PATH = REPO / "src/workspace_bench/workspace/data/daloopa.json"

SEED_PREFIX = "daloopa-v1"
LATEST_CALENDAR_QUARTER = "2026Q1"
INTERNAL_QUARTERS = 12  # 4 warm-up quarters so YoY exists for every published one
PUBLISHED_QUARTERS = 8
DOC_ID_OFFSET = 500

FINANCIAL_SERIES = [
    ("total_revenue", "Total Revenue", "Income Statement", "USD mn"),
    ("gross_profit", "Gross Profit", "Income Statement", "USD mn"),
    ("operating_income", "Operating Income", "Income Statement", "USD mn"),
    ("depreciation_amortization", "Depreciation & Amortization", "Income Statement", "USD mn"),
    ("net_income", "Net Income", "Income Statement", "USD mn"),
    ("diluted_eps", "Diluted EPS", "Income Statement", "USD"),
    ("diluted_shares", "Diluted Weighted Average Shares", "Income Statement", "shares mn"),
    ("cash_and_equivalents", "Cash & Equivalents", "Balance Sheet", "USD mn"),
    ("total_debt", "Total Debt", "Balance Sheet", "USD mn"),
    ("operating_cash_flow", "Operating Cash Flow", "Cash Flow", "USD mn"),
    ("capital_expenditures", "Capital Expenditures", "Cash Flow", "USD mn"),
    ("free_cash_flow", "Free Cash Flow", "Cash Flow", "USD mn"),
    ("share_buybacks", "Share Buybacks", "Cash Flow", "USD mn"),
    ("dividends_paid", "Dividends Paid", "Cash Flow", "USD mn"),
]

GUIDED_FINANCIAL_SERIES = ["total_revenue", "diluted_eps"]

JsonDict = dict[str, Any]

COMPANIES: list[JsonDict] = [
    {
        "ticker": "AAPL",
        "company_id": 2001,
        "name": "Apple Inc.",
        "sector": "Consumer Technology",
        "fy_end_month": 9,
        "revenue_base_musd": 94_900.0,
        "growth_per_quarter": 0.012,
        "seasonal": [0.94, 0.88, 0.93, 1.25],
        "gross_margin": 0.465,
        "operating_margin": 0.317,
        "da_ratio": 0.028,
        "capex_ratio": 0.026,
        "shares_mn": 15_300.0,
        "cash_base_musd": 62_000.0,
        "debt_base_musd": 97_000.0,
        "buyback_ratio": 0.95,
        "dividend_ratio": 0.16,
        "price_base": 232.0,
        "volume_base": 48_000_000,
        "kpis": [
            ("installed_base_devices", "Installed Base Active Devices", "mn", 2_300.0, 0.012),
            ("paid_subscriptions", "Paid Subscriptions", "mn", 1_050.0, 0.02),
        ],
        "segments": [
            ("iPhone", 0.51),
            ("Services", 0.25),
            ("Wearables, Home & Accessories", 0.09),
            ("Mac", 0.08),
            ("iPad", 0.07),
        ],
    },
    {
        "ticker": "MSFT",
        "company_id": 2002,
        "name": "Microsoft Corporation",
        "sector": "Software & Cloud",
        "fy_end_month": 6,
        "revenue_base_musd": 68_500.0,
        "growth_per_quarter": 0.028,
        "seasonal": [1.0, 0.98, 1.01, 1.06],
        "gross_margin": 0.69,
        "operating_margin": 0.45,
        "da_ratio": 0.065,
        "capex_ratio": 0.19,
        "shares_mn": 7_440.0,
        "cash_base_musd": 78_000.0,
        "debt_base_musd": 45_000.0,
        "buyback_ratio": 0.55,
        "dividend_ratio": 0.38,
        "price_base": 505.0,
        "volume_base": 22_000_000,
        "kpis": [
            ("azure_revenue_growth", "Azure Revenue Growth", "%", 29.0, 0.02),
            ("commercial_rpo", "Commercial RPO", "USD bn", 290.0, 0.03),
        ],
        "segments": [
            ("Intelligent Cloud", 0.43),
            ("Productivity & Business Processes", 0.32),
            ("More Personal Computing", 0.25),
        ],
    },
    {
        "ticker": "NVDA",
        "company_id": 2003,
        "name": "NVIDIA Corporation",
        "sector": "Semiconductors",
        "fy_end_month": 1,
        "revenue_base_musd": 39_300.0,
        "growth_per_quarter": 0.06,
        "seasonal": [1.0, 1.0, 1.0, 1.0],
        "gross_margin": 0.74,
        "operating_margin": 0.61,
        "da_ratio": 0.015,
        "capex_ratio": 0.03,
        "shares_mn": 24_600.0,
        "cash_base_musd": 43_000.0,
        "debt_base_musd": 8_500.0,
        "buyback_ratio": 0.6,
        "dividend_ratio": 0.01,
        "price_base": 172.0,
        "volume_base": 240_000_000,
        "kpis": [
            ("networking_revenue", "Networking Revenue", "USD mn", 4_800.0, 0.05),
            ("supply_committed_backlog", "Supply-Committed Backlog", "USD bn", 55.0, 0.04),
        ],
        "segments": [
            ("Data Center", 0.87),
            ("Gaming", 0.08),
            ("Professional Visualization", 0.03),
            ("Automotive", 0.02),
        ],
    },
    {
        "ticker": "NFLX",
        "company_id": 2004,
        "name": "Netflix, Inc.",
        "sector": "Media & Entertainment",
        "fy_end_month": 12,
        "revenue_base_musd": 10_500.0,
        "growth_per_quarter": 0.03,
        "seasonal": [0.99, 1.0, 1.01, 1.03],
        "gross_margin": 0.46,
        "operating_margin": 0.27,
        "da_ratio": 0.035,
        "capex_ratio": 0.035,
        "shares_mn": 432.0,
        "cash_base_musd": 7_200.0,
        "debt_base_musd": 14_500.0,
        "buyback_ratio": 0.55,
        "dividend_ratio": 0.0,
        "price_base": 1_220.0,
        "volume_base": 3_400_000,
        "kpis": [
            ("paid_memberships", "Paid Memberships", "mn", 315.0, 0.015),
            ("global_arpu", "Global ARPU", "USD", 12.4, 0.008),
        ],
        "segments": [
            ("UCAN", 0.44),
            ("EMEA", 0.32),
            ("LATAM", 0.12),
            ("APAC", 0.12),
        ],
    },
    {
        "ticker": "TSLA",
        "company_id": 2005,
        "name": "Tesla, Inc.",
        "sector": "Automotive & Energy",
        "fy_end_month": 12,
        "revenue_base_musd": 25_200.0,
        "growth_per_quarter": 0.015,
        "seasonal": [0.92, 0.99, 1.02, 1.1],
        "gross_margin": 0.18,
        "operating_margin": 0.08,
        "da_ratio": 0.05,
        "capex_ratio": 0.09,
        "shares_mn": 3_480.0,
        "cash_base_musd": 33_000.0,
        "debt_base_musd": 7_800.0,
        "buyback_ratio": 0.0,
        "dividend_ratio": 0.0,
        "price_base": 315.0,
        "volume_base": 95_000_000,
        "kpis": [
            ("vehicle_deliveries", "Vehicle Deliveries", "units k", 465.0, 0.02),
            ("energy_storage_deployed", "Energy Storage Deployed", "GWh", 11.5, 0.06),
        ],
        "segments": [
            ("Automotive", 0.79),
            ("Energy Generation & Storage", 0.12),
            ("Services & Other", 0.09),
        ],
    },
    {
        "ticker": "AMZN",
        "company_id": 2006,
        "name": "Amazon.com, Inc.",
        "sector": "E-Commerce & Cloud",
        "fy_end_month": 12,
        "revenue_base_musd": 158_000.0,
        "growth_per_quarter": 0.025,
        "seasonal": [0.92, 0.95, 0.97, 1.18],
        "gross_margin": 0.49,
        "operating_margin": 0.11,
        "da_ratio": 0.08,
        "capex_ratio": 0.16,
        "shares_mn": 10_500.0,
        "cash_base_musd": 82_000.0,
        "debt_base_musd": 130_000.0,
        "buyback_ratio": 0.1,
        "dividend_ratio": 0.0,
        "price_base": 226.0,
        "volume_base": 41_000_000,
        "kpis": [
            ("aws_revenue_growth", "AWS Revenue Growth", "%", 19.0, 0.02),
            ("paid_units_growth", "Paid Units Growth", "%", 11.0, 0.02),
        ],
        "segments": [
            ("North America", 0.61),
            ("International", 0.22),
            ("AWS", 0.17),
        ],
    },
]


def _rng(*key_parts: Any) -> random.Random:
    return random.Random(":".join([SEED_PREFIX, *[str(part) for part in key_parts]]))


def quarter_add(quarter: str, count: int) -> str:
    year, index = int(quarter[:4]), int(quarter[5:])
    total = year * 4 + (index - 1) + count
    return f"{total // 4}Q{total % 4 + 1}"


def quarter_sequence(last: str, count: int) -> list[str]:
    return [quarter_add(last, offset) for offset in range(1 - count, 1)]


def quarter_end(quarter: str) -> date:
    year, index = int(quarter[:4]), int(quarter[5:])
    month = index * 3
    next_month = date(year + (month == 12), month % 12 + 1, 1)
    return next_month - timedelta(days=1)


def quarter_end_business_day(quarter: str) -> date:
    day = quarter_end(quarter)
    while day.weekday() >= 5:
        day -= timedelta(days=1)
    return day


def fiscal_period(quarter: str, fy_end_month: int) -> str:
    """Map a calendar quarter to the company's FQx'YY fiscal label."""

    year, index = int(quarter[:4]), int(quarter[5:])
    end_month = index * 3
    fy_start_month = fy_end_month % 12 + 1
    fiscal_quarter = ((end_month - fy_start_month) % 12) // 3 + 1
    fiscal_year = year + (1 if end_month > fy_end_month else 0)
    return f"FQ{fiscal_quarter}'{fiscal_year % 100:02d}"


INTERNAL_PERIODS = quarter_sequence(LATEST_CALENDAR_QUARTER, INTERNAL_QUARTERS)
PUBLISHED_PERIODS = INTERNAL_PERIODS[-PUBLISHED_QUARTERS:]
GUIDANCE_PERIODS = PUBLISHED_PERIODS + [quarter_add(LATEST_CALENDAR_QUARTER, 1)]
RECENT_TRADING_DAYS = [date(2026, 7, 6) + timedelta(days=offset) for offset in range(5)]


def _series_catalog(company: JsonDict) -> list[JsonDict]:
    """Ordered series metadata for one company; order fixes series ids."""

    entries: list[JsonDict] = []
    for slug, name, category, unit in FINANCIAL_SERIES:
        entries.append({"slug": slug, "series": name, "category": category, "unit": unit})
    for slug, name, unit, _base, _drift in company["kpis"]:
        entries.append({"slug": slug, "series": name, "category": "KPI", "unit": unit})
    for segment, _share in company["segments"]:
        entries.append(
            {
                "slug": f"segment_{segment.lower().replace(' ', '_').replace(',', '').replace('&', 'and')}",
                "series": f"Revenue — {segment}",
                "category": "Segment",
                "unit": "USD mn",
            }
        )
    for slug in GUIDED_FINANCIAL_SERIES + [company["kpis"][0][0]]:
        base = next(entry for entry in entries if entry["slug"] == slug)
        entries.append(
            {
                "slug": f"{slug}_guidance",
                "series": f"{base['series']} Guidance",
                "category": "Guidance",
                "unit": base["unit"],
            }
        )
    for ordinal, entry in enumerate(entries, start=1):
        entry["series_id"] = company["company_id"] * 1000 + ordinal
    return entries


def _series_id(catalog: list[JsonDict], slug: str) -> int:
    return next(entry["series_id"] for entry in catalog if entry["slug"] == slug)


def _financial_model(company: JsonDict) -> dict[str, list[float]]:
    """Internally consistent quarterly financials over INTERNAL_PERIODS."""

    ticker = company["ticker"]
    values: dict[str, list[float]] = {slug: [] for slug, *_ in FINANCIAL_SERIES}
    cash = company["cash_base_musd"]
    debt = company["debt_base_musd"]
    for index, quarter in enumerate(INTERNAL_PERIODS):
        rng = _rng(ticker, "financials", quarter)
        season = company["seasonal"][int(quarter[5:]) - 1]
        revenue = (
            company["revenue_base_musd"]
            * season
            * (1 + company["growth_per_quarter"]) ** index
            * rng.uniform(0.985, 1.015)
        )
        gross = revenue * company["gross_margin"] * rng.uniform(0.99, 1.01)
        operating = revenue * company["operating_margin"] * rng.uniform(0.97, 1.03)
        d_and_a = revenue * company["da_ratio"] * rng.uniform(0.97, 1.03)
        net = operating * rng.uniform(0.80, 0.86)
        shares = company["shares_mn"] * (1 - 0.003 * index)
        ocf = (net + d_and_a) * rng.uniform(0.95, 1.1)
        capex = revenue * company["capex_ratio"] * rng.uniform(0.9, 1.1)
        cash *= 1 + rng.uniform(-0.04, 0.05)
        debt *= 1 + rng.uniform(-0.02, 0.02)
        buybacks = net * company["buyback_ratio"] * rng.uniform(0.8, 1.2)
        dividends = net * company["dividend_ratio"] * rng.uniform(0.95, 1.05)

        ocf_rounded = round(ocf, 1)
        capex_rounded = round(capex, 1)
        values["total_revenue"].append(round(revenue, 1))
        values["gross_profit"].append(round(gross, 1))
        values["operating_income"].append(round(operating, 1))
        values["depreciation_amortization"].append(round(d_and_a, 1))
        values["net_income"].append(round(net, 1))
        values["diluted_eps"].append(round(net / shares, 2))
        values["diluted_shares"].append(round(shares, 1))
        values["cash_and_equivalents"].append(round(cash, 1))
        values["total_debt"].append(round(debt, 1))
        values["operating_cash_flow"].append(ocf_rounded)
        values["capital_expenditures"].append(capex_rounded)
        values["free_cash_flow"].append(round(ocf_rounded - capex_rounded, 1))
        values["share_buybacks"].append(round(buybacks, 1))
        values["dividends_paid"].append(round(dividends, 1))
    return values


def _kpi_model(company: JsonDict) -> dict[str, list[float]]:
    values: dict[str, list[float]] = {}
    for slug, _name, _unit, base, drift in company["kpis"]:
        series: list[float] = []
        current = base
        for quarter in INTERNAL_PERIODS:
            rng = _rng(company["ticker"], "kpi", slug, quarter)
            current *= 1 + rng.uniform(-drift / 2, drift)
            series.append(round(current, 1))
        values[slug] = series
    return values


def _segment_model(company: JsonDict, revenue: list[float]) -> dict[str, list[float]]:
    values: dict[str, list[float]] = {}
    for segment, share in company["segments"]:
        series = []
        for index, quarter in enumerate(INTERNAL_PERIODS):
            rng = _rng(company["ticker"], "segment", segment, quarter)
            series.append(round(revenue[index] * share * rng.uniform(0.96, 1.04), 1))
        values[segment] = series
    return values


def _citation(fundamental_id: int) -> str:
    return f"https://daloopa.com/src/{fundamental_id}"


def _fundamental_id(series_id: int, period_index: int) -> int:
    return series_id * 100 + period_index


def _company_directory_rows() -> list[JsonDict]:
    return [
        {
            "company_id": company["company_id"],
            "ticker": company["ticker"],
            "name": company["name"],
            "sector": company["sector"],
            "fiscal_year_end": date(2000, company["fy_end_month"], 1).strftime("%B"),
            "latest_calendar_quarter": LATEST_CALENDAR_QUARTER,
            "latest_fiscal_quarter": fiscal_period(
                LATEST_CALENDAR_QUARTER, company["fy_end_month"]
            ),
        }
        for company in COMPANIES
    ]


def _series_directory_rows() -> list[JsonDict]:
    rows = []
    for company in COMPANIES:
        for entry in _series_catalog(company):
            rows.append(
                {
                    "ticker": company["ticker"],
                    "series_id": entry["series_id"],
                    "series": entry["series"],
                    "category": entry["category"],
                    "unit": entry["unit"],
                }
            )
    return rows


def _fundamentals_rows() -> list[JsonDict]:
    rows = []
    for company in COMPANIES:
        catalog = _series_catalog(company)
        model = _financial_model(company)
        for slug, name, _category, unit in FINANCIAL_SERIES:
            series_id = _series_id(catalog, slug)
            for period_index, quarter in enumerate(PUBLISHED_PERIODS):
                internal_index = INTERNAL_PERIODS.index(quarter)
                fundamental_id = _fundamental_id(series_id, period_index)
                rows.append(
                    {
                        "fundamental_id": fundamental_id,
                        "ticker": company["ticker"],
                        "series_id": series_id,
                        "series": name,
                        "calendar_period": quarter,
                        "fiscal_period": fiscal_period(quarter, company["fy_end_month"]),
                        "value": model[slug][internal_index],
                        "unit": unit,
                        "source_url": _citation(fundamental_id),
                    }
                )
    return rows


def _kpi_rows() -> list[JsonDict]:
    rows = []
    for company in COMPANIES:
        catalog = _series_catalog(company)
        model = _kpi_model(company)
        for slug, name, unit, _base, _drift in company["kpis"]:
            series_id = _series_id(catalog, slug)
            for period_index, quarter in enumerate(PUBLISHED_PERIODS):
                internal_index = INTERNAL_PERIODS.index(quarter)
                fundamental_id = _fundamental_id(series_id, period_index)
                rows.append(
                    {
                        "fundamental_id": fundamental_id,
                        "ticker": company["ticker"],
                        "series_id": series_id,
                        "series": name,
                        "calendar_period": quarter,
                        "fiscal_period": fiscal_period(quarter, company["fy_end_month"]),
                        "value": model[slug][internal_index],
                        "unit": unit,
                        "source_url": _citation(fundamental_id),
                    }
                )
    return rows


def _segment_rows() -> list[JsonDict]:
    rows = []
    for company in COMPANIES:
        catalog = _series_catalog(company)
        revenue = _financial_model(company)["total_revenue"]
        segments = _segment_model(company, revenue)
        for segment, _share in company["segments"]:
            slug = next(
                entry["slug"]
                for entry in catalog
                if entry["category"] == "Segment" and entry["series"].endswith(segment)
            )
            series_id = _series_id(catalog, slug)
            for period_index, quarter in enumerate(PUBLISHED_PERIODS):
                internal_index = INTERNAL_PERIODS.index(quarter)
                fundamental_id = _fundamental_id(series_id, period_index)
                current = segments[segment][internal_index]
                year_ago = segments[segment][internal_index - 4]
                rows.append(
                    {
                        "fundamental_id": fundamental_id,
                        "ticker": company["ticker"],
                        "segment": segment,
                        "calendar_period": quarter,
                        "fiscal_period": fiscal_period(quarter, company["fy_end_month"]),
                        "revenue_musd": current,
                        "yoy_growth": round(current / year_ago - 1, 4),
                        "source_url": _citation(fundamental_id),
                    }
                )
    return rows


def _guidance_rows() -> list[JsonDict]:
    rows = []
    for company in COMPANIES:
        catalog = _series_catalog(company)
        financials = _financial_model(company)
        kpis = _kpi_model(company)
        guided = [
            (slug, financials.get(slug) or kpis[slug])
            for slug in GUIDED_FINANCIAL_SERIES + [company["kpis"][0][0]]
        ]
        for slug, actuals in guided:
            guidance_slug = f"{slug}_guidance"
            series_id = _series_id(catalog, guidance_slug)
            base_entry = next(entry for entry in catalog if entry["slug"] == slug)
            decimals = 2 if base_entry["unit"] == "USD" else 1
            for period_index, quarter in enumerate(GUIDANCE_PERIODS):
                rng = _rng(company["ticker"], "guidance", slug, quarter)
                if quarter in INTERNAL_PERIODS:
                    actual = actuals[INTERNAL_PERIODS.index(quarter)]
                    mid = actual * rng.uniform(0.97, 1.03)
                else:
                    actual = None
                    mid = actuals[-1] * rng.uniform(1.0, 1.04)
                low = round(mid * 0.985, decimals)
                high = round(mid * 1.015, decimals)
                if actual is None:
                    verdict = "Pending"
                elif actual > high:
                    verdict = "Beat"
                elif actual < low:
                    verdict = "Missed"
                else:
                    verdict = "In Line"
                fundamental_id = _fundamental_id(series_id, period_index)
                rows.append(
                    {
                        "fundamental_id": fundamental_id,
                        "ticker": company["ticker"],
                        "series": next(
                            entry["series"] for entry in catalog if entry["slug"] == guidance_slug
                        ),
                        "calendar_period": quarter,
                        "guidance_low": low,
                        "guidance_high": high,
                        "actual": actual,
                        "unit": base_entry["unit"],
                        "verdict": verdict,
                        "source_url": _citation(fundamental_id),
                    }
                )
    return rows


def _consensus_rows() -> list[JsonDict]:
    rows = []
    for company in COMPANIES:
        financials = _financial_model(company)
        for slug, name in [("total_revenue", "Total Revenue"), ("diluted_eps", "Diluted EPS")]:
            decimals = 2 if slug == "diluted_eps" else 1
            for quarter in PUBLISHED_PERIODS:
                rng = _rng(company["ticker"], "consensus", slug, quarter)
                actual = financials[slug][INTERNAL_PERIODS.index(quarter)]
                consensus = round(actual * rng.uniform(0.96, 1.02), decimals)
                rows.append(
                    {
                        "ticker": company["ticker"],
                        "series": name,
                        "calendar_period": quarter,
                        "consensus": consensus,
                        "actual": actual,
                        "surprise_pct": round(actual / consensus - 1, 4),
                        "unit": "USD" if slug == "diluted_eps" else "USD mn",
                    }
                )
    return rows


def _document_rows() -> list[JsonDict]:
    rows = []
    for company in COMPANIES:
        sequence = 0
        for quarter in PUBLISHED_PERIODS:
            fiscal = fiscal_period(quarter, company["fy_end_month"])
            filings = [
                ("10-K" if fiscal.startswith("FQ4") else "10-Q", "Form"),
                ("Earnings Call Transcript", "Transcript"),
            ]
            if quarter in PUBLISHED_PERIODS[-2:]:
                filings.append(("8-K", "Form"))
            for doc_type, flavor in filings:
                rng = _rng(company["ticker"], "document", doc_type, quarter)
                sequence += 1
                document_id = company["company_id"] * 1000 + DOC_ID_OFFSET + sequence
                lag = rng.randint(20, 30) if flavor == "Transcript" else rng.randint(25, 40)
                filing_date = quarter_end(quarter) + timedelta(days=lag)
                if flavor == "Transcript":
                    title = f"{company['name']} {fiscal} Earnings Call Transcript"
                else:
                    title = f"{company['name']} Form {doc_type} — {fiscal}"
                rows.append(
                    {
                        "document_id": document_id,
                        "ticker": company["ticker"],
                        "title": title,
                        "doc_type": doc_type,
                        "calendar_period": quarter,
                        "filing_date": filing_date.isoformat(),
                        "url": f"https://marketplace.daloopa.com/document/{document_id}",
                    }
                )
    return rows


def _stock_price_rows() -> list[JsonDict]:
    rows = []
    for company in COMPANIES:
        dates = [quarter_end_business_day(quarter) for quarter in PUBLISHED_PERIODS]
        dates += RECENT_TRADING_DAYS
        close = company["price_base"]
        for index, day in enumerate(dates):
            rng = _rng(company["ticker"], "price", day.isoformat())
            step = (
                rng.uniform(-0.015, 0.02)
                if index >= PUBLISHED_QUARTERS
                else rng.uniform(-0.06, 0.08)
            )
            previous = close
            close = previous * (1 + step)
            open_price = previous * (1 + rng.uniform(-0.01, 0.01))
            high = max(open_price, close) * (1 + rng.uniform(0.0, 0.015))
            low = min(open_price, close) * (1 - rng.uniform(0.0, 0.015))
            rows.append(
                {
                    "ticker": company["ticker"],
                    "date": day.isoformat(),
                    "open": round(open_price, 2),
                    "high": round(high, 2),
                    "low": round(low, 2),
                    "close": round(close, 2),
                    "volume": rng.randint(
                        int(company["volume_base"] * 0.6), int(company["volume_base"] * 1.5)
                    ),
                }
            )
    return rows


def _coverage_note() -> str:
    tickers = ", ".join(company["ticker"] for company in COMPANIES)
    return (
        "## Daloopa Coverage & Citation Policy\n\n"
        f"This fixture covers {len(COMPANIES)} companies ({tickers}) across "
        f"{PUBLISHED_QUARTERS} calendar quarters ending {LATEST_CALENDAR_QUARTER}. "
        "It mirrors the data surface used by the Daloopa Claude plugin skills: "
        "company discovery, series discovery, fundamentals, KPIs, segments, "
        "guidance, consensus, documents, and stock prices.\n\n"
        "Every Daloopa-sourced figure carries a `fundamental_id` and citation of "
        "the form `https://daloopa.com/src/{fundamental_id}`; documents link to "
        "`https://marketplace.daloopa.com/document/{document_id}`. Reports are "
        'attributed to the firm name "Daloopa" unless the user supplies one. '
        "Anchor period math on `latest_calendar_quarter`, never the wall clock."
    )


def _table_schema(fields: list[tuple[str, str, str]]) -> JsonDict:
    return {
        "table": {
            "columnsDefs": [
                {"field": field, "headerName": header, "cellDataType": kind}
                for field, header, kind in fields
            ]
        }
    }


def _ticker_param() -> JsonDict:
    return {
        "paramName": "ticker",
        "type": "text",
        "label": "Ticker",
        "description": "Covered company ticker.",
        "value": "AAPL",
        "options": [
            {"label": f"{company['name']} ({company['ticker']})", "value": company["ticker"]}
            for company in COMPANIES
        ],
    }


def _period_param() -> JsonDict:
    return {
        "paramName": "period",
        "type": "text",
        "label": "Calendar Quarter",
        "description": "Calendar quarter; fiscal labels are returned per row.",
        "value": LATEST_CALENDAR_QUARTER,
        "options": [{"label": quarter, "value": quarter} for quarter in PUBLISHED_PERIODS],
    }


def _doc_type_param() -> JsonDict:
    return {
        "paramName": "doc_type",
        "type": "text",
        "label": "Document Type",
        "description": "SEC filing or transcript type.",
        "value": "10-Q",
        "options": [
            {"label": value, "value": value}
            for value in ["10-K", "10-Q", "8-K", "Earnings Call Transcript"]
        ],
    }


def _category_param() -> JsonDict:
    return {
        "paramName": "category",
        "type": "text",
        "label": "Series Category",
        "description": "Daloopa series family.",
        "value": "Income Statement",
        "options": [
            {"label": value, "value": value}
            for value in [
                "Income Statement",
                "Balance Sheet",
                "Cash Flow",
                "KPI",
                "Segment",
                "Guidance",
            ]
        ],
    }


def _widget(
    name: str,
    description: str,
    endpoint: str,
    grid: tuple[int, int],
    params: list[JsonDict],
    data: Any,
    schema: JsonDict | None = None,
    widget_type: str = "table",
) -> JsonDict:
    definition: JsonDict = {
        "name": name,
        "description": description,
        "type": widget_type,
        "endpoint": endpoint,
        "category": "Daloopa",
        "source": ["Daloopa MCP", "SEC Filings"],
        "gridData": {"w": grid[0], "h": grid[1]},
        "params": params,
        "data": data,
    }
    if schema is not None:
        definition["schema_data"] = schema
    return definition


def build_widgets() -> dict[str, JsonDict]:
    return {
        "daloopa_company_directory": _widget(
            "Company Directory",
            "Covered companies with Daloopa company ids and latest reported "
            "quarters. Mirrors the discover_companies lookup; anchor all period "
            "math on latest_calendar_quarter.",
            "/daloopa_company_directory",
            (40, 8),
            [],
            _company_directory_rows(),
            _table_schema(
                [
                    ("company_id", "Company ID", "number"),
                    ("ticker", "Ticker", "text"),
                    ("name", "Name", "text"),
                    ("sector", "Sector", "text"),
                    ("fiscal_year_end", "FY End", "text"),
                    ("latest_calendar_quarter", "Latest Calendar Qtr", "text"),
                    ("latest_fiscal_quarter", "Latest Fiscal Qtr", "text"),
                ]
            ),
        ),
        "daloopa_series_directory": _widget(
            "Series Directory",
            "Available data series per company with series ids, categories, and "
            "units. Mirrors the discover_company_series lookup.",
            "/daloopa_series_directory",
            (20, 12),
            [_ticker_param(), _category_param()],
            _series_directory_rows(),
            _table_schema(
                [
                    ("ticker", "Ticker", "text"),
                    ("series_id", "Series ID", "number"),
                    ("series", "Series", "text"),
                    ("category", "Category", "text"),
                    ("unit", "Unit", "text"),
                ]
            ),
        ),
        "daloopa_company_fundamentals": _widget(
            "Company Fundamentals",
            "As-reported quarterly financials with calendar and fiscal period "
            "labels and per-datapoint citation urls. Mirrors "
            "get_company_fundamentals; every value carries a fundamental_id.",
            "/daloopa_company_fundamentals",
            (20, 12),
            [_ticker_param(), _period_param()],
            _fundamentals_rows(),
            _table_schema(
                [
                    ("fundamental_id", "Fundamental ID", "number"),
                    ("ticker", "Ticker", "text"),
                    ("series", "Series", "text"),
                    ("calendar_period", "Calendar Qtr", "text"),
                    ("fiscal_period", "Fiscal Qtr", "text"),
                    ("value", "Value", "number"),
                    ("unit", "Unit", "text"),
                    ("source_url", "Citation", "text"),
                ]
            ),
        ),
        "daloopa_kpi_metrics": _widget(
            "Operating KPIs",
            "Business-driver operating KPIs (installed base, subscribers, "
            "deliveries, cloud growth) per quarter with citation urls.",
            "/daloopa_kpi_metrics",
            (20, 12),
            [_ticker_param(), _period_param()],
            _kpi_rows(),
            _table_schema(
                [
                    ("fundamental_id", "Fundamental ID", "number"),
                    ("ticker", "Ticker", "text"),
                    ("series", "KPI", "text"),
                    ("calendar_period", "Calendar Qtr", "text"),
                    ("fiscal_period", "Fiscal Qtr", "text"),
                    ("value", "Value", "number"),
                    ("unit", "Unit", "text"),
                    ("source_url", "Citation", "text"),
                ]
            ),
        ),
        "daloopa_segment_breakdown": _widget(
            "Segment Breakdown",
            "Segment revenue per quarter with year-over-year growth and "
            "citation urls.",
            "/daloopa_segment_breakdown",
            (20, 12),
            [_ticker_param(), _period_param()],
            _segment_rows(),
            _table_schema(
                [
                    ("fundamental_id", "Fundamental ID", "number"),
                    ("ticker", "Ticker", "text"),
                    ("segment", "Segment", "text"),
                    ("calendar_period", "Calendar Qtr", "text"),
                    ("fiscal_period", "Fiscal Qtr", "text"),
                    ("revenue_musd", "Revenue ($M)", "number"),
                    ("yoy_growth", "YoY Growth", "number"),
                    ("source_url", "Citation", "text"),
                ]
            ),
        ),
        "daloopa_management_guidance": _widget(
            "Management Guidance",
            "Guidance ranges vs. actuals per quarter with Beat/In Line/Missed "
            "verdicts; the next unreported quarter is Pending.",
            "/daloopa_management_guidance",
            (20, 12),
            [_ticker_param()],
            _guidance_rows(),
            _table_schema(
                [
                    ("fundamental_id", "Fundamental ID", "number"),
                    ("ticker", "Ticker", "text"),
                    ("series", "Guided Series", "text"),
                    ("calendar_period", "Calendar Qtr", "text"),
                    ("guidance_low", "Low", "number"),
                    ("guidance_high", "High", "number"),
                    ("actual", "Actual", "number"),
                    ("unit", "Unit", "text"),
                    ("verdict", "Verdict", "text"),
                    ("source_url", "Citation", "text"),
                ]
            ),
        ),
        "daloopa_consensus_estimates": _widget(
            "Consensus Estimates",
            "Street consensus vs. actual revenue and EPS with surprise "
            "percentages. Consensus values are not Daloopa-sourced and carry "
            "no citation ids.",
            "/daloopa_consensus_estimates",
            (20, 12),
            [_ticker_param()],
            _consensus_rows(),
            _table_schema(
                [
                    ("ticker", "Ticker", "text"),
                    ("series", "Series", "text"),
                    ("calendar_period", "Calendar Qtr", "text"),
                    ("consensus", "Consensus", "number"),
                    ("actual", "Actual", "number"),
                    ("surprise_pct", "Surprise", "number"),
                    ("unit", "Unit", "text"),
                ]
            ),
        ),
        "daloopa_document_search": _widget(
            "Document Search",
            "SEC filings and earnings call transcripts with marketplace "
            "document links. Mirrors search_documents.",
            "/daloopa_document_search",
            (26, 12),
            [_ticker_param(), _doc_type_param()],
            _document_rows(),
            _table_schema(
                [
                    ("document_id", "Document ID", "number"),
                    ("ticker", "Ticker", "text"),
                    ("title", "Title", "text"),
                    ("doc_type", "Type", "text"),
                    ("calendar_period", "Calendar Qtr", "text"),
                    ("filing_date", "Filed", "dateString"),
                    ("url", "Link", "text"),
                ]
            ),
        ),
        "daloopa_stock_prices": _widget(
            "Stock Prices",
            "Daily OHLCV rows at quarter ends plus the most recent trading "
            "week. Mirrors get_stock_prices; use the latest close as the spot "
            "price.",
            "/daloopa_stock_prices",
            (20, 12),
            [_ticker_param()],
            _stock_price_rows(),
            _table_schema(
                [
                    ("ticker", "Ticker", "text"),
                    ("date", "Date", "dateString"),
                    ("open", "Open", "number"),
                    ("high", "High", "number"),
                    ("low", "Low", "number"),
                    ("close", "Close", "number"),
                    ("volume", "Volume", "number"),
                ]
            ),
        ),
        "daloopa_coverage_note": _widget(
            "Coverage & Citation Policy",
            "Fixture coverage summary plus the mandatory Daloopa citation and "
            "firm-attribution rules the plugin skills follow.",
            "/daloopa_coverage_note",
            (14, 12),
            [],
            _coverage_note(),
            widget_type="markdown",
        ),
    }


def build_daloopa_catalog() -> JsonDict:
    # Apps are intentionally empty: the fixture is a standalone vendor data
    # feed, and dashboard composition is exercised through the daloopa-*
    # workspace skills instead of pre-built app templates.
    return {
        "apps": [],
        "source": {
            "repo": "daloopa-plugin-claude",
            "url": "https://github.com/daloopa/daloopa-plugin-claude",
            "reference": "skills/data-access.md",
            "notes": "Synthetic catalog modeled on the Daloopa MCP surface the "
            "plugin skills consume; all values are deterministic fixture data.",
        },
        "widgets": build_widgets(),
    }


def main(path: Path = DEFAULT_DATA_PATH) -> None:
    catalog = build_daloopa_catalog()
    path.write_text(json.dumps(catalog, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(
        f"Wrote {len(catalog['widgets'])} widgets and {len(catalog['apps'])} apps to {path}"
    )


if __name__ == "__main__":
    main()
