# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

#from crypt import methods
from services.pbiembedservice import PbiEmbedService
from services.aadservice import AadService
from utils import Utils
import requests
from flask import (
    Flask, render_template, request, session,
    url_for, redirect, send_from_directory, flash
)
from functools import wraps
import json
import os
from flask_sqlalchemy import SQLAlchemy
import logging
import sys

# Initialize the Flask app
app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)
# Load configuration
app.config.from_object('config.BaseConfig')

app.secret_key = b'23423423djkabsdjkqebh1297831y$%^&&^%&()_()+_!#@@@291q2314yu1298qwjhc'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(50))


def __init__(self, username, password):
    self.username = username
    self.password = password


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        try:
            if not session["authenticated"] and session["username"]:
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        except:
            return redirect(url_for('login'))
    return wrap


@app.route("/view-users/", methods=["GET"])
@login_required
def view_users():
    users = User.query.all()
    return render_template("users.html", data=users)


@app.route("/delete-user/", methods=["GET"])
@login_required
def delete_user():
    id = request.args['id']
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    flash("Deleted successfully")
    return redirect(url_for('view_users'))


@app.route('/signup', methods=['POST', 'GET'])
@login_required
def signup():
    msg = None
    if(request.method == "POST"):
        if(request.form["username"] and request.form["password"]):
            username = request.form["username"]
            password = request.form["password"]
            user = User(
                username=username,
                password=password
            )
            db.session.add(user)
            db.session.commit()
            flash("Your account is created")
            return redirect(url_for('signup'))
        else:
            msg = "Something wents wrong"
    return render_template("signup.html", msg=msg)


@app.route('/login', methods=['POST', 'GET'])
def login():
    msg = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not username and not password:
            flash("Please enter valid username and password")
            return redirect(url_for("login"))
        user = bool(User.query.filter_by(
            username=username, password=password).first())

        if user:
            session["authenticated"] = True
            session["username"] = username
            return redirect(url_for("index"))
        else:
            flash("Please enter valid username and password")
            return redirect(url_for("login"))

    return render_template("login.html", msg=msg)


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    del session["authenticated"]
    del session["username"]

    return redirect(url_for("login"))


@app.route('/')
@login_required
def index():
    '''Returns a static HTML page'''
    return render_template('index.html')


@app.route("/get-access-token/", methods=["GET"])
def get_access_token():
    token = PbiEmbedService().get_request_header()
    print(token['Authorization'])
    return token['Authorization']


@app.route('/getembedinfo', methods=['GET'])
@login_required
def get_embed_info():
    '''Returns report embed configuration'''

    config_result = Utils.check_config(app)
    if config_result is not None:
        return json.dumps({'errorMsg': config_result}), 500

    try:
        embed_info = PbiEmbedService().get_embed_params_for_single_report_user(
            "Edit", session["username"],
            ["MANAGER"], ["7d9ea59d-0bdd-4eb8-913c-f03cfb038fcc"],
            app.config['WORKSPACE_ID'], app.config['REPORT_ID'],
            "Retail Analysis Sample"
        )
        return embed_info
    except Exception as ex:
        return json.dumps({'errorMsg': str(ex)}), 500

@app.route('/getembedinfo-for-custom-report/', methods=['GET'])
@login_required
def get_embed_info_for_custom_reports():
    '''Returns report embed configuration'''

    config_result = Utils.check_config(app)
    if config_result is not None:
        return json.dumps({'errorMsg': config_result}), 500

    try:
        embed_info = PbiEmbedService().get_embed_params_for_single_report_user(
            "Edit", session["username"],
            ["MANAGER"], ["7d9ea59d-0bdd-4eb8-913c-f03cfb038fcc"],
            app.config['WORKSPACE_ID'], app.config['CUSTOM_REPORT_ID'],
            "CreateCustomReport"
        )
        return embed_info
    except Exception as ex:
        return json.dumps({'errorMsg': str(ex)}), 500


@app.route('/favicon.ico', methods=['GET'])
@login_required
def getfavicon():
    '''Returns path of the favicon to be rendered'''

    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico', mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run(debug=True)

