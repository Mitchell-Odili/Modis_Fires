from modis_data_download import countries, getmodis3
from modis_data_prep import process_date
from modis_concatenate import combine_csv


'''Check if directory exists, if not, create it'''
import os

for country in countries:

  # You should check in your preferred folder.
  MYDIR = ('D:/Mitch/Repos/Streamlit/measuring_carbon/test/Modis_Fires/modis_firms' + country)
  CHECK_FOLDER = os.path.isdir(MYDIR)

  # If folder doesn't exist, then create it.
  if not CHECK_FOLDER:
    os.makedirs(MYDIR)
    #   print("created folder : ", MYDIR)
    # change working directory to folder
  os.chdir(MYDIR)   
  # scrape & download the files
  getmodis3(country,range(2015,2022))
  # preprocess country files
  modis_2015 = process_date(r'modis_2015_'+ country +'.csv')
  modis_2016 = process_date(r'modis_2016_'+ country +'.csv')
  modis_2017 = process_date(r'modis_2017_'+ country +'.csv')
  modis_2018 = process_date(r'modis_2018_'+ country +'.csv')
  modis_2019 = process_date(r'modis_2019_'+ country +'.csv')
  modis_2020 = process_date(r'modis_2020_'+ country +'.csv')
  modis_2021 = process_date(r'modis_2021_'+ country +'.csv')

  modis_2015.to_csv('modis_2015_' + country + '.csv', index = False)
  modis_2016.to_csv('modis_2016_' + country + '.csv', index = False)
  modis_2017.to_csv('modis_2017_' + country + '.csv', index = False)
  modis_2018.to_csv('modis_2018_' + country + '.csv', index = False)
  modis_2019.to_csv('modis_2019_' + country + '.csv', index = False)
  modis_2020.to_csv('modis_2020_' + country + '.csv', index = False)
  modis_2021.to_csv('modis_2021_' + country + '.csv', index = False)
  print(f"{country} preprocessing done ")
  # concatenate
  #export to csv
  combined_csv = combine_csv()
  combined_csv.to_csv(country + ".csv", index=False, encoding='utf-8-sig')
  print(f"{country} concatenated")

      
#   else:
    # print(MYDIR, "folder already exists.")