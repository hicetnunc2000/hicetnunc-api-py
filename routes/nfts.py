from flask import request
from flask_restx import fields, Resource, Api, Namespace
from libs.validate import Validate
from libs.objkts import Objkt

import requests
import json

v = Validate()
o = Objkt()
api = Namespace('objkt')

@api.route('/swaps')
class swaps(Resource):
    def get(self):
        return { 'result' :  o.swaps('mainnet') }

@api.route('/feed')
class feed(Resource):
    def get(self):
        return { 'result' : o.get_metadata('mainnet', 'KT1M2JnD1wsg7w2B4UXJXtKQPuDUpU2L7cJH')}

@api.route('/id')
@api.doc(params={
    'id': 'objkt id',
    'network' : 'delphi/mainnet'
})
class objkt_id(Resource):
    def post(self):
        payload = v.read_requests(request)
        return { 
            'result' : o.get_metadata_id('mainnet', 'KT1M2JnD1wsg7w2B4UXJXtKQPuDUpU2L7cJH', payload['objkt_id']) , 
            'balance' : o.objkt_balance('mainnet', 'KT1M2JnD1wsg7w2B4UXJXtKQPuDUpU2L7cJH', int(payload['objkt_id'])),
            'owners' : o.objkt_ledger('mainnet', 'KT1M2JnD1wsg7w2B4UXJXtKQPuDUpU2L7cJH', int(payload['objkt_id']))
            }

@api.route('/tz_ledger')
@api.doc(params={
    'tz': 'tz address',
    'network': 'delphi/mainnet'
})
class tz_resources(Resource):
    def post(self):
        payload = v.read_requests(request)
        return { 'result' : o.tz_ledger('mainnet', 'KT1M2JnD1wsg7w2B4UXJXtKQPuDUpU2L7cJH', payload['tz']) }

@api.route('/tz_swaps')
@api.doc(params={
    'tz': 'tz address',
    'network': 'delphi/mainnet'
})
class tz_swaps(Resource):
    def post(self):
        payload = v.read_requests(request)
        return { 'result' : o.tz_swaps('mainnet', payload['tz']) }

@api.route('/swap_metadata')
@api.doc(params={
    'tz': 'tz address',
    'network': 'delphi/mainnet'
})
class swap_metadata(Resource):
    def post(self):
        payload = v.read_requests(request)
        return { 'result' : o.swap_metadata('mainnet', payload['kt']) }

@api.route('/ledger')
@api.doc(params={
    'tz': 'tz address',
    'network': 'delphi/mainnet'
})
class ledger(Resource):
    def post(self):
        payload = v.read_requests(request)
        return { 'result' : o.get_ledger('mainnet', 'KT1M2JnD1wsg7w2B4UXJXtKQPuDUpU2L7cJH') }