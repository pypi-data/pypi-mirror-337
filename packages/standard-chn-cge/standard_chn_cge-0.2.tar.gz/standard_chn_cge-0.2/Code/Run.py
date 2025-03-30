import numpy as np
import pandas as pd
from scipy import optimize as opt

import Calibration
import Consumer as Cons
import Producer as Prod
import MacroEconomy as Macro
import CGESystem as CGE

sam_table = pd.read_excel(r"D:\OneDriveSyn\OneDrive - The University of Hong Kong - Connect\SynJunex\Project\HKU\CGE\Mix\ICountry-2Input-2Consumer-3Sector-Invest-Trade\Data\SAM.xlsx")
sam_table = sam_table.set_index('Cat')
# Define sets in the model
Ind = ['Pri', 'Sec', 'Ter']
Com = ['Com1', 'Com2', 'Com3']
Hoh = ['Rural', 'Urban']


def execute():

    error_term = 100
    iteration = 0
    max_iteration = 5000
    max_tolerance = 1e-10
    adjust_rate = 0.1

    vars = Calibration.CGE_Data(sam_table, Ind, Com, Hoh)
    params = Calibration.CGE_Param(vars, Ind, Com, Hoh)

    price_armington_array = np.array([1.0, 100.0, 100.0])
    price_agg_factor = params.price_agg_factor
    price_agg_intermediate = params.price_agg_intermediate
    agg_production = vars.agg_production
    armington_good = vars.armington_good
    labour_wage = vars.labour_wage
    capital_rent = vars.capital_rent
    total_hoh_income = vars.total_hoh_income
    labour = vars.labour
    capital = vars.capital

    while (error_term > max_tolerance) & (iteration < max_iteration):
        iteration += 1
        cge_args = [vars, params, Ind, Com, Hoh, agg_production, armington_good, total_hoh_income, price_agg_intermediate,
                    price_agg_factor, labour, capital, labour_wage, capital_rent]

        print('Iteration =', iteration)
        print('Initialized armington price =', price_armington_array)

        results = opt.root(CGE.cge_system, price_armington_array, args=cge_args, method='lm', tol=1e-5)
        price_armington_array = results.x
        price_armington_array[0] = 1.0
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

        price_agg_intermediate = Prod.price_aggregate_intermediate(intermediate, price_armington, agg_intermediate, Ind, Com)
        total_hoh_income = Cons.total_hoh_incomes(params.share_labour_by_hoh, params.share_capital_by_hoh, labour_wage, capital_rent, labour,
                                                  capital, gov_transfer, Ind, Hoh)

        price_armington_process = Prod.price_armington_good(params.scale_prod_armington, params.share_domestic_armington_ces, params.elas_subs_armington,
                                                    price_good_consumer, params.tariff_rate, price_import, Com)
        labour_process = Prod.labour_input_cd(params.share_labour_cd, agg_factor, params.price_agg_factor, vars.labour_wage, Ind)
        capital_process = Prod.capital_input_cd(params.share_capital_cd, agg_factor, params.price_agg_factor, vars.capital_rent, Ind)
        agg_production_process = Prod.total_production(params.scale_prod_ces, params.share_agg_intermediate_ces, agg_intermediate, params.share_agg_factor_ces,
                                                         agg_factor, params.elas_subs_prod, Ind)

        GDP1 = Macro.gdp_use(params.share_production_to_com, price_good_producer, agg_production, price_armington, intermediate, Ind, Com)
        GDP2 = Macro.gdp_value_added(labour, labour_wage, capital, capital_rent, params.tax_rate_production, marginal_cost, agg_production, Ind)
        GDP3 = Macro.gdp_consumption(price_armington, hoh_good, gov_good, invest_good, price_export, export_supply, price_import, params.tariff_rate,
                                     armington_import, vars.inventory, Com, Hoh)

        final_price_armington = price_armington
        final_agg_production = agg_production_process

        processed_model = {}
        for ind in Ind:
            processed_model[ind] = ((agg_production[ind] - agg_production_process[ind]) ** 2) ** (1 / 2)

        distance_iter = sum(processed_model[ind] for ind in Ind)
        print('Distance at iteration', iteration, '=', distance_iter)

        price_armington = (adjust_rate * price_armington_process[c] + (1 - adjust_rate) * price_armington[c] for c in Com)
        labour = (adjust_rate * labour_process[ind] + (1 - adjust_rate) * labour[ind] for ind in Ind)
        capital = (adjust_rate * capital_process[ind] + (1 - adjust_rate) * capital[ind] for ind in Ind)
        total_production = (adjust_rate * agg_production_process[ind] + (1 - adjust_rate) * agg_production[ind] for ind in Ind)

        print("Model solved, price = ", price_armington_array)
        return final_price_armington, hoh_good, gov_good, invest_good, final_agg_production, intermediate, labour, capital, GDP1, GDP2, GDP3

if __name__ == '__main__':
    final_price_armington, hoh_good, gov_good, invest_good, final_agg_production, intermediate, labour, capital, GDP1, GDP2, GDP3 = execute()
    print(final_agg_production)
    print(hoh_good)
    print([GDP1, GDP2, GDP3])
