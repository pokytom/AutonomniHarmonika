import os.path
from flask import Flask, render_template, request, url_for, abort, send_from_directory
from os import walk
from komAMidi import play_song, play_note, reset, air_on, set_wind_power, get_wind_power

SONG_FOLDR = 'songs/'
#rnd cmt
app = Flask(__name__)

@app.route("/set-wind-power/<int:wind_power>", methods=['GET', 'POST'])
def set_wind_power_fnc(wind_power):
    print("set_wind: ", wind_power)
    set_wind_power(wind_power)
    return render_template('200.html')

@app.route("/stop-playing", methods=['GET', 'POST'])
def stop_playing():
    print("stop playing")
    reset()
    return render_template('200.html')

@app.route("/start-air", methods=['GET', 'POST'])
def start_air():
    print("start air")
    air_on()
    return render_template('200.html')

@app.route("/start-playing", methods=['GET', 'POST'])
def start_playing():
    air_on()
    return render_template('200.html')

@app.route("/play-notes/<int:note_number>", methods=['GET', 'Post'])
def playing_note(note_number):
    # metoda pro stisk klavesy
    print("nota:  "+str(note_number))
    play_note(note_number)
    return render_template('200.html')

@app.route("/play-notes", methods=['GET', 'Post'])
def play_notes():
    #TODO: sem napsat ty noty
    notes = {50: "a",
             51: "b",
             52: "c",
             53: "d",
             54: "e"}
    # prepne na stranku s klavesama
    wind_power = get_wind_power()
    return render_template('notes_play.html', notes=notes, wind_power=wind_power)

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
    wind_power = get_wind_power()
    return render_template('home.html',
                           songs=f, wind_power=wind_power)

@app.route('/song/<string:song_name>', methods=['GET', 'POST'])
def show_post(song_name):
    msg = ''
    if not play_song(song_name):
        abort(404)
    return render_template('200.html')

@app.route("/admin")
def admin(): return render_template('admin.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
