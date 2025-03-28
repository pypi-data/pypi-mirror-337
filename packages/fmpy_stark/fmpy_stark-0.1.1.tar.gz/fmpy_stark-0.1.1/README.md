# FMPY - Financial Modeling Prep API Python SDK

A Python SDK for the [Financial Modeling Prep](https://financialmodelingprep.com) API. This package provides a simple, Pythonic interface to access financial data, stock quotes, and company information.

## Installation

Use `uv` to install the package:

```bash
uv pip install fmpy
```

Or using regular pip:

```bash
pip install fmpy
```

## Authentication

To use the FMP API, you need an API key. You can sign up for one on the [FMP website](https://financialmodelingprep.com/developer/docs/).

You can provide your API key in two ways:

1. Pass it directly when creating the client:

```python
import fmpy

client = fmpy.Client(api_key="your_api_key")
```

2. Set the `FMP_API_KEY` environment variable:

```bash
export FMP_API_KEY="your_api_key"
```

```python
import fmpy

client = fmpy.Client()  # Will use the environment variable
```

## Features

FMPY provides access to a wide range of financial data:

- Company information
- Real-time and historical stock quotes
- Financial statements (income statements, balance sheets, cash flows)
- Ratios and metrics
- Cryptocurrency and forex data
- News and press releases
- And more...

## Examples

### Getting Company Information

```python
import fmpy

client = fmpy.Client(api_key="your_api_key")

# Get company profile
apple_profile = client.company.profile("AAPL")
print(apple_profile)

# Get company peers
peers = client.company.peers("AAPL")
print(peers)
```

### Retrieving Stock Quotes

```python
import fmpy

client = fmpy.Client(api_key="your_api_key")

# Get real-time quotes
quote = client.quote.real_time("AAPL")
print(quote)

# Get quotes for multiple symbols
quotes = client.quote.batch(["AAPL", "MSFT", "GOOGL"])
print(quotes)
```

### Fetching Historical Price Data

```python
import fmpy
from datetime import date

client = fmpy.Client(api_key="your_api_key")

# Get historical daily prices
historical_data = client.chart.full("AAPL", 
                                   from_date="2022-01-01", 
                                   to_date="2022-12-31")
print(historical_data)

# Get intraday prices (1-minute intervals)
intraday_data = client.chart.one_minute("AAPL")
print(intraday_data)
```

### Accessing Financial Statements

```python
import fmpy

client = fmpy.Client(api_key="your_api_key")

# Get income statements
income_statements = client.statements.income_statement("AAPL", period="annual", limit=5)
print(income_statements)

# Get balance sheets
balance_sheets = client.statements.balance_sheet("AAPL", period="quarter", limit=10)
print(balance_sheets)

# Get cash flow statements
cash_flows = client.statements.cash_flow("AAPL")
print(cash_flows)
```

### Using the Stock Screener

```python
import fmpy

client = fmpy.Client(api_key="your_api_key")

# Screen for technology stocks with market cap > $100B
tech_stocks = client.search.screener(
    sector="Technology",
    market_cap_more_than=100000000000,
    is_actively_trading=True
)
print(tech_stocks)
```

### Getting Analyst Data

```python
import fmpy

client = fmpy.Client(api_key="your_api_key")

# Get analyst estimates
estimates = client.analyst.financial_estimates("AAPL")
print(estimates)

# Get price targets
price_targets = client.analyst.price_target_summary("AAPL")
print(price_targets)

# Get analyst grades
grades = client.analyst.grades("AAPL")
print(grades)
```

### Calendar Events

```python
import fmpy
from datetime import datetime, timedelta

client = fmpy.Client(api_key="your_api_key")

# Get upcoming earnings calendar
today = datetime.now()
next_month = today + timedelta(days=30)
earnings = client.calendar.earnings_calendar(
    from_date=today.strftime("%Y-%m-%d"),
    to_date=next_month.strftime("%Y-%m-%d")
)
print(earnings)

# Get dividend history
dividends = client.calendar.dividends("AAPL")
print(dividends)
```

### News and Press Releases

```python
import fmpy

client = fmpy.Client(api_key="your_api_key")

# Get latest stock news
stock_news = client.news.stock_news(limit=10)
print(stock_news)

# Get news for specific stocks
apple_news = client.news.search_stock_news("AAPL", limit=5)
print(apple_news)
```

### ETF and Mutual Fund Data

```python
import fmpy

client = fmpy.Client(api_key="your_api_key")

# Get ETF holdings
spy_holdings = client.etf.holdings("SPY")
print(spy_holdings)

# Get ETF sector weightings
spy_sectors = client.etf.sector_weightings("SPY")
print(spy_sectors)
```

### Cryptocurrency Data

```python
import fmpy

client = fmpy.Client(api_key="your_api_key")

# Get cryptocurrency list
crypto_list = client.crypto.list()
print(crypto_list)

# Get Bitcoin price history
btc_history = client.crypto.historical_price_full("BTCUSD", 
                                               from_date="2022-01-01", 
                                               to_date="2022-12-31")
print(btc_history)
```

### Forex Data

```python
import fmpy

client = fmpy.Client(api_key="your_api_key")

# Get forex pairs list
forex_list = client.forex.list()
print(forex_list)

# Get EUR/USD exchange rate history
eurusd_history = client.forex.historical_price_full("EURUSD", 
                                                 from_date="2022-01-01", 
                                                 to_date="2022-12-31")
print(eurusd_history)
```

### SEC Filings

```python
import fmpy
from datetime import datetime, timedelta

client = fmpy.Client(api_key="your_api_key")

# Get recent 8-K filings
today = datetime.now()
one_month_ago = today - timedelta(days=30)
filings = client.sec.latest_8k_filings(
    from_date=one_month_ago.strftime("%Y-%m-%d"),
    to_date=today.strftime("%Y-%m-%d")
)
print(filings)

# Get company filings
apple_filings = client.sec.filings_by_symbol("AAPL", limit=10)
print(apple_filings)
```

### Bulk Data Access

```python
import fmpy

client = fmpy.Client(api_key="your_api_key")

# Get company profiles in bulk
profiles = client.bulk.company_profile(part=0)
print(profiles)

# Get financial scores in bulk
scores = client.bulk.financial_scores()
print(scores)

# Get income statements in bulk for a specific year and period
income_statements = client.bulk.income_statement(year=2023, period="FY")
print(income_statements)

# Get key metrics TTM in bulk
key_metrics = client.bulk.key_metrics_ttm()
print(key_metrics)
```

### Directory and Symbol Listings

```python
import fmpy

client = fmpy.Client(api_key="your_api_key")

# Get list of all available company symbols
symbols = client.directory.company_symbols()
print(symbols)

# Get list of available exchanges
exchanges = client.directory.available_exchanges()
print(exchanges)

# Get list of available sectors
sectors = client.directory.available_sectors()
print(sectors)

# Get list of actively trading companies
active_companies = client.directory.actively_trading_list()
print(active_companies)
```

## DataFrame Support

By default, all responses are returned as pandas DataFrames for easy data analysis. If you prefer to get the raw JSON response, set `as_dataframe=False` in any method call:

```python
# Get response as DataFrame (default)
df = client.company.profile("AAPL")

# Get response as JSON
json_data = client.company.profile("AAPL", as_dataframe=False)
```

## Documentation

For more details on available endpoints and parameters, please refer to the official [FMP API documentation](https://financialmodelingprep.com/developer/docs/).


## FMPY Project Structure

```bash
fmpy/
├── fmpy/
│   ├── __init__.py          # Package initialization
│   ├── client.py            # Main client class
│   ├── exceptions.py        # Custom exceptions
│   ├── config.py            # Configuration settings
│   ├── utils.py             # Utility functions
│   └── endpoints/           # API endpoint modules
│       ├── __init__.py
│       ├── search.py        # Search endpoints
│       ├── company.py       # Company endpoints 
│       ├── quote.py         # Quote endpoints
│       ├── chart.py         # Chart endpoints
│       ├── statements.py    # Financial statements
│       ├── analyst.py       # Analyst endpoints
│       ├── calendar.py      # Calendar endpoints
│       ├── market.py        # Market data endpoints
│       ├── crypto.py        # Cryptocurrency endpoints
│       ├── forex.py         # Forex endpoints
│       ├── etf.py           # ETF and mutual funds
│       ├── news.py          # News endpoints
│       ├── sec.py           # SEC filings
│       └── bulk.py          # Bulk data endpoints
├── setup.py                 # Package setup file
├── pyproject.toml           # Project metadata and dependencies
├── README.md                # Documentation
├── LICENSE                  # License information
└── tests/                   # Test cases
    └── test_client.py       # Client tests
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.