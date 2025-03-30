

def agg_intermediate_input_ces(total_production, scale_prod_ces, share_agg_intermediate_ces, marginal_cost, price_agg_intermediate, elas_subs_prod, Ind):
    agg_intermediate_ces = {}
    for ind in Ind:
        agg_intermediate_ces[ind] = total_production[ind] / scale_prod_ces[ind] * (share_agg_intermediate_ces[ind]
                                                                                         * scale_prod_ces[ind] * marginal_cost[ind] / price_agg_intermediate[ind]) ** elas_subs_prod[ind]
    return agg_intermediate_ces


def agg_factor_input_ces(total_production, scale_prod_ces, share_agg_labour_ces, marginal_cost, price_agg_factor, elas_subs_prod, Ind):
    agg_factor_ces = {}
    for ind in Ind:
        agg_factor_ces[ind] = total_production[ind] / scale_prod_ces[ind] * (share_agg_labour_ces[ind]
                                                                                         * scale_prod_ces[ind] * marginal_cost[ind] / price_agg_factor[ind]) ** elas_subs_prod[ind]
    return agg_factor_ces


def intermediate_input_leontief(share_intermediate_leontief, agg_intermediate_ces, Ind, Com):
    intermediate_leontief = {}
    for ind in Ind:
        for c in Com:
            intermediate_leontief[c, ind] = share_intermediate_leontief[c, ind] * agg_intermediate_ces[ind]
    return intermediate_leontief


def labour_input_cd(share_labour_cd, agg_factor_ces, price_agg_factor, labour_wage, Ind):
    labour_cd = {}
    for ind in Ind:
        labour_cd[ind] = share_labour_cd[ind] * agg_factor_ces[ind] * price_agg_factor[ind] / labour_wage
    return labour_cd


def capital_input_cd(share_capital_cd, agg_factor_ces, price_agg_factor, capital_rent, Ind):
    capital_input_cd = {}
    for ind in Ind:
        capital_input_cd[ind] = share_capital_cd[ind] * agg_factor_ces[ind] * price_agg_factor[ind] / capital_rent
    return capital_input_cd


def ind_to_commodity(share_production_to_com, agg_production, Ind, Com):
    produced_good = {}
    for c in Com:
        produced_good[c] = sum(share_production_to_com[ind, c] * agg_production[ind] for ind in Ind)
    return produced_good


def domestic_supply_commodity_cet(produced_good, scale_prod_transform, share_domestic_supply_cet, price_good_producer, price_good_consumer, elas_subs_transform, Com):
    domestic_supply_cet = {}
    for c in Com:
        domestic_supply_cet[c] = produced_good[c] / scale_prod_transform[c] * ((share_domestic_supply_cet[c] *
                                                                                price_good_producer[c] * scale_prod_transform[c] / price_good_consumer[c]) ** elas_subs_transform[c])
    return domestic_supply_cet


def export_supply_commodity_cet(produced_good, scale_prod_transform, share_domestic_supply_cet, price_good_producer, price_export, elas_subs_transform, Com):
    export_supply_cet = {}
    for c in Com:
        export_supply_cet[c] = produced_good[c] / scale_prod_transform[c] * (((1-share_domestic_supply_cet[c]) *
                                                                               price_good_producer[c] * scale_prod_transform[c] / price_export[c]) ** elas_subs_transform[c])
    return export_supply_cet


def consumed_domestic_armington(armington_good, share_domestic_armington_ces, scale_prod_armington, price_armington, price_good_consumer, elas_subs_armington, Com):
    armington_domestic = {}
    for c in Com:
        armington_domestic[c] = armington_good[c] / scale_prod_armington[c] * (share_domestic_armington_ces[c] *
                                                                              scale_prod_armington[c] * price_armington[c] / price_good_consumer[c]) ** elas_subs_armington[c]
    return armington_domestic


def consumed_import_armington(armington_good, share_domestic_armington_ces, scale_prod_armington, price_armington, price_import, elas_subs_armington, tariff_rate, Com):
    armington_import_ces = {}
    for c in Com:
        armington_import_ces[c] = armington_good[c] / scale_prod_armington[c] * ((1-share_domestic_armington_ces[c]) * scale_prod_armington[c] * price_armington[c] /
                                                                                 (1 + tariff_rate[c]) * price_import[c]) ** elas_subs_armington[c]
    return armington_import_ces


def price_imports(exchange_rate, price_word_import, Com):
    price_import = {}
    for c in Com:
        price_import[c] = exchange_rate * price_word_import[c]
    return price_import


def price_exports(exchange_rate, price_word_export, Com):
    price_export = {}
    for c in Com:
        price_export[c] = exchange_rate * price_word_export[c]
    return price_export


def armington_goods(intermediate_leontief, hoh_good_cd, gov_good_cd, invest_good, invest_inventory, Ind, Com, Hoh):
    armington_good = {}
    for c in Com:
        armington_good[c] = sum(intermediate_leontief[c, ind] for ind in Ind) + sum(hoh_good_cd[h, c] for h in Hoh) + gov_good_cd[c] + invest_good[c] + invest_inventory[c]
    return armington_good


def price_production_activity(share_production_to_com, price_good_producer, Ind, Com):
    price_prod_good = {}
    for ind in Ind:
        price_prod_good[ind] = sum(share_production_to_com[ind, cc] * price_good_producer[cc] for cc in Com)
    return price_prod_good


def price_aggregate_intermediate(intermediate_leontief, price_armington, agg_intermediate_ces, Ind, Com):
    price_agg_intermediate = {}
    for ind in Ind:
        price_agg_intermediate[ind] = sum(intermediate_leontief[c, ind] * price_armington[c] for c in Com) / agg_intermediate_ces[ind]
    return price_agg_intermediate


def price_aggregate_factor(scale_factor_cd, labour_wage, capital_rent, share_labour_cd, share_capital_cd, Ind):
    price_agg_factor_cd = {}
    for ind in Ind:
        price_agg_factor_cd[ind] = 1 / scale_factor_cd[ind] * (labour_wage / share_labour_cd[ind]) ** share_labour_cd[ind] * (capital_rent / share_capital_cd[ind]) ** share_capital_cd[ind]
    return price_agg_factor_cd


def price_goods_producer(scale_prod_transform, share_domestic_supply_cet, elas_subs_transform, price_good_consumer, price_export, Com):
    price_good_producer = {}
    for c in Com:
        price_good_producer[c] = (1 / scale_prod_transform[c]) * (share_domestic_supply_cet[c] ** elas_subs_transform[c] * price_good_consumer[c] ** (1 - elas_subs_transform[c])
                                                                  + (1 - share_domestic_supply_cet[c]) ** elas_subs_transform[c] * price_export[c] ** (1 - elas_subs_transform[c])) ** (1 / (1 - elas_subs_transform[c]))
    return price_good_producer


def price_armington_good(scale_prod_armington, share_domestic_armington_ces, elas_subs_armington, price_good_consumer, tariff_rate, price_import, Com):
    price_armington = {}
    for c in Com:
        price_armington[c] = (1 / scale_prod_armington[c]) * (share_domestic_armington_ces[c] ** elas_subs_armington[c] * price_good_consumer[c] ** (1 - elas_subs_armington[c])
                                                                  + (1 - share_domestic_armington_ces[c]) ** elas_subs_armington[c] * ((1 + tariff_rate[c]) * price_import[c]) ** (1 - elas_subs_armington[c])) ** (1 / (1 - elas_subs_armington[c]))
    return price_armington


def price_labour(labour_input, total_labour, Ind):
    labour_wage = total_labour / sum(labour_input[ind] for ind in Ind)
    return labour_wage


def price_capital(capital_input, total_capital, Ind):
    capital_rent = total_capital / sum(capital_input[ind] for ind in Ind)
    return capital_rent


def marginal_prod_cost(scale_prod_ces, share_agg_intermediate_ces, elas_subs_prod, price_agg_intermediate, share_agg_factor_ces, price_agg_factor, Ind):
    marginal_cost_ces = {}
    for ind in Ind:
        marginal_cost_ces[ind] = 1 / scale_prod_ces[ind] * ((share_agg_intermediate_ces[ind] ** elas_subs_prod[ind] * price_agg_intermediate[ind] ** (1 - elas_subs_prod[ind])
                                     + share_agg_factor_ces[ind] ** elas_subs_prod[ind] * price_agg_factor[ind] ** (1 - elas_subs_prod[ind])) ** (1 / (1 - elas_subs_prod[ind])))
    return marginal_cost_ces


def total_production(scale_prod_ces, share_agg_intermediate_ces, agg_intermediate, share_agg_factor_ces, value_added, elasticity_subs_prod, Ind):
    total_production = {}
    for ind in Ind:
        total_production[ind] = scale_prod_ces[ind] * (share_agg_intermediate_ces[ind] * agg_intermediate[ind] ** (1 - 1 / elasticity_subs_prod[ind]) +
                                                       share_agg_factor_ces[ind] * value_added[ind] ** (1 - 1 / elasticity_subs_prod[ind])) ** (
                                                        elasticity_subs_prod[ind] / (elasticity_subs_prod[ind] - 1))
    return total_production


# Extra functions
def price_commodity_to_marginal_cost(share_production_to_com, price_domestic_armington, production_tax_rate, Ind, Com):
    marginal_prod_cost = {}
    for ind in Ind:
        marginal_prod_cost[ind] = sum(share_production_to_com[ind, c] * price_domestic_armington[c] for c in Com) * (1 - production_tax_rate[ind])
    return marginal_prod_cost


def labour_demand(total_production, scale_prod_ces, share_labour_prod, marginal_cost, wage_labour, elas_subs_prod, Ind):
    labour_input = {}
    for ind in Ind:
        labour_input[ind] = total_production[ind] / scale_prod_ces[ind] * (share_labour_prod[ind] *
                              scale_prod_ces[ind] * marginal_cost[ind] / wage_labour[ind])**elas_subs_prod[ind]
    return labour_input

def capital_demand(total_production, scale_prod_ces, share_capital_prod, marginal_cost, rent_capital, elas_subs_prod, Ind):
    capital_input = {}
    for ind in Ind:
        capital_input[ind] = total_production[ind] / scale_prod_ces[ind] * (share_capital_prod[ind] *
                                                                     scale_prod_ces[ind] * marginal_cost[ind] / rent_capital[ind])**elas_subs_prod[ind]
    return capital_input


def armington_commodity(scale_prod_armington, share_armington_prod, consumed_domestic, consumed_import, elas_subs_armington, Com):
    armington_commodity = {}
    for c in Com:
        armington_commodity[c] = scale_prod_armington[c] * (share_armington_prod[c] * consumed_domestic[c] ** (1-1/elas_subs_armington[c]) +
                                                           (1-share_armington_prod[c]) * consumed_import[c] ** (1-1/elas_subs_armington[c]))**(elas_subs_armington[c]/(elas_subs_armington[c]-1))
    return armington_commodity