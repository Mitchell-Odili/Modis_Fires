from modis_data_download import countries


'''Check if directory exists, if not, create it'''
import os

for country in countries:

  # You should check in your preferred folder.
  MYDIR = ('D:/Mitch/Repos/Streamlit/measuring_carbon/test/Modis_Fires/modis_firms' + country)
  CHECK_FOLDER = os.path.isdir(MYDIR)

  # If folder doesn't exist, then create it.
  if not CHECK_FOLDER:
    os.makedirs(MYDIR)
    print("created folder : ", MYDIR)
      
  else:
    print(MYDIR, "folder already exists.")
