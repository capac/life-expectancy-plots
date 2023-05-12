import matplotlib.pyplot as plt
from matplotlib import ticker
import pandas as pd
from pathlib import Path

plt.style.use('scatterplot-style.mplstyle')

data_dir = Path.home() / 'Programming/data/life-expectancy-vs-gdp-pc/'
python_work_dir = Path.home() / 'Programming/Python/'
work_dir = python_work_dir / 'data-visualization/life-expectancy-vs-gdp-pc/'

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
merged_df.replace({'Country Name': {'Korea, Rep.': 'South Korea', }}, inplace=True)

merged_df.set_index('Country Name', inplace=True)
unselected_countries = ['Australia', 'Canada', 'Belgium',
                        'Luxembourg', 'Netherlands', 'New Zealand',]
selected_countries = ['Switzerland', 'Austria', 'Germany', 'Denmark',
                      'Spain', 'Finland', 'France', 'United Kingdom',
                      'Greece', 'Ireland', 'Italy', 'Japan',
                      'South Korea', 'Norway', 'Portugal', 'Singapore',
                      'Sweden', 'United States',]

select_countries_df = merged_df[merged_df.index.isin(selected_countries)]

# life expectancy plot versus GDP per capita for 2019
fig, ax = plt.subplots(figsize=(12, 8))
ax.scatter(select_countries_df['GDP per capita'],
           select_countries_df['Life Expectancy'],
           alpha=0.8, color='#1879CE', s=130)
ticks = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x*1e-3))
ax.xaxis.set_major_formatter(ticks)

ax.set_xlabel('GDP per capita (in thousands of USD)')
ax.set_ylabel('Life expectancy (years)')
ax.set_title('Life expectancy versus GDP per capita (2019)')

gdp_pc = merged_df['GDP per capita']
le = merged_df['Life Expectancy']

for label in selected_countries:
    ax.annotate(label, (gdp_pc.loc[label]-400, le.loc[label]-0.4))

plt.savefig(work_dir / 'plots/life_expectancy_vs_gdp.png', bbox_inches='tight')
