from starlette.testclient import TestClient
from unittest.mock import patch
import unittest

# local import
from ..IO import BASE_URL, URLs, INPUTS_USERS, OUTPUTS_USERS, MOCK_USERS
from app.main import app


class UnitTests_Users(unittest.TestCase):
    """
    Unit tests class using unittest (Users endpoints)
    """

    def __init__(self, *args, **kwargs):
        """
        self.admin_token: str (generated token from /token route for admin user)

        self.user2_token: str (second unadmin user)

        self.inputs: dict (standard tests inputs from input.py @tests dir)

        self.outputs: dict (expected outputs)

        self.urls: dict (base urls)

        self.client: starlette.testclient.TestClient
        """
        super(UnitTests_Users, self).__init__(*args, **kwargs)
        self.inputs = INPUTS_USERS()
        self.outputs = OUTPUTS_USERS()
        self.urls = URLs(True)
        self.client = TestClient(app=app)
        self.mockdb = MOCK_USERS()

    # [get_access_token : GET : /token]
    @patch("app.auth.authenticate_user")  # 1
    @patch("app.auth.get_user")  # 2
    def test_01_get_access_token_success(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = self.mockdb["admin"]
        res1 = self.client.post(
            self.urls["get_access_token"],
            headers=self.inputs["test_01_get_access_token_success"]["headers"],
            data=self.inputs["test_01_get_access_token_success"]["admin"],
        )
        patch1.return_value = self.mockdb["user2"]
        patch2.return_value = self.mockdb["user2"]
        res2 = self.client.post(
            self.urls["get_access_token"],
            headers=self.inputs["test_01_get_access_token_success"]["headers"],
            data=self.inputs["test_01_get_access_token_success"]["user2"],
        )
        assert (
            res1.status_code
            == self.outputs["test_01_get_access_token_success"]["status_code"]
        )
        assert (
            res2.status_code
            == self.outputs["test_01_get_access_token_success"]["status_code"]
        )
        UnitTests_Users.admin_token = res1.json()["access_token"]
        UnitTests_Users.user2_token = res2.json()["access_token"]

    # [get_access_token : GET : /token]
    @patch("app.auth.get_user")  # 1
    def test_02_get_access_token_401(self, patch1):
        patch1.return_value = None
        res = self.client.post(
            self.urls["get_access_token"],
            headers=self.inputs["test_02_get_access_token_401"]["headers"],
            data=self.inputs["test_02_get_access_token_401"]["data"],
        )
        assert (
            res.status_code
            == self.outputs["test_02_get_access_token_401"]["status_code"]
        )
        assert res.json() == self.outputs["test_02_get_access_token_401"]["json"]

    # [GetMe : GET : /users/me/]
    @patch("app.auth.get_user")  # 1
    def test_03_GetMe_success(self, patch1):
        patch1.return_value = self.mockdb["admin"]
        self.inputs["test_03_GetMe_success"]["headers"]["Authorization"] = (
            self.inputs["test_03_GetMe_success"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.get(
            self.urls["GetMe"], headers=self.inputs["test_03_GetMe_success"]["headers"]
        )
        assert res.status_code == self.outputs["test_03_GetMe_success"]["status_code"]
        assert res.json() == self.outputs["test_03_GetMe_success"]["json"]

    # [ListUsers : GET : /users]
    @patch("app.auth.get_user")  # 1
    @patch("app.crud.get_users")  # 2
    def test_04_ListUsers_success(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = [self.mockdb["admin"], self.mockdb["user2"]]
        self.inputs["test_04_ListUsers_success"]["headers"]["Authorization"] = (
            self.inputs["test_04_ListUsers_success"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.get(
            self.urls["ListUsers"],
            headers=self.inputs["test_04_ListUsers_success"]["headers"],
        )
        assert (
            res.status_code == self.outputs["test_04_ListUsers_success"]["status_code"]
        )
        assert res.json() == self.outputs["test_04_ListUsers_success"]["json"]

    # [ListUsers : GET : /users]
    @patch("app.auth.get_user")  # 1
    def test_05_ListUsers_401(self, patch1):
        patch1.return_value = self.mockdb["user2"]
        self.inputs["test_05_ListUsers_401"]["headers"]["Authorization"] = (
            self.inputs["test_05_ListUsers_401"]["headers"]["Authorization"]
            % self.__class__.user2_token
        )
        res = self.client.get(
            self.urls["ListUsers"],
            headers=self.inputs["test_05_ListUsers_401"]["headers"],
        )
        assert res.status_code == self.outputs["test_05_ListUsers_401"]["status_code"]
        assert res.json() == self.outputs["test_05_ListUsers_401"]["json"]

    # [GetAdmins : GET : /users/admins]
    @patch("app.auth.get_user")  # 1
    @patch("app.crud.get_admins")  # 2
    def test_06_GetAdmins_success(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = [self.mockdb["admin"]]
        self.inputs["test_06_GetAdmins_success"]["headers"]["Authorization"] = (
            self.inputs["test_06_GetAdmins_success"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.get(
            self.urls["GetAdmins"],
            headers=self.inputs["test_06_GetAdmins_success"]["headers"],
        )
        assert (
            res.status_code == self.outputs["test_06_GetAdmins_success"]["status_code"]
        )
        assert res.json() == self.outputs["test_06_GetAdmins_success"]["json"]

    # [ListUsers : GET : /users]
    @patch("app.auth.get_user")  # 1
    def test_07_GetAdmins_401(self, patch1):
        patch1.return_value = self.mockdb["user2"]
        self.inputs["test_07_GetAdmins_401"]["headers"]["Authorization"] = (
            self.inputs["test_07_GetAdmins_401"]["headers"]["Authorization"]
            % self.__class__.user2_token
        )
        res = self.client.get(
            self.urls["GetAdmins"],
            headers=self.inputs["test_07_GetAdmins_401"]["headers"],
        )
        assert res.status_code == self.outputs["test_07_GetAdmins_401"]["status_code"]
        assert res.json() == self.outputs["test_07_GetAdmins_401"]["json"]

    # [CreateUser : POST : /user]
    @patch("app.auth.get_user")  # 1
    @patch("app.crud.get_user")  # 2
    @patch("app.crud.create_user")  # 3
    def test_08_CreateUser_success(self, patch3, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = None
        patch3.return_value = self.mockdb["test08"]
        self.inputs["test_08_CreateUser_success"]["headers"]["Authorization"] = (
            self.inputs["test_08_CreateUser_success"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.post(
            self.urls["CreateUser"],
            headers=self.inputs["test_08_CreateUser_success"]["headers"],
            json=self.inputs["test_08_CreateUser_success"]["json"],
        )
        assert (
            res.status_code == self.outputs["test_08_CreateUser_success"]["status_code"]
        )
        assert res.json() == self.outputs["test_08_CreateUser_success"]["json"]

    # [CreateUser : POST : /user]
    @patch("app.auth.get_user")  # 1
    def test_09_CreateUser_401(self, patch1):
        patch1.return_value = self.mockdb["user2"]
        self.inputs["test_09_CreateUser_401"]["headers"]["Authorization"] = (
            self.inputs["test_09_CreateUser_401"]["headers"]["Authorization"]
            % self.__class__.user2_token
        )
        res = self.client.post(
            self.urls["CreateUser"],
            headers=self.inputs["test_09_CreateUser_401"]["headers"],
            json=self.inputs["test_09_CreateUser_401"]["json"],
        )
        assert res.status_code == self.outputs["test_09_CreateUser_401"]["status_code"]
        assert res.json() == self.outputs["test_09_CreateUser_401"]["json"]

    # [CreateUser : POST : /user]
    @patch("app.auth.get_user")  # 1
    @patch("app.crud.get_user")  # 2
    def test_10_CreateUser_400(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = self.mockdb["test08"]
        self.inputs["test_10_CreateUser_400"]["headers"]["Authorization"] = (
            self.inputs["test_10_CreateUser_400"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.post(
            self.urls["CreateUser"],
            headers=self.inputs["test_10_CreateUser_400"]["headers"],
            json=self.inputs["test_10_CreateUser_400"]["json"],
        )
        assert res.status_code == self.outputs["test_10_CreateUser_400"]["status_code"]
        assert res.json() == self.outputs["test_10_CreateUser_400"]["json"]

    # [GetUser : GET : /user/{username}]
    @patch("app.auth.get_user")  # 1
    @patch("app.crud.get_user")  # 2
    def test_11_GetUser_success(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = self.mockdb["test08"]
        self.inputs["test_11_GetUser_success"]["headers"]["Authorization"] = (
            self.inputs["test_11_GetUser_success"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.get(
            (self.urls["GetUser"] % self.inputs["test_11_GetUser_success"]["name"]),
            headers=self.inputs["test_11_GetUser_success"]["headers"],
        )
        assert res.status_code == self.outputs["test_11_GetUser_success"]["status_code"]
        assert res.json() == self.outputs["test_11_GetUser_success"]["json"]

    # [GetUser : GET : /user/{username}]
    @patch("app.auth.get_user")  # 1
    def test_12_GetUser_401(self, patch1):
        patch1.return_value = self.mockdb["user2"]
        self.inputs["test_12_GetUser_401"]["headers"]["Authorization"] = (
            self.inputs["test_12_GetUser_401"]["headers"]["Authorization"]
            % self.__class__.user2_token
        )
        res = self.client.get(
            (self.urls["GetUser"] % self.inputs["test_12_GetUser_401"]["name"]),
            headers=self.inputs["test_12_GetUser_401"]["headers"],
        )
        assert res.status_code == self.outputs["test_12_GetUser_401"]["status_code"]
        assert res.json() == self.outputs["test_12_GetUser_401"]["json"]

    # [GetUser : GET : /user/{username}]
    @patch("app.auth.get_user")  # 1
    @patch("app.crud.get_user")  # 2
    def test_13_GetUser_404(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = None
        self.inputs["test_13_GetUser_404"]["headers"]["Authorization"] = (
            self.inputs["test_13_GetUser_404"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.get(
            (self.urls["GetUser"] % self.inputs["test_13_GetUser_404"]["name"]),
            headers=self.inputs["test_13_GetUser_404"]["headers"],
        )
        assert res.status_code == self.outputs["test_13_GetUser_404"]["status_code"]
        assert res.json() == self.outputs["test_13_GetUser_404"]["json"]

    # [UpdateUser : PUT : /user/{username}/{set_admin}]
    @patch("app.auth.get_user")  # 1
    @patch("app.crud.update_user")  # 2
    def test_14_UpdateUser_success(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = self.mockdb["test08"]
        self.inputs["test_14_UpdateUser_success"]["headers"]["Authorization"] = (
            self.inputs["test_14_UpdateUser_success"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.put(
            (
                self.urls["UpdateUser"]
                % (
                    self.inputs["test_14_UpdateUser_success"]["username"],
                    self.inputs["test_14_UpdateUser_success"]["set_admin"],
                )
            ),
            headers=self.inputs["test_14_UpdateUser_success"]["headers"],
        )
        assert (
            res.status_code == self.outputs["test_14_UpdateUser_success"]["status_code"]
        )
        assert res.json() == self.outputs["test_14_UpdateUser_success"]["json"]

    # [UpdateUser : PUT : /user/{username}/{set_admin}]
    @patch("app.auth.get_user")  # 1
    def test_15_UpdateUser_401(self, patch1):
        patch1.return_value = self.mockdb["user2"]
        self.inputs["test_15_UpdateUser_401"]["headers"]["Authorization"] = (
            self.inputs["test_15_UpdateUser_401"]["headers"]["Authorization"]
            % self.__class__.user2_token
        )
        res = self.client.put(
            (
                self.urls["UpdateUser"]
                % (
                    self.inputs["test_15_UpdateUser_401"]["username"],
                    self.inputs["test_15_UpdateUser_401"]["set_admin"],
                )
            ),
            headers=self.inputs["test_15_UpdateUser_401"]["headers"],
        )
        assert res.status_code == self.outputs["test_15_UpdateUser_401"]["status_code"]
        assert res.json() == self.outputs["test_15_UpdateUser_401"]["json"]

    # [UpdateUser : PUT : /user/{username}/{set_admin}]
    @patch("app.auth.get_user")  # 1
    @patch("app.crud.update_user")  # 2
    def test_16_UpdateUser_404(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = None
        self.inputs["test_16_UpdateUser_404"]["headers"]["Authorization"] = (
            self.inputs["test_16_UpdateUser_404"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.put(
            (
                self.urls["UpdateUser"]
                % (
                    self.inputs["test_16_UpdateUser_404"]["username"],
                    self.inputs["test_16_UpdateUser_404"]["set_admin"],
                )
            ),
            headers=self.inputs["test_16_UpdateUser_404"]["headers"],
        )
        assert res.status_code == self.outputs["test_16_UpdateUser_404"]["status_code"]
        assert res.json() == self.outputs["test_16_UpdateUser_404"]["json"]

    # [DeleteUser : Delete : /user/{username}]
    @patch("app.auth.get_user")  # 1
    @patch("app.crud.delete_user")  # 2
    def test_17_Delete_success(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = True
        self.inputs["test_17_Delete_success"]["headers"]["Authorization"] = (
            self.inputs["test_17_Delete_success"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.delete(
            (
                self.urls["DeleteUser"]
                % (self.inputs["test_17_Delete_success"]["username"])
            ),
            headers=self.inputs["test_17_Delete_success"]["headers"],
        )
        assert res.status_code == self.outputs["test_17_Delete_success"]["status_code"]
        assert res.json() == self.outputs["test_17_Delete_success"]["json"]

    # [DeleteUser : Delete : /user/{username}]
    @patch("app.auth.get_user")  # 1
    def test_18_Delete_401(self, patch1):
        patch1.return_value = self.mockdb["user2"]
        self.inputs["test_18_Delete_401"]["headers"]["Authorization"] = (
            self.inputs["test_18_Delete_401"]["headers"]["Authorization"]
            % self.__class__.user2_token
        )
        res = self.client.delete(
            (self.urls["DeleteUser"] % (self.inputs["test_18_Delete_401"]["username"])),
            headers=self.inputs["test_18_Delete_401"]["headers"],
        )
        assert res.status_code == self.outputs["test_18_Delete_401"]["status_code"]
        assert res.json() == self.outputs["test_18_Delete_401"]["json"]

    # [DeleteUser : Delete : /user/{username}]
    @patch("app.auth.get_user")  # 1
    @patch("app.crud.delete_user")  # 2
    def test_19_Delete_404(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = False
        self.inputs["test_19_Delete_404"]["headers"]["Authorization"] = (
            self.inputs["test_19_Delete_404"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.delete(
            (self.urls["DeleteUser"] % (self.inputs["test_19_Delete_404"]["username"])),
            headers=self.inputs["test_19_Delete_404"]["headers"],
        )
        assert res.status_code == self.outputs["test_19_Delete_404"]["status_code"]
        assert res.json() == self.outputs["test_19_Delete_404"]["json"]
