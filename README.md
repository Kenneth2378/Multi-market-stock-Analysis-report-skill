# Multi-Market Stock Report Skill

Codex skill name: `a-share-stock-report`

This project was previously introduced as **Multi-Market Stock Report Skill**. The Codex skill name remains `a-share-stock-report`.

本项目早期曾以 **Multi-Market Stock Report Skill** 介绍；为兼容老用户，Codex 调用名仍为 `a-share-stock-report`。

一个用于生成 A股、B股、港股和美股股票研究 PDF 报告的 Codex Skill，覆盖基本面、估值、技术面、公开量价资金推断、消息情绪和研究判断框架。仅供学习研究，不构成投资建议。

A Codex Skill for generating deep PDF stock research reports across A-shares, B-shares, Hong Kong stocks, and US stocks, covering fundamentals, valuation, technical analysis, public price-volume inference, news sentiment, and a research judgment framework. For research and learning only. Not investment advice.

If this skill is useful, please consider giving it a Star.
如果这个 Skill 对你有帮助，欢迎点一个 Star 支持。

The public repository includes the deterministic research-pack renderer, report validator, privacy scanner, and HTML template. Local generated reports remain private and ignored.

## Backward Compatibility

- Existing prompts continue to work.
- The default behavior is a deep stock research PDF report with a sibling quality check.
- The public Codex skill name remains `a-share-stock-report`.
- Each report should generate a sibling `quality_check.md`.

## Public Community Scope

This public version supports:

- Deep, source-backed stock research PDF reports.
- A-share, B-share, Hong Kong stock, and US stock research.
- Recent three-month price and volume chart.
- Fundamentals, valuation, technical analysis, news/sentiment, and public price-volume inference.
- Research judgment and methodology.
- Observation conditions, invalidation conditions, and risk warnings.
- Numeric validation gate.
- Public depth-standard gate.
- `quality_check.md`.
- Data-source citation, copyright boundary, disclaimer, and private-information protection.

## Example Reports

- A-share example: 中际旭创
- US stock example: NVIDIA
- Stable income example: 京沪高铁

## What This Skill Generates

- PDF stock research report.
- Recent 3-month chart.
- Fundamentals.
- Valuation.
- Technical analysis.
- Public price-volume inference.
- Research judgment framework.
- Observation and invalidation conditions.
- Risk disclaimer.
- `quality_check.md`.

## Deterministic Deep-Report Pipeline

The current standard uses a structured research pack plus deterministic rendering and validation. Updating `SKILL.md` alone is not sufficient.

Required public files:

- `references/legacy_report_contract.md`
- `references/research_depth_gate.md`
- `references/research_pack_schema.md`
- `templates/report_template.html`
- `templates/quality_check_schema.md`
- `scripts/generate_stock_report.py`
- `scripts/validate_report.py`
- `scripts/scan_pdf_privacy.py`
- `scripts/check_report_depth_standard.py`
- `scripts/collect_eastmoney_evidence.py`
- `scripts/init_research_pack.py`

Usage:

```text
python scripts/generate_stock_report.py --input research_pack.json --validate-only
python scripts/generate_stock_report.py --input research_pack.json --output-dir reports
python scripts/check_report_depth_standard.py reports/<report.pdf>
```

The generator rejects incomplete research packs. The final validator requires the legacy content contract, at least 3537 extracted PDF characters, target-specific semantic checks, all numeric validation rows to pass, no privacy hits, the latest complete trading day, and no forced page break or sparse non-final page.

`quality_check.md` passing is necessary but not sufficient. The final PDF must also pass `scripts/check_report_depth_standard.py`, which blocks shallow reports with low page count, low character count, weak numeric density, missing valuation/fundamental/judgment terms, privacy problems, mojibake, or forbidden transaction language.

The initialized research pack from `init_research_pack.py` is only a draft. It intentionally contains pending verification and must be deepened with company-specific financials, valuation basis, peer context, price-volume evidence, catalysts, observation conditions, invalidation conditions, and numeric validation before delivery.

## Features

- Resolve stock names, codes, markets, and trading currencies.
- Gather recent market data and financial information.
- Analyze fundamentals, valuation, technical structure, news, sentiment, and observable public price-volume signals.
- Add an evidence-based research judgment with methodology, scenarios, observation conditions, and invalidation conditions.
- Generate Chinese PDF reports with charts.
- Include data sources and risk disclaimers.
- Support market-specific caveats for A股、B股、港股、美股.

## PDF Export Privacy Regression

Chrome or Edge headless PDF exports must disable browser default headers and footers. Prefer:

```text
--no-pdf-header-footer
```

If using Playwright or Puppeteer, explicitly set:

```python
display_header_footer=False
```

After every PDF export, run the hard gate:

```text
python scripts/scan_pdf_privacy.py path/to/report.pdf
```

The generator must write the scan result to the sibling `quality_check.md`, including extractor, privacy keyword list, hit list, and `PDF Privacy Scan` status.

Extract the final PDF text with a reliable extractor and scan it for local paths or credential-like keywords. Do not rely only on HTML/SVG scanning, raw zlib stream scanning, or browser export flags.

Extractor priority:

1. PyMuPDF / fitz
2. pypdf
3. pdfminer.six
4. pdftotext / mutool

Minimum privacy patterns include:

```text
file://
D:/
D:\
C:/
C:\
C:\Users
/Users/
\Users\
api_key
token
cookie
secret
password
```

If any pattern is found in extracted PDF text, `quality_check.md` must mark `PDF Privacy Scan` as `FAIL`, and the final conclusion cannot be `PASS`. If the privacy scan passes but data pending verification fields remain, the final conclusion must be `NEEDS_REVIEW`.

## Numeric Validation Gate

Before producing the final report, the Skill should validate:

- `price x share count = market cap`, with unit and currency checks.
- Latest close, prior close, intraday price, and after-hours price are not mixed.
- YoY, QoQ, and period return are recalculated from source numbers.
- Units are consistent across 亿、万亿、million、billion、trillion.
- PE, PB, PS, market cap, and share-count source bases are stated.
- If data conflicts, label the conflict and do not force a conclusion.
- If key data cannot be verified, write `数据待核验`.

## Installation

Copy this folder into your Codex skills directory:

```text
~/.codex/skills/a-share-stock-report
```

Then restart Codex.

Runtime requirements:

- Python 3.10 or newer.
- Google Chrome, Chromium, or Microsoft Edge for PDF export.
- Internet access for current market data and public filings.

Install the Python dependency before first use:

```text
python -m pip install -r requirements.txt
```

On a non-standard browser installation, pass its executable path with `--browser` when running `scripts/generate_stock_report.py`.

## Public Evidence Workflow

For A-shares and B-shares, first collect a reproducible public-evidence snapshot:

```text
python scripts/collect_eastmoney_evidence.py --ticker 600845.SH --output workspace/600845_evidence.json
python scripts/init_research_pack.py --evidence workspace/600845_evidence.json --output workspace/600845_research_pack.json
```

The initialized research pack is deliberately marked `数据待核验` and cannot pass generation. Codex must verify the annual report, latest quarterly report, exchange announcements, peers, valuation basis, and every numeric-validation row before removing `pending_verification`.

Then run the deterministic gates:

```text
python scripts/generate_stock_report.py --input workspace/600845_research_pack.json --validate-only
python scripts/generate_stock_report.py --input workspace/600845_research_pack.json --output-dir workspace/reports
python scripts/check_report_depth_standard.py workspace/reports/<report.pdf>
```

The collector is an evidence aid, not an investment-analysis engine. Hong Kong and US securities require the public alternatives listed in `SKILL.md`.

## Reproducibility Boundary

The repository fixes the report contract, renderer, numeric trail, semantic checks, privacy scan, public depth-standard gate, and PASS threshold. Live prices, newly published filings, source availability, and model-written analysis can change, so different runs should meet the same validation standard but are not expected to produce identical wording or conclusions.

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

```text
用 a-share-stock-report skill 分析 NVDA
```

## Supported Markets

| Market | Examples | Currency Notes |
| --- | --- | --- |
| A股 | `300308.SZ`, `600030.SH` | RMB |
| B股 | `900948.SH`, `200xxx.SZ` | Usually USD for Shanghai B-shares and HKD for Shenzhen B-shares |
| 港股 | `09988.HK`, `00763.HK` | HKD |
| 美股 | `TSLA`, `NVDA`, `AAPL` | USD |

## Data And Copyright

This skill may use public market and financial sources such as Eastmoney, StockAnalysis, Yahoo Finance, company announcements, CNINFO, HKEXnews, SEC filings, company investor-relations pages, exchange filings, and financial media.

Reports should cite sources and summarize facts in original wording. Do not copy full articles, long copyrighted passages, proprietary research reports, paid data, API keys, cookies, account information, or personal local paths.

## Disclaimer

Reports generated with this skill are for research and learning only. They do not constitute investment advice or any recommendation to buy, sell, or hold securities.
