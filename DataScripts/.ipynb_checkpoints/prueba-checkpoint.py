import psycopg2
import pandas as pd
from postgreSQLpassword import passW
import numpy as np
from flask import Flask, jsonify

conn = psycopg2.connect(database="ecobici", user="postgres", password=passW, host="localhost", port="5432")
print("Database Connected....")
cursor=conn.cursor()
cursor.execute("SELECT AVG(hora_arribo-hora_retiro) FROM ecobicidf GROUP BY (EXTRACT(MONTH FROM fecha_retiro));")
tabla=pd.DataFrame(cursor.fetchall())
cursos.close()

# Flask
app=Flask(__name__)

@app.route("/")
def welcome():
    all_names=list(np.ravel(tabla))
    return jsonify(all_names)

if __name__=="__main__":
    app.run(debug=True)