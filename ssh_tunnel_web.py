from flask import Flask, g, render_template, request, redirect
import redis, json

app = Flask(__name__)

def get_redis():
	_redis = getattr(g, "_redis", None)
	if _redis is None:
		_redis = g._redis = redis.StrictRedis(host="127.0.0.1", port=6379)
	return _redis

@app.route("/", methods=["GET", "POST"])
def index():
	conn = get_redis()
	data = conn.get("ssh-tunnel")
	if data is None:
		data = "{}"
	data = json.loads(data)

	if request.method == "POST":
		try:
			if int(request.form["ex_port"]) > 65536 or int(request.form["in_port"]) > 65536 or request.form["in_ip"].count('.') != 3 or len(request.form["ex_port"]) == 0 or len(request.form["in_port"]) == 0 or len(request.form["in_ip"]) == 0:
				return redirect("/")
		except:
			return redirect("/")

		data[request.form["ex_port"]] = {"in_i": request.form["in_ip"], "in_p": request.form["in_port"], "memo": request.form["memo"]}
		conn.set("ssh-tunnel", json.dumps(data))

	return render_template("index.html", data=data)

@app.route("/d/<ex_p>")
def delete(ex_p):
	conn = get_redis()
	data = conn.get("ssh-tunnel")
	if data is None:
		data = "{}"
	data = json.loads(data)

	try:
		del data[ex_p]
		conn.set("ssh-tunnel", json.dumps(data))
	except:
		pass

	return redirect("/")

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)