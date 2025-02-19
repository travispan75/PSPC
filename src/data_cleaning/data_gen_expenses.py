import numpy as np
import pandas as pd

cost_centers = {
    465410: {
        ("B122", "P51510", "Salaries & Wages", "KR03"): 2_000_000,
        ("B122", "P51510", "Salaries & Wages", "KT04"): 1_500_000,
        ("B122", "P51050", "Travel", "KR03"): 150_000,
        ("B122", "P51200", "Rentals Informatics", "KR03"): 400_000,
        ("B122", "P51320", "Software, IT & Commu Eqp", "KR03"): 600_000,
        ("B122", "P51370", "Program Systems", "KR03"): 2_000_000
    },
    465420: {
        ("B122", "P51510", "Salaries & Wages", "KR45"): 3_200_000,
        ("B122", "P51510", "Salaries & Wages", "KT04"): 1_800_000,
        ("B122", "P51100", "Training", "KT04"): 150_000,
        ("B122", "P51150", "Consulting Services", "KT04"): 400_000,
        ("B122", "P51200", "Rentals Informatics", "KT04"): 1_000_000,
        ("B122", "P51260", "Other Operating Exp", "KR03"): 350_000,
        ("B122", "P51290", "Trans & Interpretn", "KT04"): 50_000,
        ("B122", "P51370", "Program Systems", "KR45"): 2_500_000,
        ("B122", "P51370", "Program Systems", "KT04"): 2_000_000,
        ("B141", "P51510", "Salaries & Wages", "KT04"): 1_700_000,
        ("B141", "P51100", "Training", "KT04"): 120_000,
        ("B141", "P51130", "Temporary Help", "KT04"): 200_000,
        ("B141", "P51150", "Consulting Services", "KT04"): 350_000,
        ("B141", "P51200", "Rentals Informatics", "KT04"): 950_000,
        ("B141", "P51370", "Program Systems", "KT04"): 1_800_000,
        ("B174", "P51510", "Salaries & Wages", "KT04"): 1_600_000,
        ("B174", "P51200", "Rentals Informatics", "KT04"): 900_000,
        ("B174", "P51370", "Program Systems", "KT04"): 1_700_000,
        ("B175", "P51510", "Salaries & Wages", "KR03"): 2_200_000,
        ("B175", "P51510", "Salaries & Wages", "KT04"): 1_500_000
    },
    465425: {
        ("B122", "P51510", "Salaries & Wages", "KR04"): 2_500_000,
        ("B122", "P51510", "Salaries & Wages", "KR45"): 3_000_000,
        ("B122", "P51510", "Salaries & Wages", "KT04"): 2_000_000,
        ("B122", "P51100", "Training", "KR45"): 100_000,
        ("B122", "P51150", "Consulting Services", "KR45"): 250_000,
        ("B122", "P51200", "Rentals Informatics", "KR45"): 150_000,
        ("B122", "P51260", "Other Operating Exp", "KR45"): 300_000,
        ("B122", "P51290", "Trans & Interpretn", "KR45"): 50_000,
        ("B122", "P51320", "Software, IT & Commu Eqp", "KR45"): 500_000,
        ("B122", "P51370", "Program Systems", "KR44"): 1_000_000,
        ("B122", "P51370", "Program Systems", "KR45"): 1_500_000,
        ("B322", "P42050", "Services Non-Reg", "KR45"): 2_000_000,
        ("B322", "P51260", "Other Operating Exp", "KR45"): 250_000
    },
    465430: {
        ("B122", "P51510", "Salaries & Wages", "KT04"): 2_500_000,
        ("B122", "P51130", "Temporary Help", "KT04"): 200_000,
        ("B122", "P51290", "Trans & Interpretn", "KT04"): 50_000
    },
    465610: {
        ("B122", "P51510", "Salaries & Wages", "KR03"): 3_000_000,
        ("B122", "P51050", "Travel", "KR03"): 150_000,
        ("B122", "P51100", "Training", "KR03"): 100_000,
        ("B122", "P51230", "Material & Supplies", "KR03"): 50_000,
        ("B122", "P51260", "Other Operating Exp", "KR03"): 200_000,
        ("B122", "P51290", "Trans & Interpretn", "KR03"): 50_000,
        ("B122", "P51320", "Software, IT & Commu Eqp", "KR03"): 500_000,
        ("F119", "P51050", "Travel", "KR03"): 100_000
    },
    471465: {
        ("B122", "P51510", "Salaries & Wages", "KT04"): 2_500_000,
        ("B122", "P51150", "Consulting Services", "KT04"): 300_000,
        ("B122", "P51370", "Program Systems", "KT04"): 1_000_000,
        ("B141", "P51510", "Salaries & Wages", "KT04"): 2_000_000
    },
    471500: {
        ("B122", "P51510", "Salaries & Wages", "KT04"): 1_500_000,
        ("B122", "P51150", "Consulting Services", "KT04"): 300_000,
        ("B122", "P51370", "Program Systems", "KT04"): 1_000_000,
        ("B141", "P51510", "Salaries & Wages", "KT04"): 900_000,
        ("B141", "P51150", "Consulting Services", "KT04"): 800_000,
        ("B141", "P51370", "Program Systems", "KT04"): 700_000
    }
}

seasonality = {
    "April": 1.0,
    "May": 1.0,
    "June": 0.9,
    "July": 0.8,
    "August": 0.8,
    "September": 1.0,
    "October": 1.0,
    "November": 1.1,
    "December": 1.2,
    "January": 1.0,
    "February": 1.0,
    "March": 1.2
}

year_multipliers = {
    2020: 0.95,
    2021: 0.98,
    2022: 1.02,
    2023: 1.05,
    2024: 1.00
}

def distribute_normal(total, std):
    mean_sales_per_month = abs(total / sum(seasonality.values()))
    sales = []
    for month, factor in seasonality.items():
        month_sales = np.random.normal(mean_sales_per_month * factor, mean_sales_per_month * std)
        sales.append(month_sales)
    total_sales = sum(sales)
    sales = [sale * (total / total_sales) for sale in sales]
    sales.append(total)

    return sales

def distribute_log_normal(total, skew):
    mean_sales_per_month = abs(total / sum(seasonality.values()))
    log_mean = np.log(mean_sales_per_month)
    sales = []

    for month, factor in seasonality.items():
        month_sales = np.random.lognormal(log_mean + np.log(factor), skew)
        sales.append(month_sales)
    
    total_sales = sum(sales)
    sales = [sale * (total / total_sales) for sale in sales]
    sales.append(total)

    return sales

def distribute_poisson(total):
    mean_sales_per_month = abs(total / sum(seasonality.values()))
    sales = []
    for month, factor in seasonality.items():
        month_sales = np.random.poisson(mean_sales_per_month * factor)
        sales.append(month_sales)
    total_sales = sum(sales)
    sales = [sale * (total / total_sales) for sale in sales]
    sales.append(total)
    
    return sales

def distribute_gamma(total, shape):
    mean_sales_per_month = abs(total / sum(seasonality.values()))
    scale = mean_sales_per_month / shape
    sales = []

    for month, factor in seasonality.items():
        month_sales = np.random.gamma(shape, scale * factor)
        sales.append(month_sales)

    total_sales = sum(sales)
    sales = [sale * (total / total_sales) for sale in sales]
    sales.append(total)
    return sales

def distribute_exponential(total, lambdaVal):
    mean_sales_per_month = abs(total / sum(seasonality.values()))
    scale = mean_sales_per_month / lambdaVal
    sales = []

    for month, factor in seasonality.items():
        month_sales = np.random.exponential(scale) * factor
        sales.append(month_sales)

    total_sales = sum(sales)
    sales = [sale * (total / total_sales) for sale in sales]
    sales.append(total)
    return sales

def distribute_weibull(total, shape):
    mean_sales_per_month = abs(total / sum(seasonality.values()))
    scale = mean_sales_per_month / (shape ** (1 / shape))
    sales = []

    for month, factor in seasonality.items():
        month_sales = np.random.weibull(shape) * scale * factor
        sales.append(month_sales)

    total_sales = sum(sales)
    sales = [sale * (total / total_sales) for sale in sales]
    sales.append(total)
    return sales

distributions = {
    "Salaries & Wages": (distribute_normal, { "std": 0.05 }),
    "Travel": (distribute_log_normal, { "skew": 0.7 }),
    "Training": (distribute_poisson, {}),
    "Rentals Informatics": (distribute_gamma, { "shape": 2 }),
    "Software, IT & Commu Eqp": (distribute_log_normal, { "skew": 0.9 }),
    "Program Systems": (distribute_exponential, { "lambdaVal": 0.00005 }),
    "Consulting Services": (distribute_gamma, { "shape": 3 }),
    "Other Operating Exp": (distribute_normal, { "std": 0.15 }),
    "Trans & Interpretn": (distribute_poisson, {}),
    "Temporary Help": (distribute_normal, { "std": 0.2 }),
    "Material & Supplies": (distribute_log_normal, { "skew": 0.6 }),
    "Services Non-Reg": (distribute_weibull, { "shape": 1.5 })
}

output = pd.DataFrame(columns=(list(seasonality.keys()) + ["YTD"]))

# print(output)

for cost_center, expenditures in cost_centers.items():
    for expense, total in expenditures.items():
        row_name = str(cost_center) + "-".join(expense)
        distribution_func = distributions[expense[2]][0]
        params = distributions[expense[2]][1]

        output.loc[row_name] = distribution_func(total, **params)

print(output)

output.to_excel('generated_data.xlsx')

