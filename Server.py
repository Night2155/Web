from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import json
import aiml
import os
import sys
import random
app = Flask(__name__)
# 連接資料庫
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://DESKTOP-GPKL4Q4\SQLEXPRESS/Video_data?driver=SQL+Server'
db = SQLAlchemy(app)
# Robot Path and Learning Path
mybot = aiml.Kernel()
mybot.learn("./chat_robot/*.aiml")
# mybot.respond('load aiml b')
KeyWordsInDB = []
def ReadFileInArray(path):
    with open(path, encoding='utf-8-sig') as f:
        data_read = f.read().splitlines()
        array_data = data_read
    f.close
    return array_data
KeyWordsInDB = ReadFileInArray("Data/filtered_all_keywords.txt")
# print(KeyWordsInDB)

@app.route("/", methods=['GET', 'POST'])
def homepage():
    # return render_template('All_Video_Page.html', result=grammar_result, result2=Writing_result, result3=Reading_result)
    return render_template('HomePage.html')
    # return render_template('show_data.html', result=grammar_result, result2=Writing_result, result3=Reading_result)


@app.route("/Grammar_data", methods=['GET', 'POST'])
def Grammar_data():
    # 載入所有資料庫的影片資訊
    # grammar_query = ''' SELECT * FROM Grammar_Table '''
    Grammar_random_sql = '''
    SELECT TOP 18 Grammar_Table.Video_Title, Grammar_Table.VideoID, Grammar_Table.keywords
    FROM Grammar_Table
    ORDER BY NEWID()'''
    grammar_result = db.engine.execute(Grammar_random_sql).fetchall()
    text_df = pd.DataFrame(
        grammar_result, columns=['Title', 'video_id', 'keywords'])
    text_df = text_df.to_json(orient='records', lines=False, force_ascii=False)
    text_df = text_df.replace("\/", "/")
    text_df = json.loads(text_df)
    return text_df


@app.route("/Writing_data", methods=['GET', 'POST'])
def Writing_data():
    Writing_random_sql = '''
    SELECT TOP 18 Writing_Table.Video_Title, Writing_Table.VideoID, Writing_Table.keywords
    FROM Writing_Table
    ORDER BY NEWID()'''
    Writing_result = db.engine.execute(Writing_random_sql).fetchall()
    text_df = pd.DataFrame(
        Writing_result, columns=['Title', 'video_id', 'keywords'])
    text_df = text_df.to_json(
        orient='records', lines=False, force_ascii=False)
    text_df = text_df.replace("\/", "/")
    text_df = json.loads(text_df)
    return text_df


@app.route("/Reading_data", methods=['GET', 'POST'])
def Reading_data():
    Reading_random_sql = '''
    SELECT TOP 18 Reading_Table.Video_Title, Reading_Table.VideoID, Reading_Table.keywords
    FROM Reading_Table
    ORDER BY NEWID()'''
    Reading_result = db.engine.execute(Reading_random_sql).fetchall()
    text_df = pd.DataFrame(
        Reading_result, columns=['Title', 'video_id', 'keywords'])
    text_df = text_df.to_json(
        orient='records', lines=False, force_ascii=False)
    text_df = text_df.replace("\/", "/")
    return text_df


@app.route("/SecondPage", methods=['GET', 'POST'])
def SecondPage():
    query = ''' SELECT Grammar_Table.Video_Title, Grammar_Table.VideoID, Grammar_Table.keywords FROM Grammar_Table '''
    Grammar_result = db.engine.execute(query).fetchall()
    Grammar_result = ChangeDataToList(Grammar_result)
    query = ''' SELECT Reading_Table.Video_Title, Reading_Table.VideoID, Reading_Table.keywords FROM Reading_Table '''
    Reading_result = db.engine.execute(query).fetchall()
    Reading_result = ChangeDataToList(Reading_result)
    query = ''' SELECT Writing_Table.Video_Title, Writing_Table.VideoID, Writing_Table.keywords FROM Writing_Table '''
    Writing_result = db.engine.execute(query).fetchall()
    Writing_result = ChangeDataToList(Writing_result)
    result = Grammar_result + Reading_result + Writing_result
    # List 排序
    result = sorted(result, key=lambda i: i["Title"])
    return render_template('All_Video_Page.html', result1=result)


@app.route("/search", methods=['GET', 'POST'])
def search():
    # 搜尋結果以更新放置影片資訊的欄位呈現(篩選出有關鍵字的影片)
    # if 關鍵字 == 進行式 then 影片資訊的欄位只會出現關鍵字有進行式的影片
    # keywords 網站傳來的關鍵字
    if request.method == 'POST':
        # keyword = request.form['search_bar']
        # searchtext 前端傳來的搜尋關鍵字
        keyword = request.values.get('keyword')
        print(keyword, len(keyword))
    if(len(keyword) > 0):
        bindingwords = "'%"+keyword+"%'"  # 字串串接
        query = '''
        SELECT Grammar_Table.Video_Title, Grammar_Table.VideoID, Grammar_Table.keywords FROM Grammar_Table
        WHERE Video_Title LIKE '''+bindingwords + ''' OR keywords LIKE '''+bindingwords + '''
        union
        SELECT Reading_Table.Video_Title, Reading_Table.VideoID, Reading_Table.keywords FROM Reading_Table
        WHERE Video_Title LIKE '''+bindingwords + ''' OR keywords LIKE '''+bindingwords + '''
        union
        SELECT Writing_Table.Video_Title, Writing_Table.VideoID, Writing_Table.keywords FROM Writing_Table
        WHERE video_Title LIKE '''+bindingwords + ''' OR keywords LIKE '''+bindingwords
    result = db.engine.execute(query).fetchall()
    result = ChangeDataToList(result)

    def find_index_with_cond(elements, condition):
        for i, element in enumerate(elements):
            if condition(element):
                return i

        return 100000

    def sort_condition(element):
        keyword_list = element["keywords"].split(" ")

        def condition(element):
            return keyword in element

        return find_index_with_cond(keyword_list, condition)

    result.sort(key=sort_condition)

    return result


@app.route("/robot", methods=['GET', 'POST'])
def robot_response():
    if request.method == 'POST':
        user_text = request.values.get('user_Text')
        print(user_text)
        for item in KeyWordsInDB:
            if item in user_text:
                print(item)
                # response = mybot.respond(item)
                bindingwords = "'%" + item + "%'"  # 字串串接
                query = '''
                        SELECT Grammar_Table.Video_Title, Grammar_Table.VideoID, Grammar_Table.keywords FROM Grammar_Table
                        WHERE Video_Title LIKE ''' + bindingwords + ''' OR keywords LIKE ''' + bindingwords + '''
                        union
                        SELECT Reading_Table.Video_Title, Reading_Table.VideoID, Reading_Table.keywords FROM Reading_Table
                        WHERE Video_Title LIKE ''' + bindingwords + ''' OR keywords LIKE ''' + bindingwords + '''
                        union
                        SELECT Writing_Table.Video_Title, Writing_Table.VideoID, Writing_Table.keywords FROM Writing_Table
                        WHERE video_Title LIKE ''' + bindingwords + ''' OR keywords LIKE ''' + bindingwords
                result = db.engine.execute(query).fetchall()
                result = ChangeDataToList(result)
                result_len = len(result)
                result_ran_index = random.randint(0, result_len - 1)
                response_text = result[result_ran_index]['Title']
                url = "https://www.youtube.com/watch?v=" + result[result_ran_index]['video_id']
                robot_response = mybot.respond("回應推薦影片")
                # response = f"{robot_response}\n{response_text}\n{url}"
                response = robot_response + '<br>' + response_text + "<br>" + '<a href = ' + url + ' target =_blank >' + url + '</a>'
                break
            else:
                response = mybot.respond("對話未進入辭庫")
    # if user_text[0:4] == "我想搜尋":
    #     response = response.replace(" ", "")
    #     response = mybot.respond(user_text)

    return response

@app.route("/robot2", methods=['GET', 'POST'])
def robot_response_HomePage():
    if request.method == 'POST':
        user_text = request.values.get('user_Text')
        print(user_text)
        for item in KeyWordsInDB:
            if item in user_text:
                print(item)
                # response = mybot.respond(item)
                bindingwords = "'%" + item + "%'"  # 字串串接
                query = '''
                        SELECT Grammar_Table.Video_Title, Grammar_Table.VideoID, Grammar_Table.keywords FROM Grammar_Table
                        WHERE Video_Title LIKE ''' + bindingwords + ''' OR keywords LIKE ''' + bindingwords + '''
                        union
                        SELECT Reading_Table.Video_Title, Reading_Table.VideoID, Reading_Table.keywords FROM Reading_Table
                        WHERE Video_Title LIKE ''' + bindingwords + ''' OR keywords LIKE ''' + bindingwords + '''
                        union
                        SELECT Writing_Table.Video_Title, Writing_Table.VideoID, Writing_Table.keywords FROM Writing_Table
                        WHERE video_Title LIKE ''' + bindingwords + ''' OR keywords LIKE ''' + bindingwords
                result = db.engine.execute(query).fetchall()
                result = ChangeDataToList(result)
                result_len = len(result)
                result_ran_index = random.randint(0, result_len - 1)
                response_text = result[result_ran_index]['Title']
                url = "https://www.youtube.com/watch?v=" + result[result_ran_index]['video_id']
                robot_response = mybot.respond("回應推薦影片")
                # response = f"{robot_response}\n{response_text}\n{url}"
                response = robot_response +'<br>'+ response_text+"<br>" + '<a href = ' + url +' target =_blank >'+ url +'</a>'
                break
            else:
                response = mybot.respond("對話未進入辭庫")
        # if user_text[0:4] == "我想搜尋":
        #     response = "不好意思 此功能正在維修 請在ALL Video使用此功能"
    return response

def ChangeDataToList(data):
    data = pd.DataFrame(
        data, columns=['Title', 'video_id', 'keywords'])
    data = data.to_json(orient='records', lines=False, force_ascii=False)
    data = data.replace("\/", "/")
    data = json.loads(data)
    return data

if __name__ == "__main__":
    app.run(debug=True, port=7616)
