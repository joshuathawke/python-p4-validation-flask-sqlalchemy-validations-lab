from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String(10))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, value):
        if not value:
            raise ValueError('Name is required')
        return value

    @validates('phone_number')
    def validate_phone_number(self, key, value):
        if value and len(value) != 10:
            raise ValueError('Phone number must be exactly 10 digits')
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def validate_title(self, key, value):
        if not value:
            raise ValueError('Title is required')
        if not any(clickbait_word in value for clickbait_word in ['Won\'t Believe', 'Secret', 'Top', 'Guess']):
            raise ValueError('Title is not clickbait-y enough')
        return value
    
    
    
    @validates('content')
    def validate_content(self, key, value):
        if value and len(value) < 250:
            raise ValueError('Content must be at least 250 characters')
        return value

    @validates('summary')
    def validate_summary(self, key, value):
        if value and len(value) <= 250:
            raise ValueError('Summary must be at most 250 characters')
        return value

    @validates('category')
    def validate_category(self, key, value):
        if value not in ('Fiction', 'Non-Fiction'):
            raise ValueError('Category must be either Fiction or Non-Fiction')
        return value
    
    

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'
