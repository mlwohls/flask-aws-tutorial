'''
Simple Flask application to test deployment to Amazon Web Services
Uses Elastic Beanstalk and RDS

Author: Scott Rodkey - rodkeyscott@gmail.com

Step-by-step tutorial: https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80
'''

from flask import Flask, render_template, request, redirect, url_for
from application import db
from application.models import Data
from application.forms import EnterDBInfo, RetrieveDBInfo
# import psycopg2

### setup hunt club database ###
# conn = psycopg2.connect(host="ec2-52-201-127-122.compute-1.amazonaws.com", database="dalsteca66kgv9", user="udemeb02aj6tg6", password="p17p03n8l7pr0t8lvsfk1crol6d")
# cur = conn.cursor()


# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug=True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'

@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    form1 = EnterDBInfo(request.form)
    form2 = RetrieveDBInfo(request.form)

    if request.method == 'POST' and form1.validate():
        data_entered = Data(notes=form1.dbNotes.data)
        try:
            db.session.add(data_entered)
            db.session.commit()
            db.session.close()
        except:
            db.session.rollback()
        return render_template('thanks.html', notes=form1.dbNotes.data)

    if request.method == 'POST' and form2.validate():
        try:
            num_return = int(form2.numRetrieve.data)
            query_db = Data.query.order_by(Data.id.desc()).limit(num_return)
            for q in query_db:
                print(q.notes)
            db.session.close()
        except:
            db.session.rollback()
        return render_template('results.html', results=query_db, num_return=num_return)

    return render_template('index.html', form1=form1, form2=form2)

# @application.route('/hc_db', methods=['GET'])
# def hc_db():
#         cur.execute(''' SELECT id FROM candidates''')
#         test_a = cur.fetchall()
#         test_number = len(test_a)
#         output = ""
#         output += "<html><body>"
#         output += "<h1>" + str(test_number) + "</h1>"
#
#         output += "</body></html>"
#         return output







########### Only for running locally ###########
if __name__ == '__main__':
    application.run(host='0.0.0.0', debug=True)
