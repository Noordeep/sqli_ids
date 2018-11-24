from app import db
from app import Blacklist, Injections
import sys
first_arg = sys.argv[1]

obj = Blacklist.query.filter_by(ip=first_arg).first()
if obj:
	inj = Injections.query.filter_by(attacker_id=obj.id).first()
	if inj:
		db.session.delete(inj)
	db.session.delete(obj)
	print("Entry Deleted!!")
else:
	print("Entry not found!!")
db.session.commit()