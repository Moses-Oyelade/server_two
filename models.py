from extensions import db
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash


user_organisation = db.Table(
        'user_organisation',
        db.Column('user_id', db.String(), db.ForeignKey("users.userId")),
        db.Column('organisation_id', db.String(), db.ForeignKey('organisations.orgId'))
    )


class User(db.Model):
    __tablename__ = 'users'
    
    userId = db.Column(db.String(), primary_key=True, unique=True, default = str(uuid4()) )
    firstName = db.Column(db.String(), nullable=False)
    lastName = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    phone = db.Column(db.String())
    
    organisation = db.relationship('Organisation', secondary = user_organisation, backref='users')
    
    def __repr__(self):
        return f"<User {self.firstName} {self.lastName}>"
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
        
    @classmethod
    def get_user_by_username(cls,email):
        return cls.query.filter_by(email =email).first()
    
    def get_user_by_userId(cls, userId):
        return cls.query.filter_by(userId = userId).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
        
class Organisation(db.Model):
    __tablename__ = 'organisations'
    
    orgId = db.Column(db.String(), primary_key=True, unique=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    
    user = db.relationship('User', secondary = user_organisation, backref='organisations')
    
    def __repr__(self):
        return f"<Organisation {self.name} title {self.description}>"
    
    def organisation_by_orgId(cls, orgId):
        return cls.query.filter_by(orgId = orgId).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    