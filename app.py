from flask import Flask, render_template, request, redirect
from werkzeug import secure_filename
import draw_bounding_boxes, cal
from PIL import Image

global box_data

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('home.html')
  
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    global box_data
    if request.method == 'POST':
        f = request.files['file']
        f.save('./static/photo.jpg')
        file = Image.open('./static/photo.jpg')
        box_data = draw_bounding_boxes.draw_boxes(f.filename)
        return render_template('form.html')

@app.route('/event', methods = ['GET', 'POST'])
def create_event():
    global box_data
    if request.method == 'POST':
        form_dict = request.form
        event_dict = {}
        for entry_name, entry in form_dict.items():
            entry = entry.split(' ')
            final = []
            for box in entry:
                if box != '':
                    final.append(box_data[int(box)-1]['text'])
            final = ' '.join(final)
            event_dict[entry_name] = final


        cal.create_event(event_dict)
        return render_template('again.html')


if __name__ == '__main__':
    app.run(debug=True)

