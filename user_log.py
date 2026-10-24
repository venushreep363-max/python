
from flask import Flask, request, render_template_string

app = Flask(__name__)

inbuilt_user_name = "venushree"
inbuilt_user_password = "venushree123"

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Animated Login Page</title>

    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', sans-serif;
        }

        body {
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            background: linear-gradient(135deg, #10152f, #34246b, #7541a8);
            padding: 20px;
        }

        /* Animated background circles */
        .bubble {
            position: absolute;
            border-radius: 50%;
            filter: blur(2px);
            animation: float 7s ease-in-out infinite;
        }

        .bubble.one {
            width: 220px;
            height: 220px;
            background: #ff75b5;
            top: -70px;
            left: -60px;
            opacity: 0.45;
        }

        .bubble.two {
            width: 280px;
            height: 280px;
            background: #5ce1e6;
            bottom: -100px;
            right: -70px;
            opacity: 0.3;
            animation-delay: 2s;
        }

        .bubble.three {
            width: 100px;
            height: 100px;
            background: #b9a0ff;
            top: 20%;
            right: 15%;
            opacity: 0.5;
            animation-delay: 1s;
        }

        @keyframes float {
            0%, 100% {
                transform: translateY(0) rotate(0deg);
            }
            50% {
                transform: translateY(-30px) rotate(15deg);
            }
        }

        /* Main login container */
        .container {
            position: relative;
            z-index: 1;
            width: 900px;
            max-width: 100%;
            min-height: 520px;
            display: flex;
            border: 1px solid rgba(255,255,255,0.25);
            border-radius: 25px;
            overflow: hidden;
            background: rgba(255,255,255,0.10);
            backdrop-filter: blur(18px);
            box-shadow: 0 25px 70px rgba(0,0,0,0.35);
            animation: appear 0.9s ease;
        }

        @keyframes appear {
            from {
                opacity: 0;
                transform: translateY(25px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Left design section */
        .left-panel {
            flex: 1;
            padding: 45px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            color: white;
            background: linear-gradient(
                145deg,
                rgba(255,255,255,0.13),
                rgba(255,255,255,0.02)
            );
        }

        .art {
            width: 190px;
            height: 190px;
            border-radius: 50%;
            background: linear-gradient(135deg, #ff8bc4, #a68aff);
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 95px;
            box-shadow: 0 0 45px rgba(255,139,196,0.35);
            animation: bounce 3s ease-in-out infinite;
            margin-bottom: 30px;
        }

        @keyframes bounce {
            0%, 100% {
                transform: translateY(0);
            }
            50% {
                transform: translateY(-15px);
            }
        }

        .left-panel h1 {
            font-size: 30px;
            margin-bottom: 12px;
        }

        .left-panel p {
            font-size: 15px;
            line-height: 1.7;
            color: #e4ddff;
        }

        /* Right login section */
        .right-panel {
            flex: 1;
            padding: 55px 45px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            color: white;
        }

        .right-panel h2 {
            font-size: 32px;
            margin-bottom: 10px;
        }

        .subtitle {
            color: #d5cbed;
            margin-bottom: 30px;
            font-size: 14px;
        }

        .input-group {
            margin-bottom: 22px;
        }

        .input-group label {
            display: block;
            margin-bottom: 9px;
            font-size: 14px;
        }

        .input-group input {
            width: 100%;
            padding: 15px;
            border-radius: 12px;
            outline: none;
            border: 1px solid rgba(255,255,255,0.3);
            background: rgba(255,255,255,0.09);
            color: white;
            font-size: 15px;
            transition: 0.3s;
        }

        .input-group input::placeholder {
            color: #c6bcdf;
        }

        .input-group input:focus {
            border-color: #ff91ca;
            box-shadow: 0 0 12px rgba(255,145,202,0.25);
        }

        .login-btn {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 12px;
            background: linear-gradient(90deg, #ff70b7, #a879ff);
            color: white;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }

        .login-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 25px rgba(255,112,183,0.35);
        }

        .message {
            margin-top: 20px;
            padding: 12px;
            border-radius: 10px;
            text-align: center;
            font-size: 14px;
            animation: appear 0.4s ease;
        }

        .success {
            background: rgba(45, 220, 150, 0.18);
            border: 1px solid #52e5ad;
            color: #a8ffda;
        }

        .error {
            background: rgba(255, 75, 100, 0.18);
            border: 1px solid #ff7b90;
            color: #ffc0ca;
        }

        .footer {
            text-align: center;
            margin-top: 25px;
            color: #c6bcdf;
            font-size: 12px;
        }

        @media (max-width: 650px) {
            body {
                overflow-y: auto;
            }

            .container {
                flex-direction: column;
                margin: 10px 0;
            }

            .left-panel {
                padding: 30px 20px;
            }

            .art {
                width: 110px;
                height: 110px;
                font-size: 55px;
                margin-bottom: 20px;
            }

            .left-panel h1 {
                font-size: 24px;
            }

            .right-panel {
                padding: 35px 25px;
            }
        }
    </style>
</head>

<body>

    <div class="bubble one"></div>
    <div class="bubble two"></div>
    <div class="bubble three"></div>

    <div class="container">

        <div class="left-panel">
            <div class="art">👩🏻‍💻</div>
            <h1>Welcome Back!</h1>
            <p>
                Your next chapter starts here.<br>
                Sign in and continue your journey.
            </p>
        </div>

        <div class="right-panel">
            <h2>Login</h2>
            <p class="subtitle">Enter your details to access your account.</p>

            <form method="POST">

                <div class="input-group">
                    <label for="username">Username</label>
                    <input
                        type="text"
                        id="username"
                        name="username"
                        placeholder="Enter your username"
                        autocomplete="username"
                        required>
                </div>

                <div class="input-group">
                    <label for="password">Password</label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        placeholder="Enter your password"
                        autocomplete="current-password"
                        required>
                </div>

                <button type="submit" class="login-btn">
                    Sign In →
                </button>

            </form>

            {% if message %}
                <div class="message {{ status }}">
                    {{ message }}
                </div>
            {% endif %}

            <div class="footer">
                ✦ Your journey, your possibilities ✦
            </div>
        </div>

    </div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    status = ""

    if request.method == "POST":
        user_name = request.form.get("username", "")
        user_password = request.form.get("password", "")

        if (user_name == inbuilt_user_name and
                user_password == inbuilt_user_password):
            message = "Login successful! Welcome, Venushree!"
            status = "success"
        else:
            message = "Invalid username or password."
            status = "error"

    return render_template_string(
        HTML,
        message=message,
        status=status
    )


if __name__ == "__main__":
    app.run(debug=True)
