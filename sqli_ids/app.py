import string
import hashlib
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import math
from rules import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ids.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

DROP_THRESHOLD = 4

class Blacklist(db.Model) :

	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	ip = db.Column(db.String(20), nullable = False)
	count = db.Column(db.Integer, nullable = False, default=1)
	avg_score = db.Column(db.Integer, nullable = False, default=1)
	threshhold = db.Column(db.Integer, nullable = False)
	attacks = db.relationship('Injections', lazy=True)

	def __repr__(self):
		return '( ID: ' + str(self.id) + ' IP: ' + self.ip + ' Count: ' + str(self.count) + ' Avg.Score: ' + str(self.avg_score) + ' Threshhold: ' + str(self.threshhold) + ' )'


class Injections(db.Model):

	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	score = db.Column(db.Integer, nullable = False)
	attacker_id = db.Column(db.Integer, db.ForeignKey('blacklist.id'), nullable = False)

	def __repr__(self):
		return '( ID: ' + str(self.id) + ' IP: ' + str(self.attacker_id) + ' Score: ' + str(self.score) + ' )'


def set_threshhold(current_score):
	if(current_score >= 10):
		return 0
	if(current_score >= 9):
		return 1
	if(current_score >= 7):
		return 2
	if(current_score >= 5):
		return 3
	if(current_score >= 4):
		return 4


def update_drop_threshhold():
	injection = Injections.query.all()
	total = 0
	for i in range(len(injection)):
		total = total + injection[i].score
	avg = (int)(math.ceil((float)(total)/len(injection)))
	DROP_THRESHOLD = set_threshhold(avg)
	print("Updated Drop Threshhold: " + str(DROP_THRESHOLD))


@app.route('/answer/', methods=['POST', 'GET'])
def func():
	print(request.json)
	if request.json:
		User = request.json['user']
		Pass = request.json['pass']
		ip = request.json['ip']
		# admin = "admin"
		# admin = hashlib.md5(admin.encode())
		# admin = admin.hexdigest()
		# if admin in User:
		# 	print("The string contains admin")
		# orl = "or"
		# orl = hashlib.md5(orl.encode())
		# orl = orl.hexdigest()
		# if orl in User:
		# 	print("The string contains or")
		# 	print(orl)
		char_score_user = int(request.json['user_score'])
		char_score_pass = int(request.json['pass_score'])
		score = max(calculate_score_hex(User, char_score_user), calculate_score_hex(Pass, char_score_pass))
		exist = Blacklist.query.filter_by(ip=ip).first()
		level = score - DROP_THRESHOLD + 1
		if exist:
			level = score - exist.threshhold + 1
		isAttacked = False
		if(level > 0):
			isAttacked = True
		if exist:
			if isAttacked:
				print("Attack Detected!! ")
				if(exist.count == 5):
					injection = Injections.query.filter_by(attacker_id=exist.id).first()
					if injection:
						injection.score = exist.avg_score
						db.session.commit()
					else:
						injection = Injections(score=exist.avg_score, attacker_id=exist.id)
						db.session.add(injection)
						db.session.commit()
					exist.count = 1
					update_drop_threshhold()
				exist.avg_score = (int)(math.ceil((float)(exist.avg_score*exist.count + score)/(exist.count + 1)))
				exist.count = exist.count + 1
				exist.threshhold = set_threshhold(exist.avg_score)
				db.session.commit()
				print(exist)
				print("IP has already been blacklisted, and site has been Attacked!!\n")
				return jsonify({'ACK' : 'SUCCESS', 'attack':'true'})
			print("IP has already been blacklisted, but site has NOT been attacked!!\n")
			print(exist)
			return jsonify({'ACK' : 'SUCCESS', 'attack':'false'})
		elif (not exist) and isAttacked:
			print("Site has been attacked, but IP has not been blacklisted yet!!\n")
			exist = Blacklist(ip=ip, count=1, avg_score=score, threshhold=DROP_THRESHOLD)
			db.session.add(exist)
			db.session.commit()
			print(exist)
			return jsonify({'ACK' : 'SUCCESS', 'attack':'true'})
		else:
			print("Attack not detected!!\n")
			return jsonify({'ACK' : 'SUCCESS', 'attack':'false'})
	else:
		return jsonify({'ACK': 'FAILURE'})


if __name__ == '__main__':
	app.run(host='localhost',port=8000, debug=True)
