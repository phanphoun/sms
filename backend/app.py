from flask import Flask, request, jsonify

app = Flask(__name__)

students = [
    {"id": 1, "name": "John", "age": 22},
    {"id": 2, "name": "Jane", "age": 21},
    {"id": 3, "name": "Jack", "age": 23},
]

@app.route("/students", methods = ["GET"])

def get_students():
    return jsonify(students)


if __name__ == "__main__":
    app.run(debug=True, port = 8000)