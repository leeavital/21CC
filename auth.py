from flask import g

class User:
   
   def __init__(self, username, uid):
	  self.username = username
	  self.uid = uid

def log_user_in( username, password ):
   query = """SELECT COUNT(*) AS matched, name, id  FROM""" + \
	  """ users WHERE password=MD5("%s") AND name="%s";""" \
	  % (password, username)
   
   
   cur = g.db.cursor()
   
   cur.execute(query)
   
   
   match = cur.fetchone() 
   num_matches = match["matched"]
   matched_uname = match["name"]
   matched_id = match["id"]


   if num_matches == 0:
	  raise Exception("Bad Password")
   else:
	  return User( matched_uname, matched_id )
	  
   
    
   
       

