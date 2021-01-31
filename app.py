
from flask import Flask
from flask_restx import Api
from flask_cors import CORS

# ROUTES

from routes.mfp import api as mfp_api
from routes.nfts import api as objkt_api

app = Flask(__name__)

cors = CORS(app, supports_credentials=True)

api = Api()
api = Api(version = 'v1.0.0', 
          title = 'hicetnunc-api', 
          description= 'A serverless API for getting dApps data',
          contact='hicetnunc2000@protonmail.com')

# NAMESPACES

api.add_namespace(mfp_api)
api.add_namespace(objkt_api)

api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)