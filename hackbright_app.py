import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """Student: %s %s  Github account: %s"""%(row[0], row[1], row[2])

def make_new_student(first_name, last_name, github):
    query = """INSERT INTO Students VALUES (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def get_project():
    query = """SELECT title, max_grade FROM Projects"""
    DB.execute(query)
    rows = DB.fetchall()
    print rows

def make_new_project(project_title, description, max_grade):
    query = """INSERT INTO Projects(title, description, max_grade) VALUES (?,?,?)"""
    DB.execute(query, (project_title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s" % project_title

def get_student_project_grade(last_name, project_title):
    query = """SELECT grade FROM Grades JOIN Students ON (Grades.student_github = Students.github) WHERE last_name = ? AND project_title = ?"""
    DB.execute(query, (last_name, project_title))
    row = DB.fetchone()
    print """Student: %s got %d on %s.""" % (last_name, row[0], project_title) 

def give_student_grade(last_name, project_title, grade):
    query = """SELECT github FROM Students WHERE last_name = (?)"""
    DB.execute(query, (last_name,))
    github = DB.fetchone()[0]
    query = """INSERT INTO Grades(student_github, project_title, grade) VALUES (?,?,?)"""
    DB.execute(query, (github, project_title, grade))
    CONN.commit()
    print "Successfully added grade: %s." % grade

def return_student_grades(last_name):
    query = """SELECT github FROM Students WHERE last_name = (?)"""
    DB.execute(query, (last_name,))
    github = DB.fetchone()[0]
    query = """SELECT project_title, grade FROM Grades WHERE student_github = ?"""
    DB.execute(query, (github,))
    rows = DB.fetchall()
    for project in rows:
        print "On project %s, %s got %d" % (str(project[0]), last_name, project[1])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(',')
       # print tokens
        command = tokens[0].strip()
        args = tokens[1:]
        newargs = []
        for arg in args:
            arg = arg.strip()
            newargs.append(arg)

        if command == "student":
            get_student_by_github(*newargs) 
        elif command == "new student":
            make_new_student(*newargs)
        elif command == "project":
            get_project()
        elif command == "new project":
            make_new_project(*newargs)
        elif command == "student project grade":
            get_student_project_grade(*newargs)
        elif command == "give grade":
            give_student_grade(*newargs)
        elif command == "student grades":
            return_student_grades(*newargs)
 

    CONN.close()

if __name__ == "__main__":
    main()
