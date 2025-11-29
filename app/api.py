from flask import Flask, jsonify, request, render_template

from app.db import get_conn, init_db

def create_app() -> Flask:
    app = Flask(__name__)
    init_db()
    # Health check endpoint
    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})
    @app.get("/")
    def dashboard():
        return render_template("dashboard.html")


    @app.get("/metrics/daily-summary")
    def daily_summary():
        # Get the date query parameter
        date = request.args.get("date")
        # If the date is not provided, there will be an error
        if not date:
            return jsonify({"error": "date query param is required, e.g. ?date=2024-11-01"}), 400

        # Query the database for the daily summary
        with get_conn() as conn:
            row = conn.execute("""
                SELECT
                    date,
                    SUM(transactions) AS total_transactions,
                    ROUND(SUM(revenue), 2) AS total_revenue,
                    ROUND(AVG(avg_rating), 2) AS avg_rating
                FROM metrics
                WHERE date = ?
                GROUP BY date                   
            """, (date,)).fetchone()

        if row is None:
            return jsonify({"error": f"no data for date={date}"}), 404
        # Return the summary as JSON
        return jsonify(dict(row))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)