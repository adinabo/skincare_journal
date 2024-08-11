from skincare_package import db


class SkinType(db.Model):
    # schema for the SkinType model
    id = db.Column(db.Integer, primary_key=True)
    skin_type = db.Column(db.String(25), unique=True, nullable=False)
    routines = db.relationship("Routine", backref="skin_type", cascade="all, delete", lazy=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.skin_type


class users_routines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    routine_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    skin_type_id = db.Column(db.Integer, db.ForeignKey("skin_type.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Routine: {1}".format(self.id, self.routine_name)