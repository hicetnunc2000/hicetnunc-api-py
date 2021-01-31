import requests
import ipfshttpclient
import json

client = ipfshttpclient.connect('/dns4/ipfs.infura.io/tcp/5001/https')
kt = 'KT1M2JnD1wsg7w2B4UXJXtKQPuDUpU2L7cJH'
curate = 'KT1WVnT2tqB5spWaQu6iuf3SWwpkhZmvYnZ9'
network = 'mainnet'
class Objkt:
    def get_storage(self, network, kt):
        return requests.get('https://better-call.dev/v1/contract/{}/{}/storage'.format(network, kt)).json()

    def get_ledger(self, network, kt):
        ptr = self.get_storage(network, kt)['children'][2]['value']
        big_map = requests.get('https://better-call.dev/v1/bigmap/{}/{}/keys'.format(network, ptr)).json()
        ledger = [ {
            'address': e['data']['key']['children'][0]['value'], 
            'tk_id' : e['data']['key']['children'][1]['value'],
            'balance' : e['data']['value']['value']
        } for e in big_map ]
        metadata = self.get_metadata(network, kt)
        
        for e1 in ledger:
            for e2 in metadata:
                if e1['tk_id'] == e2['tk_id']:
                    e1.update(e2)
        
        return ledger
    
    def tz_ledger(self, network, kt, tz):
        ledger = self.get_ledger(network, kt)
        return list(filter(lambda x : x is not None, [ e if e['address'] == tz else None for e in ledger ]))
        
    def swap_metadata(self, network, kt):
        arr = self.swaps(network)
        ret = list(filter(lambda x : x is not None, [ e['objkt_id'] if e['address'] == kt else None for e in arr ]))
        print(ret)
        return self.get_metadata_id(network, 'KT1M2JnD1wsg7w2B4UXJXtKQPuDUpU2L7cJH', ret[0])

    def swaps(self, network):
        res = requests.get('https://better-call.dev/v1/contract/{}/{}/same'.format(network, curate)).json()
        kts = list(filter(lambda x : x is not None, [ e['address'] if e['network'] == 'mainnet' and e['manager'] == 'KT1PAV4ayvsDYi9zBFsLepnkPkpEspeYefNX' else None for e in res['contracts']]))
        storages = [self.get_storage(network, e) for e in kts]
        arr = []

        i = 0
        for e1 in storages:
            print(e1)
            aux_arr = []
            obj = {}
            aux_arr = [ { e2['name'] : e2['value'] } for e2 in e1['children'] ]
            for e3 in aux_arr:
                obj.update(e3)
            obj.update({'address':kts[i]})
            arr.append(obj)
            i += 1
            
        return arr
    
    def tz_swaps(self, network, tz):
        storages = self.swaps(network)
        return list(filter(lambda x : x is not None, [e if e['issuer'] == tz else None for e in storages]))
    
    def get_metadata(self, network, kt):
        ptr = self.get_storage(network, kt)['children'][6]['value']
        big_map = requests.get('https://better-call.dev/v1/bigmap/{}/{}/keys'.format(network, ptr)).json()
        arr = [ {
            'tk_id' : e['data']['key']['value'],
            'metadata' : self.get_json(e['data']['value']['children'][1]['children'][0]['value'].split('ipfs://')[1])
        } for e in big_map ]
        
        for e in arr:
            e['view'] = self.get_json(e['metadata']['NFT'].split('/')[4])
        
        return arr
    
    def get_json(self, cid):
        return json.loads(client.cat(cid))
    
    def get_metadata_id(self, network, kt, id):
        tks = self.get_metadata(network, kt)
        return (list(filter(lambda x : x is not None, [ e if int(e['tk_id']) == int(id) else None for e in tks ]))[0])

    def objkt_balance(self, network, kt, objkt_id):
        ptr = self.get_storage(network, kt)['children'][2]['value']
        big_map = requests.get('https://better-call.dev/v1/bigmap/{}/{}/keys'.format(network, ptr)).json()
        ledger = [ {
            'address': e['data']['key']['children'][0]['value'], 
            'tk_id' : e['data']['key']['children'][1]['value'],
            'balance' : e['data']['value']['value']
        } for e in big_map ]
        
        balance = 0
        
        for e in ledger:
            if e['tk_id'] == str(objkt_id):
                balance += int(e['balance'])
                
        return balance
    
    def objkt_ledger(self, network, kt, objkt_id):
        ptr = self.get_storage(network, kt)['children'][2]['value']
        big_map = requests.get('https://better-call.dev/v1/bigmap/{}/{}/keys'.format(network, ptr)).json()
        ledger = [ {
            'address': e['data']['key']['children'][0]['value'], 
            'tk_id' : e['data']['key']['children'][1]['value'],
            'balance' : e['data']['value']['value']
        } for e in big_map ]
        return list(filter(lambda x : x is not None, [e if e['tk_id'] == str(objkt_id) else None for e in ledger]))
    