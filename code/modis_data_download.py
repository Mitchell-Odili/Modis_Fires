import requests
from time import sleep
import pandas as pd

baseurl="https://firms.modaps.eosdis.nasa.gov/country/list/?source=modis&year="
url=baseurl+str(2000)# contains names to all the csvs in a specific year
i=0
response=requests.get(url)
javas=str(response.content)
javas=javas.split("\\n")
javas[0]=javas[0].replace("b\'","")
files=[jav.split(",")[0] for jav in javas]

csvs=['_'.join(file.split("_")[2:]) for file in files]
countries=[csv.split('.')[0] for csv in csvs]

# import pandas as pd 
# countries = pd.DataFrame(countries, columns = ['Countries'])
# countries.to_csv('countries.csv', index = False)

def getmodis3(country,years):
    for year in years:
        i=0
        getcsv="https://firms.modaps.eosdis.nasa.gov/data/country/modis/"+str(year)+"/modis_"+str(year)+"_"+country+".csv"
        while i < (len(csvs)):
            try:
                with requests.Session() as sesh:
                    with open('modis_'+str(year)+'_'+country+".csv","wb") as f:
                        f.write(sesh.get(getcsv).content)
                        print(getcsv)
                        i+=1
            except Exception as e:
                print("Connect refuse",e)
                sleep(10)
                continue
            break


# getmodis3('Togo',range(2015,2022))

