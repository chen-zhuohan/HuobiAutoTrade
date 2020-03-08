from itsdangerous import JSONWebSignatureSerializer, TimedJSONWebSignatureSerializer
import base64
import json

text_type = str


data = dict(a='a', b='b')
secret_key = '1234567890'

jwt = JSONWebSignatureSerializer(secret_key).dumps(obj=data)

header_a, payload_a, sign = jwt.split(b'.')

kwargs = {}
kwargs.setdefault("ensure_ascii", False)
kwargs.setdefault("separators", (",", ":"))
header_b = json.dumps({"alg": "HS512"}, **kwargs).encode(encoding="utf-8", errors="strict")
header_b = base64.urlsafe_b64encode(header_b).rstrip(b'=')

kwargs = {}
kwargs.setdefault("ensure_ascii", False)
kwargs.setdefault("separators", (",", ":"))
payload_b = json.dumps(data, **kwargs).encode(encoding="utf-8", errors="strict")
payload_b = base64.urlsafe_b64encode(payload_b).rstrip(b'=')

print(payload_a, payload_b, payload_a == payload_b, sep='\n')
print(header_a, header_b, header_a == header_b, sep='\n')