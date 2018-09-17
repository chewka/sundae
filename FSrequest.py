import json, requests
url = 'https://api.foursquare.com/v2/venues/categories'

params = dict(
  client_id='UVKD0BBIB1U5VVAXXUR2CHCILG3F1IJHHQ1NE2OJ2GT3NJMQ',
  client_secret='0DKIIQ5LILHHVSTSBHOVQVIWQX1HCYGZBTOQWVZ2OQCPMWL4',
  v='20180323',
  ll='40.7243,-74.0018',
  query='coffee',
  limit=1
)

resp = requests.get(url=url, params=params)
data = json.loads(resp.text)




