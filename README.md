# Multi-Market Stock Report Skill

Generate stock analysis PDF reports for A-shares, B-shares, Hong Kong stocks, and US stocks with recent price action, fundamentals, valuation, technical analysis, news/sentiment, and inferred capital movement.

## Features

- Resolve stock names, codes, markets, and trading currencies.
- Gather recent market data and financial information.
- Analyze fundamentals, valuation, technical structure, news, sentiment, and observable capital-flow signals.
- Generate Chinese PDF reports with charts.
- Include data sources and risk disclaimers.
- Support market-specific caveats for A股、B股、港股、美股.

## Installation

Copy this folder into your Codex skills directory:

```text
~/.codex/skills/multi-market-stock-analysis-report-skill
```

Then restart Codex.

Skill Name
Use this name when calling the skill in Codex:a-share-stock-report

Install From GitHub
Repository: Kenneth2378/multi-market-stock-analysis-report-skill

Skill path:
Then call it in Codex like this:
用 a-share-stock-report skill 分析特斯拉

## Example Prompts

```text
用 a-share-stock-report skill 分析伊泰B股
```

```text
用 a-share-stock-report skill 分析比亚迪
```

```text
用 a-share-stock-report skill 分析中际旭创
```

```text
用 a-share-stock-report skill 分析特斯拉
```

## Supported Markets

| Market | Examples | Currency Notes |
| --- | --- | --- |
| A股 | `300308.SZ`, `600030.SH` | RMB |
| B股 | `900948.SH`, `200xxx.SZ` | Usually USD for Shanghai B-shares and HKD for Shenzhen B-shares |
| 港股 | `09988.HK`, `00763.HK` | HKD |
| 美股 | `TSLA`, `NVDA`, `AAPL` | USD |

## Data And Copyright

This skill may use public market and financial sources such as Eastmoney, StockAnalysis, Yahoo Finance, company announcements, CNINFO, HKEXnews, SEC filings, company investor-relations pages, exchange filings, and financial media. Reports should cite sources and summarize facts in original wording. Do not copy full articles, long copyrighted passages, or proprietary research reports.

## Disclaimer

Reports generated with this skill are for research and learning only. They do not constitute investment advice or any recommendation to buy, sell, or hold securities.
