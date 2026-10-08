# Learning guide: understand and explain the Dixon case

## Your explanation in plain English

I studied Dixon's public consolidated financial statements for FY2024-FY2026. I separated operating performance from investment-related gains, then examined how inventory, customer payments and supplier payments affect cash. I built an Excel model to test five-day operational changes and evaluated a hypothetical collections pilot. The proposed benefits depend on actually reducing financing costs, so my recommendation is to validate the operational and funding evidence before scaling.

## What each financial statement tells us

The profit and loss statement tells us revenue, expenses and profit over a year. Profit records earnings according to accounting rules, including sales that customers may not have paid yet. The balance sheet shows assets, liabilities and equity at a date. The cash-flow statement explains cash received and spent during the year.

A supplier can provide materials today and accept payment later. That delay funds part of the operating cycle. A customer can owe money on a sale already counted in profit. Inventory can sit on a shelf even though the company paid for it. These timing differences explain why cash and profit differ.

Consolidated means the parent and subsidiaries together. Standalone means the parent alone. We keep the analysis consolidated throughout. Otherwise, a revenue number and the receivables used with it could refer to different businesses.

## Units and source files

The reports use INR lakh. The model uses INR crore. Divide by 100 to convert: 48,87,280 lakh becomes 48,872.80 crore. Do not divide again because a chart label says crore.

`data/financials.json` stores original reported amounts. Each metric has its values and source page references. `Sources & Data!D7:G49` contains those same original inputs. FY2023 is a reference column used to calculate FY2024 growth and opening balance averages. We do not present a full FY2023 cash-flow analysis.

## Profitability calculation

In `Performance!E13:G13`, operating EBITDA equals revenue minus materials consumed, inventory-change expense, employee benefits and other expenses. Depreciation, finance costs, other income, joint-venture profit and exceptional gains are excluded. Operating EBIT then deducts depreciation.

Inventory-change expense is negative when qualifying closing finished goods and work-in-progress exceed opening quantities after reported adjustments. Preserve the sign. Subtracting a negative expense increases EBITDA. Do not change it to a positive cost just because the number appears in brackets.

Our EBITDA measure differs from Dixon's reported EBITDA because the company includes certain other income. Ours deliberately excludes all other income and labels that choice. We can compare our own consistent measure across years without claiming it is the company's official EBITDA.

FY2026's operating EBITDA margin is 1,866.52 / 48,872.80 = 3.82%. FY2024's is 3.94%. The modest narrowing matters, but public statements alone do not establish its operational cause.

## Why the profit bridge matters

`Performance!E22:G22` reconstructs total group PAT:

Operating EBIT + other income - finance costs + joint-venture profit + exceptional gain - tax expense.

The result should match reported group PAT in row 23. PAT attributable to owners in row 24 excludes non-controlling interests. OCF covers the consolidated group, so the cash-conversion ratio uses total group PAT.

FY2025 has an exceptional gain of INR459.98 crore. FY2026 other income contains an equity investment gain of INR670.75 crore. We do not call the full profit increase recurring operating improvement. We also do not subtract pre-tax gains directly from after-tax profit to invent an adjusted PAT.

## Working-capital days

`Performance!E31:G31`: average inventory / materials-based cost proxy x 365.

`Performance!E36:G36`: average net receivables / revenue x 365.

`Performance!E42:G42`: average total trade payables / raw material and component purchases x 365.

`Performance!E43:G43`: inventory days + collection days - supplier days.

Each average is (opening balance + closing balance) / 2. For FY2026, receivables averaged INR6,747.68 crore. Dividing by FY2026 revenue and multiplying by 365 gives 50.4 days.

Our inventory denominator is a proxy because a complete disclosed COGS measure is not available in the extracted statement. Collection days use total revenue as a proxy for credit sales. Payables include all disclosed trade balances while purchases cover materials/components. These coverage differences matter. We do not present these calculations as exact invoice-level turnaround times.

A negative cycle means the calculated supplier payment period exceeds the combined inventory and collection periods. It can be efficient funding. It does not prove late payments or poor supplier treatment.

Management's FY2026 reported cycle is negative 8 days on a quarterly basis. Our annual proxy is negative 4.96 days. We explain the different period and definitions instead of forcing an artificial match.

## Cash conversion and the cash-flow bridge

OCF / group PAT is in `Performance!E25:G25`. It is 1.08x in FY2026 and 0.93x in FY2025. Ratios above one are not automatically a permanent sign of high-quality earnings: working-capital timing and exceptional gains can change the denominator and cash flow.

Cash after cash capex in row 48 equals row 46 minus row 47. FY2026: 1,782.29 - 1,067.51 = INR714.78 crore. This measure leaves out financing and other investing flows, including acquisitions.

Rows 49-57 explain working-capital cash changes. Positive means the statement records a source of cash; negative means cash was used. Total WC effect equals cash generated before tax minus cash flow before WC changes. Trade WC effect sums inventory, receivables and payables adjustments. Other WC effect is the residual of the disclosed total, not an independently observed operational cause.

Closing cash in FY2026 is opening cash plus the net cash change from operating, investing and financing activities plus acquisition/disposal adjustments: 230.85 + 423.60 + 112.98 = INR767.43 crore. Forgetting the group adjustment would create a false reconciliation error.

## The three cash scenarios

`Assumptions!E5` selects one case. CHOOSE picks the active driver. The model always uses the same calculation cells in `Cash Scenarios` rather than separate copies of the model.

Five days of slower collections: annual revenue / 365 x 5 = INR669.49 crore.

Five additional inventory days: annual materials-based cost / 365 x 5 = INR620.24 crore.

Five days of earlier supplier payment: annual purchases / 365 x 5 = INR621.46 crore.

These are whole-business, steady-state sensitivities, assuming evenly spread activity and unchanged volumes/prices. They are not predicted losses. Cash in receivables or inventory is still an asset. Earlier payment changes cash timing rather than creating an equivalent expense.

To combine shocks, select case 4 and change its values in `Assumptions!E14`, `E21` and `E28`. Restore 0, 0 and 5 afterward for the saved default. We test one case at a time. The README and deck contain fixed default comparisons.

## Pilot economics and the decision

Pilot annual sales = 48,872.80 x 2% = INR977.456 crore.

One-time cash release = 977.456 / 365 x 5 = INR13.3898 crore.

Financed cash displaced = 13.3898 x 50% = INR6.6949 crore.

Full annual financing saving = 6.6949 x 10% = INR0.66949 crore.

Year 1 net = 0.66949 x 50% - 0.12 running cost - 0.25 setup = negative INR0.03525 crore, approximately INR3.53 lakh.

Year 2 net = 0.66949 - 0.12 = INR0.54949 crore.

24-month net = Year 1 net + Year 2 net = INR0.51424 crore. ROI = net benefit / (setup + two years' running cost) = 104.9%.

Cash release is excluded from the ROI numerator. Counting it together with interest savings would overstate the economic benefit. The 10% rate, 50% financed share, costs, cohort size and five-day target are analyst assumptions.

Payback treats Year 1's savings as a uniform 50% run rate, then uses the full run rate in Year 2. At the defaults, the initial INR0.25 crore cost has not quite been recovered after 12 months. The remaining INR0.03525 crore takes approximately 0.77 months at the Year 2 net run rate, giving 12.77 months in total. This is simplified timing, not a month-by-month forecast.

24-month break-even funded share is 24.4% at the assumed financing rate. If actual released cash does not replace borrowing, set the financed share to zero. The liquidity release remains, but financing savings become zero and this benefit channel cannot fund the project costs.

## What Excel functions we used

| Function or syntax | Role | Example location |
|---|---|---|
| Direct references | Connect reported inputs and calculations | `Performance!G7` |
| SUM | Add the component cash requirements | `Cash Scenarios!E21` |
| AVERAGE | Calculate opening/closing balance averages | `Performance!G30` |
| CHOOSE | Select one active scenario | `Assumptions!E10` |
| IF | Handle missing inputs and unavailable payback | `Pilot Business Case!E30` |
| ISNUMBER | Keep an empty selected assumption from silently becoming zero | `Assumptions!E10` |
| AND | Check the first-year payback conditions | `Pilot Business Case!E30` |
| Absolute references ($) | Keep shared unit and day conventions fixed | `Performance!G7` |

## What the Python code does

`scripts/analyse.py` reads the two JSON files. `historical()` calculates the annual diagnostic. `scenario()` calculates cash effects. `pilot()` calculates the intervention economics. `verify()` checks accounting reconciliations and boundary cases. `main()` writes the calculated-results JSON and raw CSV.

`argparse` reads the optional --check flag. `json` reads/writes the structured files. `csv` writes the source table. `pathlib` locates files relative to the script, so the analysis can run after the project folder moves. There are no installed third-party dependencies for this script.

Excel changes and JSON changes are separate. Changing the workbook does not edit assumptions.json. Running the script does not rewrite the workbook or presentation. If changing the default case study, update the JSON, recalculate, update the workbook consistently, then update the deck and memo numbers.

## Interview questions

**Why this project?** It connects public financial evidence with operational decisions and cash requirements. It adds Excel modelling and a business case to my existing analytics and market research work.

**Did you work with Dixon?** No. This is independent secondary research using public reports. I did not interview employees or access their invoice ledger.

**Did the company save INR13.39 crore?** No. That is modelled one-time cash release under an assumed pilot. Actual savings have not been achieved or validated.

**Why choose a company with an efficient cash cycle?** The question includes resilience and preserving that funding model. A strong current cycle does not eliminate sensitivity to customer or supplier terms.

**What would you request from a real client?** Invoice dates, acceptance dates, due dates, payment dates, credit notes, dispute codes, customer concentration, supplier terms, purchase schedules, seasonal forecasts and actual marginal borrowing costs.

**How would you prove the pilot worked?** Match comparable treated/untreated invoice cohorts. Adjust for customer and sales mix. Track collection timing, discounts, bad debts and financing balances over enough cycles. Validate that the improvement reduced borrowing rather than only increasing cash held.

**What is your recommendation?** Validate the invoice and financing assumptions, then approve a limited pilot only if the measured economics support it. Avoid a company-wide rollout based only on a public-data sensitivity.
