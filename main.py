"""
FastAPI 入门项目
=================
功能：挂载静态文件，访问根路径 / 时自动跳转到主页 index.html
"""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

# 1. 创建应用实例
#    提示：FastAPI() 是整个应用的核心对象
#    语法：变量名 = FastAPI(title="项目名")
app = FastAPI(title="冲突分支版本")

# 2. 挂载静态文件目录
#    提示：把 static/ 目录暴露成 URL
#    语法：app.mount("URL前缀", StaticFiles(directory="硬盘目录名"), name="定位器名")
app.mount("/static",StaticFiles(directory="static"),name="static")

# 3. 查询参数 API
#    需求：访问 /api/hello?name=赵工 返回 {"message": "你好，赵工！"}
#         不传 name 时默认用 "世界"
#    提示：@app.get + def + 类型注解 + 默认值 + return 字典
@app.get("/api/hello")
def hello(name: str = "测试"):
    return {"message": f"你好，{name}！"}

# 4. 路径参数 API
#    需求：访问 /api/user/123 返回 {"user_id": 123, "name": "用户123"}
#         访问 /api/user/abc 自动返回 422
#    提示：路径里 {user_id} 占位，参数 int，return 字典
@app.get("/api/user/{user_id}")
def user(user_id: int):
    return {"user_id":user_id,"name":f"用户{user_id}"}

# 5. 根路径重定向
#    需求：访问 / 自动跳转到 /static/index.html
#    提示：@app.get + def + RedirectResponse(url="...")
@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")