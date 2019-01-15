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


from itertools import groupby
running_total = 0
for k in qs:
    running_total += k['count_items']
    print(str(k['month'])+','+str(k['count_items']),','+str(running_total))
print('Total: '+str(running_total))

