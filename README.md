# Requirements

Some help resources used for this code:

* https://realpython.com/python-web-scraping-practical-introduction/
* https://www.crummy.com/software/BeautifulSoup/bs4/doc/

To be installed in a virtual environment with "pip3 install ...":
* bs4
* click
* dash-ag-grid (automatically installs Dash as well)
* numpy
* pandas
* pip3 install -I gunicorn (on server)

Saved as:

        $ pip3 freeze > requirements.txt 

# Virtual environment

Something like:

        at home: 
        $ python3 -m venv venv-AQAS-app
        then
        $ source ~/tmp/venv-AQAS-app/bin/activate

# Work pipeline

In the following order:

        $ ./scrape.py --command download
        $ ./scrape.py --command parse
        $ HOST=0.0.0.0 PORT=8050 python3 gui.py

# Run test server

Something like:

    $cd tmp-akkreditasyon-webscrape
    $~/venv-AQAS-app/bin/gunicorn  -w 4 -b 0.0.0.0:8050 app:app --daemon
    $pkill gunicorn

# Evidence matching scheme

It is difficult to match OBS grade exports (which are the evidence of learning outcome achievement) with the matrices based on syllbus, for many reasons including the changes in syllabi and detached processes of OBS grade column creation and syllabus entry. Therefor a 'coarse' scheme for matching evidence excel files to assessment activities is proposed as follows:

* a list of evidence column no's (counts from 1) match a list of activity IDs (multi-to-multi mapping)
* When the left hand side is multiple evidence columns, their 'weighted' average is taken, using OBS percentages as weights.
* When the right hand side is multiple activities, the above calculated average is used as the assessment value for all of them.
* All grades are assumed to be over 100
* Use of the above scheme should not change the resulting student grade (HBN in OBS, over 100)
* Evidence files must be named as "year-year-semester-sectionno.xlsx" under the folder for the course. There can be multiple files but they all use the matching scheme stored in "_matching.json" in the same folder
* OBS table header names have the structure "activity(%xx)_instructortag"