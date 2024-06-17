from flask import Flask, jsonify
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
    conn = sqlitecloud.connect(CLOUD_DB_URL)
    cursor = conn.cursor()
    cursor.execute("USE DATABASE VSoC24Leaderboard")
    cursor.execute("SELECT name, score, gitlink FROM participants ORDER BY score DESC")
    participants = cursor.fetchall()
    conn.close()

    # Assign rank to each participant
    leaderboard_data = [{"rank": idx + 1, "name": row[0], "score": row[1], "gitlink": row[2]} for idx, row in enumerate(participants)]

# API endpoint to get leaderboard data
@app.route('/leaderboard')
def leaderboard_api():
    return jsonify(leaderboard_data)

# Scheduler setup
scheduler = BackgroundScheduler()
scheduler.add_job(fetch_leaderboard_data, 'interval', minutes=1)
scheduler.start()

# Initial fetch
fetch_leaderboard_data()

if __name__ == '__main__':
    app.run(host='13.228.225.19', port=80)