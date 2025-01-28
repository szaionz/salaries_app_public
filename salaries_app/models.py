from django.db import models
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
import base64
from io import BytesIO

class StateSalary(models.Model):
    state= models.CharField(max_length=100)
    position= models.CharField(max_length=100)
    min_state_salary= models.FloatField()
    max_state_salary= models.FloatField()
    pace = models.FloatField()
    scale = models.FloatField()
    
    @staticmethod
    def get_all_states():
        return sorted(StateSalary.objects.values_list('state', flat=True).distinct())
    @staticmethod
    def get_all_positions():
        return sorted(StateSalary.objects.values_list('position', flat=True).distinct())
    
    def get_expected_salary(self, experience):
        return min(self.scale*np.exp(self.pace*experience), self.max_state_salary)
    
    @staticmethod
    def get_similar_jobs_salaries(job, state, experience):
        my_state_salary = StateSalary.objects.get(
            position=job, state=state
            )

        query = [my_state_salary]+list(StateSalary.objects.raw(
            """
            SELECT * FROM 
            (salaries_app_statesalary INNER JOIN
            salaries_app_similaritypair ON salaries_app_statesalary.position = salaries_app_similaritypair.similar)
            WHERE state=%s AND role=%s
            ORDER BY [index] asc;
            """, [state, job]
            ))
        return zip(range(len(query)), query, [f"${state_salary.get_expected_salary(experience):,.2f}" for state_salary in query],
                   [HistogramCount.get_base64_histogram(state_salary.position, state_salary.get_expected_salary(experience)) for state_salary in query])
    
    
    
class SimilarityPair(models.Model):
    role = models.CharField(max_length=100)
    index = models.IntegerField()
    similar = models.CharField(max_length=100)
    
    
class HistogramCount(models.Model):
    position = models.CharField(max_length=100)
    salary = models.FloatField()
    count = models.IntegerField()

    @staticmethod
    def get_histogram_data(position):
        return HistogramCount.objects.filter(position=position).order_by('salary').values_list('salary', 'count')
    
    @staticmethod
    def get_base64_histogram(position, my_salary=None):
        fig, ax = plt.subplots(figsize=(10,5))
        data = np.array(HistogramCount.get_histogram_data(position))
        ax.hist(np.array(data)[:,0],bins=np.array(data)[:,0], weights=np.array(data)[:,1])
        # ax.set_xlabel('Salary')
        # ax.set_ylabel('Count')
        ax.tick_params(axis='x', labelsize=24, rotation=45)
        ax.tick_params(axis='y', labelsize=24)
        ax.xaxis.set_major_formatter('${:,.0f}'.format)
        if my_salary:
            ax.axvline(x=my_salary, color='black', label='My Salary', linewidth=2)
        fig.tight_layout()
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        image_png=buffer.getvalue()
        buffer.close()
        return base64.b64encode(image_png).decode('utf-8')