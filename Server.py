from unittest import result
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
import pandas as pd
import json
app = Flask(__name__)
# 連接資料庫
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DESKTOP-GPKL4Q4\SQLEXPRESS/Video_data?driver=SQL+Server'
db = SQLAlchemy(app)


@app.route("/", methods=['GET', 'POST'])
def homepage():
    # 載入所有資料庫的影片資訊
    # query = '''
    # SELECT video_and_channel_id.Title, video_and_channel_id.video_id, video_keywords.video_keywords
    # FROM   video_and_channel_id INNER JOIN
    #         video_keywords ON video_and_channel_id.id = video_keywords.uid
    # '''
    # result = db.engine.execute(query)
    # return render_template('DemoHomepage.html', vc_id=result)
    grammer_query = '''
    SELECT  Grammer_id_table.Grammer_title, Grammer_id_table.Grammer_video_id,Grammer_keywords_table.Grammer_keywords                  
    FROM    Grammer_id_table INNER JOIN
            Grammer_keywords_table ON Grammer_id_table.Grammer_id = Grammer_keywords_table.Grammer_uid
    '''
    grammer_result = db.engine.execute(grammer_query)
    return render_template('DemoHomepage.html', result=grammer_result)


@app.route("/search", methods=['GET', 'POST'])
def search():
    # 搜尋結果以更新放置影片資訊的欄位呈現(篩選出有關鍵字的影片)
    # if 關鍵字 == 進行式 then 影片資訊的欄位只會出現關鍵字有進行式的影片
    # keywords 網站傳來的關鍵字
    if request.method == 'POST':
        #keyword = request.form['search_bar']

        keyword = request.values.get('searchtext')
        # print(keyword, len(keyword))
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

    result3 = db.engine.execute(query).fetchall()
    #print([i for i in result3])
    text_df = pd.DataFrame(result3, columns=['Title', 'video_id', 'keywords'])
    text_df = text_df.to_json(orient='records', lines=False, force_ascii=False)
    text_df = text_df.replace("\/", "/")
    # print(text_df)
    return text_df


if __name__ == "__main__":
    app.run(debug=True, port=7616)
