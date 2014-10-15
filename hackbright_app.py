import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row

def make_new_student(first_name, last_name, github):
    query = """INSERT INTO Students VALUES (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" % (first_name, last_name)

def get_project(project_title):
    query = """SELECT description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query, (project_title,))
    row = DB.fetchone()
    print "%s description: %s. It has a maximum grade of %d" %(project_title, row[0], row[1])

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
    return rows
#    for project in rows:
 #       print "On project %s, %s got %d" % (str(project[0]), last_name, project[1])

def return_all_student_grades(project_title):
    query = """SELECT student_github, grade FROM Grades WHERE project_title = ?"""
    DB.execute(query, (project_title,))
    rows = DB.fetchall()
    return rows

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
        command = tokens[0].strip()
        args = tokens[1:]
        newargs = []
        for arg in args:
            arg = arg.strip()
            newargs.append(arg)

        if command == "student":
            if len(newargs) != 1:
                print "Incorrect number of arguments. This command requires 1 argument: github."
            else:
                get_student_by_github(*newargs) 
        elif command == "new student":
            if len(newargs) != 3:
                print "Incorrect number of arguments. This command requires 3 arguments: first name, last name, github."
            else:
                make_new_student(*newargs)
        elif command == "project":
            if len(newargs) != 1:
                print "Incorrect number of arguments. This command requires 1 argument: Project title."
            else:
                get_project(*newargs)
        elif command == "new project":
            if len(newargs) != 3:
                print "Incorrect number of arguments. This command requires 3 arguments: Project Title, Description, and Maximum Grade."
            else:
                try:
                    max_grade = int(newargs[2])
                    if max_grade > 100:
                        print "Max grade must be less than or equal to 100."
                    else:
                        make_new_project(*newargs)
                except ValueError:
                    print "The max grade you entered is not an integer!"
            
        elif command == "student project grade":
            if len(newargs) != 2:
                print "Incorrect number of arguments. This command requires 2 arguments: Name, project_title."
            else:
                get_student_project_grade(*newargs)
        elif command == "give grade":
            if len(newargs) != 3:
                print "Incorrect number of arguments. This command requires 3 arguments: last name, project title, grade."
            else:
                try:
                    max_grade = int(newargs[2])
                    if max_grade > 100:
                        print "Student grade must be less than or equal to 100."
                    else:
                        give_student_grade(*newargs)
                except ValueError:
                    print "The grade you entered is not an integer!"
        elif command == "student grades":
            if len(newargs) != 1:
                print "Incorrect number of arguments. This command requires 1 argument: last name."
            else:
                return_student_grades(*newargs)

        elif command == "all grades on a project":
            if len(newargs) != 1:
                print "Incorrect number of arguments. This command requires 1 argument: Project title."
            else:
                return_all_student_grades(*newargs)
 

    CONN.close()

if __name__ == "__main__":
    main()
