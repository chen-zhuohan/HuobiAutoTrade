from collections import OrderedDict


line = [('1min', 1), ('5min', 2), ('15min', 3), ('30min', 4), ('60min', 5), ('4hour', 6), ('1day', 7),
        ('1week', 8), ('1mon', 9), ('1year', 10)]

od = OrderedDict(line)
d = dict(line)

print(d.keys())
print(od.keys())