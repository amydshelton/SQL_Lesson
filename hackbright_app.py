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

#def get_student_project_grade():
#    query = """SELECT 


def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
       # print tokens
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
           # print "ehy!"
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project":
            get_project()
        elif command == "new_project":
            make_new_project(*args)
 #       elif command == "student_project_grade":
 #           get_student_project_grade(*args)
 #working on queryiing for a student's grade given a projects

    CONN.close()

if __name__ == "__main__":
    main()
