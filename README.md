# Multi-Market Stock Report Skill

一个用于生成 A股、B股、港股和美股股票研究 PDF 报告的 Codex Skill，覆盖基本面、估值、技术面、资金动向、消息情绪和投资判断框架。仅供研究参考，不构成投资建议。

A Codex Skill for generating PDF stock research reports across A-shares, B-shares, Hong Kong stocks, and US stocks, covering fundamentals, valuation, technical analysis, capital-flow signals, news sentiment, and an investment judgment framework. For research reference only. Not investment advice.

If this skill is useful, please consider giving it a Star.
如果这个 Skill 对你有帮助，欢迎点一个 Star 支持。

## Example Reports
- A-share example: 中际旭创
- US stock example: NVIDIA
- Stable income example: 京沪高铁

## What This Skill Generates
- PDF stock research report
- Recent 3-month chart
- Fundamentals
- Valuation
- Technical analysis
- Capital-flow signals
- Investment judgment framework
- Risk disclaimer

## Features

- Resolve stock names, codes, markets, and trading currencies.
- Gather recent market data and financial information.
- Analyze fundamentals, valuation, technical structure, news, sentiment, and observable capital-flow signals.
- Add an evidence-based investment judgment with methodology, scenarios, observation conditions, and invalidation conditions.
- Generate Chinese PDF reports with charts.
- Include data sources and risk disclaimers.
- Support market-specific caveats for A股、B股、港股、美股.

## Installation

Copy this folder into your Codex skills directory:

```text
~/.codex/skills/a-share-stock-report
```

Then restart Codex.

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

