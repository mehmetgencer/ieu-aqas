#!/usr/bin/python3

import sys, os, json, pprint
from pathlib import Path
from settings import *

def get_pocontrib_from_sylabus(department,course):
    fname=course+".json"
    return json.load(open(Path(storage)/"pocontrib-in-syllabus"/department/fname,"r"))
