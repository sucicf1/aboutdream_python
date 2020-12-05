from settings import *
from datetime import *
import json
from followers import Follower
from sqlalchemy import Column, Integer, DateTime, asc, desc

ROWS_PER_PAGE = 5


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    image_name = db.Column(db.String(app.config["FILENAME_LENGTH"]), nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    user_id = db.Column("user_id", db.Integer(), db.ForeignKey("users.id"))

    def json(self):
        return {
            "id": self.id,
            "text": self.text,
            "image_name": self.image_name,
            "created_date": self.created_date,
            "user_id": self.user_id,
        }

    def __filterByDatePage(_query, _asc, _page, _start_date, _end_date):
        if _asc == False:
            _query = _query.order_by(desc(Message.created_date))
        else:
            _query = _query.order_by(asc(Message.created_date))
        if _start_date > 0:
            _start_date_utc = datetime.fromtimestamp(_start_date)
            _query = _query.filter(Message.created_date >= _start_date_utc)
        if _end_date > 0:
            _end_date_utc = datetime.fromtimestamp(_end_date)
            _query = _query.filter(Message.created_date <= _end_date_utc)
        if _page > 0:
            messages = _query.paginate(page=_page, per_page=ROWS_PER_PAGE).items
        else:
            messages = _query.all()
        return messages

    def add_message(_text, _image_name, _user_id):
        new_message = Message(text=_text, image_name=_image_name, user_id=_user_id)
        db.session.add(new_message)
        db.session.commit()

    def get_messages(_follower_id, _asc, _page, _start_date, _end_date):
        if not _follower_id:
            query = Message.query
        else:
            query = Message.query.join(Follower, 
                    Message.user_id == Follower.followee_id).filter(
                        Follower.follower_id == _follower_id)
        messages = Message.__filterByDatePage(query, 
                            _asc, _page, _start_date, _end_date)
        return [Message.json(message) for message in messages]