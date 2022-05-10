from flask import Flask, render_template, request
from src.utils import *
import numpy as np
from PIL import Image
from io import BytesIO
from base64 import b64encode

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/start')
def insert():
    open_waste_slot()

    picture, path_return = take_trash_picture()
    PIL_image = Image.fromarray(np.uint8(picture)).convert('RGB')
    data = BytesIO()
    PIL_image.save(data, "JPEG")
    data64 = b64encode(data.getvalue())
    PIL_image = u'data:img/jpeg;base64,'+data64.decode('utf-8') 

    return render_template('insert.html', picture = PIL_image, path=path_return)


@app.route('/waste/pick-type', methods=['POST'])
def pick_type():
    close_waste_slot()

    img = str(request.form['path_return'])

    result, prob = waste_predictor2(img)
    res = clean_or_dirty(img)
    if res == 'Item is clean':
        return render_template('type.html', result=result, prob=prob, res=res)
    else:
        return render_template('dirty.html')



@app.route('/confirmation', methods=['POST'])
def confirmation():
    waste_type = request.form['type']
    #waste,type, im = waste_predictor(path, img)

    process_waste(waste_type)
    return render_template('confirmation.html')


if __name__ == "__main__":
    app.run(debug=True)
