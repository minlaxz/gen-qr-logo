from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def contact():
    if request.method == 'POST':
        if request.form['submit_button'] == 'Do Something':
            return 'Do something'
        elif request.form['submit_button'] == 'Do Something Else':
            return ('Do something else')
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('contact.html')


if __name__ == '__main__':
   app.run(host='0.0.0.0',port='880' ,debug=True)