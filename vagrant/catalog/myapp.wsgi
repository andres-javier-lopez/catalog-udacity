#coding: utf-8
"""WSGI application."""
import os
import sys

here = os.path.dirname(__file__)
sys.path.insert(0, here)
from application import app as application

