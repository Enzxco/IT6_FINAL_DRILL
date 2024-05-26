from flask import Flask, make_response, jsonify, request
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
def get_mydb():
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
    WHERE budget.idBUDGET = {};
    """.format(
            id
        )
    )
    return make_response(
        jsonify({"idBUDGET": id, "count": len(data), "details": data}), 200
    )


@app.route("/mydb", methods=["POST"])
def add_mydb():
    cur = mysql.connection.cursor()
    info = request.get_json()
    idBUDGET = info["idBUDGET"]
    annual_allocated = info["annual_allocated"]
    cur.execute(
        """ INSERT INTO budget (idBUDGET, annual_allocated) VALUE (%s, %s)""",
        (idBUDGET, annual_allocated),
    )
    mysql.connection.commit()
    print("row(s) affected :{}".format(cur.rowcount))
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify({"message": "mydb added successfully", "rows_affected": rows_affected}),
        201,
    )


@app.route("/mydb/<int:id>", methods=["PUT"])
def update_mydb(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    name = info["name"]
    job_title = info["job_title"]
    contact_details = info["contact_details"]
    cur.execute(
        """ UPDATE staff SET name = %s, job_title = %s, contact_details = %s WHERE idSTAFFS = %s """,
        (name, job_title, contact_details, id),
    )
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "mydb updated successfully", "rows_affected": rows_affected}
        ),
        200,
    )


if __name__ == "__main__":
    app.run(debug=True)
