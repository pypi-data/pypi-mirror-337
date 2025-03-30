# SPGMI CIQ Python Library

The Python Software Development Kit (SDK) makes REST API integration into your Python environment easier, allowing less technical and experienced Python users to start utilizing REST APIs sooner.

S&P Capital API clients can now access these SDKs to integrate end-of-day and time-series Financial and Market data such as income statements, balance sheets, pricing, and dividend information data points from the S&P Capital IQ API into their Python workflows.

The SDK seamlessly integrates with pandas DataFrames, providing a Jupyter-friendly environment and a simpler, optimized data analysis experience.

With the latest update, the SDK now features the Data Widgets Library. These new functions reflect data available on our S&P Global Capital IQ Pro platform widgets, driving seamless integration into your Python environment for streamlined access to financial, market, ESG data, and more—all in an optimized, analysis-ready format.
## Features

Integrate high-quality data with your systems, portals, and business applications, including:
1. Income statement, balance sheet, and cash flow values for backtesting models.
2. Basic automation of desktop/Excel-based modeling when Excel templates reach their limit.
3. Time-series pricing and market data values in addition to dividend information.

## Benefits
1. Output generated in a reusable/extendible object such as a DataFrame, facilitating easy data processing and analysis.
2. Ease of authentication, request, and response handling.
3. Ability to use proxy objects for enhanced network communication.
4. Simplified SDK setup with robust error handling and token management.

## Installation

Thank you for your interest in our library on PYPI. Please be aware that the version of the library available here is a placeholder/dummy version intended for demonstration purposes only.

To obtain an actual version of the Python SDK library for installation or further support, please visit the [S&P Global Support Center](https://www.support.marketplace.spglobal.com/en/delivery-resources#sec6). Note that login credentials must be created on the support center to access the content.

Our team will be happy to assist you and provide guidance based on your needs.

## Setting up the library
Using the below code, you can make the necessary import and set up the required instance to use the Python library.

```sh
from spgmi_api_sdk.ciq.services import SDKDataServices

spg = SDKDataServices(username, password)
```

## Fetching Financial Data
Our financial data service provides a number of functionalities enabling you to retrieve point-in-time and historical financial data including income statements, balance sheets, cash flow statements, and other financial metrics essential for comprehensive financial analysis.

### 1. get_income_statement_pit
Obtains income statement data for a given point in time.
```sh
spg.get_income_statement_pit(identifiers=["I_US5949181045","2588173","EG1320"],properties={"asOfDate": "12/31/2020", "currencyId": "USD","currencyConversionModeId": "HISTORICAL"})
```

### 2. get_income_statement_historical
Retrieves income statement data for a range of periods.
```sh
spg.get_income_statement_historical(identifiers=["GV012141","MSFT:NasdaqGS"], properties={"periodType":"IQ_FQ-4"})
```

### 3. get_balance_sheet_pit
Retrieves balance sheet data for a given point in time.
```sh
spg.get_balance_sheet_pit(identifiers=["RX309198","MMM:"], properties={"asOfDate": "12/31/2020", "currencyId": "USD","currencyConversionModeId": "HISTORICAL"})
```
### 4. get_balance_sheet_historical
Retrieves balance sheet data for a range of periods.
```sh
spg.get_balance_sheet_historical(identifiers=["I_US5949181045","2588173"], properties={"periodType":"IQ_FQ-2"})
```

### 5. get_cash_flow_pit
Retrieves cash flow data for a given point in time.
```sh
spg.get_cash_flow_pit(identifiers=["2588173","EG1320"], properties={"asOfDate": "12/31/2020", "currencyId": "USD","currencyConversionModeId": "HISTORICAL"})
```

### 6. get_cash_flow_historical
Returns cash flow statement data values based on a range of periods.
```sh
spg.get_cash_flow_historical(identifiers=["MSFT:NasdaqGS","DB649496569"], properties={"asOfDate": "12/31/2020", "currencyId": "USD","currencyConversionModeId": "HISTORICAL"})
```

### 7. get_financials_pit
Fetches financial data (income statement, balance sheet, cash flow) for a given point in time.
```sh
spg.get_financials_pit(identifiers=["I_US5949181045","2588173","EG1320","CSP_594918104","IQT2630413","GV012141","MSFT:NasdaqGS","DB649496569","RX309198"], mnemonics=["IQ_CASH_INVEST_NAME_AP"], properties={"asOfDate": "12/31/2020", "currencyId": "USD","currencyConversionModeId": "HISTORICAL"})

```
### 8. get_financials_historical
Fetches historical financial data based on specified mnemonics for a range of periods. 
```sh
spg.get_financials_historical(identifiers=["I_US5949181045","2588173","EG1320","CSP_594918104","IQT2630413","GV012141","MSFT:NasdaqGS","DB649496569","RX309198"], mnemonics=["IQ_CASH_INVEST_NAME_AP"], properties={"asOfDate": "12/31/2020", "currencyId": "USD","currencyConversionModeId": "HISTORICAL"})
```

## Fetching Market Data
Our market data service provides several functionalities enabling you to access end-of-day and time-series market data, including stock prices, trading volumes, dividend information, and other market-related information crucial for analysis and decision-making.

### 1. get_pricing_info_pit
Fetches pricing information for a given point in time.
```sh
spg.get_pricing_info_pit(identifiers=["I_US5949181045","2588173","EG1320","CSP_594918104","IQT2630413"], properties={}) 
```

### 2. get_pricing_info_time_series
Fetches historical pricing information over a specified time period. 
```sh
spg.get_pricing_info_time_series(identifiers=["CSP_594918104","IQT2630413","GV012141","MSFT:NasdaqGS","DB649496569","RX309198","MMM:"], properties={}) 
```

### 3. get_dividend_info_pit
Fetches dividend information for a given point in time. 
```sh
spg.get_dividend_info_pit(identifiers=["CSP_594918104","IQT2630413","GV012141","MSFT:NasdaqGS"], properties={}) 
```

### 4. get_dividend_info_time_series
Fetches historical dividend information over a specified time period 
```sh
spg.get_dividend_info_time_series(identifiers=["GV012141","MSFT:NasdaqGS","DB649496569","RX309198","MMM:"], properties={}) 
```

### 5. get_market_info_pit
Fetches market information for a given point in time. 
```sh
spg.get_market_info_pit(identifiers=["IQT2630413","GV012141","MSFT:NasdaqGS","DB649496569","RX309198"], properties={}) 
```
### 6. get_market_info_time_series
Fetches historical market information over a specified time period.
```sh 
spg.get_market_info_time_series(identifiers=["AAPL:"], properties={}) 
```


## Data Widgets Library
Easily integrate the S&P Global Capital IQ Pro platform widgets into your workflow to access company profile information such as financial highlights, market data, corporate insights, ESG scores, and more.

All functions return data in pandas DataFrames, allowing seamless analysis and automation.

### 1. get_market_data
Returns an array of end-of-day market data values including dividend, closing price, VWAP, open price, day high/low, and more.
```sh 
spg.get_market_data(identifiers=["IQ112350","MSFT","IQ24937"])
```

### 2. get_financials
Retrieves financial highlights for a defined period type, providing data values including revenue, earnings, and key performance metrics for in-depth analysis.
```sh
spg.get_financials(identifiers=["IQ21835","IQ26642","MSFT"], period_type="IQ_FY-1")
```

### 3. get_corporate_data
Provides entity-level details like company status, industry classification, incorporation date, company description, contact information, key professionals and more.
```sh 
spg.get_corporate_data(identifiers=["IQ112350","SPGI","IQ24937"])
``` 

### 4. get_esg_scores
Retrieves Environmental, Social, and Governance (ESG) scores along with key sustainability metrics. 
```sh 
spg.get_esg_scores(identifiers=["SNL4202062"],assessment_year= "2022")
```

### 5. get_multiples
Fetches key valuation multiples for the latest fiscal year including P/E Ratio, Price/Book, and TEV/EBITDA, to assess a company's market standing.
```sh 
spg.get_multiples(identifiers=["SNL4004214","MSFT"])
```

### 6. get_risk_gauge_score
Provides risk gauge scores for a given date (most recent by default).
```sh 
spg.get_risk_gauge_score(identifiers=["IQ112350", "MSFT", "IQ24937","NVDA","SNL4094286","SNL"],scoring_date="03/10/2023")
```

### 7. get_estimates
Retrieves analysts' earnings, revenue, and EBITDA estimates across different fiscal periods (IQ_FQ, IQ_FQ+1, IQ_FY, IQ_FY+1, IQ_NTM).
```sh 
spg.get_estimates(identifiers=["IQ112350", "MSFT", "IQ24937","NVDA","SNL4094286","SNL"])
```
The function output includes:

1. Analyst Recommendations & Target Price
2. Forward-Looking Valuation Multiples: P/E, P/BV, PEG, and TEV/EBIT ratios.
3. Forward-Looking Estimates: Earnings Per Share (EPS), Revenue, and EBITDA

### 8. get_transactions
Fetches the top 5 most recent corporate transactions for the given identifiers including mergers, acquisitions, buybacks and more.
```sh 
spg.get_transactions(identifiers=["IQ112350","IQ162270","MSFT","IQ32307","IQ32307","NVDA","SNL4094286"])
```
The function output includes:

1. Transaction List: A ranked list of recent transactions.
2. Transaction Type: Classification such as M&As, Buybacks, Public Offerings, or Private Placements.
3. Deal Resolution: Summary of the transaction details.
4. Transaction Value: Gross value of the transaction.
5. Announced & Completed Dates: Key dates marking the transaction timeline.

### 9. get_stock_price
Retrieves one year (rolling) of historical stock price data including open, close, high, low, and volume.
```sh 
spg.get_stock_price(identifiers=["IQ112350", "MSFT", "IQ24937"])
```

### 10. get_agency_ratings
Provides current issuer ratings and outlooks assigned by S&P Ratings, Moody's Investor Services, and Fitch Ratings, providing a one stop-shop for credit ratings. 
```sh 
spg.get_agency_ratings(identifiers=["IQ112350", "IQ24937"])
```

### 11. get_latest_activity
Retrieves a comprehensive overview of the most recent corporate activities including key documents, events, and other key developments.
```sh 
response_list=spg.get_latest_activity(identifiers=["IQ112350", "IQ24937"])
documents,events,key_devs = response_list
display(documents)
display(events)
display(key_devs)
```

The function output includes:
1. Documents (Top 10 Most Recent): A ranked list of recently published reports, filings, and transcripts for the company.
2.	Events (Top 3 Historical & Top 3 Future): A timeline of major corporate events, such as earnings calls, investor conferences, and financial disclosures.
3.	Key Developments (Top 5 Most Recent): A summary of the most important announcements, collaborations, acquisitions, and business updates etc.

## Company Name Match Function

Easily map a company name to its entity-level identifier and the associated ticker through our Kensho Link service.

### 1. get_company_name_to_id
Returns a list of close matches for a user input company name. Information returned includes companyId / institutionId, company names, and tickers of the five closest matches. 

```sh 
spg.get_company_name_to_id(companies=["Coca Cola", "Meezan Bank Limited (MEBL)"],identifier_type="CIQ")
``` 
## Using a Proxy with SDKDataServices (Optional)
If your environment requires a proxy for API requests, configure it using SDKProxy when initializing SDKDataServices.
```sh
from spgmi_api_sdk.ciq.services import SDKDataServices, SDKProxy

sdk_proxy_object = SDKProxy(
    proxy_username="", proxy_password="", proxy_host=None, proxy_port=None, proxy_domain=""
)

spg = SDKDataServices(username="your_api_username", password="your_api_password", proxy=sdk_proxy_object)
```
Note: If a proxy is not required, pass None or omit the proxy argument.

## Additional Resources
For more information on our Python SDK, please visit the [S&P Global Support Center](https://www.support.marketplace.spglobal.com/en/delivery-resources#sec6). This resource requires you to create login credentials.

On the support center, you can download the Python SDK and obtain additional resources, including a detailed CIQ Python SDK User Guide, to support your use of this offering.


