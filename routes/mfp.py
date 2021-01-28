from flask import request
from flask_restx import fields, Resource, Api, Namespace
from libs.validate import Validate
from libs.fa2 import FA2

import requests
import json

v = Validate()
fa2 = FA2()
api = Namespace('mfp')

@api.route('/feed')
class search_sources(Resource):
    def get(self):

        # get mfps from bigmap
        mfp_protocol = "KT1Q72pNNiCnBamwttWvXGE9N2yuz6c7guSD" # mainnet
        mfp_sample = "KT1UcPh3S1K1GAFqUt212H9qjFVdxEnca1qk"
        network = "mainnet"

        arr = []

        arr.append(requests.get("https://api.better-call.dev/v1/contract/{}/{}".format(network, mfp_sample)).json())
        arr.extend(requests.get("https://api.better-call.dev/v1/contract/{}/{}/same".format(network, mfp_sample)).json()['contracts'])
        #arr = [e if e['network'] == network else None for e in arr]
        arr = list(filter(lambda x: x != None and x['manager'] == mfp_protocol and x['network'] == network, arr))

        aux_arr = []

        for e in arr:

            obj = {}

            obj['address'] = e['address']
            obj['manager'] = e['manager']
            obj['timestamp'] = e['timestamp']

            l = list(map(lambda x: {x['name']: x['value']}, requests.get("https://api.better-call.dev/v1/contract/{}/{}/storage".format(network, e['address'])).json()['children']))

            storage = {}

            for e_1 in l:
                storage.update(e_1)

            obj['storage'] = storage
            obj['meta'] = requests.post('https://mf1ivet8ig.execute-api.us-east-1.amazonaws.com/dev/ipfs/read_cid', json={ "cid": obj['storage']['meta'] }).json()

            obj['balance'] = requests.get('https://api.better-call.dev/v1/account/{}/{}'.format(network, e['address'])).json()['balance']
            
            print([obj['balance'] * 100, int(obj['storage']['goal']), ((obj['balance'] * 100) / int(obj['storage']['goal']))])
            obj['percentage'] = round(((obj['balance'] * 100) / int(obj['storage']['goal'])), 2)

            aux_arr.append(obj)

        return { 'result': aux_arr }


@api.route('/kt')
@api.doc(params={
    'kt': 'kt address',
    'network': 'cartha/delphi/mainnet'
})
class search_kt(Resource):
    def post(self):

        payload = v.read_requests(request)

        kt = requests.get("https://api.better-call.dev/v1/contract/mainnet/{}".format(payload['kt'])).json()

        obj = {}

        obj['address'] = kt['address']
        obj['manager'] = kt['manager']
        obj['timestamp'] = kt['timestamp']

        l = list(map(lambda x: {x['name']: x['value']}, requests.get("https://api.better-call.dev/v1/contract/{}/{}/storage".format('mainnet', kt['address'])).json()['children']))

        storage = {}

        for e_1 in l:
            storage.update(e_1)

        obj['storage'] = storage

        obj['meta'] = requests.post('https://mf1ivet8ig.execute-api.us-east-1.amazonaws.com/dev/ipfs/read_cid', json={ "cid": obj['storage']['meta'] }).json()

        balance = requests.get('https://api.better-call.dev/v1/account/{}/{}'.format('mainnet', obj['address'])).json()['balance']

        obj['balance'] = balance
        obj['percentage'] = round(((obj['balance'] * 100) / int(obj['storage']['goal'])), 2)
        obj['storage']['goal'] = int(obj['storage']['goal']) / 1000000

        return obj

@api.route('/ledger')
@api.doc(params={
    'tz': 'tz address',
    'network': 'cartha/delphi/mainnet'
})
class ledger(Resource):
    def post(self):
        opensource_sample = "KT1UcPh3S1K1GAFqUt212H9qjFVdxEnca1qk"
        network = "mainnet"

        payload = v.read_requests(request)

        arr = []
        res = requests.get(
            "https://api.better-call.dev/v1/contract/{}/{}".format(network, opensource_sample))
        arr.append(res.json())
        res = requests.get(
            "https://api.better-call.dev/v1/contract/{}/{}/same".format(network, opensource_sample))


        aux_arr = []

        arr.extend(res.json()['contracts'])
        for e in arr:
            print(e['address'])
            obj = {}

            obj['address'] = e['address']

            if e['network'] == 'mainnet' and e['manager'] == 'KT1Q72pNNiCnBamwttWvXGE9N2yuz6c7guSD':
                balance = requests.get('https://api.better-call.dev/v1/account/{}/{}'.format(network, e['address'])).json()['balance']
                l = list(map(lambda x: {x['name']: x['value']}, requests.get("https://api.better-call.dev/v1/contract/{}/{}/storage".format('mainnet', e['address'])).json()['children']))
                
                storage = {}

                for e_1 in l:
                    storage.update(e_1)

                
                if storage['admin'] == payload['tz']:

                    obj['goal'] = int(storage['goal'])
                    obj['achieved'] = int(storage['achieved'])
                    obj['storage'] = storage
                    obj['balance'] = balance
                    obj['percentage'] = round(((obj['balance'] * 100) / int(obj['storage']['goal'])), 2)

                    aux_arr.append(obj)

            tokens_meta = fa2.get_ledger('KT1Ex8LrDbCrZuTgmWin8eEo7HFw74jAqTvz', payload['tz'], 'mainnet')
            print(tokens_meta)

        return {
            "results": aux_arr,
            "token_meta" : [e if e['address'] == payload['tz'] else None for e in tokens_meta],
            "balance" : int(requests.get('https://api.better-call.dev/v1/account/{}/{}'.format(network, payload['tz'])).json()['balance'])
        }

@api.route('/resources')
@api.doc(params={
    'tz': 'tz address',
    'network': 'cartha/delphi/mainnet'
})
class resources(Resource):
    def post(self):
        payload = v.read_requests(request)
        print(payload)
        r = requests.get('https://mf1ivet8ig.execute-api.us-east-1.amazonaws.com/dev/mfp/feed').json()

        aux_arr = []
        print(r)
        for e in r['result']:
            #print (e)
            if e['storage']['admin'] == payload['tz']:
                aux_arr.append(e)

        return aux_arr