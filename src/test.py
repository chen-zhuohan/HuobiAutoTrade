import uuid

username = 'LCUser_{}'.format(hex(int(uuid.uuid4().hex, 16) // 10**18).upper())

print(len(username))
print(username)