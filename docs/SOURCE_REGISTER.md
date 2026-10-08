# Source register and accounting choices

All financial data comes from Dixon's official integrated annual reports, retrieved on 8 October 2026. The source values are consolidated Ind AS figures in INR lakh. The model converts them to INR crore. Years refer to financial years ending 31 March.

## Official documents

| Document | Official URL |
|---|---|
| FY2026 report | https://dixon-website.s3.ap-south-1.amazonaws.com/uploads/8afe81b1-4e6c-44c3-84c5-92304ed8c07d-AnnualReportFY2025-26.pdf |
| FY2025 report | https://dixon-website.s3.ap-south-1.amazonaws.com/uploads/efdb9811-daf3-459e-ab6b-60a94aebaa4f-AnnualReport-2024-25.pdf |
| FY2024 report | https://dixon-website.s3.ap-south-1.amazonaws.com/uploads/1745428945732_dixon-annual-report-2023-24.pdf |

The reports were linked from https://www.dixoninfo.com/. They are not redistributed in this repository. A PDF viewer page number can differ from the report's printed page number, so both are recorded below.

## Financial statement locations

| Report | Statement / note | Printed page | PDF viewer page |
|---|---|---:|---:|
| FY2026 | Consolidated balance sheet | 408 | 345 |
| FY2026 | Consolidated profit and loss | 409 | 346 |
| FY2026 | Operating cash flow | 410 | 347 |
| FY2026 | Investing, financing and closing-cash bridge | 411 | 348 |
| FY2026 | Other income, materials purchases and inventory change, notes 37-39 | 458 | 395 |
| FY2025 | Consolidated balance sheet | 322 | 273 |
| FY2025 | Consolidated profit and loss | 323 | 274 |
| FY2025 | Operating cash flow and cash capex | 324 | 275 |
| FY2025 | Financing and closing-cash bridge | 325 | 276 |
| FY2025 | Other income, note 38 | 367 | 318 |
| FY2025 | Materials purchases, note 39 | 368 | 319 |
| FY2024 | Consolidated balance sheet, including FY2023 comparatives | 316 | 270 |
| FY2024 | Consolidated profit and loss, including FY2023 comparatives | 317 | 271 |

FY2026 supplies FY2026 and FY2025 values for the statement lines. FY2025 supplies FY2024 comparatives. FY2024 supplies FY2023 opening references. Key FY2024 and FY2025 revenue and balance-sheet inputs agree across overlapping reports. `data/financials.json` preserves per-metric source references. Purchases use the reported purchases line, not an inference from materials consumed.

## Management's working-capital measure

FY2026 report printed p49, the Vice Chairman's message, reports negative 8 working-capital days. Its footnote says days are calculated on a quarterly basis. It also explains that the message's revenue and EBITDA include other income. These definitions differ from our annual-average proxy and EBITDA excluding all other income.

## Definitions used in the model

| Measure | Definition and limitation |
|---|---|
| Revenue | Revenue from operations, excluding other income |
| Derived operating EBITDA | Revenue less materials consumed, inventory-change expense, employee benefits and other expenses. Excludes all other income, depreciation, finance costs, JV profit and exceptional items |
| Group PAT | Includes non-controlling interests; used with consolidated OCF |
| Materials cost proxy | Materials consumed plus inventory-change expense. Not a disclosed full COGS measure |
| Inventory days | Average total inventory / materials cost proxy x 365 |
| Collection days | Average net trade receivables / revenue x 365. Credit-only sales are not available in the extracted data |
| Supplier days | Average current plus non-current trade payables / raw material and component purchases x 365 |
| Cash-cycle proxy | Inventory days + collection days - supplier days |
| Total WC cash-flow effect | Cash generated before cash tax less cash flow before working-capital changes |
| Cash after cash capex | OCF less reported cash capex outflow. Excludes financing and other investing flows |
| Cash less borrowings | Cash and cash equivalents less current/non-current borrowings. Excludes lease liabilities and other bank balances |

Receivables include reported tax/timing effects; procurement coverage may differ from total trade payables; acquisitions and changes in business mix affect opening/closing averages. The model does not establish actual invoice collection or supplier payment delays.

## Assumptions rather than source facts

All five-day shocks, pilot sales coverage, target collection improvement, financed share, interest rate, implementation costs, annual running costs and benefit-realisation timing are analyst assumptions. They appear in `data/assumptions.json` and the workbook's Assumptions sheet. Intervention hypotheses and proposed implementation dates are not reported Dixon events.

## Verification performed

Checked key latest-year balance-sheet and profit-and-loss figures against rendered source pages. Independently reconciled the three years' balance-sheet identity, profit bridge, OCF/tax bridge and cash roll-forward including group-structure adjustments. Workbook formulas agreed with independent Python outputs for historical ratios, each selected scenario and pilot economics. Tested real zero and missing-input behaviour. Desktop Excel/PowerPoint verification was unavailable.
