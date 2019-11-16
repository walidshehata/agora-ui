from . import db, login_manager


class User(db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(40), primary_key=True)
    # first_name = db.Column(db.String(40))
    # last_name = db.Column(db.String(40))
    display_name = db.Column(db.String(60))
    tenant_id = db.Column(db.String(16), default=None)
    tenant_uuid = db.Column(db.String(36), default=None)
    api_key = db.Column(db.String(256), default=None)

    def is_active(self):
        if self.api_key:
            return True
        else:
            return False

    def get_id(self):
        return self.username

    def is_authenticated(self):
        if self.api_key:
            return True
        else:
            return False

    def is_anonymous(self):
        return False


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(username=user_id).first()
    return user

