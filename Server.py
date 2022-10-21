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

@app.route("/", methods=['GET', 'POST'])
def homepage():
    # 載入所有資料庫的影片資訊
    query = '''
    SELECT video_and_channel_id.Title, video_and_channel_id.video_id, video_keywords.video_keywords
    FROM   video_and_channel_id INNER JOIN
            video_keywords ON video_and_channel_id.id = video_keywords.uid
    '''
    result = db.engine.execute(query)
    return render_template('DemoHomepage.html', vc_id=result)


@app.route("/search=<keyword>", methods=['GET', 'POST'])
def search(keyword):
    # 搜尋結果以更新放置影片資訊的欄位呈現(篩選出有關鍵字的影片)
    # if 關鍵字 == 進行式 then 影片資訊的欄位只會出現關鍵字有進行式的影片
    # keywords 網站傳來的關鍵字
    bindingwords = "'%"+keyword+"%'"  # 字串串接
    query = '''
    SELECT video_and_channel_id.Title, video_and_channel_id.video_id, video_keywords.video_keywords FROM video_and_channel_id INNER JOIN video_keywords ON video_and_channel_id.id = video_keywords.uid WHERE video_and_channel_id.Title LIKE 
    '''+bindingwords+'''
    OR video_keywords.video_keywords LIKE
    '''+bindingwords
    result3 = db.engine.execute(query)
    # result = db.engine.execute(
    #     "SELECT * from video_and_channel_id WHERE Title LIKE '%規則%'")
    # result2 = db.engine.execute(
    #     "SELECT * from video_keywords WHERE title LIKE '%規則%'")
    return render_template('DemoHomepage.html', vc_id=result3)


if __name__ == "__main__":
    app.run(debug=True, port=7616)
