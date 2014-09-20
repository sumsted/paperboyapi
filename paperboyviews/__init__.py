__author__ = 'scottumsted'
import os, yaml
from flask import Flask
app = Flask(__name__)
app.config.from_envvar('PAPERBOY_SETTINGS', silent=False)
from data.models import PaperboyModel
pdb = PaperboyModel()
import paperboyviews.views

