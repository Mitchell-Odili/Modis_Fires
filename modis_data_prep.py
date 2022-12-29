import pandas as pd

def process_date(path):
  df = pd.read_csv(path)
  df['acq_time'] = df['acq_time'].astype('string')
#   add leading zeros to the integer column in a pandas series and makes the length of the field to 4 digit
  df['acq_time'] = df['acq_time'].apply(lambda x: '{0:0>4}'.format(x))
#   add `:` to make time format
  df['acq_time'] = df['acq_time'].str.replace(r'(\w{2}(?!$))', r'\1:', regex=True)
  df['acq_time'] = pd.to_datetime(df['acq_time'],format= '%H:%M' ).dt.time
  df['acq_date'] = df['acq_date'].astype('string')
  df['acq_time'] = df['acq_time'].astype('string')
  df['acq_date_time'] = df['acq_date'] + ' ' + df['acq_time']

  df['acq_date'] = pd.to_datetime(df['acq_date'])
  df['acq_date_time'] = pd.to_datetime(df['acq_date_time'])
  df.drop(columns = ['brightness', 'scan', 'track', 'confidence','version', 'bright_t31', 'daynight'], axis = 1, inplace = True)

  return df

# modis_2015 = process_date('modis_2015_Togo.csv')
# modis_2016 = process_date('modis_2016_Togo.csv')
# modis_2017 = process_date('modis_2017_Togo.csv')
# # modis_2018 = process_date('modis_2018_Togo.csv')
# # modis_2019 = process_date('modis_2019_Togo.csv')
# modis_2020 = process_date('modis_2020_Togo.csv')
# modis_2021 = process_date('modis_2021_Togo.csv')

# modis_2015.to_csv('modis_2015_Togo.csv', index = False)
# modis_2016.to_csv('modis_2016_Togo.csv', index = False)
# modis_2017.to_csv('modis_2017_Togo.csv', index = False)
# # modis_2018.to_csv('modis_2018_Togo.csv', index = False)
# # modis_2019.to_csv('modis_2019_Togo.csv', index = False)
# modis_2020.to_csv('modis_2020_Togo.csv', index = False)
# modis_2021.to_csv('modis_2021_Togo.csv', index = False)
