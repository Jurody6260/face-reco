from api import *

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