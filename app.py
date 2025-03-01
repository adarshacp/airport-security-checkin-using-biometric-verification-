<<<<<<< HEAD
#importing libraries
from flask import Flask,request,session,render_template,jsonify,redirect,url_for
import csv
import os
import time
import cv2

app = Flask(__name__)

app.secret_key = "my_secret_key"  #Required for session storage

user_csv_file = "userdata.csv"
secu_csv_file = "securitydata.csv"

def csv_exists(file_path,headers):
    if not os.path.exists(file_path):
        with open(file_path,mode="w",newline="",encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)

csv_exists = (secu_csv_file,["Name","Age","Shift-Rotation","UserName","Password"])
csv_exists = (user_csv_file,["Name", "Aadhar ID", "DOB", "Source", "Destination", "Reservation ID"])

def write_to_csv(secu_file,data):
    with open(secu_file,mode="a",newline="",encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(data)

def read_from_csv(file_path):
    with open(file_path,mode="r",encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)
    
@app.route('/admin',methods=["POST","GET"])
def admin():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        shift_rotation = request.form["shift-rotation"]
        username = request.form["username"]
        password = request.form["password"]

        if name and age and shift_rotation and username and password:
            write_to_csv(secu_csv_file, [name, age, shift_rotation, username, password])
            session["new_account"] = {"name": name, "age": age, "shift": shift_rotation, "username": username}
            session["message"] = "Account created successfully!"
            return redirect(url_for("admin"))
        
    message = session.pop("message", "")
    security_data = session.pop("new_account", None)
    return render_template('admin.html', message=message, security_data=security_data)


@app.route('/security', methods=["POST", "GET"])
def security():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        
        credentials = read_from_csv(secu_csv_file)
        for cred in credentials:
            if cred["Username"] == username and cred["Password"] == password:
                return jsonify({"success": True})
        return jsonify({"success": False})
    
    return render_template('security.html')

@app.route('/get_session', methods=['GET'])
def get_session():
    username = session.get('username')
    password = session.get('password')
    if username and password:
        return jsonify({"username": username, "password": password})
    else:
        return jsonify({"message": "No active session found."})


@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True})

# Generate a unique Reservation ID
def generate_reservation_id():
    return "RES" + str(int(time.time()))


@app.route('/users', methods=["POST", "GET"])
def users():
    if request.method == "POST":
        uname = request.form.get("uname")
        aid = request.form.get("aid")
        dob = request.form.get("dob")
        source = request.form.get("source")
        destination = request.form.get("destination")

        if not all([uname, aid, dob, source, destination]):
            return render_template('user.html', message="⚠️ Please fill in all fields.", users=read_from_csv(user_csv_file))

        reservation_id = generate_reservation_id()
        user_data = [uname, aid, dob, source, destination, reservation_id]
        write_to_csv(user_csv_file, user_data)

        session["reservation_message"] = f"✅ Reservation Created! Your ID: {reservation_id}"
        return redirect(url_for("users"))

    message = session.pop("reservation_message", None)
    return render_template('user.html', message=message, users=read_from_csv(user_csv_file))

@app.route('/fetch_reservation', methods=["POST"])
def fetch_reservation():
    data = request.get_json()
    reservation_id = data.get("reservation_id")
    
    users = read_from_csv(user_csv_file)
    
    for user in users:
        if user["Reservation ID"] == reservation_id:
            return jsonify({"success": True, "data": user})
    
    return jsonify({"success": False, "message": "Reservation ID not found."})


video_obj = cv2.VideoCapture(0)
@app.route('/scan')
def scan():
    data, frame = video_obj.read()
    if not data:
        return "Camera Error"
    cv2.imshow('image', frame)
    image_path = "captured_image.jpg"
    cv2.imwrite(image_path, frame)
    return jsonify({"success": True, "image": image_path})

if __name__ == "__main__":
=======
#importing libraries
from flask import Flask,request,session,render_template,jsonify,redirect,url_for
import csv
import os
import time
import cv2

app = Flask(__name__)

app.secret_key = "my_secret_key"  # Required for session storage

user_csv_file = "userdata.csv"
secu_csv_file = "securitydata.csv"

def csv_exists(file_path,headers):
    if not os.path.exists(file_path):
        with open(file_path,mode="w",newline="",encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)

csv_exists = (secu_csv_file,["Name","Age","Shift-Rotation","UserName","Password"])
csv_exists = (user_csv_file,["Name", "Aadhar ID", "DOB", "Source", "Destination", "Reservation ID"])

def write_to_csv(secu_file,data):
    with open(secu_file,mode="a",newline="",encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(data)

def read_from_csv(file_path):
    with open(file_path,mode="r",encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)
    
@app.route('/admin',methods=["POST","GET"])
def admin():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        shift_rotation = request.form["shift-rotation"]
        username = request.form["username"]
        password = request.form["password"]

        if name and age and shift_rotation and username and password:
            write_to_csv(secu_csv_file, [name, age, shift_rotation, username, password])
            session["new_account"] = {"name": name, "age": age, "shift": shift_rotation, "username": username}
            session["message"] = "Account created successfully!"
            return redirect(url_for("admin"))
        
    message = session.pop("message", "")
    security_data = session.pop("new_account", None)
    return render_template('admin.html', message=message, security_data=security_data)


@app.route('/security', methods=["POST", "GET"])
def security():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        
        credentials = read_from_csv(secu_csv_file)
        for cred in credentials:
            if cred["Username"] == username and cred["Password"] == password:
                return jsonify({"success": True})
        return jsonify({"success": False})
    
    return render_template('security.html')

@app.route('/get_session', methods=['GET'])
def get_session():
    username = session.get('username')
    password = session.get('password')
    if username and password:
        return jsonify({"username": username, "password": password})
    else:
        return jsonify({"message": "No active session found."})


@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True})

# Generate a unique Reservation ID
def generate_reservation_id():
    return "RES" + str(int(time.time()))


@app.route('/users', methods=["POST", "GET"])
def users():
    if request.method == "POST":
        uname = request.form.get("uname")
        aid = request.form.get("aid")
        dob = request.form.get("dob")
        source = request.form.get("source")
        destination = request.form.get("destination")

        if not all([uname, aid, dob, source, destination]):
            return render_template('user.html', message="⚠️ Please fill in all fields.", users=read_from_csv(user_csv_file))

        reservation_id = generate_reservation_id()
        user_data = [uname, aid, dob, source, destination, reservation_id]
        write_to_csv(user_csv_file, user_data)

        session["reservation_message"] = f"✅ Reservation Created! Your ID: {reservation_id}"
        return redirect(url_for("users"))

    message = session.pop("reservation_message", None)
    return render_template('user.html', message=message, users=read_from_csv(user_csv_file))

@app.route('/fetch_reservation', methods=["POST"])
def fetch_reservation():
    data = request.get_json()
    reservation_id = data.get("reservation_id")
    
    users = read_from_csv(user_csv_file)
    
    for user in users:
        if user["Reservation ID"] == reservation_id:
            return jsonify({"success": True, "data": user})
    
    return jsonify({"success": False, "message": "Reservation ID not found."})


video_obj = cv2.VideoCapture(0)
@app.route('/scan')
def scan():
    data, frame = video_obj.read()
    if not data:
        return "Camera Error"
    cv2.imshow('image', frame)
    image_path = "captured_image.jpg"
    cv2.imwrite(image_path, frame)
    return jsonify({"success": True, "image": image_path})

if __name__ == "__main__":
>>>>>>> 1b0319678e17c3a2dc892265faa00ec281f069fd
    app.run(debug=True)