import re
from google.appengine.ext import ndb
from google.appengine.datastore.datastore_query import Cursor

# DEFAULT_QUESTION_NAME="default_question_name"

# def question_key(question_name=DEFAULT_QUESTION_NAME):
#     return ndb.Key('Question', question_name)

class Question(ndb.Model):
    author = ndb.StringProperty()
    title = ndb.StringProperty()
    questionId = ndb.StringProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    edit_date = ndb.DateTimeProperty(auto_now=True)
    upList = ndb.StringProperty(repeated=True)
    downList = ndb.StringProperty(repeated=True)
    up = ndb.ComputedProperty(lambda self: len(self.upList))
    down = ndb.ComputedProperty(lambda self: len(self.downList))
    vote = ndb.ComputedProperty(lambda self: self.up - self.down)
    tags = ndb.StringProperty(repeated=True)
    
    def get_question(cls, user):
        q = Question.query(Question.author == user).order(-Question.date)
        return q.fetch()

    def get_all_question(cls):
        q = Question.query().order(-Question.date)
        return q.fetch()

class Answer(ndb.Model):
    author = ndb.StringProperty()
    answerId = ndb.StringProperty()
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    edit_date = ndb.DateTimeProperty(auto_now=True)
    upList = ndb.StringProperty(repeated=True)
    downList = ndb.StringProperty(repeated=True)
    up = ndb.ComputedProperty(lambda self: len(self.upList))
    down = ndb.ComputedProperty(lambda self: len(self.downList))
    vote = ndb.ComputedProperty(lambda self: self.up - self.down)
    questionId = ndb.StringProperty()

    def get_question_answer(cls, questionId):
        a = Answer.query(Answer.questionId==questionId).order(-Answer.date)
        return a.fetch()

    def get_answers_orderBy_vote(cls, questionId):
        a = Answer.query(Answer.questionId==questionId).order(-Answer.vote)
        return a.fetch()

class Util():
    def contentParser(self, result):
        #httpStr='http://www.baid.com'
        result = re.sub(r'(http[s]?://)([^\s]*)','<a href="\\1\\2">\\2</a>',result)
        result = re.sub(r'<a href="(http[s]?://[^\s]*[(.jpg)(.png)(.gif)])">.*</a>', '<img src="\\1" width="300" height="300">', result)
        result = result.replace('\n', '<br/>')
        return result

class Image(ndb.Model):
    ifile = ndb.BlobProperty()
    url = ndb.StringProperty()
    user = ndb.StringProperty()
    name = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)

    def get_user_image(cls, user):
        i = Image.query(Image.user==user).order(-Image.date)
        return i.fetch()
