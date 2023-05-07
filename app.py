from datetime import timedelta
import os
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.engine import Engine
from sqlalchemy import event

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY']='004f2af45d3a4e161a7dd2d17fdae47f'
app.config['JWT_SECRET_KEY']='004f2af45d3a4e161a7dd2d17fdae47f'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'kanban.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
 
db = SQLAlchemy(app, session_options={'autocommit': True})
jwt = JWTManager(app)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data['email']
    test = db.session.execute("select email from EMPLOYEE_EMAIL where email=:email", {'email':email})
    check_email = [i for i in test]
    if len(check_email):
        return jsonify(message='That email already exists'), 409
    else:
        emp_id = str(uuid.uuid4())
        fname = data['fname']
        lname = data['lname']
        birth_date = data['birth_date']
        gender = data['gender']
        password = generate_password_hash(data['password'])
        db.session.execute('insert into EMPLOYEE values(:emp_id, :fname, :lname, :birth_date, :gender);', 
        {
            'emp_id': emp_id,
            'fname': fname,
            'lname': lname,
            'birth_date': birth_date,
            'gender': gender
        })
        db.session.execute('insert into EMPLOYEE_EMAIL values(:emp_id, :email);',
        {
            'emp_id': emp_id,
            'email': email,
        })
        db.session.execute('insert into EMPLOYEE_PASSWORD values(:emp_id, :password);',
                           {
            'emp_id': emp_id,
            'password': password,
        })
        return jsonify(message='User created successfully'), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    test = db.session.execute("select password from EMPLOYEE_EMAIL natural join EMPLOYEE_PASSWORD where email=:email", {'email':email})
    check_pass = [i for i in test]
    if(len(check_pass)):
        check_pass = check_pass[0][0]
        if check_password_hash(check_pass, password):
            access_token = create_access_token(identity=email)
            return jsonify(message='Login Successful', access_token=access_token)
        else:
            return jsonify('Bad email or Password'), 401
    else:
        return jsonify('Bad email or Password'), 401

@app.route('/get_profile', methods=['GET'])
@jwt_required()
def get_profile():
    email = get_jwt_identity()
    result = db.session.execute("select * from EMPLOYEE natural join EMPLOYEE_EMAIL where email=:email", {'email':email})
    res_data = [i for i in result][0]
    fname = res_data[1]
    lname = res_data[2]
    birth_date = res_data[3]
    gender = res_data[4]
    print(res_data)
    response = {
        'fname': fname,
        'lname': lname,
        'birth_date': birth_date,
        'gender': gender,
        'email': email,
    }
    return jsonify(response)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    data = request.get_json()
    email = data['email']
    fname = data['fname']
    lname = data['lname']
    birth_date = data['birth_date']
    gender = data['gender']
    password = generate_password_hash(data['password'])
    result = db.session.execute("select emp_id from EMPLOYEE_EMAIL where email=:email", {'email':email})
    res_data = [i for i in result][0]
    emp_id = res_data[0]
    print(emp_id)
    db.session.execute('update EMPLOYEE set fname=:fname, lname=:lname, birth_date=:birth_date, gender=:gender where emp_id=:emp_id;', 
    {
        'emp_id': emp_id,
        'fname': fname,
        'lname': lname,
        'birth_date': birth_date,
        'gender': gender
    })
    db.session.execute('update EMPLOYEE_PASSWORD set password=:password where emp_id=:emp_id;', 
    {
        'emp_id': emp_id,
        'password': password
    })
    return jsonify(message='User updated successfully'), 201

@app.route('/search', methods=['GET'])
@jwt_required()
def search():
    result = db.session.execute("select * from EMPLOYEE natural join EMPLOYEE_EMAIL")
    response = []
    for each in result:
        res_data = list(each)
        emp_id = res_data[0]
        fname = res_data[1]
        lname = res_data[2]
        birth_date = res_data[3]
        gender = res_data[4]
        email = res_data[5]
        data = {
            'emp_id': emp_id,
            'fname': fname,
            'lname': lname,
            'birth_date': birth_date,
            'gender': gender,
            'email': email,
            'found': True
        }
        response.append(data)
    return jsonify(response)


@app.route("/projects", methods=["GET"])
@jwt_required()
def projects():
    result = db.session.execute("select * from PROJECTS")
    response = []
    for each in result:
        res_data = list(each)
        data = {
            "project_id": res_data[0],
            "name": res_data[1],
            "start_date": res_data[2],
            "end_date": res_data[3],
        }
        response.append(data)
    return jsonify(response)

@app.route("/add_project", methods=["POST"])
@jwt_required()
def add_project():
    data = request.get_json()
    name = data['name']
    test = db.session.execute("select name from PROJECTS where name=:name", {'name':name})
    check_name = [i for i in test]
    if len(check_name):
        return jsonify(message='That project already exists'), 409
    else:
        project_id = str(uuid.uuid4())
        name = data['name']
        start_date = data['start_date']
        end_date = data['end_date']
        db.session.execute('insert into PROJECTS values(:project_id, :name, :start_date, :end_date);', 
        {
            'project_id': project_id,
            'name': name,
            'start_date': start_date,
            'end_date': end_date
        })
        return jsonify(message='Project created successfully'), 201

@app.route("/delete_project", methods=["POST"])
@jwt_required()
def delete_project():
    data = request.get_json()
    project_id = data['project_id']
    test = db.session.execute("select project_id from HAS where project_id=:project_id", {'project_id':project_id})
    check_name = [i for i in test]
    if len(check_name):
        return jsonify(message='That project has tasks associated with it. Reassign those tasks and then delete this project.'), 409
    else:
        db.session.execute("delete from PROJECTS where project_id=:project_id", {'project_id':project_id})
        return jsonify(message='Project deleted successfully'), 200

@app.route("/statuses", methods=["GET"])
@jwt_required()
def statuses():
    result = db.session.execute("select * from STATUS")
    response = []
    for each in result:
        res_data = list(each)
        data = {
            "status_id": res_data[0],
            "name": res_data[1]
        }
        response.append(data)
    return jsonify(response)

@app.route("/add_status", methods=["POST"])
@jwt_required()
def add_status():
    data = request.get_json()
    name = data['name']
    test = db.session.execute("select status_type from STATUS where status_type=:name", {'name':name})
    check_name = [i for i in test]
    if len(check_name):
        return jsonify(message='That status already exists'), 409
    else:
        status_id = str(uuid.uuid4())
        name = data['name']
        db.session.execute('insert into STATUS values(:status_id, :name);', 
        {
            'status_id': status_id,
            'name': name
        })
        return jsonify(message='Status added successfully'), 201

@app.route("/delete_status", methods=["POST"])
@jwt_required()
def delete_status():
    data = request.get_json()
    status_id = data['status_id']
    test = db.session.execute("select status_id from IS_UNDER where status_id=:status_id", {'status_id':status_id})
    check_name = [i for i in test]
    if len(check_name):
        return jsonify(message='That status has tasks associated with it. Reassign those tasks and then delete this status.'), 409
    else:
        db.session.execute("delete from STATUS where status_id=:status_id", {'status_id':status_id})
        return jsonify(message='Status deleted successfully'), 200

@app.route("/tasks", methods=["GET"])
@jwt_required()
def tasks():
    project_id = request.args['project_id']
    result = db.session.execute("select * from HAS as h natural join TASK as t natural join IS_UNDER as i natural join STATUS as s natural join WORKS_ON natural join EMPLOYEE where project_id=:project_id", {'project_id':project_id})
    status_list = db.session.execute("select * from STATUS")
    
    response = {}
    response['status'] = {}
    response['tasks'] = {}
    for each in status_list:
        res_data = list(each)
        print(res_data)
        response['tasks'][res_data[0]] = []
        response['status'][res_data[0]] = res_data[1]
    for each in result:
        res_data = list(each)
        response['status'][res_data[5]] = res_data[6]
        response['tasks'][res_data[5]].append({
            "task_id": res_data[1],
            "name": res_data[2],
            'start_date': res_data[3],
            'end_date': res_data[4],
            'employee': res_data[8] + " " + res_data[9]
            })
    return jsonify(response)

@app.route("/add_task", methods=["POST"])
@jwt_required()
def add_task():
    data = request.get_json()
    name = data['name']
    project_id = data['project']
    test = db.session.execute("select name from TASK natural join HAS where name=:name and project_id=:project_id", {'name':name, 'project_id': project_id})
    check_name = [i for i in test]
    if len(check_name):
        return jsonify(message='That task already exists in this project'), 409
    else:
        task_id = str(uuid.uuid4())
        status_id = data['status']
        project_id = data['project']
        employee_email = get_jwt_identity()
        employee_id_res = db.session.execute("select emp_id from EMPLOYEE_EMAIL where email=:email", {'email':employee_email})
        emp_id = [i for i in employee_id_res][0][0]
        start_date = data['start_date']
        end_date = data['end_date']
        db.session.execute('insert into TASK values(:task_id, :name, :start_date, :end_date);', 
        {
            'task_id': task_id,
            'name': name,
            'start_date': start_date,
            'end_date': end_date
        })
        db.session.execute('insert into HAS values(:project_id, :task_id);', 
        {
            'project_id': project_id,
            'task_id': task_id
        })
        db.session.execute('insert into IS_UNDER values(:task_id, :status_id);', 
        {
            'task_id': task_id,
            'status_id': status_id,
        })
        try:
            db.session.execute('insert into PART_OF values(:emp_id, :project_id);', 
            {
                'emp_id': emp_id,
                'project_id': project_id,
            })
        except Exception as e:
            print(e)
        db.session.execute('insert into WORKS_ON values(:emp_id, :task_id);', 
        {
            'emp_id':emp_id,
            'task_id': task_id
        })
        
        return jsonify(message='Task added successfully'), 201

@app.route("/save_tasks", methods=["POST"])
@jwt_required()
def save_tasks():
    data = request.get_json()
    updated_list = [(list, i['task_id']) for list in data.keys() for i in data[list]]
    for i in updated_list:
        db.session.execute("update IS_UNDER set status_id=:status_id where task_id=:task_id", {'status_id':i[0], 'task_id':i[1]})
    return jsonify(message='Received'), 200

@app.route("/delete_task", methods=["POST"])
@jwt_required()
def delete_task():
    data = request.get_json()
    employee_email = get_jwt_identity()
    employee_id_res = db.session.execute("select emp_id from EMPLOYEE_EMAIL where email=:email", {'email':employee_email})
    emp_id = [i for i in employee_id_res][0][0]
    task_id = data['task_id']
    project_id = data['project_id']
    test = db.session.execute("select * from HAS natural join WORKS_ON where emp_id=:emp_id and project_id=:project_id;", {'emp_id':emp_id, 'project_id': project_id})
    check_name = [i for i in test]
    if len(check_name) == 1:
        db.session.execute("delete from PART_OF where emp_id=:emp_id and project_id=:project_id;", {'emp_id':emp_id, 'project_id': project_id})
    try:
        db.session.execute("delete from TASK where task_id=:task_id", {'task_id':task_id})
        return jsonify(message='Task deleted successfully'), 200
    except:
        return jsonify(message='Unable to delete task'), 409

@app.route("/chat_messages", methods=["GET"])
@jwt_required()
def chat_messages():
    project_id = request.args['project_id']
    result = db.session.execute("select * from CHAT where project_id=:project_id", {'project_id':project_id})
    response = []
    for each in result:
        res_data = list(each)
        data = {
            "chat_id": res_data[0],
            "email": res_data[1],
            "date_time": res_data[2],
            "text": res_data[3],
            "project_id": res_data[4]
        }
        response.append(data)
    return jsonify(response)

@app.route("/add_chatmessage", methods=["POST"])
@jwt_required()
def add_chatmessage():
    data = request.get_json()
    email = get_jwt_identity()
    chat_id = str(uuid.uuid4())
    date_time = data['date_time']
    text = data['text']
    project_id = data['project_id']
    db.session.execute('insert into CHAT values(:chat_id, :email, :date_time, :text, :project_id);', 
    {
        "chat_id": chat_id,
        "email": email,
        "date_time": date_time,
        "text": text,
        "project_id": project_id
    })
    return jsonify(message='Chat message added successfully'), 201

if __name__ == '__main__':
    app.run(debug=True)
