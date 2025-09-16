from flask import Flask, render_template, request, redirect
import csv

app = Flask(__name__)
FILENAME = "students.csv"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_student():
    roll = request.form["roll"]
    name = request.form["name"]
    marks = [int(request.form["sub1"]), int(request.form["sub2"]), int(request.form["sub3"])]

    total = sum(marks)
    percentage = total / 3
    grade = "A" if percentage >= 75 else "B" if percentage >= 60 else "C" if percentage >= 40 else "F"

    with open(FILENAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([roll, name] + marks + [total, percentage, grade])

    return redirect("/results")

@app.route("/results")
def results():
    students = []
    try:
        with open(FILENAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                students.append(row)
    except FileNotFoundError:
        pass
    return render_template("results.html", students=students)

@app.route("/search", methods=["GET", "POST"])
def search():
    student = None
    if request.method == "POST":
        roll = request.form["roll"]
        try:
            with open(FILENAME, "r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[0] == roll:  # roll number matches
                        student = row
                        break
        except FileNotFoundError:
            pass
    return render_template("search.html", student=student)
import pandas as pd
from flask import send_file

@app.route("/export")
def export():
    try:
        df = pd.read_csv(FILENAME)
        output_file = "exported_results.xlsx"
        df.to_excel(output_file, index=False)
        return send_file(output_file, as_attachment=True)
    except FileNotFoundError:
        return "No data available to export!"



if __name__ == "__main__":
    app.run(debug=True)
