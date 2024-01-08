from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class User(db.Model):
    # Fields are assigned a type using Python type hints (using ":"), wrapped with SQLAlchemy's so.Mapped generic type.
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(                    # so.relationship to connect to Post DB
    back_populates='author')                                                # back_populates arguments reference the name of the relationship attribute on the other side
                                                                            # Instead of so.Mapped, we use so.WriteOnlyMapped, which defines posts as a collection type with Post objects inside
    def __repr__(self):
        return f'<User {self.username}>'
    

class Post(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id),
                                               index=True)

    author: so.Mapped[User] = so.relationship(back_populates='posts')       # so.relationship to connect to User DB

    def __repr__(self):
        return '<Post {}>'.format(self.body)