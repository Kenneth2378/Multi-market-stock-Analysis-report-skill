---
name: a-share-stock-report
description: Generate deep, source-backed stock research PDF reports for A-shares, B-shares, Hong Kong stocks, and US stocks. Use for company fundamentals, valuation, recent price action, public price-volume inference, catalysts, risks, research judgment, PDF output, and quality_check.md validation.
---

# Deep Multi-Market Stock Report

Generate company-specific research reports, not generic market-data summaries. Preserve analytical depth while enforcing numeric, sourcing, language, semantic, and privacy gates.

Before research or drafting, read [references/legacy_report_contract.md](references/legacy_report_contract.md), [references/research_depth_gate.md](references/research_depth_gate.md), and [references/research_pack_schema.md](references/research_pack_schema.md). The legacy contract is the minimum content standard; current numeric and privacy controls are additive, not replacements. Use [templates/quality_check_schema.md](templates/quality_check_schema.md) for final validation.

Always create a research-pack JSON and use the bundled deterministic pipeline:

```text
python scripts/collect_eastmoney_evidence.py --ticker <A_OR_B_TICKER> --output evidence.json
python scripts/init_research_pack.py --evidence evidence.json --output research_pack.json
python scripts/generate_stock_report.py --input research_pack.json --validate-only
python scripts/generate_stock_report.py --input research_pack.json --output-dir <reports>
python scripts/validate_report.py <report.pdf> --pack research_pack.json --html <report.html>
python scripts/scan_pdf_privacy.py <report.pdf>
python scripts/check_report_depth_standard.py <report.pdf>
```

Do not write a one-off renderer when these scripts are available. Do not report success unless the generated sibling `quality_check.md` ends in `PASS` and `scripts/check_report_depth_standard.py` returns `PASS`.

For A-shares and B-shares, use the bundled collector as the initial public-evidence snapshot when the endpoint is available. Inspect `source_errors` before research and replace missing evidence with statutory filings or another named public source. Treat the initialized pack as a draft only: it intentionally contains `数据待核验`, an empty numeric-validation list, and non-empty `pending_verification`. Complete company-specific research and numeric validation before running `--validate-only`. For Hong Kong and US stocks, gather equivalent evidence from the public alternatives below and construct the same schema manually.

Default behavior is a deep PDF research report plus a sibling `quality_check.md`. The public deterministic renderer and validators are included under `scripts/`. `quality_check.md PASS` is necessary but not sufficient: the final PDF must also pass the public depth-standard gate.

## Public depth-standard gate

Run `scripts/check_report_depth_standard.py` on every final PDF. This gate prevents shallow reports that pass only by headings or file existence.

Minimum public thresholds:

- At least 3 PDF pages.
- At least 3500 extracted PDF characters.
- At least 400 digits.
- At least 15 percentage values.
- At least 45 finance or money terms.
- Must contain fundamentals, valuation, research judgment/methodology, operating cash flow, gross margin, net profit, PE, observation conditions, invalidation conditions, and the investment-advice disclaimer.
- Must not contain direct transaction commands or guaranteed-return language.

If the public depth-standard gate returns `NEEDS_REVIEW`, do not tell the user that the report is complete. Add company-specific evidence, numbers, valuation basis, observation conditions, and invalidation conditions, then regenerate.

## Required stance

- Treat all market data as time-sensitive. Verify the latest available complete trading day, price, valuation, announcements, and financial results before writing the report.
- Include a clear disclaimer in every report: `仅供学习研究，不构成投资建议`.
- State the market, ticker, currency, latest complete trading day, time zone, and data-source limitations for each stock.
- Phrase `主力/资金动向` as `公开量价资金推断` or `public price-volume inference` from observable public signals only: price, volume, turnover, amplitude, gaps, high-volume up/down days, short interest, institutional ownership, support/resistance, and market context. Do not present it as confirmed account-level behavior.
- Use `研究判断 / 投资判断框架`, not direct transaction commands.
- Use `适合的研究场景`, not `适合的投资者`.
- Use `观察区间 / 风险参考区间`, not direct buy/sell zones.
- Cite data sources by name or link. Summarize facts in original wording. Do not copy full articles, long copyrighted passages, proprietary reports, paid data, API keys, cookies, account names, personal local paths, or private files.
- Do not output trading commands, follow-trade language, guaranteed-return language, target-return language, or direct transaction language.

## Workflow

### 1. Identify securities

- Resolve each company name to stock code, market, exchange suffix, and trading currency.
- Examples:
  - A股深市: `002698.SZ`, Eastmoney `0.002698`
  - A股沪市: `600845.SH`, Eastmoney `1.600845`
  - B股沪市: `900926.SH`, Eastmoney `1.900926`, usually USD-denominated
  - B股深市: `200xxx.SZ`, Eastmoney `0.200xxx`, usually HKD-denominated
  - 港股: `00241.HK` or `0241.HK`, commonly Eastmoney `116.00241`, Yahoo/StockAnalysis `0241.HK`
  - 美股: `TSLA`, `NVDA`, `AAPL`, Yahoo/StockAnalysis ticker symbols
- If sources disagree on ticker, market, currency, trading status, or latest data date, label the conflict and do not force a conclusion.

### 2. Gather current and historical market data

- Pull daily K-line data for at least the most recent three calendar months.
- Include date, open, close, high, low, volume, amount when available, amplitude, percent change, and turnover when available.
- Pull quote and valuation fields where available: latest complete close, prior close, intraday price if relevant, volume/amount, turnover, total market cap, float market cap, PE, PB, PS, and industry.
- For A股 and B股, a usable Eastmoney daily K-line pattern:

```text
https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=<SECID>&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&klt=101&fqt=1&beg=<YYYYMMDD>&end=<YYYYMMDD>
```

- A usable Eastmoney batch quote pattern:

```text
https://push2.eastmoney.com/api/qt/ulist.np/get?secids=<SECID1>,<SECID2>&fields=f12,f14,f2,f3,f4,f5,f6,f8,f9,f20,f21,f23,f100
```

- For 港股 and 美股, use reliable public alternatives when Eastmoney is incomplete or unstable: StockAnalysis, Yahoo Finance historical data, Nasdaq, NYSE, HKEX, company investor-relations pages, MarketWatch, Investing, AAStocks, Futu, or other public quote pages.
- Keep market-specific caveats in the report. For example, B股 liquidity may be low, 港股 turnover may differ by source, and 美股 latest data uses US market dates.

### 3. Numeric validation gate

Run this gate before generating the PDF, chart, `quality_check.md`, or final response:

1. Validate `price x share count = market cap`; check unit and currency consistency.
2. Do not mix latest close, prior close, intraday price, and after-hours price. Label each price basis clearly.
3. Recalculate YoY, QoQ, and period return from source numbers.
4. Check unit consistency for 亿、万亿、million、billion、trillion.
5. State the source basis for PE, PB, PS, total market cap, float market cap, and share count.
6. If two sources conflict, label the conflict and do not force a conclusion.
7. If key data cannot be verified, write `数据待核验`. Do not invent data.
8. Public price-volume inference must be written as inference only, not real account behavior.
9. Do not output trading commands, follow-trade language, guaranteed-return language, target-return language, or direct transaction language.

Every numeric validation item must leave a reproducible trail in `quality_check.md`:

- raw field
- data source
- date
- unit
- formula
- calculated result
- source result
- difference ratio
- `PASS` / `NEEDS_REVIEW` / `FAIL`

If the numeric validation gate fails, mark the output as `NEEDS_REVIEW` and clearly state what needs review.

### 4. Gather fundamentals and news

- Verify latest annual report and latest quarterly report from company announcements, exchange filings, CNINFO, HKEXnews, SEC filings, company investor-relations pages, Eastmoney/F10, Sina Finance, StockAnalysis, or another public source.
- Capture revenue, YoY growth, net profit attributable to parent, gross margin/net margin when available, operating cash flow, total assets/equity/liabilities or leverage, and major governance/shareholder notes.
- Check recent company announcements and major news. Prefer dated, sourceable facts over vague market rumors.
- For copyrighted news and research reports, use short summaries and source names/links only. Avoid reproducing large excerpts or full tables unless the source license clearly permits it.

### 4A. Deep-research gate

- Treat the annual report and latest quarterly report as the primary evidence, not optional enrichment.
- Capture adjusted profit, gross/net margin, operating cash flow, total assets, equity, liabilities, debt ratio, receivables, inventory, financing, and material impairment where available.
- Identify the actual profit engine: business segments, material subsidiaries, customers, product cycle, competitive position, and controlling shareholder/governance.
- Explain at least two material announcements or catalysts: what changed, the financial or strategic mechanism, expected timing, and confirmation/invalidation evidence. Listing titles alone does not pass.
- Add historical valuation context or a clearly labeled substitute and at least two relevant peers when reliable comparable data exists.
- If a key field cannot be verified, write `数据待核验`, explain why, and set the final conclusion to `NEEDS_REVIEW`.
- For every analytical paragraph, apply the replacement test: if another ticker could replace the company name without changing the paragraph, add company-specific evidence or remove it.

### 5. Compute technical summary

- For the three-month window, compute start close, latest close, period return, period high/low with dates, 20-day MA, 60-day MA when available, average turnover or volume, average transaction amount when available, top high-volume days, and a simple 14-day RSI if helpful.
- Interpret structure as public price-volume inference:
  - High-volume rise followed by failure to hold: possible short-term distribution or speculative retreat.
  - High-volume breakout with continued elevated turnover: strong capital contest and possible active-money participation.
  - High-volume down days after a high platform: high-position disagreement and possible profit-taking.
  - Shrinking volume near support: possible stabilization, but require follow-up confirmation.
- For US stocks, include large-cap context where useful: index weight, institutional ownership, short interest trend, options/event volatility, and major earnings/news catalysts.

### 6. Form the research judgment framework

- Add a `研究判断与方法论` section to every report. This section is a research conclusion, not a buy/sell command.
- The judgment must be evidence-based and explain the reasoning chain. Avoid vague labels such as `看好` or `谨慎` without support.
- Use this framework:
  - Fundamental direction: revenue/profit trend, margin trend, cash-flow quality, balance-sheet risk, governance quality.
  - Valuation position: PE/PB/PS/EV metrics where available, historical range, peer comparison, and whether growth can justify valuation.
  - Price/volume confirmation: trend, support/resistance, volume behavior, high-volume up/down days, and whether price confirms the fundamental story.
  - Catalyst and sentiment: earnings, policy, product cycle, industry theme, analyst/institution view, and crowd sentiment where sourceable.
  - Risk-reward framing: upside/base/downside scenarios and the trigger that would invalidate the judgment.
- Use clear non-transaction language:
  - `综合判断`: e.g. `偏积极但需等待确认`, `中性观察`, `高波动成长跟踪`, `风险偏高需复核`.
  - `适合的研究场景`: growth, value, dividend, event-driven, short-term observation, long-term tracking.
  - `观察条件`: what must happen before the view improves.
  - `失效条件`: what would make the view wrong.
  - `方法论说明`: which signals carried the most weight and why.
- If the user asks for buy/sell zones, phrase them as observation zones or risk reference zones with clear caveats, not as direct orders.

The evidence chain must contain at least three company-specific points covering fundamentals, valuation, and price/volume or catalysts. Each upside/base/downside scenario must include measurable triggers. Generic sector language cannot substitute for a company thesis.

### 7. Report structure

Follow this Chinese outline unless the user asks otherwise:

Every section must satisfy the item counts and evidence requirements in `references/legacy_report_contract.md`. Do not shorten or replace the legacy content with a generic table or summary.

1. `一、核心结论`
2. `二、基本面分析`
   - 业务模式
   - 赚钱能力
   - 成长性
   - 偿债与资产质量
   - 现金流质量
   - 公司治理与股东背景
3. `三、估值面分析`
   - PE/PB/PS and relative industry position
   - historical valuation position
   - multi-metric valuation view
   - growth/price match
   - dividend suitability if relevant
4. `四、技术面与近三个月公开量价资金推断`
5. `五、消息与市场情绪`
6. `六、研究判断与方法论`
   - comprehensive judgment
   - evidence chain
   - suitable research scenario
   - upside/base/downside scenarios
   - observation and invalidation conditions
7. `七、风险提示与跟踪要点`
8. `主要数据来源`

### 8. Chart and PDF output

- Generate one recent-three-month price/volume chart per stock. A simple line chart for closing price plus volume bars is sufficient; label the latest data date.
- Let content flow naturally across pages. Do not force section-level page breaks that leave large blank areas. Keep charts within the printable height and re-export if any page has conspicuous unused space.
- Show the trading currency on the chart/report: RMB, USD, or HKD.
- Prefer a stable local pipeline:
  - Build a static HTML report with Chinese fonts such as Microsoft YaHei/SimHei/SimSun.
  - Embed the local chart image.
  - Export to PDF with local Chrome or Edge headless printing.
- If the workspace is read-only, request filesystem approval before creating report files.
- Save one PDF per stock with clear Chinese filenames, for example `中际旭创_股票分析报告.pdf`, `阿里健康_股票分析报告.pdf`, or `特斯拉_股票分析报告.pdf`.
- Generate a sibling quality check file such as `workspace/reports/中际旭创_quality_check.md`.
- Render with `templates/report_template.html` through `scripts/generate_stock_report.py`; do not introduce section-level forced page breaks.

### Semantic quality gate

Extract and inspect the final report text before assigning a quality status:

- Verify company, ticker, exchange, board, risk label, industry, major subsidiary, currency, catalysts, and risks are mutually consistent.
- Fail any unrelated company, board, `ST/*ST`, business model, or copied boilerplate language.
- Require substantive financial, valuation, price/volume, catalyst, observation, and invalidation evidence. Heading presence alone is insufficient.
- Fail unsupported generic phrases such as `制造业需求与产品升级` unless they accurately describe the company and are evidence-backed.
- A semantic mismatch forces `FAIL`; missing depth or unverified key fields forces `NEEDS_REVIEW`.

### PDF Privacy Requirement

When exporting HTML to PDF, the browser default header and footer must be disabled.

If using Chrome or Edge headless printing, use a header/footer-free export option. Prefer:

```text
--no-pdf-header-footer
```

If using Playwright or Puppeteer, set:

```text
displayHeaderFooter: false
```

After PDF generation, run the PDF privacy hard gate against the final exported PDF:

```text
python scripts/scan_pdf_privacy.py path/to/report.pdf
```

The generator must write the scan result to the sibling `quality_check.md`, including extractor, privacy keyword list, hit list, `PDF Privacy Scan`, and final conclusion.

Extract final PDF text with a reliable parser. Use this priority order:

1. PyMuPDF / fitz
2. pypdf
3. pdfminer.six
4. pdftotext / mutool

Scan extracted PDF text for local paths or credential-like keywords:

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

Do not rely only on HTML scanning, SVG scanning, raw zlib stream scanning, or browser export flags.

If any local path or credential-like keyword is found in the generated PDF, `quality_check.md` must mark `PDF Privacy Scan` as `FAIL` and the final conclusion as `FAIL` or `NEEDS_REVIEW`. Do not mark the privacy scan or final conclusion as `PASS`.

If PDF privacy scan passes but key data remains unverified, keep `Final Conclusion: NEEDS_REVIEW`.

Only allow `Final Conclusion: PASS` when PDF privacy scan, forbidden-language scan, numeric validation, and all key data verification pass.


## Quality checks

Every report must include a `quality_check.md` file.

Minimum fields:

- 股票名称、ticker、市场、货币
- 最新完整交易日
- 价格口径是否一致
- 市值计算是否通过
- 涨跌幅计算是否通过
- 三个月区间涨幅是否通过
- 估值指标来源
- 图表文件是否存在
- PDF 文件是否存在且非空
- 是否包含免责声明
- 是否包含数据来源
- 是否发现本地路径、账号、API key、cookie 或隐私信息
- 是否出现禁止词或交易诱导语
- 每个数字校验的原始字段、数据来源、日期、单位、公式、计算结果、来源结果、差异比例和结论
- 数据冲突字段、冲突来源、暂采用口径
- 数据待核验字段
- 最终结论: `PASS` / `NEEDS_REVIEW` / `FAIL`

Before final response:

- Confirm all requested PDFs exist and have nonzero file sizes.
- Confirm each report states the latest market data date.
- Confirm each report has a chart, core conclusion, fundamentals, valuation, technical/public price-volume inference, news/sentiment, research judgment/methodology, risks, and data sources.
- Confirm each research judgment is supported by concrete evidence and includes observation conditions plus invalidation conditions.
- Confirm each report states market, ticker, currency, latest complete trading day, and source limitations if any.
- Confirm the report includes the disclaimer: `仅供学习研究，不构成投资建议`.
- Confirm the report does not expose personal paths, account names, credentials, screenshots, API keys, cookies, tokens, or private files.
- Confirm data sources are cited by name or link, and source content is summarized rather than copied at length.
- If `quality_check.md` is not `PASS`, tell the user what must be reviewed.
- If `scripts/check_report_depth_standard.py` is not `PASS`, tell the user that the report is too shallow and must be deepened before delivery.
- Keep the final response short and link generated PDF files.
