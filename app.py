from flask import Flask, render_template, request, redirect, url_for,  jsonify, send_from_directory
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

import os
from dotenv import load_dotenv

from database import db
from models import Data

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')

app.config['SECRET_KEY'] = '6CFCB93DAEB4EFCBF84E4EB59CC4C'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config["TEMPLATES_AUTO_RELOAD"] = True

db.init_app(app)

class AddDataForm(FlaskForm):
    class_name = StringField('Класс:', validators=[DataRequired()])
    culture = StringField('Культура:', validators=[DataRequired()])
    damage = StringField('Повреждения:', validators=[DataRequired()])
    disease = StringField('Болезнь:', validators=[DataRequired()])
    description = TextAreaField('Описание болезни:')
    ir_spectrum = StringField('ИК спектр:')
    uv_spectrum = StringField('HDR спектр:')
    visible_spectrum = StringField('Видимый спектр:')
    ir_file = FileField('ИК файл:')
    uv_file = FileField('HDR файл:')
    visible_image = FileField('Изображение, предпросмотр:')
    submit = SubmitField('Сохранить данные')

    
@app.route('/')
def index():
    #data = Data.query.all()
    first_page = 1
    per_page = 10
    data = Data.query.paginate(page=first_page, per_page= per_page, error_out=False)
    return render_template('index.html', data=data, form=AddDataForm())


@app.route('/process_data', methods=['POST'])
def process_data():
    form = AddDataForm(request.form)
    
    if form.validate():
        new_data = Data(
            class_name = form.class_name.data,
            culture=form.culture.data,
            damage=form.damage.data,
            disease=form.disease.data,
            description=form.description.data,
            ir_spectrum=form.ir_spectrum.data,
            visible_spectrum=form.visible_spectrum.data,
            uv_spectrum=form.uv_spectrum.data,
        )
        
        db.session.add(new_data)
        db.session.flush()
        
        data_id = new_data.id
        
        data_folder = os.path.join(app.config['UPLOAD_FOLDER'], str(data_id))
        os.makedirs(data_folder)
        
        if 'ir_file' in request.files:
            ir_file = request.files['ir_file']
            if ir_file:
                filename = secure_filename(ir_file.filename)
                ir_file_path = os.path.join(data_folder, filename)
                ir_file.save(ir_file_path)
                new_data.ir_image_url = ir_file_path
            
        
        if 'uv_file' in request.files:
            uv_file = request.files['uv_file']
            if uv_file:
                filename = secure_filename(uv_file.filename)
                uv_file_path = os.path.join(data_folder, filename)
                uv_file.save(uv_file_path)
                new_data.uv_image_url = uv_file_path
            
        if 'visible_image' in request.files:
            visible_image = request.files['visible_image']
            if visible_image:
                filename = secure_filename(visible_image.filename)
                visible_image_path = os.path.join(data_folder, filename)
                visible_image.save(visible_image_path)
                new_data.visible_image_url=visible_image_path
        
        db.session.add(new_data)
        db.session.flush()
        db.session.commit()
        
            
            
    return redirect(url_for('index'))

@app.route('/details/<int:data_id>', methods=['GET'])
def get_data_details(data_id):
    data = Data.query.get(data_id)
    if data:
        response = {
            'id': data.id,
            'class_name': data.class_name,
            'culture': data.culture,
            'damage': data.damage,
            'disease': data.disease,
            'description': data.description,
            'ir_spectrum': data.ir_spectrum,
            'visible_spectrum': data.visible_spectrum,
            'uv_spectrum': data.uv_spectrum,
            'ir_image_url': data.ir_image_url,
            'visible_image_url': data.visible_image_url,
            'uv_image_url': data.uv_image_url
        }
        return jsonify(response), 200
    else:
        return jsonify({'message': 'Data not found'}), 404


@app.route('/static/js/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.root_path + '/static/js/', filename, mimetype='text/javascript')

if __name__ == '__main__':
    app.run()