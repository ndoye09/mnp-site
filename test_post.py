import urllib.request, json
url='https://script.google.com/macros/s/AKfycbyreZVCwXkzkpoQczxTMWgXjuEIiXbhKVuDu_bRWhBbgXEnsnDoXUiENFkn3YcrNLIHUA/exec'
data=json.dumps({'nom':'Test','prenom':'Test','email':'test@example.com'}).encode('utf-8')
req=urllib.request.Request(url, data=data, headers={'Content-Type':'application/json'})
try:
    with urllib.request.urlopen(req, timeout=20) as r:
        print('STATUS', r.status)
        print(r.read().decode('utf-8'))
except Exception as e:
    print('ERROR', e)
