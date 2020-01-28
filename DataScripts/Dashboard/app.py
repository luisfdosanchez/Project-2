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
    plugQueryMid1=""
    plugQueryMid2=""
    plugQueryMid3=""
    plugQueryEnd=""

    if varGtype=="daily":
        plugQueryBegin="SELECT fecha_retiro AS ddate, "
        plugQueryEnd=" FROM ecobicidf GROUP BY(fecha_retiro) ORDER BY(fecha_retiro);"
    elif varGtype=="monthly":
        plugQueryBegin="SELECT TO_CHAR(DATE_TRUNC('month',fecha_retiro)::DATE,'Mon-YYYY') AS ddate, "
        plugQueryEnd=" FROM ecobicidf GROUP BY(DATE_TRUNC('month',fecha_retiro)::date ) ORDER BY (DATE_TRUNC('month',fecha_retiro)::DATE);"
    elif varGtype=="yearly":
        plugQueryBegin="SELECT EXTRACT(YEAR FROM fecha_retiro) as ddate, "
        plugQueryEnd=" FROM ecobicidf GROUP BY EXTRACT(YEAR FROM fecha_retiro);"
    elif varGtype=="dayOfWeek":
        plugQueryBegin="WITH sub AS(SELECT fecha_retiro, "
        plugQueryMid2=" FROM ecobicidf GROUP BY(fecha_retiro)) SELECT TO_CHAR(fecha_retiro,'Dy') AS ddate, "
        plugQueryEnd=" , TO_CHAR(fecha_retiro, 'D') AS junk FROM sub GROUP BY(TO_CHAR(fecha_retiro,'Dy'),TO_CHAR(fecha_retiro,'D')) ORDER BY junk;"
        if varDisagg=="all":
            plugQueryMid3=" AVG(count) AS count "
        elif varDisagg=="gender":
            plugQueryMid3=" AVG(tot_fem) AS tot_fem, AVG(tot_masc) AS tot_masc "
        elif varDisagg=="age":
            plugQueryMid3=" AVG(tot_you) AS tot_you, AVG(tot_mid) AS tot_mid, AVG(tot_old) AS tot_old, AVG(tot_eld) AS tot_eld "
        elif varDisagg=="time":
            plugQueryMid3=" AVG(tot_beg) AS tot_beg, AVG(tot_mor) AS tot_mor, AVG(tot_aft) AS tot_aft, AVG(tot_eve) AS tot_eve "
        elif varDisagg=="length":
            plugQueryMid3=" AVG(tot_zeroten) AS tot_zeroten, AVG(tot_tentwenty) AS tot_tentwenty, AVG(tot_tewntythirty) AS tot_tewntythirty, AVG(tot_thritymore) AS tot_thritymore "
    elif varGtype=="monthOfYear":
        plugQueryBegin="WITH sub AS(SELECT fecha_retiro, "
        plugQueryMid2=" FROM ecobicidf GROUP BY(fecha_retiro)) SELECT TO_CHAR(fecha_retiro,'Mon') AS ddate, "
        plugQueryEnd=" , TO_CHAR(fecha_retiro, 'MM') AS junk FROM sub GROUP BY(TO_CHAR(fecha_retiro,'MM'), TO_CHAR(fecha_retiro,'Mon')) ORDER BY junk;"
        if varDisagg=="all":
            plugQueryMid3=" AVG(count) AS count "
        elif varDisagg=="gender":
            plugQueryMid3=" AVG(tot_fem) AS tot_fem, AVG(tot_masc) AS tot_masc "
        elif varDisagg=="age":
            plugQueryMid3=" AVG(tot_you) AS tot_you, AVG(tot_mid) AS tot_mid, AVG(tot_old) AS tot_old, AVG(tot_eld) AS tot_eld "
        elif varDisagg=="time":
            plugQueryMid3=" AVG(tot_beg) AS tot_beg, AVG(tot_mor) AS tot_mor, AVG(tot_aft) AS tot_aft, AVG(tot_eve) AS tot_eve "
        elif varDisagg=="length":
            plugQueryMid3=" AVG(tot_zeroten) AS tot_zeroten, AVG(tot_tentwenty) AS tot_tentwenty, AVG(tot_tewntythirty) AS tot_tewntythirty, AVG(tot_thritymore) AS tot_thritymore "
            plugQueryBegin="WITH sub AS(SELECT fecha_retiro, "
            plugQueryMid2=" FROM ecobicidf GROUP BY(fecha_retiro)) SELECT EXTRACT(YEAR FROM fecha_retiro) AS ddate, "
            plugQueryEnd=" FROM sub GROUP BY EXTRACT(YEAR FROM fecha_retiro);"
        if varDisagg=="all":
            plugQueryMid3=" AVG(count) AS count "
        elif varDisagg=="gender":
            plugQueryMid3=" AVG(tot_fem) AS tot_fem, AVG(tot_masc) AS tot_masc "
        elif varDisagg=="age":
            plugQueryMid3=" AVG(tot_you) AS tot_you, AVG(tot_mid) AS tot_mid, AVG(tot_old) AS tot_old, AVG(tot_eld) AS tot_eld "
        elif varDisagg=="time":
            plugQueryMid3=" AVG(tot_beg) AS tot_beg, AVG(tot_mor) AS tot_mor, AVG(tot_aft) AS tot_aft, AVG(tot_eve) AS tot_eve "
        elif varDisagg=="length":
            plugQueryMid3=" AVG(tot_zeroten) AS tot_zeroten, AVG(tot_tentwenty) AS tot_tentwenty, AVG(tot_tewntythirty) AS tot_tewntythirty, AVG(tot_thritymore) AS tot_thritymore "

    if varDisagg=="all":
        plugQueryMid1=" COUNT(*) "
    elif varDisagg=="gender":
        plugQueryMid1=" SUM(CASE WHEN genero_usuario = 'F' THEN 1 ELSE 0 END) AS tot_fem, SUM(CASE WHEN genero_usuario = 'M' THEN 1 ELSE 0 END) AS tot_masc "
    elif varDisagg=="age":
        plugQueryMid1=" SUM(CASE WHEN edad_usuario BETWEEN 0 AND 25 THEN 1 ELSE 0 END) AS tot_you, SUM(CASE WHEN edad_usuario BETWEEN 26 AND 35 THEN 1 ELSE 0 END) AS tot_mid, SUM(CASE WHEN edad_usuario BETWEEN 36 AND 45 THEN 1 ELSE 0 END) AS tot_old, SUM(CASE WHEN edad_usuario>=46 THEN 1 ELSE 0 END) AS tot_eld "
    elif varDisagg=="time":
        plugQueryMid1=" SUM(CASE WHEN (hora_retiro>='00:00:00' AND hora_retiro<'06:00:00') THEN 1 ELSE 0 END) AS tot_beg, SUM(CASE WHEN (hora_retiro>='06:00:00' AND hora_retiro<'12:00:00') THEN 1 ELSE 0 END) AS tot_mor, SUM(CASE WHEN (hora_retiro>='12:00:00' AND hora_retiro<'18:00:00') THEN 1 ELSE 0 END) AS tot_aft, SUM(CASE WHEN (hora_retiro>='18:00:00') THEN 1 ELSE 0 END) AS tot_eve "
    elif varDisagg=="length":
        plugQueryMid1=" SUM(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:00:00' AND ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))<'00:10:00' THEN 1 ELSE 0 END) AS tot_zeroten, SUM(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:10:00' AND ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))<'00:20:00' THEN 1 ELSE 0 END) AS tot_tentwenty, SUM(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:20:00' AND ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))<'00:30:00' THEN 1 ELSE 0 END) AS tot_tewntythirty, SUM(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:30:00' THEN 1 ELSE 0 END) AS tot_thritymore "

    plugQuery=plugQueryBegin+plugQueryMid1+plugQueryMid2+plugQueryMid3+plugQueryEnd

    conn = psycopg2.connect(database="newecobici",user="postgres", password=passW, host ="localhost",port="5432")
    df = pd.read_sql_query(plugQuery,conn)
    conn.close()
    json = df.to_json(orient='records',date_format='iso')
    response = Response(response=json, status=200, mimetype="application/json")
    return(response)

@app.route("/api/dash3", methods=["POST"])
def dash3():
    miRequest = request.json
    varDisagg = str(miRequest["valueDisagg"])

    plugQueryBegin="SELECT ciclo_estacion_retiro AS station_begin, ciclo_estacion_arribo AS station_end, "
    plugQueryEnd="AVG((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro)) AS triptime FROM ecobicidf WHERE(ciclo_estacion_retiro<>ciclo_estacion_arribo) GROUP BY 1,2 ORDER BY tot DESC LIMIT 10;"
    if varDisagg=="all":
        plugQueryMid="COUNT(*) AS tot, "
    elif varDisagg=="genderfemale":
        plugQueryMid="SUM(CASE WHEN genero_usuario = 'F' THEN 1 ELSE 0 END) AS tot, "
    elif varDisagg=="gendermale":
        plugQueryMid="SUM(CASE WHEN genero_usuario = 'M' THEN 1 ELSE 0 END) AS tot, "
    elif varDisagg=="timebeg":
	    plugQueryMid="SUM(CASE WHEN (hora_retiro>='00:00:00' AND hora_retiro<'06:00:00') THEN 1 ELSE 0 END) AS tot, "
    elif varDisagg=="timemor":
	    plugQueryMid="SUM(CASE WHEN (hora_retiro>='06:00:00' AND hora_retiro<'12:00:00') THEN 1 ELSE 0 END) AS tot, "
    elif varDisagg=="timeaft":
	    plugQueryMid="SUM(CASE WHEN (hora_retiro>='12:00:00' AND hora_retiro<'18:00:00') THEN 1 ELSE 0 END) AS tot, "
    elif varDisagg=="timeeve":
	    plugQueryMid="SUM(CASE WHEN (hora_retiro>='18:00:00') THEN 1 ELSE 0 END) AS tot, "
    elif varDisagg=="length010":
	    plugQueryMid="SUM(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:00:00' AND ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))<'00:10:00' THEN 1 ELSE 0 END) AS tot, "
    elif varDisagg=="length1020":
	    plugQueryMid="SUM(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:10:00' AND ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))<'00:20:00' THEN 1 ELSE 0 END) AS tot, "
    elif varDisagg=="length2030":
	    plugQueryMid="SUM(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:20:00' AND ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))<'00:30:00' THEN 1 ELSE 0 END) AS tot, "
    elif varDisagg=="length30more":
	    plugQueryMid="SUM(CASE WHEN ((fecha_arribo+hora_arribo)-(fecha_retiro+hora_retiro))>='00:30:00' THEN 1 ELSE 0 END) AS tot, "
    elif varDisagg=="age025":
	    plugQueryMid="SUM(CASE WHEN edad_usuario BETWEEN 0 AND 25 THEN 1 ELSE 0 END) AS tot, "
    elif varDisagg=="age2635":
	    plugQueryMid="SUM(CASE WHEN edad_usuario BETWEEN 26 AND 35 THEN 1 ELSE 0 END) AS tot, "
    elif varDisagg=="age3645":
	    plugQueryMid="SUM(CASE WHEN edad_usuario BETWEEN 36 AND 45 THEN 1 ELSE 0 END) AS tot, "
    elif varDisagg=="age46more":
	    plugQueryMid="SUM(CASE WHEN edad_usuario>=46 THEN 1 ELSE 0 END) AS tot, "

    plugQuery=plugQueryBegin+plugQueryMid+plugQueryEnd

    conn = psycopg2.connect(database="newecobici",user="postgres", password=passW, host ="localhost",port="5432")
    df = pd.read_sql_query(plugQuery,conn)
    conn.close()
    json = df.to_json(orient='records',date_format='iso')
    response = Response(response=json, status=200, mimetype="application/json")
    return(response)
    
if __name__=="__main__":
    app.run()
