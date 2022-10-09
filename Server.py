from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy.dialects.mssql import \
    BIGINT, BINARY, BIT, CHAR, DATE, DATETIME, DATETIME2, \
    DATETIMEOFFSET, DECIMAL, FLOAT, IMAGE, INTEGER, MONEY, \
    NCHAR, NTEXT, NUMERIC, NVARCHAR, REAL, SMALLDATETIME, \
    SMALLINT, SMALLMONEY, SQL_VARIANT, TEXT, TIME, \
    TIMESTAMP, TINYINT, UNIQUEIDENTIFIER, VARBINARY, VARCHAR
from sqlalchemy import Table, MetaData, Column, Integer, String, ForeignKey, INT, create_engine
from sqlalchemy.orm import mapper, sessionmaker
app = Flask(__name__)
# 連接資料庫
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DESKTOP-GPKL4Q4\SQLEXPRESS/Video_data?driver=SQL+Server'
db = SQLAlchemy(app)


class V_keywords(db.Model):
    __tablename__ = 'video_keywords'
    uid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(max))
    video_keywords = db.Column(db.String(max))
    db_keywords_id = db.relationship("VC_id", backref="video_keywords")

    def __init__(self, id, title, video_keywords):
        self.id = id
        self.title = title
        self.video_keywords = video_keywords


class VC_id(db.Model):
    __tablename__ = 'video_and_channel_id'
    id = db.Column(db.Integer, db.ForeignKey(
        'video_keywords.uid'), primary_key=True)
    Title = db.Column(db.String(max))
    video_id = db.Column(db.String(max))
    channel_id = db.Column(db.String(max))

    def __init__(self, Title, video_id, channel_id):
        self.Title = Title
        self.video_id = video_id
        self.channel_id = channel_id


# Session = sessionmaker()
# Session.configure(bind=db)
# session = Session()
# query = db.session.query(VC_id).all()
#     for i in query:
#         print(i.video_id)


@app.route("/", methods=['GET', 'POST'])
def homepage():

    return render_template("DemoHomepage.html", vc_id=VC_id.query.all(), v_keywords=V_keywords.query.all())


if __name__ == "__main__":
    app.run(debug=True, port=7616)
