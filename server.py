from flask import stream_with_context, Flask, Response, jsonify
from psycopg2.extensions import AsIs
import os
import json
import psycopg2
import time
from psycopg2.extras import RealDictCursor

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

@app.route("/runs/<name>", methods = ["PUT"])
def create(name):
    con = psycopg2.connect(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port="5432")

    cursor = con.cursor()
    cursor.execute("INSERT INTO runs (name, start_at) VALUES(%s, %s) RETURNING id", (name,int(time.time())))
    con.commit()
    id = cursor.fetchone()[0]

    return jsonify(id=id)

@app.route("/runs/<id>/complete", methods = ["PUT"])
def complete(id):
    con = psycopg2.connect(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port="5432")

    cursor = con.cursor()
    cursor.execute("UPDATE runs set end_at = %s, status = 1 where id = %s", (int(time.time()),id,))
    con.commit()

    return id

@app.route("/runs/status/<status>")
def runs(status):
    con = psycopg2.connect(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port="5432")

    def streamer():
        seen = {'0':1}
        cursor = con.cursor(cursor_factory=RealDictCursor)
        while True:
            ids = ','.join(list(seen.keys()))
            cursor.execute("SELECT id, name, start_at, end_at, status from runs where status = %s and id not in (%s)", (int(status), AsIs(ids),))
            for row in cursor.fetchall():
                seen[str(row['id'])] = 1
                print(row)
                yield json.dumps(row) + "\n"

            #t=time.time()
            #yield json.dumps(jsonify(heartbeat=t)) + "\n"
            time.sleep(1)

    response = Response(stream_with_context(streamer()))
    return response


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(debug=True,host='0.0.0.0',port=port)
