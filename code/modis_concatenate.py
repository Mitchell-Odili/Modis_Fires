import pandas as pd
import glob
# from bounding_box import x


def combine_csv():
    extension = 'csv'
    all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

    #combine all files in the list
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
    
    return combined_csv
    # #export to csv
    # combined_csv.to_csv("Togo.csv", index=False, encoding='utf-8-sig')
    
# combine_csv()
