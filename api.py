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


@app.route("/budget", methods=["GET"])
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


@app.route("/staff/<int:id>/details", methods=["GET"])
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


@app.route("/budget", methods=["POST"])
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


@app.route("/budget/<int:id>", methods=["PUT"])
def update_mydb(id):
    cur = mysql.connection.cursor()
    info = request.get_json()
    idBUDGET = info["idBUDGET"]
    annual_allocated = info["annual_allocated"]
    cur.execute(
        """ UPDATE budget SET annual_allocated = %s WHERE idBUDGET = %s """,
        (annual_allocated, idBUDGET),
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


@app.route("/budget/<int:id>", methods=["DELETE"])
def delete_mydb(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM budget where idBUDGET = %s """, (id,))
    mysql.connection.commit()
    rows_affected = cur.rowcount
    cur.close()
    return make_response(
        jsonify(
            {"message": "mydb deleted successfully", "rows_affected": rows_affected}
        ),
        200,
    )

@app.route("/mydb/format", methods=["GET"])
def get_params():
    fmt = request.args.get('id')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format":fmt, "foo":foo}),200)


if __name__ == "__main__":
    app.run(debug=True)
