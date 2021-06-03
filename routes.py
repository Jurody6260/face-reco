from api import *
import os

UPLOAD_FOLDER = 'imgs/'

@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == "POST":
        name = request.form['name']
       
        group = request.form.get("group_id")
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
        grou = Group.query.all()
        return render_template("add.html", data=grou)




@app.route('/add_group', methods=['POST', 'GET'])
def add_group():
    if request.method == "POST":
        group = request.form.get('group')
        fac_id = request.form.get("faculty_id")
        if group is not None and fac_id is not None:
            gr = Group(name=group, faculty_id=fac_id)

        try:
            db.session.add(gr)
            db.session.commit()
            return redirect('/add_group')
        except:
            return "При добавлении статьи возникла ошибка"

    else:
        facs = Faculty.query.all()
        return render_template("add_group.html", data=facs)


@app.route('/add_depart', methods=['POST', 'GET'])
def add_departp():
    if request.method == "POST":
        depart = request.form.get('depart')
        fac_id = request.form.get("faculty_id")
        if depart is not None and fac_id is not None:
            dep = Depart(name=depart, faculty_id=fac_id)

        try:
            db.session.add(dep)
            db.session.commit()
            return redirect('/add_depart')
        except:
            return "При добавлении статьи возникла ошибка"

    else:
        facs = Faculty.query.all()
        return render_template("add_depart.html", data=facs)


@app.route('/add_faculty', methods=['POST', 'GET'])
def add_faculty():
    if request.method == "POST":
        faculty = request.form['faculty']
        fac = Faculty(name=faculty)

        try:
            db.session.add(fac)
            db.session.commit()
            return redirect('/add_faculty')
        except:
            return "При добавлении статьи возникла ошибка"

    else:
        return render_template("add_faculty.html")





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