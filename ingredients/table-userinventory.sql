USE prod;

CREATE TABLE userinventory(
   
   uid INT NOT NULL REFERENCES users(id),
   item VARCHAR(255)
   


);
