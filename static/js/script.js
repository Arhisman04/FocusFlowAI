<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Focus Timer</title>

    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>

<body>

    <div class="timer-container">

        <h1>Focus Timer</h1>

        <div class="timer-display" id="timer">
            25:00
        </div>

        <div class="timer-buttons">

            <button onclick="startTimer()">Start</button>

            <button onclick="pauseTimer()">Pause</button>

            <button onclick="resetTimer()">Reset</button>

        </div>

    </div>

    <script src="{{ url_for('static', filename='js/script.js') }}"></script>

</body>
</html>