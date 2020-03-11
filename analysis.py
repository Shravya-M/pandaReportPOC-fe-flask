import pandas as pd
from pandas_profiling import ProfileReport
import traceback, sys
from typing import Dict
import json
import datetime
from collections import defaultdict


def get_EDA(file_path):
    try:
        df = pd.read_csv(file_path)
        profile = ProfileReport(df, minimal=True)
        # profile.to_file(output_file="your_report.json") 
        profile = json.loads(profile.to_json())
        features = set(["distinct_count_with_nan", "distinct_count_without_nan", "count", "distinct_count", "n_unique", "n_missing", "n_infinite", "is_unique", "freq", "type", "mode", "min", "max", "sum", "range"])
        ignore_features = set(["value_counts", "value_counts_with_nan", "value_counts_without_nan" , "histogram_data", "scatter_data" ])
        table_features = set(["memory_size", "n_cells_missing"])
        # print(f'Profile: {profile.keys()}')
        report = defaultdict(str)
        report["overview"] = defaultdict(str)
        report["variables"] = defaultdict(str)


        #overview of table
        for feature, val in profile['table'].items():
            
            if feature in table_features:
                report["overview"][feature] = list(val.values())[0]
            elif feature == "types":
                report["overview"][feature] = defaultdict(str)
                for k,v in profile['table']['types'].items():
                    report["overview"][feature][k] = list(v.values())[0]
            else:
                report["overview"][feature] = val
        for variable in profile['variables'].keys():
            # print("variable", variable)
            # print(f'{type(variable):>20} ')
            report['variables'][variable] = defaultdict(str)
            for feature, val in profile['variables'][variable].items():
                if feature not in ignore_features:
                    if isinstance(val, dict):
                        # print(f'{feature:>30}')
                        report['variables'][variable][feature] = list(val.values())[0]
                    elif 'date_warning' == feature and val == True:
                        report['variables'][variable]["type"] = "datetime"
                    else:
                        report['variables'][variable][feature] = val
                
        sample = df.sample(20).to_json(orient='index')
        # report['sample'] = sample
        with open('result.json','w') as f:
            json.dump(profile,f)
        with open('report.json','w') as f:
            json.dump(report,f)
        return { "report": json.dumps(report)}
    except Exception as e:
        tb = sys.exc_info()[-1]
        print(f'Error: {str(e)} in line {tb.tb_lineno} in function: {traceback.extract_tb(tb, 1)[0][2]}')   

