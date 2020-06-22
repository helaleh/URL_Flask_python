from flask import Flask, render_template,request,redirect, url_for,flash,abort
import json
import os.path
from werkzeug.utils import secure_filename


app= Flask(__name__)
app.secret_key= 'hgfggdrddfdfd'

@app.route('/')

def home():
    return render_template('home.html',name='helaleh',logo='iran')


@app.route('/your_url', methods=['GET','POST'])
def your_url():
    if request.method== 'POST':
        urls={}
        if os.path.exists('urls.json'):
            with open('urls.json') as url_file:
                urls=json.load(url_file)

        if request.form['code'] in urls.keys():
            flash('the name has already taken.please pick new one')
            return redirect(url_for('home'))

        if 'url' in request.form.keys():
            urls[request.form['code']]= {'url': request.form['url']}
        else:
            f= request.files['file']
            full_name= request.form['code'] +  secure_filename(f.filename)
            f.save("/Users/helaleh/Desktop/url_shortner/static/user_files/" + full_name) # add back slash for path
            urls[request.form['code']]= {'file':full_name}

        with open('urls.json','w') as url_file:
            json.dump(urls,url_file)
        return render_template('your_url.html',code=request.form['code'])
    else:
        return redirect(url_for('home'))


@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls= json.load(urls_file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                else:
                    return redirect(url_for('static', filename='user_files/' + urls[code]['file']))
    return abort(404)
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404
