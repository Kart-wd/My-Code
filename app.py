#Simple File Manager with Python and Flask

#import packages
from flask import Flask
from flask import render_template_string
import os
import subprocess
from flask import redirect
from flask import request

#create web app instance
app = Flask(__name__)

#handle root route
@app.route('/')
def root():
    return render_template_string('''
    <html>
      <head>
        <title>File manager</title>
      </head>
      <body>
        <div align="center">
        <h1>Local file System</h1>
        <p><strong> CWD: </strong>{{ current_working_directory }}</p>
        </div>
        <ul>
          <li style = "list-style:none"><strong><a href="/cd?path=..">Home</strong></a></li>
          {% for item in file_list[0:-1] %}
            {% if  '.' not in item %}
            <li><strong><a href="/cd?path={{current_working_directory + '/' + item }}">{{item}}</a></strong></li>
            {% elif '.txt' in item or '.py' in item or '.html' in item %}
            <li><strong><a href="/view?file={{current_working_directory + '/' + item }}">{{item}}</a></strong></li>
            {% else %}
            <li>{{item}}</li>
            {% endif %}
          {% endfor %}
        </ul>
      </body>
    </html>
    ''', current_working_directory=os.getcwd(),file_list=subprocess.check_output('dir /b',shell=True).decode('utf-8').split('\n'))

#handle the cd command
@app.route('/cd')
def cd():
  #run cd
  os.chdir(request.args.get('path'))
  
  #redirect to file manager
  return redirect('/')

  #view files
@app.route('/view')
def view():
  #get the file content
   return subprocess.check_output('more ' + request.args.get('file'), shell=True).decode('utf-8')


#run the http server
if __name__=='__main__':
    app.run(debug=True,threaded=True)