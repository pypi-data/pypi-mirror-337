import numpy as np
import Calibration as Calibration
import Consumer as Cons
import Producer as Prod
import MacroEconomy as Macro

def cge_system(price_armington_array, args):
    (vars, params, Ind, Com, Hoh, agg_production, armington_good, total_hoh_income, price_agg_intermediate, price_agg_factor, labour, capital, labour_wage, capital_rent) = args
    price_armington = dict(zip(Com, price_armington_array))

    price_import = Prod.price_imports(params.exchange_rate, params.price_word_import, Com)
    price_good_consumer = price_armington
    price_export = price_armington
    price_good_producer = Prod.price_goods_producer(params.scale_prod_transform, params.share_domestic_supply_cet, params.elas_subs_transform,
                                                    price_good_consumer, price_export, Com)
    price_prod_good = Prod.price_production_activity(params.share_production_to_com, price_good_producer, Ind, Com)
    tax_production = Cons.production_tax_revenue(params.tax_rate_production, agg_production, price_prod_good, Ind)
    price_agg_factor = Prod.price_aggregate_factor(params.scale_factor_cd, labour_wage, capital_rent, params.share_labour_cd, params.share_capital_cd, Ind)
    marginal_cost = Prod.marginal_prod_cost(params.scale_prod_ces, params.share_agg_intermediate_ces, params.elas_subs_prod, price_agg_intermediate,
                                            params.share_agg_factor_ces, price_agg_factor, Ind)
    agg_intermediate = Prod.agg_intermediate_input_ces(agg_production, params.scale_prod_ces, params.share_agg_intermediate_ces,
                                                       marginal_cost, price_agg_intermediate, params.elas_subs_prod, Ind)
    intermediate = Prod.intermediate_input_leontief(params.share_intermediate_leontief, agg_intermediate, Ind, Com)
    armington_import = Prod.consumed_import_armington(armington_good, params.share_domestic_armington_ces, params.scale_prod_armington, price_armington,
                                                      price_import, params.elas_subs_armington, params.tariff_rate, Com)
    tariff_revenue = Cons.tariff_import_revenue(params.tariff_rate, armington_import, price_import, Com)
    tax_income = Cons.income_tax_revenue(params.tax_rate_income, total_hoh_income, Hoh)
    total_gov_income = Cons.total_gov_incomes(tax_production, tariff_revenue, tax_income, Ind, Com, Hoh)
    gov_transfer = Cons.gov_transfers(params.transfer_rate_hoh, total_gov_income, Hoh)
    hoh_good = Cons.hoh_good_cd(params.share_hoh_utility_cd, total_hoh_income, price_armington, Hoh, Com)
    gov_good = Cons.gov_good_cd(params.share_gov_utility_cd, total_gov_income, price_armington, Com)
    gov_saving = Cons.gov_savings(params.saving_rate_gov, total_gov_income)
    hoh_saving = Cons.hoh_savings(params.saving_rate_hoh, total_hoh_income, Hoh)
    total_saving = Cons.total_savings(hoh_saving, gov_saving, Hoh)
    total_invest = Cons.total_investment(total_saving)
    invest_good = Cons.investment_goods(params.share_inv_utility_cd, total_invest, price_armington, Com)
    total_invest_inventory = Cons.total_investment_inventory(params.share_inv_inventory, total_invest)
    invest_inventory = Cons.investment_inventory(params.share_inv_inventory_good, total_invest_inventory, price_armington, Com)
    armington_good = Prod.armington_goods(intermediate, hoh_good, gov_good, invest_good, invest_inventory, Ind, Com, Hoh)
    agg_factor = Prod.agg_factor_input_ces(agg_production, params.scale_prod_ces, params.share_agg_factor_ces,
                                           marginal_cost, price_agg_factor, params.elas_subs_prod, Ind)

    labour_wage = Prod.price_labour(labour, vars.total_labour, Ind)
    capital_rent = Prod.price_capital(capital, vars.total_capital, Ind)
    hoh_utility = Cons.hoh_utility_cd(params.scale_hoh_utility_cd, params.share_hoh_utility_cd, hoh_good, Hoh, Com)
    produced_good = Prod.ind_to_commodity(params.share_production_to_com, agg_production, Ind, Com)
    domestic_supply = Prod.domestic_supply_commodity_cet(produced_good, params.scale_prod_transform, params.share_domestic_supply_cet,
                                                         price_good_producer, price_good_consumer, params.elas_subs_transform, Com)
    export_supply = Prod.export_supply_commodity_cet(produced_good, params.scale_prod_transform, params.share_domestic_supply_cet,
                                                     price_good_producer, price_export, params.elas_subs_transform, Com)
    armington_domestic = Prod.consumed_domestic_armington(armington_good, params.share_domestic_armington_ces, params.scale_prod_armington,
                                                          price_armington, price_good_consumer, params.elas_subs_armington, Com)
    invest_foreign = Cons.investment_foreign(invest_good, total_invest, total_invest_inventory, Com)
    foreign_inventory = Cons.foreign_owned_inventory(params.share_foreign_inventory, total_invest_inventory)

    trade_world_error = Macro.trade_balance(price_export, export_supply, price_import, armington_import, invest_foreign, foreign_inventory, Com)

    good_error = Macro.commodity_clearing(params.share_production_to_com, agg_production, armington_import, marginal_cost, params.tax_rate_production, price_import,
                                          intermediate, price_armington, params.tariff_rate, export_supply, price_export, hoh_good, gov_good, invest_good, vars.inventory, Ind, Com, Hoh)

    price_agg_intermediate = Prod.price_aggregate_intermediate(intermediate, price_armington, agg_intermediate, Ind, Com)
    total_hoh_income = Cons.total_hoh_incomes(params.share_labour_by_hoh, params.share_capital_by_hoh, labour_wage, capital_rent, labour,
                                              capital, gov_transfer, Ind, Hoh)

    error_labour = Macro.labour_clearing(labour, vars.total_labour, Ind)
    error_capital = Macro.capital_clearing(capital, vars.total_capital, Ind)
    error_good = Macro.commodity_clearing(params.share_production_to_com, agg_production, armington_import, marginal_cost, params.tax_rate_production, price_import,
                                              intermediate, price_armington, params.tariff_rate, export_supply, price_export, hoh_good, gov_good, invest_good, vars.inventory, Ind, Com, Hoh)

    error_commodity = [error_good[cc] for cc in Com]
    error_list = np.append(error_commodity, [error_labour, error_capital])
    return error_list