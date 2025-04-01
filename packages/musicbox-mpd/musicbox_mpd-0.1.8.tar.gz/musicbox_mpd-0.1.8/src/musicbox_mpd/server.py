from bottle import route, post, run, request, app, static_file, delete
from bottle_cors_plugin import cors_plugin
import json
import os
import sys
import time
from urllib.parse import unquote
import pathlib
import argparse

from musicbox_mpd.musicplayer import MusicPlayer
from musicbox_mpd import data
from musicbox_mpd import __about__
from musicbox_mpd import startup


def query(sql, params):
    res = con.execute(sql, params)
    rows = res.fetchall()
    return [dict(row) for row in rows]


def status_json(status, message=""):
    return f"""{{"status": "{status}", "message": "{message}"}}"""


def get_static_path():
    return os.path.join(pathlib.Path(__file__).parent.resolve(), "ui")


@route('/ui')
def ui():
    # ui.html is not a static file, as using version number to bust cache of javascript file.
    with open(os.path.join(get_static_path(), "ui.html")) as f:
        html = f.read()
        return html.replace("{ver}", __about__.__version__)


@route('/settingsui')
def settingsui():
    return static_file("settings.html", get_static_path())


@route('/ui/<file>')
def ui2(file):
    return static_file(file, get_static_path())


@route('/version')
def get_version():
    # return status_json("OK", __about__.__version__)
    return f"""{{"musicbox": "{__about__.__version__}", "mpd": "{player.get_mpd_version()}"}}"""


@route('/coverart/<id>')
def coverart(id):
    uri = data.get_uri(con, id)

    if uri == None:
        return static_file("default.gif", get_static_path())

    image_folder = config.get("image_folder")

    cover = player.get_cover_art(uri, image_folder)
    if cover == None:
        return static_file("default.gif", get_static_path())
        # cover = config.get("default_image")

    if not cover == None:
        path = os.path.dirname(cover)
        filename = os.path.basename(cover)
        return static_file(filename, path)


@route('/search')
def search():
    result = data.search(con, request.query.search)

    # If no results and no search filters, try to cache the library and search again
    if len(result) == 0 and request.query.search == "":
        print("Library empty - Caching library and retrying search")
        player.cache_library(con)
        result = data.search(con, request.query.search)

    return json.dumps(result)


@route('/album')
def album():
    search = unquote(request.query.search)
    result = data.get_album(con, search)

    return json.dumps(result)


@post('/add/<id>')
def add(id):
    uri = data.get_uri(con, id)
    player.add_to_queue(uri)

    return status_json("OK")


@delete('/<id>')
def remove(id):
    player.remove_from_queue(id)

    return status_json("OK")


@delete('/all')
def remove():
    player.clear_queue()
    return status_json("OK")


@route("/queue")
def queue():
    result = player.get_queue()
    return json.dumps(result)


@route("/queuestatus")
def queuestatus():
    result = player.get_queue()
    return f"""{{ "queueCount" : {len(result)}, "queueLength" : {sum([float(x.get("duration")) for x in result if x.get("duration") != None])} }}"""


@route("/status")
def status():
    status = player.status()
    uri = status.get("file")
    if uri == None:
        status["libraryid"] = 0
    else:
        status["libraryid"] = data.get_id(con, uri)
    return json.dumps(status)


@post('/play')
def play():
    status = player.play()
    if status == False:
        return status_json("Error", player.error_message)
    return status_json("OK")


@post('/stop')
def stop():
    player.stop()
    return status_json("OK")


@post('/skip')
def skip():
    player.skip()
    return status_json("OK")


@post('/pause')
def pause():
    player.pause()
    return status_json("OK")


@post('/volume/<vol>')
def volume(vol):
    result = player.volume(vol)
    return status_json(result)


@post('/queuealbum')
def queuealbum():
    params = request.json
    uri = params["path"][:-1]
    player.add_to_queue(uri)

    return status_json("OK")


@post('/playsong/<id>')
def playsong(id):
    status = player.status()
    if status.get("state") == "play":
        return status_json("Already playing")
    uri = data.get_uri(con, id)
    player.clear_queue()
    player.add_to_queue(uri)
    if not player.play():
        return status_json("Error", player.error_message)
    return status_json("OK")

# Use for scanning QR codes TODO: Implement


@post('/playalbum')
def playalbum():
    status = player.status()
    if status.get("state") == "play":
        return status_json("Already playing")
    player.clear_queue()
    uri = request.json["path"][:-1]
    player.add_to_queue(uri)
    player.play()
    return status_json("OK")


@post('/rand/<num>')
def random_queue(num):
    for song in data.get_random_songs(con, num):
        player.add_to_queue(song["filename"])
    return status_json("OK")


@route("/mix")
def get_mixtapes():
    result = player.get_playlists()
    return json.dumps(result)


@post('/loadmix/<name>')
def load_mixtape(name):
    player.load_playlist(name)
    return status_json("OK")


@post('/savemix/<name>')
def load_mixtape(name):
    player.update_playlist(name)
    return status_json("OK")


@post('/mix/<name>')
def create_mixtape(name):
    result = player.save_playlist(name)
    if result:
        return status_json("OK")
    else:
        return status_json("Error", player.error_message)


@delete('/mix/<name>')
def delete_mixtape(name):
    player.delete_playlist(name)
    return status_json("OK")


@post('/update')
def update():
    result = player.update(con)
    return json.dumps(result)


@post('/setting/<name>/<value>')
def setting(name, value):
    player.set_setting(name, value)
    return status_json("OK")


@route('/replaygain')
def replaygain():
    result = player.get_replay_gain_status()
    if result == None:
        return status_json("Error", player.error_message)
    return status_json("OK", result)


@post('/replaygain')
def set_replaygain():
    value = request.json["mode"]
    result = player.set_replay_gain_mode(value)
    if result == False:
        return status_json("Error", player.error_message)
    return status_json("OK", result)


@post('/shuffle')
def shuffle():
    result = player.shuffle()
    if result == False:
        return status_json("Error", player.error_message)
    return status_json("OK", result)


def main():
    global app
    global config
    global player
    global con

    if args.service:
        startup.create_service()
        return

    if args.version:
        print(f"Musicbox MPD version {__about__.__version__}")
        return

    if args.create_config:
        startup.get_default_config(True)
        print("Config file 'musicbox-mpd.conf.json' created")
        return

    config = startup.get_config(args.configfile)

    con = data.in_memory_db()
    app = app()
    app.install(cors_plugin('*'))
    player = MusicPlayer(config["mpd_host"], config["mpd_port"])

    startup.try_cache_library(player, con)
    startup.add_radio_stations(con, config.get("stations"))
    run(host=config["host"], port=config["port"])


##### ENTRY POINT #####
parser = argparse.ArgumentParser(
    prog='Musicbox MPD',
    description='A MPD Client')
parser.add_argument('-v', '--version', action='store_true')
parser.add_argument('-c', '--configfile')
parser.add_argument('-s', '--service', action='store_true',
                    help="create systemd service file in current directory")

parser.add_argument('--create-config', action='store_true',
                    help="create default config file in current directory")
args = parser.parse_args()

if __name__ == "__main__":
    main()
