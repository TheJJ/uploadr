import hashlib
import pathlib

from flask import (Flask, request, redirect, url_for, send_from_directory,
                   flash, render_template)


UPLOAD_FOLDER = '/tmp/stuff'

APP = Flask(__name__)
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
APP.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
APP.config['SECRET_KEY'] = b"sofuckingsecretsrsly"


@APP.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file received')
            return redirect(request.url)

        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No file uploaded')
            return redirect(request.url)

        if file:
            hash = hashlib.sha256()
            hash.update(file.read())
            filename = hash.hexdigest()

            folder = pathlib.Path(APP.config['UPLOAD_FOLDER'])

            if (folder / filename).exists():
                flash('File already known')
                return redirect(url_for('index'))

            file.save(str(folder / filename))

            return redirect(url_for('thanks'))


@APP.route('/')
def index():
    return render_template("index.html")


@APP.route('/thx')
def thanks():
    flash('File was uploaded')
    return render_template("thx.html")


if __name__ == '__main__':
    APP.run()
