from flask import Flask, jsonify, request, render_template, Response
import psycopg2
import pandas as pd
from postgreSQLpassword import passW

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dash1")
def dashB1():
    return render_template("dashboard1.html")

@app.route("/dash2")
def dashB2():
    return render_template("dashboard2.html")

@app.route("/dash3")
def dashB3():
    return render_template("dashboard3.html")

@app.route("/contacts")
def contacts():
    return render_template("contacts.html")



@app.route("/api/dash1", methods=["POST"])
def dash1():
    miRequest = request.json

    varYrD1 = int(miRequest["valueYearD1"])

    conn = psycopg2.connect(database="newecobici",user="postgres", password=passW, host ="localhost",port="5432")
    df = pd.read_sql_query(f'with mes as(select genero_usuario,mes_retiro,count(genero_usuario) as numero_usuarios,avg(edad_usuario) as edad_promedio,AVG((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro)) AS avgtime from ecobicidf where anio_retiro in ({varYrD1}) group by 1,2) select genero_usuario, sum(numero_usuarios) as numero_usuarios, avg(edad_promedio) as avg_edad, AVG(avgtime) AS avg_time, avg(numero_usuarios) as avg_usuarios from mes group by 1',conn)
    conn.close()
    json = df.to_json(orient='records',date_format='iso')
    response = Response(response=json, status=200, mimetype="application/json")
    return(response)

@app.route("/api/dash2", methods=["POST"])
def dash2():
    miRequest = request.json
    varDisagg = str(miRequest["valueDisagg"])
    varGtype = str(miRequest["valueGtype"])
    
    plugQueryBegin=""
    plugQueryMid=""
    plugQueryEnd=""

    if varGtype=="daily":
        plugQueryBegin="SELECT fecha_retiro AS ddate, "
        plugQueryEnd=" GROUP BY(fecha_retiro) ORDER BY(fecha_retiro);"
    elif varGtype=="monthly":
        plugQueryBegin="SELECT TO_CHAR(DATE_TRUNC('month',fecha_retiro)::DATE,'Mon-YYYY') AS ddate, "
        plugQueryEnd=" GROUP BY(DATE_TRUNC('month',fecha_retiro)::date ) ORDER BY (DATE_TRUNC('month',fecha_retiro)::DATE);"
    elif varGtype=="yearly":
        plugQueryBegin="SELECT EXTRACT(YEAR FROM fecha_retiro) as ddate, "
        plugQueryEnd=" GROUP BY EXTRACT(YEAR FROM fecha_retiro);"

    if varDisagg=="all":
        plugQueryMid="COUNT(*) FROM ecobicidf"
    elif varDisagg=="gender":
        plugQueryMid="SUM(CASE WHEN genero_usuario = 'F' THEN 1 ELSE 0 END) AS tot_fem, SUM(CASE WHEN genero_usuario = 'M' THEN 1 ELSE 0 END) AS tot_masc, 100*AVG(CASE WHEN genero_usuario = 'F' THEN 1 ELSE 0 END) AS pct_fem, 100*AVG(CASE WHEN genero_usuario = 'M' THEN 1 ELSE 0 END) AS pct_masc, AVG(CASE WHEN genero_usuario = 'F' THEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro)) ELSE NULL END) AS time_fem, AVG(CASE WHEN genero_usuario = 'M' THEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro)) ELSE NULL END) AS time_masc, AVG(CASE WHEN genero_usuario = 'F' THEN edad_usuario ELSE NULL END) AS age_fem, AVG(CASE WHEN genero_usuario = 'M' THEN edad_usuario ELSE NULL END) AS age_masc FROM ecobicidf"
    elif varDisagg=="age":
        plugQueryMid="SUM(CASE WHEN edad_usuario BETWEEN 0 AND 25 THEN 1 ELSE 0 END) AS tot_you, SUM(CASE WHEN edad_usuario BETWEEN 26 AND 35 THEN 1 ELSE 0 END) AS tot_mid, SUM(CASE WHEN edad_usuario BETWEEN 36 AND 45 THEN 1 ELSE 0 END) AS tot_old, SUM(CASE WHEN edad_usuario>=46 THEN 1 ELSE 0 END) AS tot_eld, 100*AVG(CASE WHEN edad_usuario BETWEEN 0 AND 25 THEN 1 ELSE 0 END) AS pct_you, 100*AVG(CASE WHEN edad_usuario BETWEEN 26 AND 35 THEN 1 ELSE 0 END) AS pct_mid, 100*AVG(CASE WHEN edad_usuario BETWEEN 36 AND 45 THEN 1 ELSE 0 END) AS pct_old, 100*AVG(CASE WHEN edad_usuario>=46 THEN 1 ELSE 0 END) AS pct_eld, AVG(CASE WHEN edad_usuario BETWEEN 0 AND 25 THEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro)) ELSE NULL END) AS time_you, AVG(CASE WHEN edad_usuario BETWEEN 26 AND 35 THEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro)) ELSE NULL END) AS time_mid, AVG(CASE WHEN edad_usuario BETWEEN 36 AND 45 THEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro)) ELSE NULL END) AS time_old, AVG(CASE WHEN edad_usuario>=46 THEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro)) ELSE NULL END) AS time_eld, AVG(CASE WHEN edad_usuario BETWEEN 0 AND 25 THEN edad_usuario ELSE NULL END) AS age_you, AVG(CASE WHEN edad_usuario BETWEEN 26 AND 35 THEN edad_usuario ELSE NULL END) AS age_mid, AVG(CASE WHEN edad_usuario BETWEEN 36 AND 45 THEN edad_usuario ELSE NULL END) AS age_old, AVG(CASE WHEN edad_usuario>=46 THEN edad_usuario ELSE NULL END) AS age_eld FROM ecobicidf"
    elif varDisagg=="time":
        plugQueryMid="SUM(CASE WHEN (hora_retiro>='00:00:00' AND hora_retiro<'06:00:00') THEN 1 ELSE 0 END) AS tot_beg, SUM(CASE WHEN (hora_retiro>='06:00:00' AND hora_retiro<'12:00:00') THEN 1 ELSE 0 END) AS tot_mor, SUM(CASE WHEN (hora_retiro>='12:00:00' AND hora_retiro<'18:00:00') THEN 1 ELSE 0 END) AS tot_aft, SUM(CASE WHEN (hora_retiro>='18:00:00') THEN 1 ELSE 0 END) AS tot_eve, 100*AVG(CASE WHEN (hora_retiro>='00:00:00' AND hora_retiro<'06:00:00') THEN 1 ELSE 0 END) AS pct_beg, 100*AVG(CASE WHEN (hora_retiro>='06:00:00' AND hora_retiro<'12:00:00') THEN 1 ELSE 0 END) AS pct_mor, 100*AVG(CASE WHEN (hora_retiro>='12:00:00' AND hora_retiro<'18:00:00') THEN 1 ELSE 0 END) AS pct_aft, 100*AVG(CASE WHEN (hora_retiro>='18:00:00') THEN 1 ELSE 0 END) AS pct_eve, AVG(CASE WHEN (hora_retiro>='00:00:00' AND hora_retiro<'06:00:00') THEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro)) ELSE NULL END) AS time_beg, AVG(CASE WHEN (hora_retiro>='06:00:00' AND hora_retiro<'12:00:00') THEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro)) ELSE NULL END) AS time_mor, AVG(CASE WHEN (hora_retiro>='12:00:00' AND hora_retiro<'18:00:00') THEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro)) ELSE NULL END) AS time_aft, AVG(CASE WHEN (hora_retiro>='18:00:00') THEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro)) ELSE NULL END) AS time_eve, AVG(CASE WHEN (hora_retiro>='00:00:00' AND hora_retiro<'06:00:00') THEN edad_usuario ELSE NULL END) AS age_beg, AVG(CASE WHEN (hora_retiro>='06:00:00' AND hora_retiro<'12:00:00') THEN edad_usuario ELSE NULL END) AS age_mor, AVG(CASE WHEN (hora_retiro>='12:00:00' AND hora_retiro<'18:00:00') THEN edad_usuario ELSE NULL END) AS age_aft, AVG(CASE WHEN (hora_retiro>='18:00:00') THEN edad_usuario ELSE NULL END) AS age_eve FROM ecobicidf"
    elif varDisagg=="length":
        plugQueryMid="SUM(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:00:00' AND ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))<'00:10:00' THEN 1 ELSE 0 END) AS tot_zeroten, SUM(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:10:00' AND ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))<'00:20:00' THEN 1 ELSE 0 END) AS tot_tentwenty, SUM(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:20:00' AND ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))<'00:30:00' THEN 1 ELSE 0 END) AS tot_tewntythirty, SUM(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:30:00' THEN 1 ELSE 0 END) AS tot_thritymore, 100*AVG(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:00:00' AND ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))<'00:10:00' THEN 1 ELSE 0 END) AS pct_zeroten, 100*AVG(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:10:00' AND ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))<'00:20:00' THEN 1 ELSE 0 END) AS pct_tentwenty, 100*AVG(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:20:00' AND ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))<'00:30:00' THEN 1 ELSE 0 END) AS pct_tewntythirty, 100*AVG(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:30:00' THEN 1 ELSE 0 END) AS pct_thritymore, AVG(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:00:00' AND ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))<'00:10:00' THEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro)) ELSE NULL END) AS time_zeroten, AVG(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:10:00' AND ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))<'00:20:00' THEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro)) ELSE NULL END) AS time_tentwenty, AVG(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:20:00' AND ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))<'00:30:00' THEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro)) ELSE NULL END) AS time_tewntythirty, AVG(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:30:00' THEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro)) ELSE NULL END) AS time_thritymore, AVG(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:00:00' AND ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))<'00:10:00' THEN edad_usuario ELSE NULL END) AS age_zeroten, AVG(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:10:00' AND ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))<'00:20:00' THEN edad_usuario ELSE NULL END) AS age_tentwenty, AVG(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:20:00' AND ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))<'00:30:00' THEN edad_usuario ELSE NULL END) AS age_tewntythirty, AVG(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:30:00' THEN edad_usuario ELSE NULL END) AS age_thritymore FROM ecobicidf"

    plugQuery=plugQueryBegin+plugQueryMid+plugQueryEnd

    conn = psycopg2.connect(database="newecobici",user="postgres", password=passW, host ="localhost",port="5432")
    df = pd.read_sql_query(plugQuery,conn)
    conn.close()
    json = df.to_json(orient='records',date_format='iso')
    response = Response(response=json, status=200, mimetype="application/json")
    return(response)
    
if __name__=="__main__":
    app.run()
