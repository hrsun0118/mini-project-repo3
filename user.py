from flask_login import UserMixin

from db import get_db

class User(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
    
    @staticmethod
    def add_sensor(sensor_id, user_id, s_nm, s_type):
        db = get_db()
        db.execute(
            'INSERT INTO sensors (sensor_id, user_id, sensor_name, sensor_type)  VALUES (?,?,?,?)',
            (sensor_id, user_id, s_nm, s_type),
        )
        db.commit()
    
    @staticmethod
    def get_sensors(user_id):
        db = get_db()
        sensors = db.execute("SELECT * FROM sensors WHERE user_id = ?", (user_id,)).fetchall()
        return sensors
    
    @staticmethod
    def get(user_id):
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if not user:
            return None
                          
        user = User(
                    id_=user[0], name=user[1], email=user[2], profile_pic=user[3]
                    )
        return user

    @staticmethod
    def create(id_, name, email, profile_pic):
        db = get_db()
        db.execute(
                   "INSERT INTO users (id, name, email, profile_pic) "
                   "VALUES (?, ?, ?, ?)",
                   (id_, name, email, profile_pic),
                   )
        db.commit()

    @staticmethod
    def list():
        db = get_db()
        user_list = db.execute("SELECT * FROM users").fetchall()
        return user_list

