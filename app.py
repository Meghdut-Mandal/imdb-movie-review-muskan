from flask import Flask, render_template, request
import pickle
import database_init

conn, current_conn = database_init.get_connection()

def cleardb():
    conn.execute("DELETE FROM movieReview")
    conn.commit()
    pass

def insert_into_db(movie_review,Prediction):
    current_conn.execute("INSERT INTO movieReview (Review, Prediction) VALUES (?, ?)",(movie_review,Prediction))
    conn.commit()
    id = conn.execute('SELECT last_insert_rowid()').fetchall()[0]
    return id


def review(review):
    if review is None or review == "":
        return "Try again"
    with open("model.pickle",'rb') as f:
        pkl = pickle._Unpickler(f)
        pkl.encoding = 'latin1'
        model = pkl.load()
        cv = pkl.load()
    pred = model.predict(cv.fit_transform([review]))
    if pred[0] == 0:
        return "Negative 🙁"
    else:
        return "Positive 😀"




app = Flask(__name__)

@app.route("/")
@app.route("/index.html")
def index():
    return render_template('index.html')

@app.route('/results.html',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        print(request.form['result'])
        prediction = review(request.form['result'])
        id = insert_into_db(request.form['result'],prediction)
        id = id[0]
    
        return render_template('results.html', value=prediction, id=id)

@app.route('/reviews.html')
def reviews():
    movieReview = conn.execute('SELECT * FROM movieReview').fetchall()
    return render_template('reviews.html', posts=movieReview)

@app.route('/thanks.html')
def thanks():
    print(100)
    if request.method == 'POST':
        current_conn.execute("UPDATE movieReview SET Userfeedback = ? WHERE ID = ?",(request.form['correct'], request.form['ID']))
        conn.commit()  
    return render_template('thanks.html')
    
if __name__ == "_main_":
    app.run(debug=True)
