
from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>India Quiz App</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #141e30, #243b55);
            color: #333;
            min-height: 100vh;
            padding: 30px 15px;
        }

        .container {
            max-width: 650px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.3);
        }

        h1 {
            text-align: center;
            color: #243b55;
            margin-bottom: 10px;
        }

        .subtitle {
            text-align: center;
            color: #777;
            margin-bottom: 30px;
        }

        .question {
            background: #f4f7fb;
            padding: 18px;
            margin-bottom: 18px;
            border-radius: 12px;
            border-left: 5px solid #4361ee;
        }

        label {
            display: block;
            font-weight: bold;
            margin-bottom: 12px;
        }

        input {
            width: 100%;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 16px;
            outline: none;
        }

        input:focus {
            border-color: #4361ee;
            box-shadow: 0 0 5px #4361ee55;
        }

        button {
            width: 100%;
            padding: 14px;
            background: #4361ee;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 17px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 10px;
        }

        button:hover {
            background: #3046b5;
        }

        .result {
            margin-top: 25px;
            padding: 18px;
            background: #e8f7ed;
            color: #176b35;
            text-align: center;
            border-radius: 12px;
            font-size: 20px;
            font-weight: bold;
        }

        .feedback {
            margin-top: 8px;
            font-size: 14px;
        }

        .correct {
            color: green;
        }

        .wrong {
            color: #d62828;
        }

        .reset {
            display: block;
            text-align: center;
            margin-top: 18px;
            color: #4361ee;
            text-decoration: none;
        }
    </style>
</head>

<body>
    <div class="container">
        <h1>🇮🇳 India Quiz Challenge</h1>
        <p class="subtitle">Answer all 5 questions and check your score!</p>

        <form method="POST">
            {% for question in questions %}
                <div class="question">
                    <label>{{ loop.index }}. {{ question }}</label>
                    <input
                        type="text"
                        name="answer{{ loop.index0 }}"
                        placeholder="Enter your answer"
                        value="{{ answers[loop.index0] }}"
                        required
                    >

                    {% if submitted %}
                        <div class="feedback
                            {{ 'correct' if results[loop.index0] else 'wrong' }}">
                            {% if results[loop.index0] %}
                                ✓ Correct answer!
                            {% else %}
                                ✗ Correct answer: {{ correct_answers[loop.index0] }}
                            {% endif %}
                        </div>
                    {% endif %}
                </div>
            {% endfor %}

            <button type="submit">Submit Answers</button>
        </form>

        {% if submitted %}
            <div class="result">
                Your Score: {{ score }} / {{ questions|length }}
                <p style="font-size: 15px; margin-bottom: 0;">
                    {{ message }}
                </p>
            </div>

            <a class="reset" href="/">Try Again ↻</a>
        {% endif %}
    </div>
</body>
</html>
"""

questions = [
    "What is the capital of India?",
    "What is the capital of Telangana?",
    "What is the national animal of India?",
    "What is the national flower of India?",
    "What is the national bird of India?"
]

correct_answers = [
    "delhi",
    "hyderabad",
    "tiger",
    "lotus",
    "peacock"
]

display_answers = [
    "Delhi",
    "Hyderabad",
    "Tiger",
    "Lotus",
    "Peacock"
]


@app.route("/", methods=["GET", "POST"])
def quiz():
    submitted = request.method == "POST"
    answers = []
    results = []
    score = 0

    if submitted:
        for i in range(len(questions)):
            answer = request.form.get(f"answer{i}", "").strip().lower()
            answers.append(answer)

            is_correct = answer == correct_answers[i]
            results.append(is_correct)

            if is_correct:
                score += 1
    else:
        answers = [""] * len(questions)

    message = ""

    if submitted:
        if score == 5:
            message = "Excellent! All answers are correct!"
        elif score >= 3:
            message = "Good job! Keep practising!"
        else:
            message = "Keep learning. You can try again!"

    return render_template_string(
        HTML,
        questions=questions,
        answers=answers,
        results=results,
        correct_answers=display_answers,
        submitted=submitted,
        score=score,
        message=message
    )


if __name__ == "__main__":
    app.run(debug=True)
