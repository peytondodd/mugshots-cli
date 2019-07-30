import main
from flask import Flask
from flask import send_file
from flask import jsonify
app = Flask(__name__)

@app.route("/mugshots/latest/<amount>")
def get_mugshots(amount):
    return jsonify(main.get_mugshots(int(amount)))

@app.route("/mugshots/total")
def get_total():
    count_file = open("./count.txt","r")
    count = int(count_file.readlines()[0]) + 1
    count_file.close()
    return str(count)


@app.route("/mugshots/image/<id>")
def get_image(id):
    return send_file("mugs/"+str(id) + ".jpg", mimetype="image/jpeg")

if __name__ == "__main__":
    app.run();
