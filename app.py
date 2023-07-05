import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
from flask import Flask, send_file, make_response, g
import csv
import io
import matplotlib

matplotlib.use('Agg')

app = Flask(__name__)

DB_NAME = 'database.db'
TABLE_NAME = 'movies'
CSV_FILE = 'datasets/movies_metadata.csv'


def get_data_from_db():
    """Get data from the database"""
    with sqlite3.connect(DB_NAME) as conn:
        df = pd.read_sql_query(f'SELECT * FROM {TABLE_NAME}', conn)
    return df.to_dict('records')


def generate_movie_release_chart(movies):
    """Generate a bar chart showing the number of movies released each year
    :type movies: list
    """
    # Count the number of movies released each year
    year_counts = {}
    for movie in movies:
        year = movie['release_year']
        year_counts[year] = year_counts.get(year, 0) + 1

    # Prepare data for the bar chart
    years = list(year_counts.keys())
    counts = list(year_counts.values())

    # Sort years in ascending order
    years, counts = zip(*sorted(zip(years, counts)))

    # Generate the bar chart
    plt.bar(years, counts)

    # Customize the chart
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.title('Number of Movies Released Each Year')

    # Optionally, rotate x-axis labels if needed
    plt.xticks(rotation=45)

    # Save the chart to a file instead of showing it
    plt.savefig('chart.png')
    plt.close()


@app.route('/draw-chart')
def graph_endpoint():
    """Generate a bar chart and return it to the client"""
    movies = get_data_from_db()
    generate_movie_release_chart(movies)
    return send_file('chart.png', mimetype='image/png')


@app.route('/load-data')
def load_data_endpoint():
    """Load data from CSV file into database"""
    df = pd.read_csv(CSV_FILE, usecols=['original_title', 'release_date'])

    # Filter out rows with incorrect date format
    df = df[df['release_date'].str.len() == 10]

    # Convert 'release_date' to datetime
    df['release_date'] = pd.to_datetime(df['release_date'], format="%Y-%m-%d", errors='coerce')

    # Drop rows with NaT in 'release_date'
    df = df.dropna(subset=['release_date'])

    # Create 'release_year' column
    df['release_year'] = df['release_date'].dt.year

    # Write DataFrame to SQLite
    with sqlite3.connect(DB_NAME) as conn:
        df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)

    return 'Data loaded into database successfully', 200


@app.route('/export-data')
def export_data():
    """Export data from database to CSV file"""
    headers = {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=movies.csv'
    }

    movies = get_data_from_db()
    temp_file = io.StringIO()
    fieldnames = ['original_title', 'release_year']
    writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
    writer.writeheader()

    for movie in movies:
        filtered_movie = {
            'original_title': movie['original_title'],
            'release_year': movie['release_year']
        }
        writer.writerow(filtered_movie)

    temp_file.seek(0)
    response = make_response(temp_file.getvalue())
    response.headers = headers
    temp_file.close()
    return response
