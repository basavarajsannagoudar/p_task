Below are the steps required to get this working on a base linux system.

Install all required dependencies
Install and Configure Web Server
Start Web Server

Now, we will need to create a virtual environment and install all the dependencies:
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

Start web server
FLASK_APP=app.py flask run --host=0.0.0.0
open index.html file for accessing the investors
