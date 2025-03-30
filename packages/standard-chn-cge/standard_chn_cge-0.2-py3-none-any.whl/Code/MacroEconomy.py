

def trade_balance(price_export, export_supply_cet, price_import, armington_import_ces, invest_foreign, foreign_inventory, Com):
    trade_world_error = sum(price_export[c] * export_supply_cet[c] for c in Com) - sum(price_import[c] * armington_import_ces[c] for c in Com) - invest_foreign - foreign_inventory
    return trade_world_error


def gdp_use(share_production_to_com, price_good_producer, agg_production, price_armington, intermediate, Ind, Com):
    gdp1 = sum(share_production_to_com[ind, c] * price_good_producer[c] * agg_production[ind] for ind in Ind for c in Com) - sum(
                intermediate[c, ind] * price_armington[c] for ind in Ind for c in Com)
    return gdp1


def gdp_value_added(labour, labour_wage, capital, capital_rent, tax_rate_production, marginal_cost, agg_production, Ind):
    gdp2 = sum(labour_wage * labour[ind] + capital_rent * capital[ind] for ind in Ind) + sum(tax_rate_production[ind] * marginal_cost[ind]
                                / (1 - tax_rate_production[ind]) * agg_production[ind] for ind in Ind)
    return gdp2


def gdp_consumption(price_armington, hoh_good, gov_good, invest_good, price_export, export_supply, price_import, tariff_rate, armington_import, inventory, Com, Hoh):
    gdp3 = sum(price_armington[c] * (sum(hoh_good[h, c] for h in Hoh) + gov_good[c] + invest_good[c] + inventory[c]) for c in Com) + sum(
                price_export[c] * export_supply[c] for c in Com) - sum((1 + tariff_rate[c]) * price_import[c] * armington_import[c] for c in Com)
    return gdp3


def commodity_clearing(share_production_to_com, agg_production, armington_import, marginal_cost, tax_rate_production, price_import, intermediate, price_armington, tariff_rate, export_supply, price_export, hoh_good, gov_good, invest_good, inventory, Ind, Com, Hoh):
    error_commodity = {}
    for c in Com:
        error_commodity[c] = sum(share_production_to_com[ind, c] * marginal_cost[ind] / (1 - tax_rate_production[ind]) * agg_production[ind] for ind in Ind) + (1 + tariff_rate[c]) * price_import[c] * armington_import[c] - (
                                sum(price_armington[c] * intermediate[c, ind] for ind in Ind) + price_export[c] * export_supply[c] + price_armington[c] * (sum(hoh_good[h, c] for h in Hoh) + gov_good[c] + invest_good[c] + inventory[c]))
    return error_commodity


def labour_clearing(labour, total_labour, Ind):
    error_labour = sum(labour[ind] for ind in Ind) - total_labour
    return error_labour


def capital_clearing(capital, total_capital, Ind):
    error_capital = sum(capital[ind] for ind in Ind) - total_capital
    return error_capital