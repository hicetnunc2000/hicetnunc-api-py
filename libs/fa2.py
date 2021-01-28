
import requests

class FA2:

    def get_ledger(self, kt, tz, network):
        s = requests.get('https://api.better-call.dev/v1/contract/{}/{}/storage'.format(network, kt)).json()
        print(s)

        r = requests.get(
            "https://api.better-call.dev/v1/bigmap/{}/{}/keys".format(network, s['children'][2]['value'])).json()
        
        print(r)

        return [{
            'address': e['data']['key']['children'][0]['value'],
            'id': int(e['data']['key']['children'][1]['value']),
            'balance': int(e['data']['value']['value'])
        } for e in r]