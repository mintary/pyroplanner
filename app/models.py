from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app import login
from datetime import datetime, timedelta

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    tasks: so.WriteOnlyMapped['Task'] = so.relationship(
        back_populates='author'
    ) 

    upcoming: so.Mapped[datetime] = so.mapped_column(
        index=True, nullable=True, default=lambda: datetime.now() + timedelta(hours=1)
    )

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000), nullable=True)
    deadline = db.Column(db.DateTime, nullable=True)
    weight_user = db.Column(db.Integer, nullable=True)
    complete = db.Column(db.Boolean, default=False)

    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(), nullable=True
    )

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True, nullable=True)

    author: so.Mapped[User] = so.relationship(back_populates='tasks')

    def __repr__(self):
        return '<Task {}>'.format(self.title)
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
