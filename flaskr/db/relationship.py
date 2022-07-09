from flaskr.db.base import Base, database
from flaskr.db.user import User
from peewee import *

class Relationship(Base):
  from_user = ForeignKeyField(User)
  to_user = ForeignKeyField(User)

  @classmethod
  def create_relationship(cls, from_user: User, to_user: User):
    try:
      with database.atomic():
        relationship = (Relationship
          .create(
            from_user=from_user,
            to_user=to_user
          )
        )
    except IntegrityError:
      relationship = None
    return relationship


  @classmethod
  def get_relationship(cls, from_user: User, to_user: User):
    try:
      with database.atomic():
        relationship = (Relationship
          .select()
          .where(
            ((Relationship.from_user == from_user) & (Relationship.to_user == to_user))
            |
            ((Relationship.from_user == to_user) & (Relationship.to_user == from_user))
          )
        )
    except Relationship.DoesNotExist:
      relationship = None
    return relationship

  @classmethod
  def get_relationships(cls, user: User):
    try:
      with database.atomic():
        relationships = (Relationship
        .select()
        .where(
          (Relationship.to_user == user)
          |
          (Relationship.from_user == user)
        ))
    except Relationship.DoesNotExist:
      relationships = None
    return relationships

  @classmethod
  def get_relationships_by_user(cls, user: User):
    try:
      with database.atomic():
        relationships = (Relationship
        .select()
        .where(
          Relationship.to_user == user
        ))
    except Relationship.DoesNotExist:
      relationships = None
    return relationships


  @classmethod
  def __get_relationship_template(cls, bool_statement: bool):
    try:
      with database.atomic():
        relationships = (Relationship
        .select()
        )
    except Relationship.DoesNotExist:
      relationships = None
    return relationships