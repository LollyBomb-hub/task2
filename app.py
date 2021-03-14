from flask import Flask, redirect, url_for, request

app = Flask(__name__)

N = 10
id = 1

class Note:
	def __init__(self, *args):
		self.id = id
		if len(args) == 1:
			self.content = args[0]
			self.title = args[0][:N]
		elif len(args) > 1:
			self.title, self.content = args

	def send_back(self):
		return {"id": self.id, "title": self.title, "content": self.content}

notes_list = []
notes_back_list = []

@app.route('/notes', methods = ['POST', 'GET'])
def notes():
	if request.method == 'POST':
		data = request.get_json()
		try:
			if "title" in data.keys():
				notes_list.append(Note(data["title"], data["content"]))
				notes_back_list.append(notes_list[-1].send_back())
				id += 1
			return notes_back_list[-1]
		except:
			return 500
	else:
		query = request.args.get("query")
		if len(query):
			res = []
			for i in notes_list:
				if query in i.title or query in i.content:
					res.append(i.send_back())
			return str(res),200
		return str(notes_back_list), 200

@app.route('/notes/<cid>', methods = ['GET','PUT','DELETE'])
def get_note(cid=-1):
	try:
		cid = int(cid)
	except:
		return 404
	if cid <= 0 or cid >= len(notes_list):
		return "<h1>No notes with such index</h1>", 404
	if request.method == 'GET':
		return notes_back_list[cid-1]
	elif request.method == 'PUT':
		data = request.get_json()
		if "title" in data.keys():
			notes_list[cid].title = data["title"]
		if "content" in data.keys():
			notes_list[cid].content = data["content"]
		return 200
	elif request.method == 'DELETE':
		notes_list.pop(cid)
		notes_back_list.pop(cid)
		return 200


if __name__ == "__main__":
	app.run()
