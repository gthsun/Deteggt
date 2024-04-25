#Import statements
from flask import Flask, redirect, url_for, render_template, request, session
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from wtforms import ValidationError
import importlib
import model
from clear import delete

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key' #Used for encryption - not completely necessary for this application
app.config['UPLOAD_FOLDER'] = 'static/images' #Images directory

#Class that uploads the selected file (and also validates it)
class UploadFileForm(FlaskForm): 
    def validate_file(form, field): #Validates the selected file
        if not field.data:
            raise ValidationError('File is required.') #If no file is selected
        filename = field.data.filename.lower()
        if not filename.endswith(('.jpg', '.jpeg', '.png')):
            raise ValidationError('Only image files are allowed.') #Only allows image files
        
    file = FileField("File", validators=[InputRequired(), validate_file])
    submit = SubmitField("Upload File")

#Home page routing
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    delete()
    form = UploadFileForm()
    if form.validate_on_submit():
        delete()
        file = form.file.data 
        #If everything looks good, it sends the image to the images directory, where the model can obtain it
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
        return redirect(url_for('results')) #Go to results page
    else:
        return render_template('index.html', form=form) #If something goes wrong, don't go to results page and just go back to home
    

#Results page routing
@app.route('/results')
def results():
    importlib.reload(model) #Run the model
    from model import final_string #Obtain the message the model outputs
    annotated_image_filename = 'annotated_image.jpg' #Obtain annotated image
    return render_template('results.html', final_string=final_string, annotated_image=annotated_image_filename) #Display that message on results screen

#Main method - runs application
if __name__ == '__main__':
    app.run(debug=True)
