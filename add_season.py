import pandas as pd
df = pd.read_excel("C:\\Users\\sonti\\OneDrive\\Desktop\\sales.xlsx.xlsx")
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')
df = df.asfreq('M')  
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Summer'
    elif month in [6, 7, 8, 9]:
        return 'Rainy'
    else:
        return 'Autumn'
df['Season'] = df['Date'].dt.month.apply(get_season)
df.to_excel("C:\\Users\\sonti\\OneDrive\\Desktop\\sales_with_season.xlsx", index=False)
print("New file saved successfully as 'sales_with_season.xlsx'")
print(df.head())
