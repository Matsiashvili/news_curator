from ..extensions import db


class BaseService:
    """
    Generic CRUD service meant to be subclassed.

    Subclasses set `model` to the SQLAlchemy model they operate on and
    inherit basic create/read/delete behaviour, then add their own
    domain-specific methods on top (see NewsService).
    """

    model = None  # must be overridden by subclasses

    @classmethod
    def get_by_id(cls, item_id):
        if cls.model is None:
            raise NotImplementedError("Subclasses must set `model`.")
        return cls.model.query.get(item_id)

    @classmethod
    def get_all(cls):
        return cls.model.query.all()

    @classmethod
    def create(cls, **kwargs):
        instance = cls.model(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def delete(cls, instance) -> None:
        db.session.delete(instance)
        db.session.commit()
