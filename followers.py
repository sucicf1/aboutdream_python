from settings import *
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer

class Follower(db.Model):
    __tablename__ = "followers"
    follower_id = Column(Integer, db.ForeignKey('users.id', ondelete='CASCADE'), 
                        nullable=False, primary_key=True)
    followee_id = Column(Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True)
    follower = relationship("User", foreign_keys=[follower_id], passive_deletes=True)
    followee = relationship("User", foreign_keys=[followee_id])

    def add(_follower_id, _followee_id):
        new_ff = Follower(
            follower_id =_follower_id,
            followee_id =_followee_id,
        )
        db.session.add(new_ff)
        db.session.commit()
        return new_ff

    def delete(_follower_id, _followee_id):
        Follower.query.filter_by(
            follower_id = _follower_id,
            followee_id = _followee_id).delete()
        db.session.commit()
