from flask import Flask , request , url_for
from sqlalchemy.sql.expression import table
app = Flask(__name__)
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean
import re
engine = create_engine('sqlite:///Student.db', echo = True)
meta = MetaData()

students = Table(
  'students', meta, 
  Column('USN', String(10), primary_key = True), 
  Column('student_name', String(50)), 
  Column('gender', String(1)),
  Column('entry_type', String(10)),
  Column('YOA', Integer),
  Column('migrated', String(1)),
  Column('Details_of_transfer', String(100)),
  Column('admission_in_separate_division', String(1)),
  Column('Details_of_admission_in_seperate_division', String(100)),
  Column('YOP', Integer),
  Column('degree_type', String(2)),
  Column('pu_marks', Integer),
  Column('entrance_marks', Integer)
)
meta.create_all(engine)
conn = engine.connect()

def create(body):
  conn = engine.connect()
  #N=int(input("Enter the number of student's details to be entered: "))
  N=int(body['N'])
  for i in range(N):
    #USN=str(input("Enter the USN of the student: "))
    USN=str(body['USN'])
    #student_name=str(input("Enter the name of the student: "))
    student_name=str(body['student_name'])
    #gender=str(input("Enter the gender of the student: " ))
    gender=str(body['gender'])
    if not re.match("^[m,f]*$", gender):
      #print("Error! Only letters m and f allowed!")
      return "Error! Only letters m and f allowed!"
      exit()
    entry_type=str(body['entry_type'])
    #entry_type=str(input("Enter the entry type (normal/lateral) of the student: "))
    YOA=int(body['YOA'])
    #YOA=int(input("Enter the year of admission of the student: "))
    #migrated=(input("Has the student migrated to other programs / Institutions - Yes / No: "))
    migrated=str(body['migrated'])
    if migrated=="yes":
      migrated== 1
      #Details_of_transfer= str(input("Enter the details of transfer of the student: "))
      Details_of_transfer=str(body['Details_of_transfer'])
    elif migrated=="no":
      migrated== 0
      Details_of_transfer= None
    #admission_in_separate_division=(input("Does the student have admission in a seperate division - Yes (With details) / No: "))
    admission_in_separate_division=str(body['admission_in_separate_division'])
    if admission_in_separate_division=="yes":
      admission_in_separate_division==True
      Details_of_admission_in_seperate_division=str(body['Details_of_admission_in_seperate_division'])
      #Details_of_admission_in_seperate_division= str(input("Enter the details of admission in seperate division of the student: "))
    else:
      admission_in_separate_division==False
      Details_of_admission_in_seperate_division= None
    #YOP=int(input("Year of Passing: "))
    YOP=int(body['YOP'])
    #degree_type=str(input("Student enrolled for UG / PG?: "))
    degree_type=str(body['degree_type'])
    #pu_marks=int(input("12th marks in PCM subjects: "))
    pu_marks=int(body['pu_marks'])
    #entrance_marks=int(input("Entrance Exam ranks/marks: "))
    entrance_marks=int(body['entrance_marks'])
    ins = students.insert().values(USN= USN, student_name = student_name, gender = gender, entry_type= entry_type, YOA= YOA, migrated= migrated, Details_of_transfer= Details_of_transfer, admission_in_separate_division= admission_in_separate_division, Details_of_admission_in_seperate_division= Details_of_admission_in_seperate_division, YOP= YOP, degree_type= degree_type, pu_marks= pu_marks, entrance_marks= entrance_marks)
  result = conn.execute(ins)
  s = students.select()
  result = conn.execute(s)
  for table in result:
      return table

def read(body):
  conn = engine.connect()
  s = students.select()
  result = conn.execute(s)
  for table in result:
    return table

def update(body):
  conn = engine.connect()
  #id=int(input("Enter the USN of the student: "))
  USN=str(body['USN'])
  #new=str(input("Enter the new name of the student: "))
  new_name=str(body['new_name'])
  stmt=students.update().where(students.c.USN==USN).values(student_name=new_name)
  conn.execute(stmt)
  s = students.select()
  conn.execute(s).fetchall()
  s = students.select()
  result = conn.execute(s)
  for table in result:
    return table
        
def delete(body):
  conn = engine.connect()
  #x=input("Enter the USN of the student whose record has to deleted: ")
  USN=int(body['USN'])
  stmt = students.delete().where(students.c.USN == USN)
  conn.execute(stmt)
  s = students.select()
  conn.execute(s).fetchall()
  s = students.select()
  result = conn.execute(s)
  for table in result:
    return table

@app.route('/')
def home():
  return "N/O"

@app.route('/view' , methods=['GET'])
def view():
  body = request.get_json()
  a = read(body)
  return a
   
@app.route('/enter' , methods=['POST'])
def enter():
  body = request.get_json()
  a = create(body)
  return str(a)

@app.route('/update' , methods=['PUT'])
def fix():
  body = request.get_json()
  a = update(body)
  return str(a)

@app.route('/delete' , methods=['DELETE'])
def deletee():
  body = request.get_json()
  a = delete(body)
  return str(a)

if __name__ == '__main__' :
  app.run(debug=True, port=5000)