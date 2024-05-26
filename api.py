from flask import Flask, make_response, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Required
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "rootadmin"
app.config["MYSQL_DB"] = "mydb"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data

@app.route("/mydb", methods=["GET"])
def get_actors():
    query = """
    select * from budget
    """
    data = data_fetch("""select * from budget""")
    return make_response(jsonify(data), 200)

@app.route("/mydb/<int:id>", methods=["GET"])
def get_mydb_by_id(id):
    data = data_fetch("""select * from budget where idBUDGET = {}""".format(id))
    return make_response(jsonify(data), 200)

@app.route("/mydb/<int:id>/details", methods=["GET"])
def get_details_by_mydb(id):
    data = data_fetch(
        """
    SELECT staff.name, staff.contact_details, staff.job_title, annual_allocated
    FROM budget
    INNER JOIN staff 
    ON budget.idBUDGET = staff.idSTAFFS
    INNER JOIN student
    ON staff.idSTAFFS = student.idSTUDENTS
    WHERE budget.idBUDGET IN (10, 11, 12, 13, 14, 15);
    """.format(id))
    return make_response(
        jsonify({"idBUDGET": id, "count": len(data), "details": data}), 200)


if __name__ == "__main__":
    app.run(debug=True)
