import os
import unittest
import datetime
from app.models import User, Role, Comment,Post
from app import create_app, db

app = create_app("default")

class TestDatabase(unittest.TestCase):
    """测试数据库的案例"""
    def setUp(self):
        with app.app_context():
            #开启测试模式
            app.debug = True
            #对应修改成自己测试数据库
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(basedir,"app.sqlite")
            app.config['SERVER_NAME'] = 'example.com'
            self.app = app
            db.drop_all()
            db.create_all()
            self.client = app.test_client()

    def test_signup(self):
        with app.app_context():
            """测试添加作者的案例"""
            user = User(email="1@qq.com", password="dd", username="aa")
            db.session.add(user)
            db.session.commit()

            ret_user = User.query.filter_by(username="aa").first()

            self.assertIsNotNone(ret_user)
            self.assertEqual(ret_user.username, "aa")

    def test_edit(self):
        with app.app_context():
            user = User(username="aa", password="dd")
            db.session.add(user)
            db.session.commit()
            user = User.query.filter_by(username="aa").first()
            user.password = 'b'
            db.session.commit()

            ret_user = User.query.filter_by(username="aa").first()

            self.assertIsNotNone(ret_user)
            self.assertEqual(ret_user.password, "b")

    def test_delete(self):
        with app.app_context():
            user = User(username="aa", password="dd")
            db.session.add(user)
            db.session.commit()
            user = User.query.filter_by(username="aa").first()
            db.session.delete(user)
            db.session.commit()

            ret_user = User.query.filter_by(username="aa").first()

            self.assertNotIsInstance(ret_user,User)

    def test_postadd(self):
        with app.app_context():
            """测试添加作者的案例"""
            post = Post(title="za", body="dda", author="aa")
            db.session.add(post)
            db.session.commit()

            ret_post = Post.query.filter_by(title="za").first()

            self.assertIsNotNone(ret_post)
            self.assertEqual(ret_post.title, "za")

    def test_postedit(self):
        with app.app_context():
            post = Post(title="za", body="dda", author="aa")
            db.session.add(post)
            db.session.commit()
            post = Post.query.filter_by(title="za").first()
            post.content = 'b'
            db.session.commit()

            ret_post = Post.query.filter_by(title="za").first()

            self.assertIsNotNone(ret_post)
            self.assertEqual(ret_post.content, "b")

    def test_postdelete(self):
        with app.app_context():
            post = Post(title="za", body="dda", author=1)
            db.session.add(post)
            db.session.commit()
            post = Post.query.filter_by(title="za").first()
            db.session.delete(post)
            db.session.commit()

            ret_post = Post.query.filter_by(title="za").first()

            self.assertNotIsInstance(ret_post,Post)



    def test_login(self):
        with app.app_context():
            response = self.client.post("/login", data = {"username":"aa","password":"dd"})
            self.assertTrue(response.status_code == 200)

    def tearDown(self):
        with app.app_context():
            """在所有测试方法执行后，被调用"""
            db.session.remove()
            # 清除数据库数据
            db.drop_all()

if __name__ == '__main__':
    unittest.main()

