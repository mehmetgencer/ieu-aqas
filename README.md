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
        $ python3 gui.py