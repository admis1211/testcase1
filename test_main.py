"""
FastAPI 入门项目 — 自动化测试
==============================
运行: pytest test_main.py -v
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestRootRedirect:
    """测试根路径重定向"""

    def test_root_redirects_to_static(self):
        """访问 / 应返回 307 重定向到 /static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"

    def test_root_follow_redirect_returns_html(self):
        """跟随重定向后应返回 HTML 页面"""
        response = client.get("/", follow_redirects=True)
        assert response.status_code == 200
        assert "FastAPI 主页" in response.text


class TestHelloAPI:
    """测试 /api/hello 查询参数 API"""

    def test_hello_with_default_name(self):
        """不传 name 参数时使用默认值"""
        response = client.get("/api/hello")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "你好，测试！"

    def test_hello_with_custom_name(self):
        """传 name 参数时返回自定义问候"""
        response = client.get("/api/hello?name=赵工")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "你好，赵工！"

    def test_hello_returns_valid_json(self):
        """返回正确的 JSON 结构"""
        response = client.get("/api/hello?name=World")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert isinstance(data["message"], str)


class TestUserAPI:
    """测试 /api/user/{user_id} 路径参数 API"""

    def test_user_with_valid_int(self):
        """传入合法整数返回对应用户信息"""
        response = client.get("/api/user/123")
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == 123
        assert data["name"] == "用户123"

    def test_user_with_another_int(self):
        """传入另一个整数"""
        response = client.get("/api/user/42")
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == 42
        assert data["name"] == "用户42"

    def test_user_with_string_returns_422(self):
        """传入非数字字符串应返回 422 验证错误"""
        response = client.get("/api/user/abc")
        assert response.status_code == 422


class TestStaticFiles:
    """测试静态文件服务"""

    def test_static_index_html(self):
        """静态文件 /static/index.html 可正常访问"""
        response = client.get("/static/index.html")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "<title>FastAPI 主页</title>" in response.text
