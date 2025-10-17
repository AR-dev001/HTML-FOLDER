from flask import Flask, render_template,request
app = Flask(__name__)

ALLOWED_EXTENSIONS= {'txt','pdf','png','jpg','jpeg','gif'}

@app.route('/upload')
def upload_file():
    return ('index.html')

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader', methods = ['GET','POST'])
def uploader_file():
	if request.method == 'POST':
		if 'file' not in request.files:
			# flash('No file part')
			return render_template('index.html', msg='No file part')
		file = request.files['file']   
		# If the user does not select a file, the browser submits an
		# empty file without a filename.
		if file.filename == '':
			# flash('No selected file')
			return render_template('index.html', msg='No Selected file')
		if file and allowed_file(file.filename): 
			file.save(file.filename)
			return render_template('index.html', msg='file uploaded successfully')
		else:
			return render_template('index.html', msg='This file is not supported, upload only png, pdf, txt, jpeg, jpg, gif extension files')

	 
		
@app.route('/')
def index():
	return render_template('index.html')

app.run(host='0.0.0.0', port=8080)
