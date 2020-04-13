# THIS PROJECT IS AN EXAMPLE APP. SOME CODE MAY NOT BE ACTUALLY USEFUL
# FOR DEMONSTRATION PURPOSES ONLY
# YOUR MILEAGE MAY VARY
# Requirements are Flask, Flask-WTF, Flask-SQLAlchemy

import os
import sys
from flask import (Flask,
                   Blueprint,
                   redirect,
                   render_template_string,
                   request,
                   url_for)

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextField
from wtforms.validators import Required
import utils
import pickle
BASE_PATH = os.path.abspath(os.path.dirname(__file__))

library_path = "library/"
settings = {
    'SECRET_KEY': 'super not secure development key',
    'DEBUG': True,
}

app = Flask(__name__)
app.config.update(settings)

blog = Blueprint('blog', __name__)

# The index template string for the main page
index_template = '''
<script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-3.4.1.min.js"></script>

<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.20/css/jquery.dataTables.min.css">
<script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js"></script>

<script>
$(document).ready( function () {
    $('#reading').DataTable( {
        paging: true,
        scrollY: 600
    } );
} );
</script>
<form method="POST" enctype="multipart/form-data">
    <input type="file" name="file" autocomplete="off" required>
    <p><input type="submit" value="Upload"></p>
</form>


<table id="reading" class="display">
    <thead>
        <tr>
            <th>Category</th>
            <th>Title</th>
            <th>Line Readability</th>
            <th>Morph Readability</th>
        </tr>
    </thead>
    <tbody>
        {% for row in library %}
        <tr>
        <td>{{row[0]}}</td>
        <td>{{row[1]}}</td>
        <td>{{row[2]}}</td>
        <td>{{row[3]}}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>

'''
#  {% for r in row %} {{r}} {% endfor %}
import io
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_wtf import FlaskForm, RecaptchaField
class UploadForm(FlaskForm):
    upload = FileField('morphdata', validators=[
        FileRequired(),
        # FileAllowed(['morphdata'], 'Morph data only!')
    ])



@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            app.instance_path, 'photos', filename
        ))
        return redirect(url_for('index'))

    return render_template('upload.html', form=form)


error_template = '''
<div id="error">
    <h1> Sorry, there was an error</h1>
    <p>Error:# {{ status_code }}</p>
</div>
'''

@app.errorhandler(404)
def page_not_found(e):
    return render_template_string(error_template, status_code=404), 404


@app.errorhandler(500)
def server_error(e):
    return render_template_string(error_template, status_code=500), 500


@blog.route('/', methods=['GET','POST'])
def index():
    global library_path
    library = []
    form = UploadForm()
    if request.method == 'POST':
        fname = os.urandom(16).hex()
        known_db_path = f'/tmp/{fname}'
        request.files['file'].save(known_db_path)
        known_db = utils.get_known_db(known_db_path)

    try:
        i = 0
        for collection in os.listdir(library_path):

            collection_path = os.path.join(library_path, collection)
            category = collection
            if os.path.isdir(collection_path):
                for title in os.listdir(collection_path):
                    title_path = os.path.join(collection_path, title)
                    if os.path.isfile(title_path) and title_path.endswith("morphdata"):
                        i += 1
                        # if i== 6:
                        #     break
                        line_readability  = "0"
                        morph_readability = "0"
                        if request.method == 'POST':                
                                title_obj = pickle.load(open(title_path, 'rb'))
                                line_readability, morph_readability = title_obj.evaluate_readability(known_db)
                                line_readability = f"{line_readability*100:.2f}"
                                morph_readability = f"{morph_readability*100:.2f}"
                        library.append([category, title.split(".morphdata")[0], line_readability, morph_readability])
    finally:
        if request.method == 'POST':
            os.remove(known_db_path)
                        
    return render_template_string(index_template, form=form, library=library)


app.register_blueprint(blog)

if __name__ == '__main__':
    assert os.path.isdir(library_path)
    app.run()