#!/usr/bin/python3

from urllib.request import urlopen
from urllib.parse import quote
import sys, os, json, pprint
from pathlib import Path
import click
import pandas as pd

""" json.dump({
    "dba":["BUS 210","BUS 220"]
           }, open("courselist.json","w")) """
courses=json.load(open("courselist.json","r"))
program_outcomes=json.load(open("pos.json","r"))
def download_course(department, course, storage):
    url="https://ects.ieu.edu.tr/new/syllabus.php?section=%s.ieu.edu.tr&course_code=%s"%(department,quote(course))
    print("Downloading URL:",url)
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    fname=course+".html"
    open(Path(storage)/"syllabi"/department/fname,"w").write(html)
    #print(html[:1000])
    print("Saved")

def parse_course(department, course, storage):
    print("PARSING:",department,course)
    fname=course+".html"
    html=open(Path(storage)/"syllabi"/department/fname,"r").read()
    import bs4
    soup = bs4.BeautifulSoup(html, "html.parser")
    data={"Activity":[],"ID":[],"Weighting":[]}
    idcounter=0
    for child in soup.find("table", id="evaluation_table1").contents[2:-1]:
        if type(child)==bs4.element.Tag and child.name=="tr":
            print("XXX ASSESSMENT XXX",
                  child.contents[1].get_text(),
                  child.contents[3].contents[1].get_text(),
                  child.contents[5].contents[1].get_text())
            activity=child.contents[1].get_text().strip()
            nact=child.contents[3].contents[1].get_text().strip()
            if nact and nact!="-":
                nact=int(nact)
                w=int(child.contents[5].contents[1].get_text().strip())
                for i in range(nact):
                    data["Activity"].append(activity)
                    idcounter+=1
                    data["ID"].append(idcounter)
                    data["Weighting"].append(w/nact)
            else:
                nact=None
                data["Activity"].append(activity)
                data["ID"].append(nact)
                data["Weighting"].append(None)
            pprint.pp(data)

    ono=0
    los=[]
    for child in soup.find("ul", id="outcome").find_all("li"):
        if type(child)==bs4.element.Tag:
            ono+=1
            print("XXX OUTCOME %d XXX"%ono,
                  child.get_text())
            los.append(child.get_text().strip())
    fname=course+".json"
    json.dump(los,open(Path(storage)/"lo-list"/department/fname,"w"))
    df = pd.DataFrame(data)
    for i in range(len(los)):
        colname="LO%d"%(i+1)
        df[colname]=df["Weighting"]/df["Weighting"]
    fname=course+".csv"
    df.to_csv(Path(storage)/"a-to-lo"/department/fname, index=False)
    #LOPO
    d={"LO_ID":[i+1 for i in range(len(los))]}
    pos=program_outcomes[department]
    for i in range(len(pos)):
        d["PO_%d"%(i+1)]=[None  for x in range(len(los))]
    df=pd.DataFrame(d)
    fname=course+".csv"
    df.to_csv(Path(storage)/"lo-to-po"/department/fname, index=False)

@click.command()
@click.option("--command", default="help", help="Give help")
@click.option("--storage", default="data", help="Where to store data.")
#@click.option("--name", prompt="Your name", help="The person to greet.")
def rootcmd(command, storage):
    """
    scrape.py --command <command> --storage dir ...
    Runs given command:
        download: download all business faculty syllabi from ects.ieu.edu.tr
        parse: parse downloaded syllabi into csv files
    """
    if command=="help":
        print(rootcmd.__doc__)
    elif command=="download":
        print("Downloading")
        for department in courses.keys():
            os.makedirs(Path(storage)/"syllabi"/department, exist_ok=True)
            for course in courses[department]:
                download_course(department,course, storage)
        print("Done downloading")
    elif command=="parse":
        for department in courses.keys():
            os.makedirs(Path(storage)/"a-to-lo"/department, exist_ok=True)
            os.makedirs(Path(storage)/"lo-list"/department, exist_ok=True)
            os.makedirs(Path(storage)/"lo-to-po"/department, exist_ok=True)
            for course in courses[department]:
                parse_course(department,course,storage)
    else:
        print("unknown command:", command)

if __name__ == '__main__':
    rootcmd()
