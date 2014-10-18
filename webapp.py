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
    name_and_grades_raw = hackbright_app.return_student_grades(last_name)   # [ ("proja", "A"), ("projb", "C")]
    name_and_grades = [ {'project_name': x[0], 'grade': x[1]} for x in name_and_grades_raw ]   # [ {'project_name':"proja', 'grade':'A"}]

 #   for grade in grades:

    html =  render_template("student_info.html", first_name = row[0],
                                                last_name = row[1],
                                                github = row[2], name_and_grades = name_and_grades)
    return html

@app.route("/projects")
def get_project_grades():
   hackbright_app.connect_to_db()
   project_title = request.args.get("project")
   names_and_grades = hackbright_app.return_all_student_grades(project_title)
   # student_github = row[0]
   html = render_template("return_grades_on_a_project.html", project_title = project_title, names_and_grades = names_and_grades)
   return html

@app.route("/newstudent")
def new_student():
  return render_template("create_student.html") 

@app.route("/newproject")
def new_project():
  hackbright_app.connect_to_db()
  new_student_first_name = request.args.get("new_student_first_name")
  new_student_last_name = request.args.get("new_student_last_name")
  new_student_github = request.args.get("new_student_github")
  hackbright_app.make_new_student(new_student_first_name, new_student_last_name, new_student_github)
  return render_template("new_project.html", new_student_first_name = new_student_first_name, new_student_last_name= new_student_last_name) 

def put_student_grade_in_db():
  hackbright_app.connect_to_db()
  project_name = request.args.get("project_name")
  project_grade = request.args.get("project_grade")
  hackbright_app.give_student_grade(last_name, project_name, project_grade)


def give_student_grade(last_name, project_title, grade):
    query = """SELECT github FROM Students WHERE last_name = (?)"""
    DB.execute(query, (last_name,))
    github = DB.fetchone()[0]
    query = """INSERT INTO Grades(student_github, project_title, grade) VALUES (?,?,?)"""
    DB.execute(query, (github, project_title, grade))
    CONN.commit()
    print "Successfully added grade: %s." % grade

# @app.route('/color')
# def favorite_color():
#   fav_color = request.args.get('color')  # d.get('color') => None if 'color' is not a key
#   if fav_color is None:
#     return render_template("color-form.html")    # <form action="/color">...</form>
#   else:
#     return "I love %s, too" % fav_color


#what anna would do:
#create two handlers - one that creates a new student, and one to input the grades
#for that student.
#create an html file also, that would allow you to enter info (a form)
#info would be created by both handlers.

if __name__ == "__main__":
    app.run(debug=True)