from flask import Flask, render_template
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


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DESKTOP-GPKL4Q4\SQLEXPRESS/Video_data?driver=SQL+Server'
db = SQLAlchemy(app)


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


@app.route('/')
def home():
    return render_template('show_all.html', vc_id=VC_id.query.all())


if __name__ == "__main__":
    app.run(port=5000, debug=True)
