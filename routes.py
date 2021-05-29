from api import *

UPLOAD_FOLDER = 'path/'

@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == "POST":
        name = request.form['name']
        group = request.form['group']
        level = request.form['level']
        login = request.form['login']
        password = request.form['password']
        #password2 = request.form['password2']
        
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('add',
                                    filename=filename))
        user = User(name=name, group_id=group, level=level, login=login, password=password, path=os.path.join(UPLOAD_FOLDER, filename))

        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи возникла ошибка"
    else:
        return render_template("add.html")

@app.route('/group_add', methods=['POST', 'GET'])
def group_add():
    if request.method == "POST":
        name = request.form['name']
        faculty = request.form['faculty']
        #password2 = request.form['password2']
        grp = Group(name=name, faculty_id=faculty)

        try:
            db.session.add(grp)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении группы возникла ошибка"
    else:
        return render_template("group_add.html")

@app.route('/faculty_add', methods=['POST', 'GET'])
def faculty_add():
    if request.method == "POST":
        name = request.form['name']
        #password2 = request.form['password2']
        fac = Faculty(name=name)

        try:
            db.session.add(fac)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении факультета возникла ошибка"
    else:
        return render_template("faculty_add.html")

@app.route('/depart_add', methods=['POST', 'GET'])
def depart_add():
    if request.method == "POST":
        name = request.form['name']
        faculty = request.form['faculty']
        #password2 = request.form['password2']
        dep = Depart(name=name, faculty_id = faculty)

        try:
            db.session.add(dep)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении отделения возникла ошибка"
    else:
        return render_template("faculty_add.html")


@app.route('/in_video')
def in_video_url():
    global in_video
    return Response(gen(in_video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/out_video')
def out_video_url():
    global out_video
    return Response(gen(out_video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")