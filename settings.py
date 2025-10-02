import json
from pathlib import Path

localsettings ={
    "storage": "data"
}
storage=localsettings["storage"]
courses=json.load(open(Path(localsettings["storage"])/"courselist.json","r"))
departments=list(courses.keys())
program_outcomes=json.load(open(Path(localsettings["storage"])/"pos.json","r"))

def checkpasswd(passwd):
    return passwd in ["111"]