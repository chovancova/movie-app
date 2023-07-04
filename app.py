import matplotlib
matplotlib.use('Agg')

from flask import Flask, send_file, make_response

import csv
import io

app = Flask(__name__)

movies = [
    {'title': 'Movie 1', 'release_year': 2018},
    {'title': 'Movie 2', 'release_year': 2019},
    {'title': 'Movie 3', 'release_year': 2019},
    {'title': 'Movie 4', 'release_year': 2020},
    {'title': 'Movie 5', 'release_year': 2020},
    {'title': 'Movie 6', 'release_year': 2021},
]

def generate_movie_release_chart(movies):
    # Count the number of movies released each year
    year_counts = {}
    for movie in movies:
        year = movie['release_year']
        year_counts[year] = year_counts.get(year, 0) + 1

    # Prepare data for the bar chart
    years = list(year_counts.keys())
    counts = list(year_counts.values())

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
    generate_movie_release_chart(movies)

    # Return the generated chart as a file download
    return send_file('chart.png', mimetype='image/png')

@app.route('/load-data')
def load_data_endpoint():
    # Your load_data_endpoint endpoint logic here
    return 'load_data_endpoint endpoint'

@app.route('/export-data')
def export_data():
    # Set the response headers to indicate a CSV file download
    headers = {
        'Content-Type': 'text/csv',
        'Content-Disposition': 'attachment; filename=movies.csv'
    }

    # Create a temporary in-memory file to write the CSV data
    temp_file = io.StringIO()
    writer = csv.DictWriter(temp_file, fieldnames=['title', 'release_year'])

    # Write the CSV header
    writer.writeheader()

    # Write each movie as a CSV row
    for movie in movies:
        writer.writerow(movie)

    # Move the file pointer to the beginning of the file
    temp_file.seek(0)

    # Create a Flask response with the CSV file
    response = make_response(temp_file.getvalue())
    response.headers = headers

    # Close the in-memory file
    temp_file.close()

    # Return the response
    return response
