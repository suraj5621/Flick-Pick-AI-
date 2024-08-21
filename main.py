import pickle
import pandas as pd
from flask import Flask, render_template, request
import requests
import joblib

app = Flask(__name__)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    title = data['title']
    tagline = data['tagline']
    release_date = data['release_date']
    popularity = data['popularity']
    revenue = data['revenue']
    budget = data['budget']
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path, tagline, release_date,popularity,revenue,budget

def self_details(movie,movies):
    for i in range(len(movies)):
        if movies.loc[i,"title"] ==movie:
            # print(movies.loc[i,'id'])
            break
def recommend(movie, movies, similarity):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_tagline = []
    recommended_movie_release_date = []
    recommended_movie_popularity = []
    recommended_movie_revenue = []
    recommended_movie_budget = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].id
        try:
            poster, tagline, release_date, popularity, revenue, budget = fetch_poster(movie_id)
            recommended_movie_posters.append(poster)
            recommended_movie_tagline.append((tagline))
            recommended_movie_release_date.append(release_date)
            recommended_movie_popularity.append(popularity)
            recommended_movie_revenue.append(revenue)
            recommended_movie_budget.append(budget)
            recommended_movie_names.append(movies.iloc[i[0]].title)
        except:
            recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters, recommended_movie_tagline, recommended_movie_release_date, recommended_movie_popularity, recommended_movie_revenue, recommended_movie_budget

@app.route('/')
def home():
    movies = pd.read_pickle('model/movie_list.pkl')
    return render_template('index.html', movie_list=movies['title'].values)

@app.route('/recommendations', methods=['POST'])
def recommendations():
    selected_movie = request.form['selected_movie']
    movies = pd.read_pickle('model/movie_list.pkl')
    similarity = joblib.load('./model/similarity.joblib')
    # self_details(selected_movie, movies)
    recommended_movie_names, recommended_movie_posters, recommended_movie_tagline,recommended_movie_release_date,recommended_movie_popularity,recommended_movie_revenue,recommended_movie_budget = recommend(selected_movie, movies, similarity)

    return render_template('recommendations.html',
                           movie_names=recommended_movie_names,
                           movie_posters=recommended_movie_posters,
                           movie_tagline=recommended_movie_tagline,
                           movie_release_date=recommended_movie_release_date,
                           movie_popularity=recommended_movie_popularity,
                           movie_revenue=recommended_movie_revenue,
                           movie_budget=recommended_movie_budget)


if __name__ == '__main__':
    app.run(debug=True)
