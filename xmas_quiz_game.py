from flask import Flask, render_template_string, request, redirect, url_for
import random

app = Flask(__name__)

# Questions for the quiz
EASY_QUESTIONS = [
    {"question": "What color is Santa's suit?", "options": ["Red", "Blue", "Green", "Yellow"], "answer": "Red"},
    {"question": "What is Frosty the Snowman's nose made of?", "options": ["Carrot", "Button", "Stick", "Coal"],
     "answer": "Button"},
    {"question": "How many reindeer does Santa have (including Rudolph)?", "options": ["8", "9", "10", "7"],
     "answer": "9"},
    {"question": "What do children traditionally leave out for Santa?",
     "options": ["Cookies and Milk", "Candy", "Pizza", "Cake"], "answer": "Cookies and Milk"},
    {"question": "What is the shape of a candy cane?", "options": ["J", "C", "S", "L"], "answer": "J"},
    {"question": "Which holiday is December 25?", "options": ["Christmas", "Thanksgiving", "New Year", "Easter"],
     "answer": "Christmas"},
    {"question": "What are Santa's helpers called?", "options": ["Elves", "Dwarfs", "Fairies", "Pixies"],
     "answer": "Elves"},
    {"question": "What holiday plant is hung to be kissed under?",
     "options": ["Mistletoe", "Holly", "Pine", "Poinsettia"], "answer": "Mistletoe"},
    {"question": "What does Santa say?", "options": ["Ho Ho Ho!", "Ha Ha Ha!", "Merry Merry!", "Bah Humbug!"],
     "answer": "Ho Ho Ho!"},
    {"question": "What is the Grinch's color?", "options": ["Green", "Blue", "Yellow", "Red"], "answer": "Green"}
]

HARD_QUESTIONS = [
    {"question": "Which country first started the tradition of putting up a Christmas tree?",
     "options": ["Germany", "USA", "France", "England"], "answer": "Germany"},
    {"question": "In 'The Twelve Days of Christmas', what is given on the 7th day?",
     "options": ["Swans a-Swimming", "Geese a-Laying", "Lords a-Leaping", "Pipers Piping"],
     "answer": "Swans a-Swimming"},
    {"question": "Which U.S. state was the first to declare Christmas a legal holiday?",
     "options": ["Alabama", "New York", "Texas", "California"], "answer": "Alabama"},
    {"question": "What is the name of Ebenezer Scrooge's deceased business partner?",
     "options": ["Jacob Marley", "Bob Cratchit", "Fred Scrooge", "Tiny Tim"], "answer": "Jacob Marley"},
    {"question": "What does 'X' in Xmas stand for?", "options": ["Christ", "Cross", "Star", "Gift"],
     "answer": "Christ"},
    {"question": "What popular Christmas song was originally written for Thanksgiving?",
     "options": ["Jingle Bells", "Silent Night", "Deck the Halls", "We Wish You a Merry Christmas"],
     "answer": "Jingle Bells"},
    {"question": "What is the most popular ornament for a Christmas tree top?",
     "options": ["Star", "Angel", "Santa", "Snowflake"], "answer": "Star"},
    {"question": "In the movie *Elf*, what is Buddy's favorite food?",
     "options": ["Candy", "Pizza", "Spaghetti", "Syrup"], "answer": "Syrup"},
    {"question": "In what year did Coca-Cola start using Santa Claus in advertisements?",
     "options": ["1931", "1920", "1950", "1905"], "answer": "1931"},
    {"question": "How many ghosts show up in *A Christmas Carol*?", "options": ["4", "3", "2", "1"], "answer": "4"}
]

# Template for rendering the quiz
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Christmas Quiz</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: #12232E; color: #ffffff; text-align: center; padding: 20px; }
        header, footer { background: #E63946; color: white; padding: 10px; position: fixed; width: 100%; z-index: 100; }
        header { top: 0; }
        footer { bottom: 0; }
        .quiz-container { max-width: 600px; margin: 60px auto 80px auto; padding: 20px; border: 1px solid #ccc; border-radius: 10px; background: rgba(255, 255, 255, 0.9); color: #333; box-shadow: 0 0 20px rgba(0, 0, 0, 0.2); }
        .question { margin-bottom: 20px; font-size: 1.5em; }
        .options label { display: block; margin-bottom: 10px; }
        .button { padding: 10px 20px; background: #E63946; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 1em; }
        .button:hover { background: #9d2c34; }
        .score { font-size: 1.2em; margin-top: 20px; }
        .restart { background: #457B9D; color: white; }
        .restart:hover { background: #2b5d77; }
        #snow { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; }
    </style>
</head>
<body>
    <header>
        Made by Jason Hoyle
    </header>
    <div id="snow"></div>
    <div class="quiz-container">
        {% if question %}
            <form method="post">
                <div class="question">
                    <h3>{{ question }}</h3>
                </div>
                <div class="options">
                    {% for option in options %}
                        <label>
                            <input type="radio" name="answer" value="{{ option }}" required>
                            {{ option }}
                        </label>
                    {% endfor %}
                </div>
                <button type="submit" class="button">Next</button>
            </form>
        {% elif result %}
            <h3>Your Score: {{ score }}/{{ total }}</h3>
            <p class="score">{{ "Great job!" if score >= total / 2 else "Better luck next time!" }}</p>
            <a href="{{ url_for('index') }}" class="button restart">Restart Quiz</a>
        {% endif %}
    </div>
    <footer>
        Thank you for playing! Happy Holidays!
    </footer>
    <!-- Snow animation -->
    <script>
        const snowContainer = document.getElementById('snow');
        for (let i = 0; i < 100; i++) {
            const snowflake = document.createElement('div');
            snowflake.style.position = 'absolute';
            snowflake.style.top = Math.random() * window.innerHeight + 'px';
            snowflake.style.left = Math.random() * window.innerWidth + 'px';
            snowflake.style.width = snowflake.style.height = Math.random() * 5 + 2 + 'px';
            snowflake.style.background = 'white';
            snowflake.style.borderRadius = '50%';
            snowflake.style.opacity = Math.random();
            snowflake.style.animation = `fall ${Math.random() * 3 + 2}s linear infinite`;
            snowContainer.appendChild(snowflake);
        }
        const style = document.createElement('style');
        style.innerHTML = `
            @keyframes fall {
                to { transform: translateY(100vh); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    </script>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        answer = request.form.get("answer")
        if answer == session['questions'][session['current_question']]["answer"]:
            session['score'] += 1
        session['current_question'] += 1

        if session['current_question'] >= len(session['questions']):
            # Quiz finished
            return render_template_string(
                TEMPLATE,
                result=True,
                score=session['score'],
                total=len(session['questions']),
            )

    # Start/restart the quiz
    if 'questions' not in session or session['current_question'] >= len(session['questions']):
        session['questions'] = random.sample(EASY_QUESTIONS, 5) + random.sample(HARD_QUESTIONS, 5)
        random.shuffle(session['questions'])
        session['current_question'] = 0
        session['score'] = 0

    current_q = session['questions'][session['current_question']]
    return render_template_string(
        TEMPLATE,
        question=current_q["question"],
        options=current_q["options"],
        result=False,
    )


if __name__ == "__main__":
    from flask import session

    app.secret_key = "your_secret_key"  # Replace with a strong secret key
    app.run(debug=True)