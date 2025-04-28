import json
import csv


def is_movie(x):
    return x['type'] == 'movie'


def get_movie_list(file_path):
    with open(file_path) as export_file:
        parsed_json = json.load(export_file)

    return filter(is_movie, parsed_json)


def create_export_list(movies):
    export_list = []

    for movie in movies:
        obj = {}
        obj['tmdbID'] = movie['movie']['ids']['tmdb']
        obj['imdbID'] = movie['movie']['ids']['imdb']
        obj['Title'] = movie['movie']['title']
        obj['Year'] = movie['movie']['year']
        #obj['Rating10']
        obj['WatchedDate'] = movie['watched_at'].split('T')[0]
        #obj['Rewatch']
        export_list.append(obj)

    return export_list


def write_to_csv(movies, file_path):

    if len(movies) == 0:
        return

    headers = movies[0].keys()

    with open(file_path, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(movies)


trakt_file_path = 'trakt.json'
csv_file_path = 'export.csv'

movies = get_movie_list(trakt_file_path)
movies = create_export_list(movies)
write_to_csv(movies, csv_file_path)

