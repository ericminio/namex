import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from solr_feeder.feeder import Feeder
from config import TestConfig

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(TestConfig)
db = SQLAlchemy(app)
solr = os.getenv('SOLR_TEST_URL') + '/solr'

Feeder(db, solr).go()
