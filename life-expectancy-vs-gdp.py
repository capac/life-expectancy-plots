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

# dataframes
le_df = pd.read_csv(le_data_file)
gdp_df = pd.read_csv(gdp_data_file, header=4, na_values='')

# life expectancy data
le_nat_yr_df = le_df.loc[:, ['location_name', 'val']]
# there is a difference in naming between the two dataframes
# for the United States and the Republic of Korea.
le_nat_yr_df.replace({'location_name': {'United States of America': 'United States',
                     'Republic of Korea': 'Korea, Rep.'}}, inplace=True)

# gdp per capita data
nat_name_filter = gdp_df['Country Name'].isin(le_nat_yr_df.location_name)
gdp_nat_yr_df = gdp_df.loc[nat_name_filter, ['Country Name', '2019']]
merged_df = gdp_nat_yr_df.merge(le_nat_yr_df, how='inner', left_on='Country Name',
                                right_on='location_name')
merged_df = merged_df[['Country Name', '2019', 'val']]
merged_df.rename(columns={'val': 'Life Expectancy', '2019': 'GDP per capita'},
                 inplace=True)
merged_df.replace({'Country Name': {'Korea, Rep.': 'South Korea'}}, inplace=True)

# print(merged_df['GDP per capita'].to_list())
# print(merged_df['Life Expectancy'].to_list())

# life expectancy plot for 2019
fig, ax = plt.subplots(figsize=(12, 8))
ax.scatter(merged_df['GDP per capita'], merged_df['Life Expectancy'],
           alpha=0.5, color='g', s=60)
ax.set_xlabel('GDP per capita (USD)', fontsize=11)
ax.set_ylabel('Life expectancy (years)', fontsize=11)
ax.set_title('Life expectancy per GDP per capita (2019)', fontsize=12)

countries = merged_df['Country Name'].to_list()
gdp_pc = merged_df['GDP per capita'].to_list()
le = merged_df['Life Expectancy'].to_list()

for txt, x, y in zip(countries, gdp_pc, le):
    ax.annotate(txt, (x-500, y-0.3))

fig.tight_layout()
plt.grid(linestyle=':')
plt.savefig('life_expectancy_vs_gdp_pc.png', bbox_inches='tight')
