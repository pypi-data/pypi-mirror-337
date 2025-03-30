import numpy as np
import pandas as pd

class CGE_Data(object):
    def __init__(self, sam, Ind, Com, Hoh):
        # Intermediate input
        self.intermediate = sam.loc[Com, Ind]
        self.intermediate = self.intermediate.stack().to_dict()
        self.agg_intermediate = {}
        for ind in Ind:
            self.agg_intermediate[ind] = sum(self.intermediate[c, ind] for c in Com)
        # Labour input
        self.labour = sam.loc['Lab', Ind]
        self.labour = self.labour.to_dict()
        self.total_labour = sum(self.labour[ind] for ind in Ind)
        self.labour_wage = sum(self.labour[ind] for ind in Ind) / self.total_labour
        # Capital input
        self.capital = sam.loc['Cap', Ind]
        self.capital = self.capital.to_dict()
        self.total_capital = sum(self.capital[ind] for ind in Ind)
        self.capital_rent = 0.15
        # Value added
        self.value_added = {}
        for ind in Ind:
            self.value_added[ind] = self.labour[ind] + self.capital[ind]

        # Production tax:
        self.tax_production = sam.loc['Gov', Ind]
        self.tax_production = self.tax_production.to_dict()
        # Tariff revenue
        self.tariff_revenue = sam.loc['Gov', Com]
        self.tariff_revenue = self.tariff_revenue.to_dict()
        # Income tax
        self.tax_income = sam.loc['Gov', Hoh]
        self.tax_income = self.tax_income.to_dict()

        # Household's demand
        self.hoh_good = sam.loc[Com, Hoh].T
        self.hoh_good = self.hoh_good.stack().to_dict()
        # Government's demand
        self.gov_good = sam.loc[Com, 'Gov']
        self.gov_good = self.gov_good.to_dict()
        # Inventory
        self.inventory = sam.loc[Com, 'Inventory']
        self.inventory = self.inventory.to_dict()
        # Foreign-owned inventory
        self.foreign_inventory = sam.loc['Foreign', 'Inventory']

        # Household's savings:
        self.hoh_saving = sam.loc['Sav/Invest', Hoh]
        self.hoh_saving = self.hoh_saving.to_dict()
        # Government's savings:
        self.gov_saving = sam.loc['Sav/Invest', 'Gov']
        # Total savings:
        self.total_saving = sum(self.hoh_saving[h] for h in Hoh) + self.gov_saving

        # Household's expenditure
        self.hoh_expenditure = sam.loc['Total', Hoh]
        self.hoh_expenditure = self.hoh_expenditure.to_dict()
        # Government's expenditure
        self.gov_expenditure = sam.loc['Total', 'Gov']

        # Household's labour income
        self.labour_income = sam.loc[Hoh, 'Lab']
        self.labour_income = self.labour_income.to_dict()

        # Household's capital income
        self.capital_income = sam.loc[Hoh, 'Cap']
        self.capital_income = self.capital_income.to_dict()

        # Government transfer
        self.gov_transfer = sam.loc[Hoh, 'Gov']

        # Household's total income
        self.total_hoh_income = {}
        for h in Hoh:
            self.total_hoh_income[h] = self.labour_income[h] + self.capital_income[h] + self.gov_transfer[h]
        # Government's income
        self.total_gov_income = sum(self.tariff_revenue[c] for c in Com) + sum(self.tax_income[h] for h in Hoh) + sum(self.tax_production[ind] for ind in Ind)

        # Goods investment
        self.invest_good = sam.loc[Com, 'Sav/Invest']
        # Foreign investment
        self.foreign_invest = sam.loc['Foreign', 'Sav/Invest']
        # Inventory investment
        self.invest_inventory = sam.loc['Inventory', 'Sav/Invest']
        # Total investment
        self.total_invest = sam.loc['Total', 'Sav/Invest']

        # Total output
        self.agg_production = sam.loc[Ind, 'Total']
        self.agg_production = self.agg_production.to_dict()

        # Commodity matrix
        self.good_structure = sam.loc[Ind, Com]
        self.good_structure = self.good_structure.stack().to_dict()
        # Aggregated commodity
        self.agg_good = {}
        for c in Com:
            self.agg_good[c] = sum(self.good_structure[ind, c] for ind in Ind)
        # Exports
        self.export_good = sam.loc[Com, 'Foreign']
        self.export_good = self.export_good.to_dict()
        # Imports
        self.import_good = sam.loc['Foreign', Com]
        self.import_good = self.import_good.to_dict()
        # Domestic good
        self.domestic_good = {}
        for c in Com:
            self.domestic_good[c] = self.agg_good[c] - self.export_good[c]
        # Armington good in domestic market
        self.armington_good = {}
        for c in Com:
            self.armington_good[c] = self.domestic_good[c] + self.import_good[c] + self.tariff_revenue[c]

class CGE_Param(object):
    def __init__(self, CGE_Data, Ind, Com, Hoh):
        # Initial elasticity value
        self.elas_subs_utility_hoh = 0.8
        self.elas_subs_prod = {key: 0.8 for key in Ind}
        self.elas_subs_transform = {key: 0.8 for key in Com}
        self.elas_subs_armington = {key: 0.8 for key in Com}

        # Initial price value
        # Price of domestic production activity
        self.price_production = {key: 1 for key in Ind}
        # Price of Armington commodity (Domestic + Import) sold in domestic market
        self.price_armington = {key: 1 for key in Com}
        # Price of aggregated intermediates
        self.price_agg_intermediate = {key: 1 for key in Ind}
        for ind in Ind:
            self.price_agg_intermediate[ind] = sum(CGE_Data.intermediate[c, ind] * self.price_armington[c] for c in Com) / CGE_Data.agg_intermediate[ind]
        # Price of aggregated value added
        self.price_agg_factor = {key: 1 for key in Ind}
        # Price of domestic commodity for producer
        self.price_good_producer = {key: 1 for key in Com}
        # Price of domestic commodity for consumer
        self.price_good_consumer = {key: 1 for key in Com}
        # Price of export at domestic currency
        self.price_export = {key: 1 for key in Com}
        # Price of import at domestic currency
        self.price_import = {key: 1 for key in Com}
        # World price of import at foreign currency
        self.price_word_import = {key: 1 for key in Com}
        # World price of export at foreign currency
        self.price_word_export = {key: 1 for key in Com}
        # Price of household's utility for aggregated consumption
        self.price_hoh_utility = {key: 1 for key in Hoh}

        # Exchange rate
        self.exchange_rate = 1
        # Depreciation rate
        self.depreciate_rate = 0.05

        # Calibrated parameters
        # Share parameter in CES utility function for households
        self.share_hoh_utility_ces = {}
        for h in Hoh:
            for c in Com:
                self.share_hoh_utility_ces[h, c] = (self.price_armington[c] * CGE_Data.hoh_good[h, c]) ** (1 / self.elas_subs_utility_hoh) / sum(
                    self.price_armington[c] * CGE_Data.hoh_good[h, c] ** (1 / self.elas_subs_utility_hoh) for c in Com)
        # Share parameter in CD utility function for households
        self.share_hoh_utility_cd = {}
        for h in Hoh:
            for c in Com:
                self.share_hoh_utility_cd[h, c] = CGE_Data.hoh_good[h, c] / CGE_Data.hoh_expenditure[h]
        # Share parameter in CD utility function for government
        self.share_gov_utility_cd = {}
        for c in Com:
            self.share_gov_utility_cd[c] =  CGE_Data.gov_good[c] / CGE_Data.gov_expenditure
        # Share parameter in CD utility function for
        self.share_inv_utility_cd = {}
        for c in Com:
            self.share_inv_utility_cd[c] = CGE_Data.invest_good[c] / CGE_Data.total_invest
        # Share parameter of investment in inventory
        self.share_inv_inventory_good = {}
        for c in Com:
            self.share_inv_inventory_good[c] = CGE_Data.inventory[c] / CGE_Data.invest_inventory
        # Share parameter of investment in inventory
        self.share_inv_inventory = CGE_Data.invest_inventory / CGE_Data.total_invest
        # Share parameter of foreign-owned inventory
        self.share_foreign_inventory = CGE_Data.foreign_inventory / CGE_Data.invest_inventory

        # Household's saving rate
        self.saving_rate_hoh = {}
        for h in Hoh:
            self.saving_rate_hoh[h] = CGE_Data.hoh_saving[h] / CGE_Data.hoh_expenditure[h]
        # Government's saving rate
        self.saving_rate_gov = CGE_Data.gov_saving / CGE_Data.gov_expenditure

        # Transfer rate to households from government
        self.transfer_rate_hoh = {}
        for h in Hoh:
            self.transfer_rate_hoh[h] = CGE_Data.gov_transfer[h] / CGE_Data.gov_expenditure

        # Tax rate of production activity
        self.tax_rate_production = {}
        for ind in Ind:
            self.tax_rate_production[ind] = CGE_Data.tax_production[ind] / CGE_Data.agg_production[ind]
        # Tariff rate of imports
        self.tariff_rate = {}
        for c in Com:
            if CGE_Data.import_good[c] == 0:
                self.tariff_rate[c] = 0
            else:
                self.tariff_rate[c] = CGE_Data.tariff_revenue[c] / CGE_Data.import_good[c]
        # Tax rate of household's income
        self.tax_rate_income = {}
        for h in Hoh:
            self.tax_rate_income[h] = CGE_Data.tax_income[h] / CGE_Data.total_hoh_income[h]

        # Share parameter in CES production function for aggregated intermediate input
        self.share_agg_intermediate_ces = {}
        for ind in Ind:
            self.share_agg_intermediate_ces[ind] = self.price_agg_intermediate[ind] * CGE_Data.agg_intermediate[ind] ** (1 / self.elas_subs_prod[ind]) / (
                                                        self.price_agg_intermediate[ind] * CGE_Data.agg_intermediate[ind] ** (1 / self.elas_subs_prod[ind])
                                                        + self.price_agg_factor[ind] * CGE_Data.value_added[ind] ** (1 / self.elas_subs_prod[ind])
                                                    )
        # Share parameter in Leontief production function for intermediate input
        self.share_intermediate_leontief = {}
        for ind in Ind:
            for c in Com:
                self.share_intermediate_leontief[c, ind] = CGE_Data.intermediate[c, ind] / CGE_Data.agg_intermediate[ind]
        # Share parameter in CES production function for aggregated value added
        self.share_agg_factor_ces = {}
        for ind in Ind:
            self.share_agg_factor_ces[ind] = self.price_agg_factor[ind] * CGE_Data.value_added[ind] ** (1 / self.elas_subs_prod[ind]) / (
                                                        self.price_agg_intermediate[ind] * CGE_Data.agg_intermediate[ind] ** (1 / self.elas_subs_prod[ind])
                                                        + self.price_agg_factor[ind] * CGE_Data.value_added[ind] ** (1 / self.elas_subs_prod[ind])
                                                    )
        # Share parameter in CD function for labour
        self.share_labour_cd = {}
        for ind in Ind:
            self.share_labour_cd[ind] = CGE_Data.labour[ind] / CGE_Data.value_added[ind]

        # Share parameter in CD function for capital
        self.share_capital_cd = {}
        for ind in Ind:
            self.share_capital_cd[ind] = CGE_Data.capital[ind] / CGE_Data.value_added[ind]

        # Share parameter in CES Armington function for domestic commodity
        self.share_domestic_armington_ces = {}
        for c in Com:
            self.share_domestic_armington_ces[c] = self.price_good_consumer[c] * CGE_Data.domestic_good[c] ** (1 / self.elas_subs_armington[c]) / (
                                                        self.price_good_consumer[c] * CGE_Data.domestic_good[c] ** (1 / self.elas_subs_armington[c])
                                                        + (1 + self.tariff_rate[c]) * self.price_import[c] * CGE_Data.import_good[c] ** (1 / self.elas_subs_armington[c])
            )
        # Share parameter in CET function for domestic commodity
        self.share_domestic_supply_cet = {}
        for c in Com:
            self.share_domestic_supply_cet[c] = self.price_good_consumer[c] * CGE_Data.domestic_good[c] ** (1 / self.elas_subs_transform[c]) / (
                                                        self.price_good_consumer[c] * CGE_Data.domestic_good[c] ** (1 / self.elas_subs_transform[c])
                                                        + self.price_export[c] * CGE_Data.export_good[c] ** (1 / self.elas_subs_transform[c])
            )

        # Share parameter of labour income by household
        self.share_labour_by_hoh = {}
        for h in Hoh:
            self.share_labour_by_hoh[h] = CGE_Data.labour_income[h] / sum(CGE_Data.labour_income[h] for h in Hoh)
        # Share parameter of capital income by household
        self.share_capital_by_hoh = {}
        for h in Hoh:
            self.share_capital_by_hoh[h] = CGE_Data.capital_income[h] / sum(CGE_Data.capital_income[h] for h in Hoh)

        # Commodity table from production industries
        self.share_production_to_com = {}
        for ind in Ind:
            for c in Com:
                self.share_production_to_com[ind, c] = CGE_Data.good_structure[ind, c] / CGE_Data.agg_production[ind]

        # Scale parameter of CD-utility function for households
        self.scale_hoh_utility_cd = {}
        for h in Hoh:
            self.scale_hoh_utility_cd[h] = CGE_Data.hoh_expenditure[h] / np.prod([CGE_Data.hoh_good[h, c] ** self.share_hoh_utility_cd[h, c] for c in Com])
        # Scale parameter of CD-utility function for government
        self.scale_gov_utility_cd = CGE_Data.gov_expenditure / np.prod([CGE_Data.gov_good[c] ** self.share_gov_utility_cd[c] for c in Com])
        # Scale parameter of CD-utility function for investment
        self.scale_inv_utility_cd = CGE_Data.total_invest / np.prod([CGE_Data.invest_good[c] ** self.share_inv_utility_cd[c] for c in Com])
        # Scale parameter of CES-production function for aggregated inputs
        self.scale_prod_ces = {}
        for ind in Ind:
            self.scale_prod_ces[ind] = CGE_Data.agg_production[ind] / (self.share_agg_intermediate_ces[ind] * CGE_Data.agg_intermediate[ind] ** (1 - 1 / self.elas_subs_prod[ind])
                                            + self.share_agg_factor_ces[ind] * CGE_Data.value_added[ind] ** (1 - 1 / self.elas_subs_prod[ind])) ** (self.elas_subs_prod[ind] / (self.elas_subs_prod[ind] - 1))
        # Scale parameter of CD-production function for aggregated value added
        self.scale_factor_cd = {}
        for ind in Ind:
            self.scale_factor_cd[ind] = CGE_Data.value_added[ind] / (CGE_Data.labour[ind] ** self.share_labour_cd[ind] * (CGE_Data.capital[ind]/0.15) ** self.share_capital_cd[ind])
        # Scale parameter of CES-Armington function
        self.scale_prod_armington = {}
        for c in Com:
            self.scale_prod_armington[c] = CGE_Data.armington_good[c] / (self.share_domestic_armington_ces[c] * CGE_Data.domestic_good[c] ** (1 - 1 / self.elas_subs_armington[c])
                                                  + (1 - self.share_domestic_armington_ces[c]) * CGE_Data.import_good[c] ** (1 - 1 / self.elas_subs_armington[c])) ** (self.elas_subs_armington[c] / (self.elas_subs_armington[c] - 1))
        # Scale parameter of CET function
        self.scale_prod_transform = {}
        for c in Com:
            self.scale_prod_transform[c] = CGE_Data.agg_good[c] / (self.share_domestic_supply_cet[c] * CGE_Data.domestic_good[c] ** (1 - 1 / self.elas_subs_transform[c])
                                                  + (1 - self.share_domestic_supply_cet[c]) * CGE_Data.export_good[c] ** (1 - 1 / self.elas_subs_transform[c])) ** (self.elas_subs_transform[c] / (self.elas_subs_transform[c] - 1))

        # Marginal production cost
        self.marginal_cost_ces = {}
        for ind in Ind:
            self.marginal_cost_ces[ind] = 1 / self.scale_prod_ces[ind] * ((self.share_agg_intermediate_ces[ind] ** self.elas_subs_prod[ind] * self.price_agg_intermediate[ind] ** (1 - self.elas_subs_prod[ind])
                                            + self.share_agg_factor_ces[ind] ** self.elas_subs_prod[ind] * self.price_agg_factor[ind] ** (1 - self.elas_subs_prod[ind])) ** (1 / (1 - self.elas_subs_prod[ind])))
        '''
        self.share_inter_prod = {}
        for ind in Ind:
            for c in Com:
                self.share_inter_prod[c, ind] = (self.price_domestic_armington[c] * CGE_IO_Data.intermediate_input[c, ind]) ** (1 / self.elas_subs_prod[ind]) / (sum((self.price_domestic_armington[c]
                                                                       * CGE_IO_Data.intermediate_input[c, ind] ** (1 / self.elas_subs_prod[ind]) for c in Com))
                                                                       + (self.wage_labour[ind] * CGE_IO_Data.labour_input[ind]) ** (1 / self.elas_subs_prod[ind])
                                                                       + (self.rent_capital[ind] * CGE_IO_Data.capital_input[ind]) ** (1 / self.elas_subs_prod[ind]))
        self.share_labour_prod = {}
        for ind in Ind:
            self.share_labour_prod[ind] = (self.wage_labour[ind] * CGE_IO_Data.labour_input[ind]) ** (1 / self.elas_subs_prod[ind]) / (sum((self.price_domestic_armington[c]
                                                                       * CGE_IO_Data.intermediate_input[c, ind] ** (1 / self.elas_subs_prod[ind]) for c in Com))
                                                                       + (self.wage_labour[ind] * CGE_IO_Data.labour_input[ind]) ** (1 / self.elas_subs_prod[ind])
                                                                       + (self.rent_capital[ind] * CGE_IO_Data.capital_input[ind]) ** (1 / self.elas_subs_prod[ind]))
        self.share_capital_prod = {}
        for ind in Ind:
            self.share_capital_prod[ind] = (self.rent_capital[ind] * CGE_IO_Data.capital_input[ind]) ** (1 / self.elas_subs_prod[ind]) / (sum((self.price_domestic_armington[c]
                                                                    * CGE_IO_Data.intermediate_input[c, ind] ** (1 / self.elas_subs_prod[ind]) for c in Com))
                                                                    + (self.wage_labour[ind] * CGE_IO_Data.labour_input[ind]) ** (1 / self.elas_subs_prod[ind])
                                                                    + (self.rent_capital[ind] * CGE_IO_Data.capital_input[ind]) ** (1 / self.elas_subs_prod[ind]))

        self.scale_hoh_utility = 1 / self.price_utility * sum((self.share_hoh_utility[c] ** self.elas_subs_utility) * (
                                    self.price_domestic_armington[c] ** (1 - self.elas_subs_utility)) for c in Com) ** (1 / (1 - self.elas_subs_utility))
'''