from app.extensions import db
from app.models import ReadingList


class ReadingListService:


    DEFAULT_LIST_NAME = "Saved Articles"

    @staticmethod
    def get_user_list(user_id, list_id):
  

        if list_id is None:
            return None

        return ReadingList.query.filter_by(
            id=list_id,
            user_id=user_id
        ).first()

    @classmethod
    def get_or_create_default_list(cls, user_id):
  

        reading_list = ReadingList.query.filter_by(
            user_id=user_id,
            name=cls.DEFAULT_LIST_NAME
        ).first()

        if reading_list is None:
            reading_list = ReadingList(
                user_id=user_id,
                name=cls.DEFAULT_LIST_NAME
            )

            db.session.add(reading_list)
            db.session.commit()

        return reading_list