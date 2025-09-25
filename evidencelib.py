#!/usr/bin/python3

import sys, os, json, pprint, glob
from pathlib import Path
import click
import pandas as pd

def make_path_pattern(storage, department, course,pattern):
    """
    Makes a glob pattern for file listing, using '*'s in place of department and course if they are empty
    User provided 'pattern' is appended at the end
    """
    tmp=Path(storage)/"evidence"
    pattern="*.xlsx"
    if department: 
        tmp=tmp/department
        if course: tmp=tmp/course
        else:pattern="*/"+pattern
    else:
        pattern="*/*/"+pattern
    return tmp,pattern

def require_department_and_course(department, course):
    if not department or not course:raise Exception("Department and course must be provided for this command")

def list_evidence(storage, department, course):
    tmp,pattern=make_path_pattern(storage, department, course,"*.xlsx")
    print("Listing:",tmp)
    evidence_files=[x for x in tmp.glob(pattern)]
    for x in evidence_files: print(x)
    return evidence_files

def get_matchscheme(storage, department, course):
    tmp=Path(storage)/"evidence"/department/course/"_matching.json"
    if os.path.exists(tmp):
        retval=json.load(open(tmp,"r"))
        pprint.pp(retval)
        return retval
    else:
        return None

def get_alo_matrix(storage, department, course):
    require_department_and_course(department, course)
    fname=course+".csv"
    df=pd.read_csv(Path(storage)/"a-to-lo"/department/fname)
    return df

def check_match_scheme(storage, department, course,check_evidence=False):
    """
    Checks if matching scheme uses all assessment activities in syllabus and maps all grades in evidence file(s) to some activity 
    (latter if check_evidence is "true").
    if check_evidence is true then evidence files are opened, number of columns checked to match in all, and 
    column ids's are checked, i.e if all grades in evidence file(s) are mapped to some activity.
    The return value is a dictionary
    """
    require_department_and_course(department, course)
    ms=get_matchscheme(storage, department, course)
    if not ms:
        return False, "No match scheme"
    df=get_alo_matrix(storage, department, course)
    print("MATCH SCHEME:")
    pprint.pp(ms)
    ids=list(df["ID"].dropna().astype(int).unique())
    anames=["%s (ID:%d)"%(row["Activity"],row["ID"]) for index,row in df.query("ID==ID").iterrows()] #since NaN==NaN is false!
    print("IDs",ids,anames)
    usedids=[x for il in ms.values() for x in il["to"]]
    print("Used ids",usedids)
    retval={}
    retval["IDs_unevidenced"]=list(set(ids)-set(usedids))
    retval["IDs_nonexistent"]=list(set(usedids)-set(ids))
    retval["evidences_inconsistent"]=None
    retval["evidences_unmatched"]=None
    retval["evidences_nonexistent"]=None
    print("Check evidence",check_evidence)
    if check_evidence:
        numcol=None
        ncmap={}
        problems=False
        for fname in list_evidence(storage, department, course):
            print("will read evidence",fname)
            df=pd.read_excel(fname)
            evnames=[x.split("_")[0].replace(' ', '') for x in df.columns[5:-3]]
            #df.columns = df.columns.str.replace(' ', '')
            ncmap[str(fname)]=(len(df.columns)-8,evnames)
            if numcol is None:
                numcol=len(df.columns)
            else:
                if numcol!=len(df.columns):
                    print("Number of columns %d is different from earlier %d"%(len(df.columns),numcol))
                    problems=True
        if problems:
            retval["evidences_inconsistent"]=ncmap
        if numcol is not None:
            print("Numcol",numcol)
            cols=list(range(1,numcol-7))
            print("cols",cols)
            usedevidences=[x for il in ms.values() for x in il["from"]]
            retval["evidences_unmatched"]=list(set(cols)-set(usedevidences))
            retval["evidences_nonexistent"]=list(set(usedevidences)-set(cols))
    print("RETVAL")
    pprint.pp(retval)
    return True, retval

@click.command()
@click.option("--command", default="help", help="Give help")
@click.option("--storage", default="data", help="Where to store data.")
@click.option("--department", default="")
@click.option("--course", default="")
def rootcmd(command, storage, department, course):
    """
    evidencelib.py --command <command> --storage dir ... --department=... --course=...
    Runs given command:
        list : List evidence
        get-match-scheme: check if match scheme exists and return it
        check-match-scheme: check if match scheme exists and have any errors
        check-evidence-structure: check if evidence structure is compatible with match-scheme
    """
    if command=="help":
        print(rootcmd.__doc__)
    elif command=="list":
        retval=list_evidence(storage,department,course)
    elif command=="get-match-scheme":
        retval=get_matchscheme(storage,department,course)
        if not retval:print("No match scheme found for departmen-course")
    elif command=="check-match-scheme":
        status,retval=check_match_scheme(storage,department,course,check_evidence=False)
        if not status:print("Check failed or not found")
    elif command=="check-evidence-structure":
        check_match_scheme(storage,department,course,check_evidence=True)
    else:
        print("Unknown command:",command)
if __name__ == '__main__':
    rootcmd()