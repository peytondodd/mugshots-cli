import main
from flask import Flask
from flask import send_file
from flask import jsonify
app = Flask(__name__)

@app.route("/mugshots/latest/<amount>")
def get_mugshots(amount):
    mugs = main.get_mugshots(int(amount))
    return jsonify(mugs)

@app.route("/mugshots/total")
def get_total():
    count_file = open("./count.txt","r")
    count = int(count_file.readlines()[0]) + 1
    count_file.close()
    return str(count)

@app.route("/mugshots/image/<id>")
def get_image(id):
    return send_file("mugs/"+str(id) + ".jpg", mimetype="image/jpeg")

@app.route("/")
def home():
    return "<h1>Welcome to the Mugshots API</h1><p> Quickly fetch south eastern North Carolina crime stats </p><h3> GET <a href='/mugshots/latest/10'>/mugshots/latest/:count</a> </h3><h3>GET <a href='/mugshots/total'>/mugshots/total</a> </h3><h3>GET <a href='/mugshots/image/221681'>/mugshots/image/:id</a></h3>"

if __name__ == "__main__":
    app.run();
