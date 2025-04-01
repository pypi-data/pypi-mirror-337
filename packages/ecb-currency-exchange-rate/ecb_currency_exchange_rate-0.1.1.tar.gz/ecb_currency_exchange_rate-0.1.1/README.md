# ECB Exchange Rates

A Python package to fetches the exchange rate for a given date, from currency, and to currency.

This package uses daily exchange rate published by ECB.
[ECB page for Euro foreign exchange reference rates](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html)

The ECB exchange rate data does **not** include weekends.
If the date falls on a weekend or holiday, it uses the last available rate.

## Installation

```sh
pip install ecb-currency-exchange-rate
```

## Usage

```Python
from ecb_rates import ecb_rates

rate = ecb_rates.get_exchange_rate("2025-03-31", "EUR", "USD")
print(rate)
```