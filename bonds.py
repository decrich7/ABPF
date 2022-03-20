# -*- coding: utf-8 -*-

import json
import math
from requests import put
import requests
from pprint import pprint
import requests
import datetime as dt
import matplotlib.pyplot as plt


class Bond:
    def __init__(self):
        self.bondds = dict()

    def get_bonds(self, money, inv_hor):
        bonds_list = []
        for i in range(1, 11):
            current_year = dt.datetime.today().year
            url = f'http://217.28.231.98:8080/v1/listing/get?id={i}'
            req = requests.get(url)
            req.encoding = 'utf-8'
            get_json = req.json()
            year_coupon = get_json.get("price") / get_json.get("prc")  # расчет годовой суммы
            coupon_yield = (year_coupon / get_json.get("nominal")) * 100  # купонная доходность
            spent = (get_json.get("year") - current_year) * year_coupon  # потрачено за года
            bonds = {
                'name_bond': get_json.get("name"),  # название облигации
                'id': get_json.get("id"),
                'coupon_yield': math.floor(coupon_yield),  # купонная доходность
                'price': get_json.get("price"),
                'repayment_year': get_json.get("year"),  # год погашения
                'spent_for_years': spent  # потрачено за года
            }
            bonds_list.append(bonds)

        count_of_yield_bonds = 0
        count_of_middle_bonds = 0
        count_of_low_bonds = 0

        for yields in bonds_list:
            if yields.get("coupon_yield") >= 18:
                count_of_yield_bonds += 1
            elif yields.get("coupon_yield") < 18 and yields.get("coupon_yield") >= 13:
                count_of_middle_bonds += 1
            elif yields.get("coupon_yield") < 13 and yields.get("coupon_yield") >= 0:
                count_of_low_bonds += 1

        money_for_one_yield_bond = money / count_of_yield_bonds
        money_for_one_middle_bond = money / count_of_middle_bonds
        money_for_one_low_bond = money / count_of_low_bonds
        bonds_count_list = list()
        if inv_hor == 1:
            for item in bonds_list:
                if item.get("coupon_yield") >= 18:
                    purchased_bonds = math.floor(((money_for_one_yield_bond + 1000) / item.get("price")))
                    bondds = {
                        'name': item.get("name_bond"),
                        'id': item.get("id"),
                        'count': purchased_bonds,
                        'price': item.get("price"),
                        'coupon_yield': item.get("coupon_yield"),
                        'repayment_year': item.get("repayment_year"),  # год погашения
                        'spent_for_years': math.floor(item.get("spent_for_years"))  # потрачено за года
                    }
                    bonds_count_list.append(bondds)
        if inv_hor == 3:
            for item in bonds_list:
                if item.get("coupon_yield") < 18 and item.get("coupon_yield") >= 13:
                    purchased_bonds = math.floor((money_for_one_middle_bond / item.get("price")))
                    bondds = {
                        'name': item.get("name_bond"),
                        'id': item.get("id"),
                        'count': purchased_bonds,
                        'price': item.get("price"),
                        'coupon_yield': item.get("coupon_yield"),
                        'repayment_year': item.get("repayment_year"),  # год погашения
                        'spent_for_years': math.floor(item.get("spent_for_years"))  # потрачено за года
                    }
                    bonds_count_list.append(bondds)
        if inv_hor == 5:
            for item in bonds_list:
                if item.get("coupon_yield") < 13 and item.get("coupon_yield") >= 0:
                    purchased_bonds = math.floor((money_for_one_low_bond / item.get("price")))
                    bondds = {
                        'name': item.get("name_bond"),
                        'id': item.get("id"),
                        'count': purchased_bonds,
                        'price': item.get("price"),
                        'coupon_yield': item.get("coupon_yield"),
                        'repayment_year': item.get("repayment_year"),  # год погашения
                        'spent_for_years': math.floor(item.get("spent_for_years"))  # потрачено за года
                    }
                    bonds_count_list.append(bondds)

        return bonds_count_list


    def buy_bond(self, money_ac, year, bonds_count_list):
        reset = f'http://217.28.231.98:8080/v1/account/reset'
        account = f'http://217.28.231.98:8080/v1/account?summa={money_ac}'
        print(put(reset).json())
        get_account = put(account).json
        bond_buy = list()
        for i in bonds_count_list:
            get_json = put(
                f'http://217.28.231.98:8080/v1/oper/deal?type=BUY&id={i.get("id")}&amount={i.get("count") - 3}&year={year}').json()
            bond_buy.append(get_json)
        get_account_data = requests.get('http://217.28.231.98:8080/v1/account').json()
        bond_buy.append(get_account_data)
        msg_list = list()
        for i in bond_buy[:-1]:
            msg = f'📜 {i.get("message").replace(" BUY", "")}'
            # print(msg)
            msg_list.append(msg)
        for i in bond_buy[-1:]:
            summa = f'🎁 Остаток средств - {i.get("summa")}'
            msg_list.append(summa)
        # pprint(get_account_data)

        # with open('bonds_count_test.json') as js:
        #     data = json.load(js)
        # stoks = data["stoks"]
        # sm = ''
        # for i in msg_list[-1:]:
        #     sm = i.replace('Остаток средств - ', '').replace('₽', ' ')
        #
        # for k, v in stoks.get('sharp').items():
        #     if k == "balance":
        #         a = f'Остаток по Шарпу(учитывая облигации) - {float(v) + float(sm)}'
        #         msg_list.append(a)
        #
        # for k, v in stoks.get('volatility').items():
        #     if k == "balance":
        #         a = f'Остаток по волатильности(учитывая облигации) - {float(v) + float(sm)}'
        #         msg_list.append(a)

        return msg_list


# def main():
#     b = Bond()
#     b.get_bonds(70000, 1)
#
#
# main()
