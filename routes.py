from api import *

UPLOAD_FOLDER = 'path/'

@app.route('/add', methods=['POST', 'GET'])
def add():
    if request.method == "POST":
        name = request.form['name']
        group = request.form['group']
        user = User(name=name, group=group)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('add',
                                    filename=filename))

        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавлении статьи возникла ошибка"

    else:
        return render_template("add.html")


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