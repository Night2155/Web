from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from matplotlib.pyplot import title
from requests import request
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


class V_keywords(db.Model):
    __tablename__ = 'video_keywords'
    uid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(max))
    video_keywords = db.Column(db.String(max))
    # 關聯 id
    db_keywords_id = db.relationship("VC_id", backref="video_keywords")

    def __init__(self, id, title, video_keywords):
        self.id = id
        self.title = title
        self.video_keywords = video_keywords


class VC_id(db.Model):
    __tablename__ = 'video_and_channel_id'
    id = db.Column(db.Integer, db.ForeignKey(
        'video_keywords.uid'), primary_key=True)
    Title = db.Column(db.String(max), primary_key=True)
    video_id = db.Column(db.String(max), primary_key=True)
    channel_id = db.Column(db.String(max), primary_key=True)

    def __init__(self, Title, video_id, channel_id):
        self.Title = Title
        self.video_id = video_id
        self.channel_id = channel_id


@app.route('/', methods=['GET', 'POST'])
def home():
    query = '''
    SELECT video_and_channel_id.Title, video_and_channel_id.video_id, video_keywords.video_keywords
    FROM   video_and_channel_id INNER JOIN
            video_keywords ON video_and_channel_id.id = video_keywords.uid
    '''
    result = db.engine.execute(query)
    return render_template('show_data.html', vc_id=result)


@app.route("/search=<keyword>", methods=['GET', 'POST'])
def search(keyword):
    # 搜尋結果以更新放置影片資訊的欄位呈現(篩選出有關鍵字的影片)
    # if 關鍵字 == 進行式 then 影片資訊的欄位只會出現關鍵字有進行式的影片
    # keywords 網站傳來的關鍵字
    if(len(keyword) > 0):
        bindingwords = "'%"+keyword+"%'"  # 字串串接
        query = '''
        SELECT video_and_channel_id.Title, video_and_channel_id.video_id, video_keywords.video_keywords FROM video_and_channel_id INNER JOIN video_keywords ON video_and_channel_id.id = video_keywords.uid WHERE video_and_channel_id.Title LIKE 
        '''+bindingwords+'''
        OR video_keywords.video_keywords LIKE
        '''+bindingwords
    elif(len(keyword) == 0):
        query = '''
        SELECT video_and_channel_id.Title, video_and_channel_id.video_id, video_keywords.video_keywords
        FROM   video_and_channel_id INNER JOIN
                video_keywords ON video_and_channel_id.id = video_keywords.uid
        '''
    result = db.engine.execute(query)
    # result = db.engine.execute(
    #     "SELECT * from video_and_channel_id WHERE Title LIKE '%規則%'")
    # result2 = db.engine.execute(
    #     "SELECT * from video_keywords WHERE title LIKE '%規則%'")
    return render_template('show_data.html', vc_id=result)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
