# ACCOUNT INFORMATION SYSTEM WITH FLASK API 

This is a Flask application that integrates with a MySQL database to manage budget and staff information. The application provides RESTful API endpoints for CRUD operations and supports JSON and XML response formats.


# SETUP
1. Clone the repository
```
git clone <repository-url>
cd <repository-directory>
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Configure MySQL
Make sure you have MySQL installed and running. Update the MySQL configuration in the Flask app as needed:
```
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "rootadmin"
app.config["MYSQL_DB"] = "mydb"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
```

4. Run the Flask <.py> in terminal
```
python app.py
```

# API Endpoints (Using Postman)
1. Protected Route*
* GET /protected
* Requires authentication
* Example Response: {"message": "You are authorized to access this resource."}

2. Hello World
* GET /budget
* Requires authentication
* Retrieves all budget records
* Example Response:
```
[
  {
    "idBUDGET": 1,
    "annual_allocated": 50000
  },
...
]
```

3. Get Budget by ID
* GET /mydb/<int:id>
* Requires authentication
* Retrieves budget record by ID
* Example Response:
```
{
  "idBUDGET": 1,
  "annual_allocated": 50000
}
```

4. Get Staff Details by Budget ID
* GET /staff/<int:id>/details
* Requires authentication
* Retrieves staff details for a specific budget ID
* Example Response:
```
{
  "idBUDGET": 1,
  "count": 2,
  "details": [
    {
      "name": "John Doe",
      "contact_details": "555-1234",
      "job_title": "Manager",
      "annual_allocated": 50000
    },
    ...
  ]
}
```

5. Add Budget
* POST /budget
* Requires authentication
* Adds a new budget record
* Request Body:
```
{
  "idBUDGET": 21,
  "annual_allocated": 95000
}

```
Example reponse: (applied to all)
```
{
  "message": "mydb added successfully",
  "rows_affected": 1
}

```

6. Update Budget
* PUT /budget/<int:id>
* Requires authentication
* Updates a budget record
* Request Body:
```
{
  "idBUDGET": 1,
  "annual_allocated": 55000
}
```

7. Delete Budget (no need a body)
* DELETE /budget/<int:id>
* Requires authentication
* Deletes a budget record
```
{
  "message": "mydb deleted successfully",
  "rows_affected": 1
}

```

8. Get Params
* GET /mydb/formatRequires authentication
* Retrieves query parameters
* Example Response:
```
{
  "format": "json",
  "foo": "bar"
}
```

# Authentication
This application uses HTTP Basic Authentication. The default credentials are:
* Username: enzo
* Password: 0512

# Helper Function
* convert_to_xml: Converts data to XML format.
* format_response: Formats the response based on the requested format (JSON or XML).
* The application will start and be available at http://127.0.0.1:5000.

# Notes
* Ensure the MySQL database and tables (budget, staff, student) are properly set up before running the application.
* Use a tool like Postman to test the API endpoints with the appropriate HTTP methods and authentication headers.
