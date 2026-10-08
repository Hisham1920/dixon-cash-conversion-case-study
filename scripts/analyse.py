import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_inputs():
    data = json.loads((ROOT / 'data/financials.json').read_text())
    assumptions = json.loads((ROOT / 'data/assumptions.json').read_text())
    figures = {
        year: {m['key']: m['values'][i] / 100 if m['values'][i] is not None else None
               for m in data['metrics']}
        for i, year in enumerate(data['years'])
    }
    return data, assumptions, figures


def historical(figures, days):
    result = {}
    for year in (2024, 2025, 2026):
        x, prior = figures[year], figures[year - 1]
        material_cost = x['materials'] + x['inventory_change']
        payables = sum(x[k] for k in ('payables_mse', 'payables_other', 'payables_noncurrent'))
        prior_payables = sum(prior[k] for k in ('payables_mse', 'payables_other', 'payables_noncurrent'))
        ebitda = x['revenue'] - material_cost - x['employees'] - x['other_expenses']
        dio = (prior['inventory'] + x['inventory']) / 2 / material_cost * days
        dso = (prior['receivables'] + x['receivables']) / 2 / x['revenue'] * days
        dpo = (prior_payables + payables) / 2 / x['purchases'] * days
        wc = x['cash_generated'] - x['pre_wc_cash']
        trade_wc = sum(x[k] for k in ('cf_inventory', 'cf_receivables', 'cf_payables_current', 'cf_payables_noncurrent'))
        result[year] = dict(
            revenue=x['revenue'], growth=x['revenue'] / prior['revenue'] - 1,
            operating_ebitda=ebitda, operating_margin=ebitda / x['revenue'],
            operating_ebit=ebitda - x['depreciation'], material_cost_proxy=material_cost,
            pat_total=x['pat_total'], pat_owners=x['pat_owners'],
            ocf=x['ocf'], ocf_to_pat=x['ocf'] / x['pat_total'],
            cash_capex=x['cash_capex'], cash_after_capex=x['ocf'] - x['cash_capex'],
            inventory_days=dio, collection_days=dso, supplier_days=dpo,
            cash_cycle_proxy=dio + dso - dpo,
            trade_working_capital=x['inventory'] + x['receivables'] - payables,
            working_capital_cf=wc, trade_working_capital_cf=trade_wc,
            other_working_capital_cf=wc - trade_wc,
            net_cash_excluding_leases=x['cash'] - x['debt_noncurrent'] - x['debt_current'],
            current_ratio=x['current_assets'] / x['current_liabilities'],
            earnings_adjustments=x['other_income'] + x['exceptional_gain'] + x['jv_profit'],
        )
    return result


def scenario(x, case, days):
    effects = dict(
        collection_cash=x['revenue'] / days * case['collection_delay_days'],
        inventory_cash=(x['materials'] + x['inventory_change']) / days * case['inventory_additional_days'],
        supplier_cash=x['purchases'] / days * case['supplier_days_reduction'],
    )
    effects['total_cash_required'] = sum(effects.values())
    effects['share_of_reported_cash'] = effects['total_cash_required'] / x['cash']
    return effects


def pilot(x, p, days):
    for key in ('sales_scope', 'financed_share', 'year_one_benefit_realisation'):
        if not 0 <= p[key] <= 1:
            raise ValueError(f'{key} must be between 0 and 1')
    if any(p[k] < 0 for k in p):
        raise ValueError('Pilot assumptions must be non-negative')
    sales = x['revenue'] * p['sales_scope']
    release = sales / days * p['collection_days_reduction']
    annual_benefit = release * p['financed_share'] * p['annual_financing_rate']
    year_one_net_before_setup = annual_benefit * p['year_one_benefit_realisation'] - p['annual_running_cost_crore']
    annual_net = annual_benefit - p['annual_running_cost_crore']
    setup = p['implementation_cost_crore']
    if setup == 0:
        payback = 0
    elif year_one_net_before_setup > 0 and setup <= year_one_net_before_setup:
        payback = setup / year_one_net_before_setup * 12
    elif annual_net > 0:
        payback = 12 + (setup - year_one_net_before_setup) / annual_net * 12
    else:
        payback = None
    horizon_cost = setup + 2 * p['annual_running_cost_crore']
    horizon_benefit = annual_benefit * (p['year_one_benefit_realisation'] + 1)
    funded_denominator = release * p['annual_financing_rate'] * (p['year_one_benefit_realisation'] + 1)
    return dict(
        pilot_sales=sales, one_time_cash_release=release,
        financed_cash_displaced=release * p['financed_share'],
        annual_financing_saving=annual_benefit, annual_net_saving=annual_net,
        year_one_net=year_one_net_before_setup - setup,
        two_year_net=horizon_benefit - horizon_cost,
        two_year_roi=(horizon_benefit - horizon_cost) / horizon_cost if horizon_cost else None,
        payback_months=payback,
        funded_share_break_even_24m=horizon_cost / funded_denominator if funded_denominator else None,
    )


def verify(figures, history, assumptions):
    for year in (2024, 2025, 2026):
        x, h = figures[year], history[year]
        assert abs(x['total_assets'] - x['total_equity'] - x['total_liabilities']) < .011
        assert abs(x['ocf'] - x['cash_generated'] + x['cash_tax']) < .011
        assert abs(x['cash_opening'] + x['net_cash_change'] + x['group_cash_adjustment'] - x['cash']) < .011
        assert abs(x['ocf'] + x['investing_cf'] + x['financing_cf'] - x['net_cash_change']) < .011
        calculated_pat = h['operating_ebit'] + x['other_income'] - x['finance_costs'] + x['jv_profit'] + x['exceptional_gain'] - x['tax_expense']
        assert abs(calculated_pat - x['pat_total']) < .011
    x = figures[2026]
    baseline = scenario(x, assumptions['cases'][0], assumptions['days_per_year'])
    assert baseline['total_cash_required'] == 0
    delayed = scenario(x, assumptions['cases'][1], assumptions['days_per_year'])
    assert abs(delayed['total_cash_required'] - x['revenue'] / 365 * 5) < 1e-9
    p = dict(assumptions['pilot'], financed_share=0)
    result = pilot(x, p, 365)
    assert result['annual_financing_saving'] == 0
    assert result['payback_months'] is None
    assert result['two_year_net'] < 0
    p = dict(assumptions['pilot'], collection_days_reduction=0)
    assert pilot(x, p, 365)['one_time_cash_release'] == 0


def main():
    parser = argparse.ArgumentParser(description='Recalculate the Dixon case study using standard-library Python.')
    parser.add_argument('--check', action='store_true', help='Run financial reconciliation and scenario boundary checks.')
    args = parser.parse_args()
    data, assumptions, figures = load_inputs()
    history = historical(figures, assumptions['days_per_year'])
    if args.check:
        verify(figures, history, assumptions)
        print('Financial reconciliations and scenario boundary checks passed.')
    output = dict(
        as_of=data['as_of'], units='INR crore unless days, percentages or multiples',
        historical=history,
        scenarios=[dict(name=c['name'], **scenario(figures[2026], c, assumptions['days_per_year'])) for c in assumptions['cases']],
        pilot=pilot(figures[2026], assumptions['pilot'], assumptions['days_per_year']),
    )
    (ROOT / 'data/calculated_results.json').write_text(json.dumps(output, indent=2))
    with (ROOT / 'data/reported_financials.csv').open('w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['metric', 'label', 'FY2023_reference_lakh', 'FY2024_lakh', 'FY2025_lakh', 'FY2026_lakh'])
        for m in data['metrics']:
            writer.writerow([m['key'], m['label'], *m['values']])
    print(json.dumps(output['pilot'], indent=2))


if __name__ == '__main__':
    main()
