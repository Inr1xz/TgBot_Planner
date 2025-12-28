from flask import Flask, render_template_string
from db import get_tasks


app = Flask(__name__)

@app.route("/<int:user_id>")
def calendar_view(user_id):
    tasks = get_tasks(user_id)
    events = [
    {
    "title": f"{task.description} (Priority {task.priority})",
    "start": task.due_date.strftime("%Y-%m-%dT%H:%M") if task.due_date else "",
    }
    for task in tasks if task.due_date
    ]
    return render_template_string("""
    <html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/fullcalendar@6.1.8/main.min.css" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/fullcalendar@6.1.8/main.min.js"></script>
    </head>
    <body>
        <div id='calendar'></div>
        <script>
            document.addEventListener('DOMContentLoaded', function() {
                var calendar = new FullCalendar.Calendar(document.getElementById('calendar'), {
                    initialView: 'dayGridMonth',
                    events: {{ events|tojson }}
                });
                calendar.render();
            });
        </script>
    </body>
    </html>
    """, events=events)


if __name__ == "__main__":
    app.run(debug=True)