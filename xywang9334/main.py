#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import json
import check

from database.user import User
from database.user import Post

from google.appengine.api import memcache

template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def cache_func(username, update = False):
    key = 'top'
    posts = memcache.get(key)
    if posts is None or update:
        posts = db.GqlQuery("select * from Posts order by created desc")
        b = list(posts)
        memcache.set(key, b)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinji_env.get_template(template)
        return t.render(params)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
        self.redirect('/')


    def render_json(self, d):
        json_txt = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json'
        self.write(json_txt)

class WelcomeHandler(BaseHandler):
    def get(self):
        self.render("welcome.html")

class RegisterHandler(BaseHandler):
    def get(self):
        self.render("register.html")
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")

        p = check.valid_password(password)
        u = check.valid_username(username)

        if p and u and ve:
            self.redirect('/')
        else:
            u = User(name = username, hash_pw = password)
            u.put()
            self.render("register.html", username = username, email = email)


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")
    def post(self):

        user_name = self.request.get("username")
        password = self.request.get("password")

        u = User.login(user_name, password)

        if u:
            self.login(u)
            self.redirect('/')
        else:
            msg = "invalid login"
            self.render('login.html', error = msg, username = user_name)

class WikiPost(BaseHandler):
    def get(self):
        self.render("wiki.html")
    def post(self):
        title = self.request.get("title")
        description = self.request.get("description")
        content = self.request.get("content")
        if title and description and content:
            p = Post(title = title, description = description, content = content)
            p.put()




app = webapp2.WSGIApplication([
    ('/', WelcomeHandler),
    ('/login', LoginHandler),
    ('/register', RegisterHandler),
    ('/postpage', WikiPost)
], debug=True)
