import pandas as pd
from .models import *

def run():
    state_salary_df = pd.read_csv('../exp_params.csv')
    StateSalary.objects.all().delete()
    for index, row in state_salary_df.iterrows():
        StateSalary.objects.create(
            state=row['state'],
            position=row['position'],
            min_state_salary=row['min_state_salary'],
            max_state_salary=row['max_state_salary'],
            pace=row['pace'],
            scale=row['scale']
        )
    similarity_pairs_df = pd.read_csv('../top_3_roles.csv')
    similarity_pairs_df=similarity_pairs_df.melt(['role'], var_name='index', value_name='similar')
    similarity_pairs_df['index']=similarity_pairs_df['index'].str[-1].astype(int)
    SimilarityPair.objects.all().delete()
    for index, row in similarity_pairs_df.iterrows():
        SimilarityPair.objects.create(
            role=row['role'],
            index=row['index'],
            similar=row['similar']
        )
        
    histogram_csv = pd.read_csv('../histograms.csv')
    HistogramCount.objects.all().delete()
    for index, row in histogram_csv.iterrows():
        HistogramCount.objects.create(
            position=row['position'],
            salary=row['salary'],
            count=row['count']
        )