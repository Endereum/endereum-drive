from flask import Flask, url_for, render_template, request
import os
import requests

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('base.html',url_for = url_for)

@app.route("/start_daemon")
def start_daemon():
    os.system("ipfs daemon")
    return "Starting daemon"

@app.route("/is_daemon_running")
def is_daemon_running():
    try:
        request = requests.get('http://127.0.0.1:5001/webui')
        if request.status_code == 200:
            return "IPFS Daemon is running"
        else:
            return "IPFS Daemon is not running"
    except requests.ConnectionError:
        return "IPFS Daemon is not running"
@app.route("/pin_from_database")
def pins_from_database():
    while True:
        r = requests.get(url="http://13.66.133.71:8000/jsony", headers={'Connection':'close'})
        data = r.json()
        data = data['array']
        str1 = ""
        hash_file = open("hashes", "r")
        hashes = hash_file.read().split()
        hash_file.close()
        for hash in data:
            if hash['ids'] not in hashes :
                status = os.system("ipfs pin add " + hash['ids'])
                hashes.append(hash['ids'])
                if status != 0:
                    str1 = str1 + hash['ids'] + " " + "Not pinned yet \n"
        hash_file = open("hashes","w")
        for hash in hashes:
            hash_file.write(hash)
            hash_file.write(" ")
        hash_file.close()
    return "Please continue running the application for continuous pinning"

@app.route('/pin', methods=["GET", "POST"])
def Pin():
    if request.method == 'POST':
        hash = request.form['Hash']
        if hash is not None:
            os.system("ipfs pin add " + hash)
            return "pinned"
        else:
            return "no hash"
    return "Not a post request"

@app.route('/local_files')
def view_local_files():
    os.system("ipfs pin ls | findstr recursive > hash")
    local_files = open("hash", "r").read()
    return local_files

@app.route('/files_pinned_dyanamically')
def view_dyanamic_files():
    str1 = ""
    hash_read = open("hashes", "r").read().split()
    for hash in hash_read:
        str1 = str1 + hash + "\n"
    if str1 == "":
        return "Files not yet pinned"
    else:
        return "displaying files that are pinned to local node from website\n" + str1

if __name__ == "__main__":
    app.run()