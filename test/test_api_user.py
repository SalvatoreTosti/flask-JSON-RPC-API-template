import os, json
import unittest
from app import app, db
from app.models.user import User
import base64
from test.utils import TEST_DB, test_setup, generate_auth_header


class UserTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        test_setup(self)

    # executed after each test
    def tearDown(self):
        pass

    # def test_fetch_users(self):
    #     # json = {"username": username, "password": "test-1"}
    #     json = {"jsonrpc": "2.0", "id": 1, "method": "test.test"}
    #     response = self.app.post("/rpc", json=json)
    #     print(response.get_data(as_text=True))
    #     print(response)
    #     # data = json.loads(response.get_data(as_text=True))
    #     # print(data)
    #     self.assertTrue(false)
    #
    #     # response = self.app.post("/rpc", follow_redirects=True)
    #     self.assertEqual(response.status_code, 200)

    def test_fetch_users(self):
        # json = {"username": username, "password": "test-1"}
        json = {"jsonrpc": "2.0", "id": 1, "method": "task.read_all"}
        response = self.app.post("/rpc", json=json)
        print(response.get_data(as_text=True))
        print(response)
        # data = json.loads(response.get_data(as_text=True))
        # print(data)
        self.assertTrue(false)

        # response = self.app.post("/rpc", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # def test_fetch_user_valid_login(self):


#      username = "user-1"
#      headers = generate_auth_header(username, "test1")
#      response = self.app.get(
#          "/api/v1.0/users/1", follow_redirects=True, headers=headers
#      )
#      self.assertEqual(response.status_code, 200)
#      u = User.query.filter_by(username=username).first()
#      self.assertEqual(username, u.username)
#
#  def test_fetch_user_invalid_login(self):
#      headers = generate_auth_header("user-1", "test2")
#      response = self.app.get(
#          "/api/v1.0/users/1", follow_redirects=True, headers=headers
#      )
#      self.assertEqual(response.status_code, 401)
#
#  def test_fetch_user_valid_token_login(self):
#      username = "user-1"
#      headers = generate_auth_header(username, "test1")
#      response = self.app.get(
#          "/api/v1.0/generate-token",
#          follow_redirects=True,
#          headers=headers
#      )
#      self.assertEqual(response.status_code, 200)
#      data = json.loads(response.get_data(as_text=True))
#      headers = generate_auth_header(data['token'], "")
#      response = self.app.get(
#          "/api/v1.0/users/1", follow_redirects=True, headers=headers
#      )
#      data = json.loads(response.get_data(as_text=True))
#      self.assertEqual(username, data['user']['username'])
#
#  def test_fetch_user_invalid_token_login(self):
#      username = "user-1"
#      headers = generate_auth_header(username, "invalid")
#      response = self.app.get(
#          "/api/v1.0/generate-token",
#          follow_redirects=True,
#          headers=headers
#      )
#      self.assertEqual(response.status_code, 401)
#
#  def test_fetch_user_token_login_invalid_token(self):
#      username = "user-1"
#      headers = generate_auth_header("INVALID_TOKEN", "")
#      response = self.app.get(
#          "/api/v1.0/users/1", follow_redirects=True, headers=headers
#      )
#      data = json.loads(response.get_data(as_text=True))
#      self.assertEqual(response.status_code, 401)
#
#  def test_fetch_user_inaccessible_user(self):
#      headers = generate_auth_header("user-1", "test1")
#      response = self.app.get(
#          "/api/v1.0/users/2", follow_redirects=True, headers=headers
#      )
#      self.assertEqual(response.status_code, 401)
#
#  def test_fetch_user_invalid_user(self):
#      headers = generate_auth_header("user-1", "test1")
#      response = self.app.get(
#          "/api/v1.0/users/0", follow_redirects=True, headers=headers
#      )
#      self.assertEqual(response.status_code, 404)
#
#  def test_create_user_valid(self):
#      username = "test-1"
#      json = {"username": username, "password": "test-1"}
#      response = self.app.post("/api/v1.0/users", json=json)
#      self.assertEqual(response.status_code, 201)
#      u = User.query.filter_by(username=username).first()
#      self.assertEqual(username, u.username)
#
#  def test_create_user_no_password(self):
#      json = {"username": "test-1"}
#      response = self.app.post("/api/v1.0/users", json=json)
#      self.assertEqual(response.status_code, 400)
#
#  def test_create_user_no_username(self):
#      json = {"password": "test-1"}
#      response = self.app.post("/api/v1.0/users", json=json)
#      self.assertEqual(response.status_code, 400)
#
#  def test_update_user_valid(self):
#      username = "test-2"
#      json = {"username": username, "password": "test-2"}
#      headers = generate_auth_header("user-1", "test1")
#      response = self.app.put(
#          "/api/v1.0/users/1", follow_redirects=True, headers=headers, json=json
#      )
#      self.assertEqual(response.status_code, 200)
#      u = User.query.filter_by(username=username).first()
#      self.assertEqual(username, u.username)
#
#  def test_update_user_invalid_login(self):
#      json = {"username": "test-2", "password": "test-2"}
#      headers = generate_auth_header("user-1", "invalid")
#      response = self.app.put(
#          "/api/v1.0/users/1", follow_redirects=True, headers=headers, json=json
#      )
#      self.assertEqual(response.status_code, 401)
#
#  def test_update_user_existing_username(self):
#      json = {"username": "user-1"}
#      headers = generate_auth_header("user-1", "test1")
#      response = self.app.put(
#          "/api/v1.0/users/1", follow_redirects=True, headers=headers, json=json
#      )
#      self.assertEqual(response.status_code, 200)
#
#  def test_update_user_non_string_username(self):
#      json = {"username": 1}
#      headers = generate_auth_header("user-1", "test1")
#      response = self.app.put(
#          "/api/v1.0/users/1", follow_redirects=True, headers=headers, json=json
#      )
#      self.assertEqual(response.status_code, 400)
#
#  def test_delete_user_valid(self):
#      username = "user-1"
#      headers = generate_auth_header(username, "test1")
#      response = self.app.delete(
#          "/api/v1.0/users/1", follow_redirects=True, headers=headers
#      )
#      self.assertEqual(response.status_code, 200)
#      u = User.query.filter_by(username=username).first()
#      self.assertIsNone(u)
#
#  def test_delete_user_nonexistant_user_id(self):
#      headers = generate_auth_header("user-1", "test1")
#      response = self.app.delete(
#          "/api/v1.0/users/0", follow_redirects=True, headers=headers
#      )
#      self.assertEqual(response.status_code, 404)
#
#  def test_delete_user_invalid_user_id(self):
#      headers = generate_auth_header("user-1", "test1")
#      response = self.app.delete(
#          "/api/v1.0/users/2", follow_redirects=True, headers=headers
#      )
#      self.assertEqual(response.status_code, 401)
