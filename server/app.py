from flask import Flask

app = Flask(__name__)

@app.route('/')
def main():
    return """
        <!DOCTYPE HTML>
        <html>
            <head>
                <title>I love you</title>
            </head>
            <body>
                <h1>아빠 사랑해영</h1>
            </body>
        </html>
        """

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)

