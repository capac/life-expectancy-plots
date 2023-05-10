import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# plt.style.use('personal-style.mplstyle')

data_dir = Path.home() / 'Programming/data/life-expectancy-vs-gdp-pc/'
# life expectancy data
le_data_dir = data_dir / 'IHME-GBD_2019_DATA-7e5aa45e-1'
le_data_file = le_data_dir / 'IHME-GBD_2019_DATA-7e5aa45e-1.csv'
# GDP per capita data
gdp_data_dir = data_dir / 'API_NY.GDP.PCAP.CD_DS2_en_csv_v2_5447781/'
gdp_data_file = gdp_data_dir / 'API_NY.GDP.PCAP.CD_DS2_en_csv_v2_5447781.csv'

le_df = pd.read_csv(le_data_file)
gdp_df = pd.read_csv(gdp_data_file, header=2, na_values='')

# life expectancy data
le_nat_yr_df = le_df.loc[:, ['location_name', 'val']]
le_nat_yr_df.replace({'location_name': {'United States of America': 'United States',
                     'Republic of Korea': 'Korea, Rep.'}}, inplace=True)

# gdp per capita data
nat_name_filter = gdp_df['Country Name'].isin(le_nat_yr_df.location_name)
gdp_nat_yr_df = gdp_df.loc[nat_name_filter, ['Country Name', '2019']]
# print(gdp_nat_yr_df.shape)
# print(le_nat_yr_df.shape)
merged_df = gdp_nat_yr_df.merge(le_nat_yr_df, how='inner', left_on='Country Name',
                                right_on='location_name')
merged_df = merged_df[['Country Name', '2019', 'val']]
merged_df.rename(columns={'val': 'Life Expectancy', '2019': 'GDP per capita'},
                 inplace=True)
# print(merged_df)
# print(gdp_df['Country Name'].loc[gdp_df['Country Name'].isin(le_df.location_name)])
# print(le_df.location_name.loc[~le_nat_yr_df.location_name.isin(gdp_df['Country Name'])])
# life expectancy plot for 2019
fig, ax = plt.subplots(figsize=(12, 8))
ax.scatter(merged_df['GDP per capita'], merged_df['Life Expectancy'],)
fig.tight_layout()
plt.show()
