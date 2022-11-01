from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import aiml
import os, sys
app = Flask(__name__)
# 連接資料庫
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DESKTOP-GPKL4Q4\SQLEXPRESS/Video_data?driver=SQL+Server'
db = SQLAlchemy(app)
# bot_path = "./Chatbot/"
# os.chdir(bot_path)
mybot = aiml.Kernel()
mybot.learn("./Chatbot/basic_chat.aiml")
mybot.respond('load aiml b')

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
    SELECT   Grammer_id.Video_Title, Grammer_id.VideoID, Grammer_keywords.keywords
    FROM     Grammer_id INNER JOIN
             Grammer_keywords ON Grammer_id.Grammer_id = Grammer_keywords.Grammer_uid
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
        SELECT   Grammer_id.Video_Title, Grammer_id.VideoID, Grammer_keywords.keywords
        FROM     Grammer_id INNER JOIN
                 Grammer_keywords ON Grammer_id.Grammer_id = Grammer_keywords.Grammer_uid
        WHERE Grammer_id.Video_Title LIKE '''+bindingwords+''' OR Grammer_keywords.keywords LIKE '''+bindingwords
    elif(len(keyword) == 0):
        query = '''
        SELECT   Grammer_id.Video_Title, Grammer_id.VideoID, Grammer_keywords.keywords
        FROM     Grammer_id INNER JOIN
                 Grammer_keywords ON Grammer_id.Grammer_id = Grammer_keywords.Grammer_uid
        '''

    result3 = db.engine.execute(query).fetchall()
    #print([i for i in result3])
    text_df = pd.DataFrame(result3, columns=['Title', 'video_id', 'keywords'])
    text_df = text_df.to_json(orient='records', lines=False, force_ascii=False)
    text_df = text_df.replace("\/", "/")
    # print(text_df)
    return text_df

@app.route("/robot", methods=['GET', 'POST'])
def robot_response():
    if request.method == 'POST':
        user_text = request.values.get('user_Text')
        print(user_text[0:4])
        response = mybot.respond(user_text)
        if user_text[0:4] == "我想搜尋":
            response = response.replace(" ", "")
    return response

if __name__ == "__main__":
    app.run(debug=True, port=7616)
