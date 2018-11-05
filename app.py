#!/usr/bin/python3
# -*- coding: utf-8 -*-
# author : zhanghaohao
# email  : 1741126544@qq.com
import tornado.ioloop
import tornado.web
import json
import requests
import time, re, os
import pymysql
#创建数据库链接
db = pymysql.connect\
('localhost','root','root','user')

settings= {
    #模板路径(渲染网页)
    "template_path":os.path.join(os.path.dirname(__file__), "templates"),
    #静态文件路径(css)
    "static_path":os.path.join(os.path.dirname(__file__), "static"),
}

#接受url请求将Welcome.htm发往浏览器
class MainPageHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.render("Welcome.htm")
        return super().get(*args, **kwargs)
    
#接受url请求将logon.htm发往浏览器
class LogonHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("logon.htm")
    def post(self):
        #接受参数
        username = self.get_argument("username")
        userpass = self.get_argument("password")
         #导入登录模板
        from model.logon_user import LogonUser

        print(username, userpass)
        #调用登录模板处理业务
        signal = LogonUser(username, userpass, db)
        signa = signal.logon()
        if signa == "OK":
            print(username, "登录成功")
            #成功则进入网站主页
            self.render("myweb/index.htm")
        elif signa == "None":
            print(username, "登录失败")
            #失败则向前端发送失败标签用户不存在
            self.write('''<div class="connect">
		                        <p style="font-size:18px;color:#DD4F43">用户不存在</p>
	                      </div>''')
            self.render("logon.htm")
        elif signa == "Error":
            print(username, "密码错误")
            #失败则向前端发送失败标签密码错误
            self.write('''<div class="connect">
		                        <p style="font-size:18px;color:#DD4F43">密码错误</p>
	                      </div>''')
            self.render("logon.htm")

#接受url请求将index.htm发往浏览器
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("myweb/index.htm")
            
#接受url请求将register.htm发往浏览器
class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("register.htm")

    def post(self):
        #接受注册参数
        username = self.get_argument("username")
        password = self.get_argument("password") 
        phone_number = self.get_argument("phone_number") 
        email = self.get_argument("email")

        #导入注册模板
        from model.register_user import RegisterUser
        print(username, password, phone_number, email)
        #调用模板文件处理注册业务
        signal = RegisterUser(username, password, phone_number, email, db)
        signa = signal.register()

        if signa == "OK":
            print("%s注册成功"%username)
            #如果注册成功向前端发送成功标签
            self.write('''<div class="connect">
		                        <p style="font-size:18px;color:#DD4F43">注册成功 请登陆</p>
	                      </div>''')
            self.render("succeed.htm")

        elif signa == "None":
            print("系统错误")
            #如果系统错误向浏览器发送404页面
            self.render("public/404.htm")

        elif signa == "EXIST":
            print("用户已存在")
            #如果用户存在则向先端发送用户已存在标签
            self.write('''<div class="connect">
		                        <p style="font-size:18px;color:#DD4F43">用户已存在</p>
	                      </div>''')
            self.render("register.htm")

#接受url请求获取系统时间
class Datetime(tornado.web.RequestHandler):
    def get(self):
        datetime = time.strftime('%Y.%m.%d--%H:%M:%S',time.localtime(time.time()))
        self.write(datetime)

#接受url请求将index-game.htm发往浏览器
class GameHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("mygame/index-game.htm")

#接受url请求将index-game1.htm发往浏览器
class Game1Handler(tornado.web.RequestHandler):
    def get(self):
        self.render("mygame1/index-game1.htm")

#接受url请求将404.htm发往浏览器
class BaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("public/404.htm")

#接受url请求将fare.htm发往浏览器
class FareHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("fare/fare.htm")

#接受查票请求进行查票并返回票池
class QueryHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        #接受参数
        from_station = self.get_argument("from_station")#出发地
        to_station = self.get_argument("to_station")#到达地
        querydate = self.get_argument("querydate")#出发时间

        # print(from_station)
        # print(to_station)
        # print(querydate)

        #调用模板文件查票并处理
        from model.query_select import Query, data_analysis
        import t1
        data = Query(from_station,to_station,querydate,t1)#查票
        data = data_analysis(data)#处理数据

        print(from_station)
        print(to_station)
        print(querydate)

        #将处理过的数据已html全局变量的形式发往前端页面
        self.write('''
        <script type="text/javascript">
            var data = %s;
        </script>'''%data)

        # self.write(json.dumps(data, ensure_ascii=False))
        self.render("fare/fare.htm")#在次将查票html发往浏览器

        return super().post(*args, **kwargs)

#分机号码 转发url路由
def make_app():
    return tornado.web.Application([
        (r"/", MainPageHandler),
        (r"/index\.*\w*", MainPageHandler),
        (r"/logon\.*\w*", LogonHandler),
        (r"/register\.*\w*", RegisterHandler),

        (r"/myweb/index\.*\w*", IndexHandler),
        (r"/mygame/index-game\.*\w*", GameHandler),
        (r"/mygame1/index-game1\.*\w*", Game1Handler),
        (r"/time", Datetime),

        (r"/fare/fare\.*\w*", FareHandler),
        (r"/query", QueryHandler),

        (r".*", BaseHandler),    
    ], **settings)

if __name__ == "__main__":

    try:
        http_server = tornado.httpserver.HTTPServer(make_app(),\
            ssl_options={
           "certfile": os.path.join(os.path.abspath("."), "server.crt"),#ssl加密文件
           "keyfile": os.path.join(os.path.abspath("."), "server.key.unsecure"),#无密码证书
    })
        http_server.bind(8888)#监听端口
        http_server.start()#开启https服务器
        tornado.ioloop.IOLoop.instance().start()#启动tornado 异步请求
    except KeyboardInterrupt:
        print("服务器正常退出")
    except Exception:
        print("服务器异常退出")