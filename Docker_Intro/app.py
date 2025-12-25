from flask import Flask

'''
It creates an instance of the Flask Class, which will be our WSGI application.
'''
app = Flask(__name__)

@app.route("/")  # URL Routing
def home():
    return "Hello Flask!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
