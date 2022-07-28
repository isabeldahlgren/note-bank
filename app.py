from flask import Flask, render_template
from converter import converter
import os

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/<section>')
def data(section):
    files = [file for file in os.listdir(f'./{section}') if file[-4:] == ".tex"]
    paths = [os.path.join(f'./{section}', file) for file in files]
    topics = [file[:-4] for file in files]
    content = converter(paths)
    return render_template('module.html', content=content, topics=topics)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')