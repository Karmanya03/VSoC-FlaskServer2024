from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlitecloud
from apscheduler.schedulers.background import BackgroundScheduler
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Cloud SQLite connection
CLOUD_DB_URL = 'sqlitecloud://cnqdxma8ik.sqlite.cloud:8860?apikey=OG2SQ5GDDmgvkkkqUItb6rhHzIloN17KpciwabUuwPM'

# Global variable to store leaderboard data
leaderboard_data = []

# Function to fetch participants from the database
def fetch_leaderboard_data():
    global leaderboard_data
    try:
        conn = sqlitecloud.connect(CLOUD_DB_URL)
        cursor = conn.cursor()
        cursor.execute("USE DATABASE VSoC24Leaderboard")
        cursor.execute("SELECT name, score, gitlink FROM participants ORDER BY score DESC")
        participants = cursor.fetchall()
        conn.close()

        # Assign rank to each participant
        leaderboard_data = [{"rank": idx + 1, "name": row[0], "score": row[1], "gitlink": row[2]} for idx, row in enumerate(participants)]
        print("Fetched leaderboard data:", leaderboard_data)
    except Exception as e:
        print("Error fetching leaderboard data:", e)

# API endpoint to get leaderboard data
@app.route('/api/leaderboard')
def leaderboard_api():
    return jsonify(leaderboard_data)

# API endpoint to get the URL of the leaderboard API
@app.route('/leaderboard-url')
def leaderboard_url_api():
    base_url = request.url_root
    leaderboard_url = base_url + 'api/leaderboard'
    return jsonify({'leaderboard_url': leaderboard_url})

# Scheduler setup
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_leaderboard_data, 'interval', minutes=1)
scheduler.start()

# Initial fetch
fetch_leaderboard_data()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)