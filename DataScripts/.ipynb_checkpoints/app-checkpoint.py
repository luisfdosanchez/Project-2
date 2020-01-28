#pip install psycopg2-binary

from flask import Flask, jsonify, request, render_template
import os
import psycopg2
import pandas as pd
from postgreSQLpassword import passW


#conectar de python a postgres

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/save/prueba")
def save(variable1=0):
    conn = psycopg2.connect(database="newecobici",user="postgres", password=passW, host ="localhost",port="5432")
    df =pd.read_sql_query("Select anio_retiro, mes_retiro, count(*) from ecobicidf group by (anio_retiro, mes_retiro) order by (anio_retiro, mes_retiro)",conn)
    anio_retiro = df.anio_retiro.to_list()
    mes_retiro = df.mes_retiro.to_list()
    count = df["count"].to_list()


    return jsonify ({"anio_retiro":anio_retiro,"mes_retiro":mes_retiro,"count":count})

if __name__=="__main__":
    app.run()
