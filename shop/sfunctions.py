import csv
'''
>> from utils import dump2csv
>> from dummy_app.models import *
>> qs = DummyModel.objects.all()
>> dump2csv.dump(qs, './data/dump.csv')
'''
def dump(qs, outfile_path):
    model = qs.model
    writer = csv.writer(open(outfile_path, 'w'))
    headers = []
    for field in model._meta.fields:
        headers.append(field.name)
    writer.writerow(headers)
    for obj in qs:
        row = []
        for field in headers:
            val = getattr(obj, field)
            if callable(val):
                val = val()
            if type(val) == unicode:
                val = val.encode("utf-8")
            row.append(val)
        writer.writerow(row)