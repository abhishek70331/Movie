from flask import Flask,render_template,request,redirect,url_for
import numpy as np
import pandas as pd
import difflib
import pickle

app = Flask(__name__)

movie = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_data = pd.read_csv('D:\movie_rec\movie_data')

@app.route('/')
@app.route("/index" , methods = ['GET','POST'])
def index():
    if request.method == "POST":
        movie = request.form['movie']
        print(movie)
        return redirect(url_for('home'))
    return render_template("index.html")
   

@app.route("/home" , methods = ['GET','POST'])
def home():
   if request.method == "POST":
        movie = request.form['movie']
        print(movie)

        list_of_movie = movie_data['title'].to_list()

        close_match = difflib.get_close_matches(movie,list_of_movie)

        best_match = close_match[0]

        movie_index = movie_data[movie_data.title==best_match]['index'].values[0]

        similarity_score = list(enumerate(similarity[movie_index]))

        similarity_movie = sorted(similarity_score,key=lambda x: x[1],reverse = True)

        i = 1
        mov = [] 
        for movies in similarity_movie:
            store = movies[0]
            title_movie = movie_data[movie_data.index==store]['title'].values[0]
         
            if i<10:
                print(i, " ", title_movie)
                mov.append(title_movie)
                i+=1
            else:
                break
            
        return render_template("home.html",mov = mov)  
   else:      
    return render_template("home.html")



if __name__ == '__main__':
   app.run()