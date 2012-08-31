# -- coding: utf8 --
import web
from config.config import render
from models import user_model
from libraries.error import *

class login:
    
    form = user_model.login_form
    
    def GET(self):
        title = '登录'
        return render.login(self.form, title)
    
    def POST(self):
        if not self.form.validates():
            return render.login(self.form, '登录失败，请重登')
        condition = {'name' : self.form.d.name, 'password' : self.form.d.password}
        user = user_model.get_user(condition)
        if user is None:
            return render.login(self.form, '登录失败，请重登')
        web.config._session.user_id = user.id
        web.config._session.name = user.name
        raise web.seeother('/')

class signup:
    
    form = user_model.signup_form
    
    def GET(self):
        title = '注册'
        return render.signup(self.form, title)
    
    def POST(self):
        if not self.form.validates():
            return render.signup(self.form, '注册失败，请重注')
        elif self.form.d.password != self.form.d.confirm_password:
            return render.signup(self.form, '密码不一致，请重注')
        try:
            user_model.insert(self.form.d.name, self.form.d.email, self.form.d.password)
        except ValueExistsError, x:
            return render.signup(self.form, x.message)
        raise web.seeother('/')

# 注销
class logout:
    
    def GET(self):
        web.config._session.kill()
        raise web.SeeOther('/')