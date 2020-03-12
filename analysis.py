import pandas as pd
from pandas_profiling import ProfileReport
import traceback, sys
from typing import Dict
import json
import datetime
from collections import defaultdict
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
        
    def handle_data(self, d):
        if d != ' ':
            self.fed.append(d)
    def get_data(self):
        return self.fed

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def get_EDA(file_path):
    try:
        df = pd.read_csv(file_path)
        profile = ProfileReport(df, minimal=True)
        # profile.to_file(output_file="your_report.json") 
        profile = json.loads(profile.to_json())
        features = set([])
        ignore_features = set(["value_counts", "value_counts_with_nan", "value_counts_without_nan" , "histogram_data", "scatter_data" ])
        table_features = set(["memory_size", "n_cells_missing"])
        # print(f'Profile: {profile.keys()}')
        report = defaultdict(str)
        overview = defaultdict(str)
        report["rows"] = []
        report["columns"] = [{"label":"Column", "field":"Column", "sort": 'asc', "width":150}]


        #overview of table
        for feature, val in profile['table'].items():
            
            if feature in table_features:
                overview[feature] = list(val.values())[0]
            elif feature == "types":
                overview[feature] = defaultdict(str)
                for k,v in profile['table']['types'].items():
                    overview[feature][k] = list(v.values())[0]
            else:
                overview[feature] = val
        
        #info about variables
        for variable in profile['variables'].keys():
            # print("variable", variable)
            row = { "Column": variable}
            for feature, val in profile['variables'][variable].items():
                if feature not in ignore_features:
                    if feature not in features: features.add(feature)
                    
                    if isinstance(val, dict):
                        # print(f'{feature:>30}')
                        row[feature] = list(val.values())[0]
                    elif 'date_warning' == feature and val == True:
                        row["type"] = "datetime"
                    else:
                        row[feature] = val
            report["rows"].append(row)
        for feature in features:
            report["columns"].append({
                    "label": feature,
                    "field": feature,
                    # "sort": 'asc',
                    # "width": 200
                })
                
        sample = json.loads(df.sample(20).to_json(orient='index'))
        
        sample_report = {"rows": [], "columns": []}
        key = ""
        for k, v in sample.items():
            
            sample_report['rows'].append(v)
            key = k
        for k in sorted(sample[key].keys()):
            sample_report['columns'].append({
                 "label": k,
                    "field": k,
                    "width": 200
                    # "sort": 'asc',
            })
        # with open('sample_json.json','w') as f:
        #     json.dump(sample_report,f)
        return { "report": json.dumps(report), "overview":overview, "sample": sample_report}
    except Exception as e:
        tb = sys.exc_info()[-1]
        print(f'Error: {str(e)} in line {tb.tb_lineno} in function: {traceback.extract_tb(tb, 1)[0][2]}')   

