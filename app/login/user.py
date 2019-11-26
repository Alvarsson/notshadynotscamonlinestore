from flask_login import UserMixin
from app import bcrypt
from app import db
from app import login_manager

class User(UserMixin):

    def __init__(self,
                 user_id=None,
                 first_name=None,
                 last_name=None,
                 username=None,
                 password=None,
                 mail=None,
                 address=None):

        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.mail = mail
        self.address = address

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    @staticmethod
    def get_user(user_id=None, username=None, mail=None):
        if user_id:
            q = "customer_id"
            p = user_id
        elif username:
            q = "user_name"
            p = username
        elif mail:
            q = 'mail'
            p = mail
        else:
            return None

        cur = db.connection.cursor()
        cur.execute("""SELECT customer_id, first_name, last_name,
                    user_name, password, mail, adress
                    FROM users WHERE """ + q + " = %s", (p,))
        res = cur.fetchone()

        if not res:
            return None
        return User(res[0], res[1], res[2], res[3], res[4], res[5], res[6])

    def commit(self):
        cur = db.connection.cursor()
        cur.execute("""INSERT INTO users
                    (`first_name`,
                    `last_name`,
                    `user_name`,
                    `password`,
                    `mail`,
                    `adress`) VALUES
                    (%(first_name)s,
                    %(last_name)s,
                    %(username)s,
                    %(password)s,
                    %(mail)s,
                    %(address)s)
                    ON DUPLICATE KEY UPDATE
                    first_name = %(first_name)s,
                    last_name = %(last_name)s,
                    user_name = %(username)s,
                    password = %(password)s,
                    mail = %(mail)s,
                    adress = %(address)s
                    """, self.to_dict())
        db.connection.commit()

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {'user_id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'username': self.username,
                'password': self.password,
                'mail': self.mail,
                'address': self.address}


@login_manager.user_loader
def load_user(id):
    return User.get_user(user_id=int(id))
