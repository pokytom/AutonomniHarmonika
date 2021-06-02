from flask import Flask, render_template, request, url_for, abort
from os import walk
from komAMidi import play_song

SONG_FOLDR = 'songs/'

app = Flask(__name__)

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
                           nadpis="sunrise", songs=f)

@app.route('/song/<string:song_name>', methods=['GET', 'POST'])
def show_post(song_name):
    msg = ''
    if not play_song(song_name):
        abort(404)
    return render_template('200.html')

@app.route("/admin")
def admin(): return render_template('admin.html')

# proto jde 'python Flask_blog.py'
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
