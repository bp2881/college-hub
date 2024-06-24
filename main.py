import os
from flask import Flask, render_template, request, send_file, url_for

app = Flask(__name__)

def list_files(path):
    """Custom Jinja2 filter to list files and directories"""
    return [entry for entry in os.scandir(path)]

app.jinja_env.filters['list_files'] = list_files

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        branch = request.form.get('branch')
        year = request.form.get('year')
        sem = request.form.get('sem')
        
        if not all([branch, year, sem]):
            error_message = "Please select all options: "
            if not branch:
                error_message += "Branch, "
            if not year:
                error_message += "Year, "
            if not sem:
                error_message += "Sem"
            return render_template('index.html', error_message=error_message)
        
        folder_path = os.path.join('files', year, branch, sem)
        files = list_files(folder_path)
        return render_template('files.html', files=files, year=year, branch=branch, sem=sem, path=folder_path)
    return render_template('index.html')

@app.route('/files/<year>/<branch>/<sem>')
def files(year, branch, sem):
    path = request.args.get('path', os.path.join(app.config['UPLOAD_FOLDER'], year, branch, sem))
    files = [f for f in os.scandir(path) if f.is_file() or f.is_dir()]
    return render_template('files.html', files=files, year=year, branch=branch, sem=sem, path=path)

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    year = request.args.get('year')
    branch = request.args.get('branch')
    sem = request.args.get('sem')
    folder_path = os.path.join('files', year, branch, sem)
    file_path = os.path.join(folder_path, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return 'File not found', 404

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'files'
    app.run(debug=True)
