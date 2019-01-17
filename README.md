# LifeWorks 

Flask app serving csv data using pandas.
Graphs mobile data coverage for selected area.


## Prerequisites

- python version 3.7+
- pip


## Setup

- Create your virtualenv if required
- `git clone git@github.com:VaughnDV/workslife.git`
- `cd workslife`
- With your own secret keys
- `export SECRET_KEY="your-own-very-sercert-key"`
- `export WTF_CSRF_SECRET_KEY="your-own-very-sercert-csrf-key"`
- `pip install -r requirements.txt`
- `python app.py`


## Usage

- Navigate browser to: `http://127.0.0.1:5000/` 


### Brief background to my decisions

#### As it is an MVP I used:

- Flask as its good for prototyping and rapid development
- Pandas as its easy to work with and modify data and its fast
- Highchart js because I saw this as an opportunity to try it out
- Python as it it cross platform, and its what I am comfortable with

#### Other considerations with regards to all libraries used:

- They must be well documented
- Well maintained
- Stable and commonly used in production
- Decent sized online community 

Thank you!