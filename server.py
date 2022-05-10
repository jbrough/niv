from flask import Flask
from flask import jsonify

import os
import psycopg2

app = Flask(__name__)

@app.route("/healthz")
def healthz():
    try:
        con = psycopg2.connect(
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port="5432")
    except:
        db = "red"
    else:
        db = "green"

    return jsonify(db=db)

@app.route("/jobs/<name>", methods = ["PUT"])
def create_job(name):
    con = psycopg2.connect(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port="5432")

    cursor = con.cursor()
    cursor.execute("INSERT INTO jobs (name) VALUES(%s) RETURNING id", (name,))
    con.commit()
    id = cursor.fetchone()[0]

    return jsonify(id=id)

@app.route("/jobs/<id>", methods = ["GET"])
def get_job(id):
    con = psycopg2.connect(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port="5432")

    cursor = con.cursor()
    cursor.execute("SELECT status from jobs where id = %s", (id,))
    con.commit()
    status = cursor.fetchone()[0]

    return jsonify(status=status)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(debug=True,host='0.0.0.0',port=port)
