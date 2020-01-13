from . import db, login_manager


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(40), primary_key=True)
    display_name = db.Column(db.String(60), default=None)
    api_key = db.Column(db.String(256), default=None)
    mail = db.Column(db.String(60), default=None)
    company = db.Column(db.String(60), default=None)
    mobile = db.Column(db.String(60), default=None)

    def is_active(self):
        if self.api_key:
            return True
        else:
            return False

    def get_id(self):
        return self.id

    def is_authenticated(self):
        if self.api_key:
            return True
        else:
            return False

    @staticmethod
    def is_anonymous():
        return False

    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        user = User.query.filter_by(id=user_id).first()
        return user


