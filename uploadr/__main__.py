"""
simple file upload flask app that stores files with its hash as name
"""

import argparse
import hashlib
import pathlib

from flask import (Flask, request, redirect, url_for, flash, render_template)


APP = Flask(__name__)
APP.config['SECRET_KEY'] = b"sofuckingsecretsrsly"


@APP.route('/upload', methods=['GET', 'POST'])
def upload_file():
    """ store the uploaded file in the targed directory """

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file received')
            return redirect(url_for('index'))

        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No file uploaded')
            return redirect(url_for('index'))

        if file:
            filehash = hashlib.sha256()
            filehash.update(file.read())
            filename = filehash.hexdigest()

            folder = pathlib.Path(APP.config['UPLOAD_FOLDER'])

            if (folder / filename).exists():
                flash('File already known')
                return redirect(url_for('index'))

            file.seek(0)

            file.save(str(folder / filename))

            return redirect(url_for('thanks'))
    else:
        flash("No POST request")
        return redirect(url_for('index'))


@APP.route('/')
def index():
    """ main page """
    return render_template("index.html")


@APP.route('/thx')
def thanks():
    """ if file was uploaded successfully """

    flash('File was uploaded')
    return render_template("thx.html")


def main():
    """ entry point and launch """

    cmd = argparse.ArgumentParser()
    cmd.add_argument("folder", help="destionation folder for uploads")
    cmd.add_argument("-p", "--port", default=5000, type=int,
                     help="port to listen on")
    cmd.add_argument("-m", "--max-size", default=32*1024*1024, type=int,
                     help="size in bytes to limit file size, default 32M")

    args = cmd.parse_args()

    APP.config['UPLOAD_FOLDER'] = args.folder
    APP.config['MAX_CONTENT_LENGTH'] = args.max_size
    APP.run(port=args.port)


if __name__ == '__main__':
    main()
