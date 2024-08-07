import os
from flask import Flask, render_template, request, send_file, url_for
from urllib.parse import unquote
import datetime
import json

app = Flask(__name__)

def list_files(path):
    """Custom Jinja2 filter to list files and directories"""
    return [entry for entry in os.scandir(path)]

app.jinja_env.filters['list_files'] = list_files

def load_streak():
    """Load the streak value from a file"""
    streak_file = 'streak.json'
    if os.path.exists(streak_file):
        with open(streak_file, 'r') as f:
            streak_data = json.load(f)
            last_opened = datetime.datetime.fromisoformat(streak_data['last_opened'])
            today = datetime.datetime.today()
            if today.date() == last_opened.date():
                streak = streak_data['streak']
            else:
                streak = streak_data['streak'] + 1
                streak_data['last_opened'] = today.isoformat()
                with open(streak_file, 'w') as f:
                    json.dump(streak_data, f)
    else:
        streak = 1
        with open(streak_file, 'w') as f:
            json.dump({'streak': 1, 'last_opened': datetime.datetime.today().isoformat()}, f)
    return streak

def save_streak(streak):
    """Save the streak value to a file"""
    streak_file = 'streak.json'
    with open(streak_file, 'w') as f:
        json.dump({'streak': streak, 'last_opened': datetime.datetime.today().isoformat()}, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    streak = load_streak()
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
            return render_template('index.html', error_message=error_message, streak=streak)
        
        folder_path = os.path.join('files', year, branch, sem)
        files = list_files(folder_path)
        return render_template('files.html', files=files, year=year, branch=branch, sem=sem, path=folder_path, streak=streak)
    return render_template('index.html', streak=streak)

@app.route('/files/<year>/<branch>/<sem>')
def files(year, branch, sem):
    path = request.args.get('path', os.path.join('files', year, branch, sem))
    files = [f for f in os.scandir(path) if f.is_file() or f.is_dir()]
    return render_template('files.html', files=files, year=year, branch=branch, sem=sem, path=path)

@app.route('/download', methods=['GET'])
def download_file():
    year = request.args.get('year')
    branch = request.args.get('branch')
    sem = request.args.get('sem')
    path = unquote(request.args.get('path'))

    root_dir = 'P:\\programming\\projects\\college hub\\files'
    file_path = os.path.join(root_dir, *path.split('\\')[1:])  # Remove the first 'files' directory
    print(f"Trying to access file at: {file_path}")

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=False)
    else:
        return 'File not found', 404

if __name__ == '__main__':
    app.run(debug=True)