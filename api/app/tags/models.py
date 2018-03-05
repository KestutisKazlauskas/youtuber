from app import db


class Tag(db.Model):
    """Class for youtube video tags table"""

    __tablename__ = 'tag'
    __table_args__ = (
        db.Index(
            'tag_name',  # Index name
            'name',
            unique=True
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    @property
    def serialize(self):
        """Method for makings json serializable object"""
        return {
            'id': self.id,
            'name': self.name
        }