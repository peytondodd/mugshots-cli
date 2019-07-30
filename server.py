import main
from flask import Flask
from flask import send_file
app = Flask(__name__)

@app.route("/mugshots/info/<amount>")
def get_mugshots(amount):
    return str(main.get_mugshots(int(amount)))

@app.route("/mugshots/image/<id>")
def get_image(id):
    return send_file("mugs/"+str(id) + ".jpg", mimetype="image/jpeg")

if __name__ == "__main__":
    app.run();
