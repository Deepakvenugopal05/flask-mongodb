from flask import Flask
from endpoints.posts import post_bp

app = Flask(__name__)
app.register_blueprint(post_bp, url_prefix='/api/')

if __name__ == '__main__':
    app.run(debug=True)