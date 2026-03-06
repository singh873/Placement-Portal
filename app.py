from flask import Flask
from application.database import db

app=None

def create_app():
    app=Flask(__name__)
    app.debug=True
    app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///placement_portal.sqlite3"
    db.init_app(app)
    app.app_context().push()
    return app

app=create_app()
from application.controllers import *



if __name__ == "__main__":

    with app.app_context():

        # create tables
        db.create_all()

        # check if admin exists
        admin = User.query.filter_by(email="sudhanshu@gmail.com").first()

        if admin is None:
            admin = User( full_name="Admin",email="sudhanshu@gmail.com",password="1234",type="admin" )
            
            db.session.add(admin)
            db.session.commit()

    app.run(debug=True)
