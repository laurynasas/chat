from flask import render_template, flash, redirect, url_for, request, Response
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, socketio
# from .audio_processing import record, genHeader, RATE, CHANNELS
from .forms import LoginForm
from .models import User
from . import db

@app.route('/')
@login_required
def sessions():
    return render_template('session.html')


@app.route('/call')
@login_required
def call():
    return render_template('call.html')


def messageReceived():
    print('message was received!!!')


@socketio.on('my event')
def handle_my_custom_event(payload):
    socketio.emit('my response', payload, callback=messageReceived)


#
# # Stream routing
# @app.route('/video_feed')
# def video_feed():
#     """Video streaming route. Put this in the src attribute of an img tag."""
#     return Response(generateVideo(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

#
# @app.route("/audio_feed")
# def audio_feed():
#     """Audio streaming route. Put this in the src attribute of an audio tag."""
#     return Response(generateAudio(),
#                     mimetype="audio/x-wav")

@app.route("/video_feed")
def video_feed():
    return render_template('video.html')

# def generateAudio():
#     while True:
#         """Audio streaming generator function."""
#         currChunk = record()
#         data_to_stream = genHeader(RATE, 32, CHANNELS, 200000) + currChunk
#         yield data_to_stream


#
# # Stream generating
# def generateVideo():
#     """Video streaming generator function."""
#     cap = cv2.VideoCapture(0)
#     while (cap.isOpened()):
#         ret, frame = cap.read()
#         output = framework.streamer(frame, 'final')
#         cv2.imwrite('signals/currFrame.jpg', output)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + open('signals/currFrame.jpg', 'rb').read() + b'\r\n')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('sessions'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('sessions')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('sessions'))
