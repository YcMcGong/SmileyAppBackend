import json
import os
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.template import Context, Template

# import utility
from utility import current_user

"""
#  ________________________________________
# |Definition of the Login Class           |
# |________________________________________|
"""

def welcome(request):
    
    return JsonResponse({'one':'plans_url', 'two':'test'})

