
from django.shortcuts import render
from .models import StateSalary
from django.contrib import messages
def index(request):
    all_states = StateSalary.get_all_states()
    all_positions = StateSalary.get_all_positions()
    similar_jobs_salaries = []
    state = ''
    job_title = ''
    experience = ''
    if request.method=="POST":
        state = request.POST.get('state')
        job_title = request.POST.get('job_title')
        experience = int(request.POST.get('experience'))
        invalid_state = state not in all_states
        if invalid_state:
            messages.add_message(request, messages.ERROR, 'Invalid state')
        invalid_position = job_title not in all_positions
        if invalid_position:
            messages.add_message(request, messages.ERROR, 'Invalid job title')
        if not invalid_state and not invalid_position:
            similar_jobs_salaries = StateSalary.get_similar_jobs_salaries(job_title, state, experience)
        
    
    return render(request, 'index.html',
                    {'states': all_states,
                     'job_titles':all_positions,
                     'state':state,
                        'job_title':job_title,
                        'experience':experience,
                        'similar_jobs_salaries':similar_jobs_salaries,
                     })