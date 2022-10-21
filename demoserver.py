from ast import keyword
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from matplotlib.pyplot import title

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


@app.route('/', methods=['GET', 'POST'])
def home():
    grammer_query = '''
    SELECT  Grammer_id_table.Grammer_title, Grammer_id_table.Grammer_video_id,Grammer_keywords_table.Grammer_keywords                  
    FROM    Grammer_id_table INNER JOIN
            Grammer_keywords_table ON Grammer_id_table.Grammer_id = Grammer_keywords_table.Grammer_uid
    '''
    grammer_result = db.engine.execute(grammer_query)
    return render_template('show_all_data.html', grammer=grammer_result)


@app.route('/search', methods=['POST', 'GET'])
def submit():
    # 搜尋結果以更新放置影片資訊的欄位呈現(篩選出有關鍵字的影片)
    # if 關鍵字 == 進行式 then 影片資訊的欄位只會出現關鍵字有進行式的影片
    # keywords 網站傳來的關鍵字
    if request.method == 'POST':
        keyword = request.form['search_bar']
    if(len(keyword) > 0):
        bindingwords = "'%"+keyword+"%'"  # 字串串接
        query = '''
        SELECT Grammer_id_table.Grammer_title, Grammer_id_table.Grammer_video_id,Grammer_keywords_table.Grammer_keywords
        FROM Grammer_id_table INNER JOIN 
             Grammer_keywords_table ON Grammer_id_table.Grammer_id = Grammer_keywords_table.Grammer_uid
             WHERE Grammer_id_table.Grammer_title LIKE '''+bindingwords+''' OR Grammer_keywords_table.Grammer_keywords LIKE '''+bindingwords
    elif(len(keyword) == 0):
        query = '''
        SELECT  Grammer_id_table.Grammer_title, Grammer_id_table.Grammer_video_id,Grammer_keywords_table.Grammer_keywords                  
        FROM    Grammer_id_table INNER JOIN
                Grammer_keywords_table ON Grammer_id_table.Grammer_id = Grammer_keywords_table.Grammer_uid
        '''
    grammer_result = db.engine.execute(query)
    # result = db.engine.execute(
    #     "SELECT * from video_and_channel_id WHERE Title LIKE '%規則%'")
    # result2 = db.engine.execute(
    #     "SELECT * from video_keywords WHERE title LIKE '%規則%'")
    return render_template('show_data.html', grammer=grammer_result)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
