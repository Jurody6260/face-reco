from models import *
from flask import Flask, render_template, Response, request, redirect, url_for
from genericpath import samefile
import face_recognition
import numpy as np
from os import *
from os.path import *
import cv2, time
from hashlib import sha256
from datetime import datetime
from werkzeug.utils import secure_filename
mypath = "imgs"

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

in_video = cv2.VideoCapture(0)
out_video = cv2.VideoCapture(1)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def SHA256(text):
    return sha256(text.encode("utf-8")).hexdigest()

def Create_Name(path):
    modTimesinceEpoc = getmtime(mypath + "/" + path)
    name = path.split(".")[0]
    enc = SHA256(str(int(modTimesinceEpoc)) + name)
    return enc + "." + name
    
def GetName(enc):
    try:
        return enc.split(".")[1]
    except:
        return enc
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
def Save(count=-1):
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]



    known_face_encodings = [
        
    ]
    known_face_names = [

    ]
    i = 0
    printProgressBar(0, len(onlyfiles), prefix = 'Loading Images:', suffix = 'Complete', length = 50)
    ll = 0
    for item in onlyfiles:
        print(item)
        if ".npz" in item:
            continue
        try:
            img = face_recognition.load_image_file(mypath + "/" + item)
            enc = face_recognition.face_encodings(img)[0]
            known_face_encodings.append(enc)
            n = Create_Name(item)
            known_face_names.append(n)
        except Exception as E:
            print("Error: %s"%str(E))
            print(item)
        if count != -1:
            if i == count:
                break
        printProgressBar(ll, len(onlyfiles), prefix = 'Loading Images:', suffix = 'Complete', length = 50)
        ll+=1
        i+=1
    printProgressBar(ll, len(onlyfiles), prefix = 'Loading Images:', suffix = 'Complete', length = 50)
    mydata=[known_face_encodings,known_face_names]
    np.savez(mypath + '/faces.npz', *mydata)

#myfmt='d'*len(mydata)
#  You can use 'd' for double and < or > to force endinness
#bin=struct.pack(myfmt,*mydata)
#print(bin)
def Load():
    print("* - Started loading binary")
    try:
        with np.load(mypath + '/faces.npz') as a:
            data = [a[key] for key in a]
    except Exception as E:
        print("* - Saved binary not found")
        print("* - Starting saving binary")
        Save()
        print("* - Binary successfuly saved")
        with np.load(mypath + '/faces.npz') as a:
            data = [a[key] for key in a]
 
    #print(container)
    
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for item in onlyfiles:
        if ".npz" in item:
            continue
        nn = Create_Name(item)
        if nn not in data[1]:
            print("* - Detected changes on files")
            print("* - Deleting binary")
            remove(mypath + "/faces.npz")
            return Load()
    
    print("* - Binary successfuly loaded")
    return data[0], data[1]

def gen(video):
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    known_face_encodings, known_face_names = Load()
    
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    while True:
        success, frame = video.read()
        if not success:
            print("fuck")
        rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face enqcodings in the frame of video
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Loop through each face in this frame of video
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            #print([x for x in matches if x ==True])
            #print(matches)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            #print(face_distances)
            best_match_index = np.argmin(face_distances)
            #print(best_match_index)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            name = GetName(name)

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        ret, frame = cv2.imencode('.jpg', frame)
        
        frame = frame.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')