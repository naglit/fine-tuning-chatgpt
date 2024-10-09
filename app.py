from flask import Flask, render_template, request, redirect, url_for, flash
from src import openai_service

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if file:
        # Save file temporarily and pass its path to openai_service
        file_path = f'/tmp/{file.filename}'
        file.save(file_path)
        openai_service.upload_dataset(file_path)
        flash('File uploaded successfully!', 'success')
    else:
        flash('No file uploaded', 'error')
    return redirect(url_for('index'))

@app.route('/tune', methods=['POST'])
def tune():
    file_id = request.form.get('file_id')
    model = request.form.get('model')
    if file_id:
        response = openai_service.start_finetune(file_id, model)
        flash(f'Model fine-tuning started. Fine-tune ID: {response}', 'success')
    else:
        flash('File ID is required', 'error')
    return redirect(url_for('index'))

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form.get('prompt')
    model_id = request.form.get('model_id')
    max_tokens = int(request.form.get('max_tokens', 100))
    
    if prompt:
        response = openai_service.generate_response(prompt, model_id, max_tokens)
        flash(f'Response generated: {response}', 'success')
    else:
        flash('Prompt is required', 'error')
    return redirect(url_for('index'))

@app.route('/check', methods=['POST'])
def check():
    fine_tune_id = request.form.get('fine_tune_id')
    if fine_tune_id:
        status = openai_service.check_finetune_status(fine_tune_id)
        flash(f'Fine-tune status: {status}', 'success')
    else:
        flash('Fine-tune ID is required', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
