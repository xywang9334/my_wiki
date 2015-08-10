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

import database.user

template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

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


class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")
    def post(self):

        # TODO: Add valid username check
        user_name = self.request.get("username")
        # TODO: Add valid password check
        password = self.request.get("password")

        u = User.login(user_name, password)

        if u:
            self.login(u)
            self.redirect('/')
        else:
            msg = "invalid login"
            self.render('login.html', error = msg, username = user_name)


app = webapp2.WSGIApplication([
    ('/', WelcomeHandler),
    ('/login', LoginHandler)
], debug=True)
