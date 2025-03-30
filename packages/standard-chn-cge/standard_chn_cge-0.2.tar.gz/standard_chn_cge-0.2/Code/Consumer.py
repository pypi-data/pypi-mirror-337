import numpy as np


def hoh_good_cd(share_hoh_utility_cd, total_hoh_income, price_armington, Hoh, Com):
    hoh_demand_cd = {}
    for h in Hoh:
        for c in Com:
            hoh_demand_cd[h, c] = share_hoh_utility_cd[h, c] * total_hoh_income[h] / price_armington[c]
    return hoh_demand_cd


def gov_good_cd(share_gov_utility_cd, total_gov_income, price_armington, Com):
    gov_demand_cd = {}
    for c in Com:
        gov_demand_cd[c] = share_gov_utility_cd[c] * total_gov_income / price_armington[c]
    return gov_demand_cd


def hoh_utility_cd(scale_hoh_utility_cd, share_hoh_utility_cd, hoh_demand_cd, Hoh, Com):
    utility_hoh_cd = {}
    for h in Hoh:
        utility_hoh_cd[h] = scale_hoh_utility_cd[h] * np.prod([hoh_demand_cd[h, c] ** share_hoh_utility_cd[h, c] for c in Com])
    return utility_hoh_cd


def total_hoh_incomes(share_labour_by_hoh, share_capital_by_hoh, labour_wage, capital_rent, labour_cd, capital_cd, gov_transfer, Ind, Hoh):
    total_hoh_income = {}
    for h in Hoh:
        total_hoh_income[h] = share_labour_by_hoh[h] * labour_wage * sum(labour_cd[ind] for ind in Ind) + share_capital_by_hoh[h] * capital_rent * sum(capital_cd[ind] for ind in Ind) + gov_transfer[h]
    return total_hoh_income


def total_gov_incomes(production_tax, tariff_revenue, tax_income, Ind, Com, Hoh):
    total_gov_income = sum(production_tax[ind] for ind in Ind) + sum(tariff_revenue[c] for c in Com) + sum(tax_income[h] for h in Hoh)
    return total_gov_income


def hoh_savings(saving_rate_hoh, total_hoh_income, Hoh):
    hoh_saving = {}
    for h in Hoh:
        hoh_saving[h] = saving_rate_hoh[h] * total_hoh_income[h]
    return hoh_saving


def gov_savings(saving_rate_gov, total_gov_income):
    gov_saving = saving_rate_gov * total_gov_income
    return gov_saving


def gov_transfers(transfer_rate_hoh, total_gov_income, Hoh):
    gov_transfer = {}
    for h in Hoh:
        gov_transfer[h] = transfer_rate_hoh[h] * total_gov_income
    return gov_transfer


def total_savings(hoh_saving, gov_saving, Hoh):
    total_saving = sum(hoh_saving[h] for h in Hoh) + gov_saving
    return total_saving


def total_investment(total_saving):
    total_invest = total_saving
    return total_invest


def investment_goods(share_inv_utility_cd, total_invest, price_armington, Com):
    invest_good = {}
    for c in Com:
        invest_good[c] = share_inv_utility_cd[c] * total_invest / price_armington[c]
    return invest_good


def total_investment_inventory(share_inv_inventory, total_invest):
    total_invest_inventory = share_inv_inventory * total_invest
    return total_invest_inventory


def investment_foreign(invest_goods, total_invest, invest_inventory, Com):
    invest_foreign = total_invest - sum(invest_goods[c] for c in Com) - invest_inventory
    return invest_foreign


def investment_inventory(share_inv_inventory_good, total_invest_inventory, price_armington, Com):
    invest_inventory = {}
    for c in Com:
        invest_inventory[c] = share_inv_inventory_good[c] * total_invest_inventory / price_armington[c]
    return invest_inventory


def foreign_owned_inventory(share_foreign_inventory, total_invest_inventory):
    foreign_inventory = share_foreign_inventory * total_invest_inventory
    return foreign_inventory


def production_tax_revenue(tax_rate_production, agg_production, price_prod_good, Ind):
    production_tax = {}
    for ind in Ind:
        production_tax[ind] = tax_rate_production[ind] * agg_production[ind] * price_prod_good[ind]
    return production_tax


def tariff_import_revenue(tariff_rate, armington_import_ces, price_import, Com):
    tariff_revenue = {}
    for c in Com:
        tariff_revenue[c] = tariff_rate[c] * armington_import_ces[c] * price_import[c]
    return tariff_revenue


def income_tax_revenue(tax_rate_income, total_hoh_income, Hoh):
    tax_income = {}
    for h in Hoh:
        tax_income[h] = tax_rate_income[h] * total_hoh_income[h]
    return tax_income



def household_consumption_ces(share_hoh_utility, price_domestic_armington, elas_subs_utility, price_utility, scale_utility, saving_rate_hoh, household_income, Com):
    household_demand = {}
    for c in Com:
        household_demand[c] = (share_hoh_utility[c] * scale_utility * price_utility / price_domestic_armington[c]) ** elas_subs_utility * (1-saving_rate_hoh) * household_income / (price_utility * scale_utility)
    return household_demand

def consumer_utility(scale_utility, share_hoh_utility, household_demand, elas_subs_utility, Com):
    utility_hoh = scale_utility * sum(share_hoh_utility[c] * (household_demand[c]**(1-1/elas_subs_utility))
                                              for c in Com)**(elas_subs_utility/(elas_subs_utility-1))
    return utility_hoh

def total_value_added(wage_labour, labour_input, rent_capital, capital_input, Ind):
    value_added = sum(wage_labour[ind]*labour_input[ind] + rent_capital[ind]*capital_input[ind] for ind in Ind)
    return value_added

def price_utility(scale_hoh_utility, share_hoh_utility, elas_subs_utility, price_domestic_armington, Com):
    price_util = (1/scale_hoh_utility) * sum(share_hoh_utility[c]**elas_subs_utility * price_domestic_armington[c]**(1-elas_subs_utility) for c in Com)**(1/(1-elas_subs_utility))
    return price_util

def agg_final_demand(household_demand, government_demand, Com):
    total_final_demand = sum(household_demand[c] + government_demand[c] for c in Com)
    return total_final_demand



