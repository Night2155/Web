# class grammer_keywords(db.Model):
#     __tablename__ = 'Grammer_keywords_table'
#     Grammer_uid = db.Column(db.Integer, primary_key=True)
#     Grammer_keywords_title = db.Column(db.String(max))
#     Grammer_keywords = db.Column(db.String(max))
#     # 關聯 id
#     db_keywords_id = db.relationship(
#         "Grammer_id_table", backref="Grammer_keywords_table")

#     def __init__(self, Grammer_uid, Grammer_keywords_title, Grammer_keywords):
#         self.uid = Grammer_uid
#         self.title = Grammer_keywords_title
#         self.keywords = Grammer_keywords


# class grammer_id_table(db.Model):
#     __tablename__ = 'Grammer_id_table'
#     Grammer_id = db.Column(db.Integer, db.ForeignKey(
#         'Grammer_keywords.uid'), primary_key=True)
#     Grammer_title = db.Column(db.String(max), primary_key=True)
#     Grammer_video_id = db.Column(db.String(50), primary_key=True)
#     Grammer_channel_id = db.Column(db.String(50), primary_key=True)

#     def __init__(self, Grammer_title, Grammer_video_id, Grammer_channel_id):
#         self.title = Grammer_title
#         self.video_id = Grammer_video_id
#         self.channel_id = Grammer_channel_id
