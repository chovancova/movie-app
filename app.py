from flask import Flask

app = Flask(__name__)

@app.route('/draw-chart')
def graph_endpoint():
    # Your draw_chart endpoint logic here
    return 'draw_chart endpoint'

@app.route('/load-data')
def load_data_endpoint():
    # Your load_data_endpoint endpoint logic here
    return 'load_data_endpoint endpoint'

@app.route('/export-data')
def export_data():
    # Your export_data endpoint logic here
    return 'export_data endpoint'
