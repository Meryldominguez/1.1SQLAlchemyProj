from flask_sqlalchemy import SQLAlchemy

class User(db.Model):
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False)
    last_name = db.Column(db.String(50),
                     nullable=False)
    image_url = db.Column(db.String(30), nullable=False)
    
    def get_full_name(self):
        return self.first_name+self.last_name
    

    