import json
import os
import django
import sys


sys.path.append("/home/salemmarafi/mbasql/")
os.environ["DJANGO_SETTINGS_MODULE"] = 'mbasql.settings'
django.setup()

from django.db.models import Count,Sum
from django.contrib.auth.models import User

qs = (User.objects.all().
    extra(select={
        'month': "EXTRACT(month FROM date_joined)",
        'year': "EXTRACT(year FROM date_joined)",
    }).
    values('month', 'year').
    annotate(count_items=Count('date_joined')))


from django.db.models import Count,Sum
from django.contrib.auth.models import User
from shop.models import *


from itertools import groupby
import csv

joined = User.objects.filter(date_joined__range=["2018-05-18","2018-05-20"]).values_list('email','first_name','last_name','date_joined').distinct()

writer = csv.writer(open("joined-lbs.csv", 'w'))

for obj in joined:

	writer.writerow(obj)
