#!/usr/bin/env python

import os
import os.path
import datetime
import time
import urllib

from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.datastore.datastore_query import Cursor

from models import *

import jinja2
import webapp2

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


def renderLogin(self):
        # Checks for active Google account session
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'        
        else: 
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'user' : user,
        }
        return template_values

class AskQuestion(webapp2.RequestHandler):
    def post(self):
        question = Question()
        if users.get_current_user() :
            question.author = str(users.get_current_user().email())
            question.title = self.request.get('title')
            question.questionId = users.get_current_user().email() + str(datetime.datetime.now())
            question.content = self.request.get('questionContent')
            tags = self.request.get('tags')
            tagsList = tags.split(',')
            for x in range(len(tagsList)):
                tagsList[x] = tagsList[x].strip()
                if tagsList[x] == '':
                    tagsList[x] = None
            tagsList = filter(None, tagsList)
            tagsList = list(set(tagsList))
            question.tags = tagsList
            question.put()
            time.sleep(1)
            self.redirect('/')

class AnswerQuestion(webapp2.RequestHandler):
    def post(self):
        answer = Answer()
        viewQuestion = ViewQuestion()
        if users.get_current_user():
            login_values = renderLogin(self)
            qId = self.request.get('qId')
            question_key = ndb.Key(urlsafe = qId)
            question = question_key.get()
            answer.author = str(users.get_current_user().email())
            answer.answerId = users.get_current_user().email() + str(datetime.datetime.now())
            answer.content = self.request.get('answerContent')
            answer.questionId = question.questionId
            answer.put()
            time.sleep(1)
            self.redirect('/viewQuestion?qId=' + question.key.urlsafe() )

class Vote(webapp2.RequestHandler):
    def get(self):
        voteType = self.request.get('type')
        if 'question' == voteType :
            qId = self.request.get('qId')
            question_key = ndb.Key(urlsafe = qId)
            question = question_key.get()
            result = self.request.get('result')
            user_id = self.request.get('user')
            if 'up' == result:
                self.voteHelper(question, user_id, True)
            else :
                self.voteHelper(question, user_id, False)
            question.put()
            time.sleep(1)
            self.redirect('/viewQuestion?qId=' + self.request.get('qId'))
        elif 'answer' == voteType:
            aId = self.request.get('id')
            answer_key = ndb.Key(urlsafe = aId)
            answer = answer_key.get()
            result = self.request.get('result')
            user_id = self.request.get('user')
            if 'up' == result:
                self.voteHelper(answer, user_id, True)
            else :
                self.voteHelper(answer, user_id, False)
                #answer.vote = answer.vote - 1
            answer.put()
            time.sleep(1)
            self.redirect('/viewQuestion?qId=' + self.request.get('qId'))

    def voteHelper(self, obj, user_id ,up):
        if up:
            if (user_id in obj.downList):
                obj.downList.remove(user_id)
            if (user_id not in obj.upList):
                obj.upList.append(user_id)
        else:
            if (user_id in obj.upList):
                obj.upList.remove(user_id)
            if (user_id not in obj.downList):
                obj.downList.append(user_id)

    def post(self):
        voteType = self.request.get('type')
        if 'question' == voteType :
            qId = self.request.get('qId')
            question_key = ndb.Key(urlsafe = qId)
            question = question_key.get()
            result = self.request.get('result')
            user_id = self.request.get('user')
            if 'up' == result:
                self.voteHelper(question, user_id, True)
            else :
                self.voteHelper(question, user_id, False)
            question.put()
            time.sleep(1)
            self.redirect('/')
            #self.redirect('/viewQuestion?qId=' + self.request.get('qId'))


class Edit(webapp2.RequestHandler):
    def post(self):
        contentType = self.request.get('type')
        if contentType == 'question' :
            qId = self.request.get('id')
            question_key = ndb.Key(urlsafe = qId)
            question = question_key.get()
            question.title = self.request.get('title')
            question.content = self.request.get('content')
            tagsStr = self.request.get('tags')
            question.tags = tagsStr.split(',')
            question.put()
        else :
            aId = self.request.get('id')
            answer_key = ndb.Key(urlsafe = aId)
            answer = answer_key.get()
            answer.title = self.request.get('title')
            answer.content = self.request.get('content')
            answer.put()
        time.sleep(1)
        self.redirect('/')

class MainPage(webapp2.RequestHandler):
    # render the default login page
    def get(self):
        login_values = renderLogin(self)
        question = Question()
        util = Util()
        curs = Cursor(urlsafe=self.request.get('page'))
        questions, next_curs, more = Question.query().order(-Question.date).fetch_page(10, start_cursor=curs)
        if more and next_curs:
            pageStr = next_curs.urlsafe()
        else:
            pageStr = ''
        for question in questions:
            question.preview = util.contentParser(question.content)[0:499]
        template_values = {
            'questions' : questions,
            'url': login_values.get('url'),
            'url_linktext': login_values.get('url_linktext'),
            'user' : login_values.get('user'),
            'page' : pageStr,
        }
        
        template = JINJA_ENVIRONMENT.get_template('showQuestions.html')
        self.response.write(template.render(template_values))

class ViewQuestion(webapp2.RequestHandler):

    def handleGet(self, login_values, questionObj):     
        answer = Answer()
        util = Util()
        questionObj.content = util.contentParser(questionObj.content)
        #answers = answer.get_question_answer(questionObj.questionId)
        answers = answer.get_answers_orderBy_vote(questionObj.questionId)
        for answer in answers :
            answer.content = util.contentParser(answer.content)
        template_values = {
            'q' : questionObj,
            #'content' : util.contentParser(questionObj.content),
            'url': login_values.get('url'),
            'url_linktext': login_values.get('url_linktext'),
            'user' : login_values.get('user'),
            'answers' : answers,
        }
        template = JINJA_ENVIRONMENT.get_template('showQuestion.html')
        self.response.write(template.render(template_values))

    def get(self):
        login_values = renderLogin(self)
        qId = self.request.get('qId')
        question_key = ndb.Key(urlsafe=qId)
        question = question_key.get()
        self.handleGet(login_values, question)

class AskQuestionView(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'        
        else: 
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'url': url,
            'url_linktext': url_linktext,
            'user' : user,
        }
        template = JINJA_ENVIRONMENT.get_template('askQuestion.html')
        self.response.write(template.render(template_values))

class EditView(webapp2.RequestHandler):
    def get(self):
        login_values = renderLogin(self)
        if self.request.get('qId') != '' :
            qUrl = self.request.get('qId')
            question_key = ndb.Key(urlsafe = qUrl)
            question = question_key.get()
            if question.tags:
                tagsStr = ''
                for index in range(len(question.tags)):
                    tagsStr += question.tags[index]
                    if index != len(question.tags)-1:
                        tagsStr += ','
            template_values = {
                'type' : 'question',
                'editObj' : question,
                'tagsStr' : tagsStr,
                'url': login_values.get('url'),
                'url_linktext': login_values.get('url_linktext'),
                'user' : login_values.get('user'),
            }
        else :
            aUrl = self.request.get('aId')
            answer_key = ndb.Key(urlsafe = aUrl)
            answer = answer_key.get()
            template_values = {
                'type' : 'answer',
                'editObj' : answer,
                'url': login_values.get('url'),
                'url_linktext': login_values.get('url_linktext'),
                'user' : login_values.get('user'),
            }
        template = JINJA_ENVIRONMENT.get_template('editContent.html')
        self.response.write(template.render(template_values))

class TagsView(webapp2.RequestHandler):
    def get(self):
        tag = self.request.get('tag')
        login_values = renderLogin(self)
        question = Question()
        util = Util()
        curs = Cursor(urlsafe=self.request.get('page'))
        questions, next_curs, more = Question.query(Question.tags==tag).order(-Question.date).fetch_page(10, start_cursor=curs)
        if more and next_curs:
            pageStr = next_curs.urlsafe()
        else:
            pageStr = ''
        for question in questions:
            question.preview = util.contentParser(question.content)[0:499]
        template_values = {
            'questions' : questions,
            'url': login_values.get('url'),
            'url_linktext': login_values.get('url_linktext'),
            'user' : login_values.get('user'),
            'page' : pageStr,
        }      
        template = JINJA_ENVIRONMENT.get_template('showQuestions.html')
        self.response.write(template.render(template_values))

class UploadImgView(webapp2.RequestHandler):
    def get(self):
        login_values = renderLogin(self)
        user = str(users.get_current_user())
        #images = Image.query().order(-Image.date).fetch()
        #print len(images)
        image = Image()
        images = image.get_user_image(user)
        template_values = {
            'images' : images,
            'url': login_values.get('url'),
            'url_linktext': login_values.get('url_linktext'),
            'user' : login_values.get('user'),
        }
        template = JINJA_ENVIRONMENT.get_template('uploadPic.html')
        self.response.write(template.render(template_values))

class UploadImg(webapp2.RequestHandler):
    def post(self):
        if users.get_current_user():
            ifile = self.request.get('img')
            image = Image()
            image.ifile = ifile
            image.user = str(users.get_current_user())
            image_key = image.put()
            image = image_key.get()
            image.name = self.request.params['img'].filename
            image.url = image_key.urlsafe() + "_" + self.request.params['img'].filename
            image.put()
            self.redirect('/upload')

class ImageHandler(webapp2.RequestHandler):
    def get(self):
        url = self.request.get('url')
        picture = Image.query(Image.url==url).get()
        if picture.ifile:
            self.response.headers['content-Type'] = 'image/png'
            self.response.write(picture.ifile)

class RSSHandler(webapp2.RequestHandler):
    def get(self, qId):
        question_key = ndb.Key(urlsafe=qId)
        question = question_key.get()
        answer = Answer()
        answers = answer.get_answers_orderBy_vote(question.questionId)
        template_value = {
            'question' : question,
            'answers' : answers,
        }
        self.response.headers['Content-Type'] = 'text/xml'
        template = JINJA_ENVIRONMENT.get_template('rss.xml')
        self.response.write(template.render(template_value))

app = webapp2.WSGIApplication([ 
    ('/', MainPage),
    ('/AskQuestionView', AskQuestionView),
    ('/askQuestion', AskQuestion),
    ('/viewQuestion',ViewQuestion),
    ('/answerQuestion',AnswerQuestion),
    ('/vote', Vote),
    ('/editView', EditView),
    ('/edit', Edit),
    ('/tags', TagsView),
    ('/upload', UploadImgView),
    ('/uploadPicture', UploadImg),
    ('/serveImage', ImageHandler),
    ('/rss/qId=(.*)',RSSHandler),
], debug=True)