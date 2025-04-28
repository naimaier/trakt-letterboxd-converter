import json
import csv
import sys
import glob
import os


def is_movie(x):
    return x['type'] == 'movie'


def get_movie_list_ordered(files):
    movie_list = []

    files.sort()
    for file in files:
        with open(file) as export_file:
            parsed_json = json.load(export_file)
            movie_list += parsed_json

    movie_list = list(filter(is_movie, movie_list))
    movie_list.reverse()

    return movie_list


def create_export_list(movies):
    export_list = []

    watched = set()

    for movie in movies:
        obj = {}
        obj['tmdbID'] = movie['movie']['ids']['tmdb']
        obj['imdbID'] = movie['movie']['ids']['imdb']
        obj['Title'] = movie['movie']['title']
        obj['Year'] = movie['movie']['year']
        #obj['Rating10']
        obj['WatchedDate'] = movie['watched_at'].split('T')[0]
        obj['Rewatch'] = obj['tmdbID'] in watched
        export_list.append(obj)
        watched.add(obj['tmdbID'])

    return export_list


def write_to_csv(movies, file_path):

    if len(movies) == 0:
        return

    headers = movies[0].keys()

    with open(file_path, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(movies)


if len(sys.argv) != 2:
    print("Wrong arguments")
    exit(0)

trakt_directory_path = sys.argv[1]
csv_file_path = 'export.csv'

history_files_pattern = os.path.join(trakt_directory_path, 'watched', 'history*.json')
history_files = glob.glob(history_files_pattern)

if len(history_files) == 0:
    print("History files not found")
    exit(0)

movies = get_movie_list_ordered(history_files)
movies = create_export_list(movies)
write_to_csv(movies, csv_file_path)

