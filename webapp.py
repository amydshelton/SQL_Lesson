from flask import Flask, render_template, request

import hackbright_app

app = Flask(__name__)

@app.route("/")
def get_github():
    return render_template("get_github.html")


@app.route("/student")
def get_student():

    hackbright_app.connect_to_db()
    student_github = request.args.get("poop")
    row = hackbright_app.get_student_by_github(student_github)
    last_name = row[1]
    grades = hackbright_app.return_student_grades(last_name)
 #   for grade in grades:

    html =  render_template("student_info.html", first_name = row[0],
                                                last_name = row[1],
                                                github = row[2], grades = grades)
    return html

@app.route("/projects")
def get_project_grades():
   hackbright_app.connect_to_db()
   project_title = request.args.get("project")
   names_and_grades = hackbright_app.return_all_student_grades(project_title)
   # student_github = row[0]
   html = render_template("return_grades_on_a_project.html", project_title = project_title, names_and_grades = names_and_grades)
   return html

#what anna would do:
#create two handlers - one that creates a new student, and one to input the grades
#for that student.
#create an html file also, that would allow you to enter info (a form)
#info would be created by both handlers.

if __name__ == "__main__":
    app.run(debug=True)