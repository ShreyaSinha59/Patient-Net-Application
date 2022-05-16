#!/usr/bin/env python

"""
Columbia's COMS W4111.003 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for
import random
import string

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


# Database URI
DATABASEURI = "postgresql://ss6415:sv2637ss6415@35.211.155.104/proj1part2"
engine = create_engine(DATABASEURI)

@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print ("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


@app.route('/')
def landing():
  return render_template("landing.html")


@app.route('/organization_register', methods=['GET', 'POST'])
def organization_register():
    if request.method == 'POST':
        try:

            username = request.form['username']
            organization_name = request.form['organization_name']
            deposit = request.form['organization_balance']
            password = request.form['password']

            letter = string.ascii_lowercase
            random_id = ''.join(random.choice(letter) for i in range(18))
            print(random_id)

            engine.execute("INSERT INTO credentials(username, password, id, type) VALUES ('{}', '{}', '{}','organization')".format(username, password, random_id))
            engine.execute("INSERT INTO organization(organization_ID,organization_name,organization_balance) VALUES ('{}', '{}', '{}')".format(random_id,organization_name,deposit))
            #engine.commit()
            return redirect("/login")

        except Exception as e:
            print(e)
            #engine.rollback()
            return render_template('organization_register.html', error='Servor Error')
    else:
        return render_template('organization_register.html')



@app.route('/hospital_register', methods=['GET', 'POST'])
def hospital_register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            hospital_name = request.form['hospital_name']
            hospital_city = request.form['hospital_city']
            hospital_address = request.form['hospital_address']
            deposit = request.form['hospital_balance']
            password = request.form['password']

            letter = string.ascii_lowercase
            random_id = ''.join(random.choice(letter) for i in range(24))
            print(random_id)

            engine.execute("INSERT INTO credentials(username, password, id, type) VALUES ('{}', '{}', '{}', 'hospital')".format(username, password, random_id))
            engine.execute("INSERT INTO hospital(hospital_ID,hospital_name,hospital_address,hospital_city,hospital_balance) VALUES ('{}', '{}', '{}', '{}', {})".format(random_id,hospital_name,hospital_address,hospital_city,deposit))
            #engine.commit()
            return redirect("/login")

        except Exception as e:
            print(e)
            #engine.rollback()
            return render_template('hospital_register.html', error='Servor Error')
    else:
        return render_template('hospital_register.html')


@app.route('/researcher_register', methods=['GET', 'POST'])
def researcher_register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            organization = request.form['organization']
            deposit = request.form['deposit']
            password = request.form['password']

            exec1 = engine.execute("SELECT c.id FROM credentials c WHERE c.username='%s'" % (username,))
            if exec1.fetchone() is not None:
                return render_template('researcher_register.html', error='User Already Exists')


            exec = engine.execute("SELECT o.organization_ID FROM organization o WHERE o.organization_name='%s'" % (organization,))
            hosp_ID = exec.fetchone()[0]
            print(hosp_ID)
            letter = string.ascii_lowercase
            random_id = ''.join(random.choice(letter) for i in range(24))
            print(random_id)

            eng1 = engine.execute("INSERT INTO researcher(researcher_ID, researcher_Balance, organization_id) VALUES ('{}', '{}', '{}')".format(random_id, deposit, hosp_ID))
            eng2 = engine.execute("INSERT INTO credentials(username, password, id, type) VALUES ('{}', '{}', '{}', 'researcher')".format(username, password, random_id))
            #eng1.commit()
            #eng2.commit()
            return redirect("/login")

        except Exception as e:

            print(e)
            #engine.rollback()
            return render_template('researcher_register.html', error='Servor Error')
    else:
        return render_template('researcher_register.html')


@app.route('/patient_register', methods=['GET', 'POST'])
def patient_register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            insurance_provider = request.form['insurance_provider']
            insurance_provider_address = request.form['insurance_provider_address']
            hospital = request.form['hospital']
            race = request.form['race']
            age = request.form['age']
            blood_group = request.form['blood_group']
            height = request.form['height']
            weight = request.form['weight']
            current_city = request.form['current_city']
            gender = request.form['gender']
            password = request.form['password']

            query = "SELECT insurer_id FROM insurance_provider WHERE insurer_name='{}'".format(insurance_provider)
            #print(query)
            exec = engine.execute(query)
            #print(exec.fetchone())
            ins_ID = exec.fetchone()[0]
            print(ins_ID)
            query2 = "SELECT hospital_id FROM hospital WHERE hospital_name='{}'".format(hospital)
            print(query2)
            exec2 = engine.execute(query2)
            hosp_ID = exec2.fetchone()[0]
            print(hosp_ID)
            letter = string.ascii_lowercase
            random_id = ''.join(random.choice(letter) for i in range(24))
            print(random_id)

            engine.execute("INSERT INTO credentials(username, password, id, type) VALUES ('{}', '{}', '{}','patient')".format(username, password, random_id))
            #DOB might be problem
            engine.execute("INSERT INTO patient(patient_ID,date_of_birth,race,height,weight,gender,current_city,blood_group,patient_balance,hospital_ID,insurer_ID) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', 0, '{}', '{}')".format(random_id,age,race,height,weight,gender,current_city,blood_group,hosp_ID,ins_ID))
            #engine.commit()
            return redirect("/login")

        except Exception as e:
            print(e)
            #engine.rollback()
            return render_template('patient_register.html', error='Servor Error')
    else:
        return render_template('patient_register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']

            exec = engine.execute("SELECT c.password FROM credentials c WHERE c.username='%s'" % (username,))
            actual_password = exec.fetchone()[0]
            print(actual_password)
            if actual_password == password:
                exec2 = engine.execute("SELECT c.type FROM credentials c WHERE c.username='%s'" % (username,))
                dashboard = exec2.fetchone()[0]
                print(dashboard)
                exec3 = engine.execute("SELECT c.id FROM credentials c WHERE c.username='%s'" % (username,))
                user_id = exec3.fetchone()[0]
                print(user_id)

                """
                if dashboard == 'organization':
                    return organization_dashboard(user_id, username)
                if dashboard == 'researcher':
                    return researcher_dashboard(user_id, username)
                if dashboard == 'patient':
                    return patient_dashboard(user_id, username)
                if dashboard == 'hospital':
                    return hospital_dashboard(user_id, username)
                """

                redirection = "{}_dashboard".format(dashboard)
                #return redirect(redirection, user_id = user_id, username = username)
                return redirect((url_for(redirection, username = username, user_id=user_id)))
                #redirection = "/{}_dashboard?username=%s".format(dashboard)
                ##return redirect("/{}_dashboard?username=%s".format(dashboard) % username))
            else:
                return render_template('login.html', error='Incorrect Password')

        except Exception as e:
            print(e)
            #engine.rollback()
            return render_template('login.html', error='Servor Error')
    else:
        return render_template('login.html')


@app.route('/researcher_dashboard', methods=['POST','GET'])
def researcher_dashboard():
    if request.method == 'POST':
        try:
            researcher_id = request.args.get('user_id').strip()
            researcher_username = request.args.get('username').strip()

            Date_of_birth=request.form['Date_of_birth']
            Race=request.form['Race']
            Gender=request.form['Gender']
            Height=request.form['Height']
            Weight=request.form['Weight']
            Current_city =request.form['Current_city']
            Blood_Group= request.form['Blood_Group']
            Medications= request.form['Medications']
            Diagnosis=request.form['Diagnosis']
            Risk_factor=request.form['Risk_factor']


            #query = "SELECT * FROM patient INNER join electronic_health_records on patient.patient_id= electronic_Health_Records.patientid WHERE date_of_birth='{}' and race='{}' and gender='{}' and height='{}' and Weight='{}' and Current_city='{}' and Blood_Group='{}' and Medications='{}' and Diagnosis='{}' and Risk_factor='{}'".format(Date_of_birth, Race, Gender, Height, Weight, Current_city, Blood_Group, Medications, Diagnosis, Risk_factor)
            query = "SELECT * FROM patient INNER join electronic_health_records on patient.patient_id= electronic_health_records.patient_id WHERE race='{}' and gender='{}' and height>{} and weight>{} and current_city='{}' and blood_group='{}' and medication='{}' and diagnosis='{}' and risk_factor>{}".format(Race, Gender, Height, Weight, Current_city, Blood_Group, Medications, Diagnosis, Risk_factor)
            exec = engine.execute(query)

            from pandas import DataFrame
            result = DataFrame(exec.fetchall())
            cost = len(result.index) * 50
            if cost == 0:
                return render_template('researcher_dashboard.html', user_id = researcher_id, username = researcher_username, error = 'No Patients Found')
            result.columns = exec.keys()
            table = result.to_html(index=False)

            patient_list = result['patient_id'].values

            engine.execute("UPDATE researcher SET researcher_balance = researcher_balance - {} WHERE researcher_id = '{}'".format(cost, researcher_id))

            print(patient_list)
            #print(result.to_string())

            for patient in patient_list:
                engine.execute("UPDATE patient SET patient_balance = patient_balance + {} WHERE patient_id = '{}'".format(cost/len(result.index), patient[0]))


            return render_template('views.html', table=table, user_id = researcher_id, username = researcher_username)

        except Exception as e:
            print(e)
            return render_template('researcher_dashboard.html', user_id = researcher_id, username = researcher_username, error = 'Servor Error: Insufficient Balance or Invalid Query')
    else:
        researcher_id = request.args.get('user_id').strip()
        researcher_username = request.args.get('username').strip()
        return render_template('researcher_dashboard.html', user_id = researcher_id, username = researcher_username, error = '')


@app.route('/patient_dashboard',methods=['POST','GET'])
def patient_dashboard():
    if request.method == 'POST':
        try:
            patient_username = request.args.get('username').strip()
            letter = string.ascii_lowercase
            record_id = random.randint(10000,900000000)
            #print(random_id)
            #record_id = "r@".join(random.choice(letter) for i in range(24))
            patient_id = request.args.get('user_id').strip()
            Medications = request.form["Medications"]
            Diagnosis = request.form["Diagnosis"]
            Risk_factor = request.form["Risk_factor"]
            engine.execute("INSERT INTO electronic_health_records(record_id,patient_id,medication,diagnosis,risk_factor) VALUES ('{}','{}','{}','{}','{}')".format(record_id,patient_id,Medications,Diagnosis,Risk_factor))
            return render_template("patient_dashboard.html", user_id = patient_id, username = patient_username, error = 'Electronic Health Record Successfully Uploaded. When a Researcher Queries your data you will be compensated.')
        except Exception as e:
            patient_id = request.args.get('user_id').strip()
            patient_username = request.args.get('username').strip()
            print(e)
            return render_template('patient_dashboard.html', user_id = patient_id, username = patient_username, error = 'Servor Error')

    else:
        patient_id = request.args.get('user_id').strip()
        patient_username = request.args.get('username').strip()
        return render_template("patient_dashboard.html", error = '', user_id = patient_id, username = patient_username)



@app.route('/hospital_dashboard')
def hospital_dashboard():
    #print(request.args.get('user_id'))
    #print(request.args.get('username'))
    return render_template('hospital_dashboard.html', user_id = request.args.get('user_id'), username=request.args.get('username'))



@app.route('/organization_dashboard')
def organization_dashboard():
    #print(request.args.get('user_id'))
    #print(request.args.get('username'))
    return render_template('organization_dashboard.html', user_id = request.args.get('user_id'), username=request.args.get('username'))

@app.route('/balance_dashboard')
def balance_dashboard():
    user_id = request.args.get('user_id').strip()
    print(user_id)
    #username = request.args.get('username')
    print("SELECT c.type FROM credentials c WHERE c.id='%s'" % (user_id,))
    exec4 = engine.execute("SELECT c.type FROM credentials c WHERE c.id='%s'" % (user_id,))
    role = exec4.fetchone()[0]
    print(role)
    balance = 0

    if role == 'organization':
        print("SELECT c.organization_balance FROM organization c WHERE c.organization_ID='%s'" % (user_id,))
        exec = engine.execute("SELECT c.organization_balance FROM organization c WHERE c.organization_id='%s'" % (user_id,))
        balance = exec.fetchone()[0]

    if role == 'researcher':
        exec = engine.execute("SELECT c.researcher_balance FROM researcher c WHERE c.researcher_id='%s'" % (user_id,))
        balance = exec.fetchone()[0]

    if role == 'patient':
        exec = engine.execute("SELECT c.patient_balance FROM patient c WHERE c.patient_id='%s'" % (user_id,))
        balance = exec.fetchone()[0]

    if role == 'hospital':
        exec = engine.execute("SELECT c.hospital_balance FROM hospital c WHERE c.hospital_id='%s'" % (user_id,))
        balance = exec.fetchone()[0]

    return render_template('balance_dashboard.html', user_id = request.args.get('user_id'), current_balance = balance)



if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print ("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
