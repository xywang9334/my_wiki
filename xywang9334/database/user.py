from google.appengine.ext import db

class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        u = User.all().filter('name = ', name).get()
        return u

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u


class Posts(db.Model):
    title = db.StringProperty(required = True)
    description = db.StringProperty()
    content = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    lastModified = db.DateTimeProperty(auto_now = True)

    def render(self):

        # render something ??
        self._render_text = self.content.replace('\n', '<br>')
        return self.render_str("wiki.html", b = self)


    def as_dict(self):
        time_fmt = '%c'
        d = {'subject': self.title,
             'description': self.description
             'content': self.content,
             'created': self.created.strftime(time_fmt),
             'last_modified': self.lastModified.strftime(time_fmt)}

        return d
