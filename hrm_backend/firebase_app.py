# hrm_project/firebase_app.py

import os
import firebase_admin
from firebase_admin import credentials
from decouple import config

# Use an environment variable to store the path securely
cred_path = config('FIREBASE_CREDENTIALS')
cred = credentials.Certificate(cred_path)
firebase_app = firebase_admin.initialize_app(cred)
