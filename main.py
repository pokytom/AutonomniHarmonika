import os.path
from flask import Flask, render_template, request, url_for, abort, send_from_directory
from os import walk
from komAMidi import play_song, play_note, reset, air_on

SONG_FOLDR = 'songs/'

app = Flask(__name__)

PLAYING_SONG = False

@app.route("/stop-playing", methods=['GET', 'POST'])
def stop_playing():
    print("stop playing")
    PLAYING_SONG = False
    reset()
    return render_template('200.html')

@app.route("/start-air", methods=['GET', 'POST'])
def start_air():
    print("start air")
    air_on()
    return render_template('200.html')
"""
@app.route("/start-playing", methods=['GET', 'POST'])
def start_playing():
    air_on()
    return render_template('200.html')
"""

@app.route("/play-notes/<int:note_number>", methods=['GET', 'Post'])
def playing_note(note_number):
    # metoda pro stisk klavesy
    print("nota:  "+str(note_number))
    play_note(note_number)
    return render_template('200.html')

@app.route("/play-notes", methods=['GET', 'Post'])
def play_notes():
    notes = {53: "f",
             54: "f#",
             55: "g",
             56: "g#",
             57: "a",
             58: "a#",
             59: "h",
             60: "C1",
             61: "C#1",
             62: "D1",
             63: "D#1",
             64: "E1",
             65: "F1",
             66: "F#1",
             67: "G1",
             68: "G#1",
             69: "A1",
             70: "A#1",
             71: "H1",
             72: "C2",
             73: "C#2",
             74: "D2",
             75: "D#2",
             76: "E2",
             77: "F2",
             78: "F#2",
             79: "G2",
             80: "G#2",
             81: "A2",
             82: "A#2",
             83: "H2",
             84: "C3"}
    # prepne na stranku s klavesama
    return render_template('notes_play.html', notes=notes)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'templates'), 'favicon.ico')

@app.route("/", methods=['GET', 'POST'])
def home():
    songy = ['prvni', 'druhy', 'treti']
    f = []
    for (dirpath, dirnames, filenames) in walk(SONG_FOLDR):
        f.extend(filenames)
    for i in range(len(f)-1):
        if f[i][-3:] != 'mid':
            f.pop(i)
    return render_template('home.html',
                           songs=f)

@app.route('/song/<string:song_name>', methods=['GET', 'POST'])
def show_post(song_name):
    msg = ''
    PLAYING_SONG = True
    if not play_song(song_name):
        abort(404)
    return render_template('200.html')

@app.route("/admin")
def admin(): return render_template('admin.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
