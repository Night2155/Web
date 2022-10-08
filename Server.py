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

# 標題、影片ID、頻道ID的資料表
# vc_id_metadata = MetaData()
# vc_id = Table('video_and_channel_id', vc_id_metadata,
#               Column('id', INT, primary_key=True),
#               Column('Title', NVARCHAR(max)),
#               Column('video_id', NVARCHAR(max)),
#               Column('channel_id', NVARCHAR(max))
#               )


class VC_id(db.Model):
    __tablename__ = 'video_and_channel_id'
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(max), primary_key=True)
    video_id = db.Column(db.String(max), primary_key=True)
    channel_id = db.Column(db.String(max), primary_key=True)

    def __init__(self, id, Title, video_id, channel_id):
        self.id = id
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
    return render_template("DemoHomepage.html")
    # query = VC_id.query.filter_by(id="5").first()
    # return query.Title


if __name__ == "__main__":
    app.run(debug=True, port=7616)
