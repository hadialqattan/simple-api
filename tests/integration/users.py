from multiprocessing import Process
import unittest
import requests
import uvicorn
import time

# local import
from ..IO import BASE_URL, URLs, INPUTS_USERS, OUTPUTS_USERS
from ..settings import create_users, create_configs
from app.main import app


class IntegrationTests_Users(unittest.TestCase):
    """
    Integration tests class using unittest (Users endpoints)
    """

    def __init__(self, *args, **kwargs):
        """
        self.admin_token: str (generated token from /token route for admin user)

        self.user2_token: str (second unadmin user)

        self.inputs: dict (standard tests inputs from input.py @tests dir)

        self.outputs: dict (expected outputs)

        self.urls: dict (base urls)
        """
        super(IntegrationTests_Users, self).__init__(*args, **kwargs)
        self.inputs = INPUTS_USERS()
        self.outputs = OUTPUTS_USERS()
        self.urls = URLs(True)

    @classmethod
    def setUpClass(cls):
        # create tests users
        create_users()
        # start the app
        IntegrationTests_Users.proc = Process(target=cls.run_app, args=(), daemon=True)
        IntegrationTests_Users.proc.start()
        base_url = BASE_URL()
        # wait the app
        while True:
            try:
                req = requests.get(base_url + "/docs")
                if req.status_code == 200:
                    break
            except Exception as requestErr:
                time.sleep(2.5)

    @classmethod
    def tearDownClass(cls):
        # stop the app
        IntegrationTests_Users.proc.join(2.5)

    @classmethod
    def run_app(cls):
        """
        run the app using uvicorn
        """
        uvicorn.run(app=app, host="127.0.0.1", port=5057)

    # [get_access_token : GET : /token]
    def test_01_get_access_token_success(self):
        res1 = requests.post(
            self.urls["get_access_token"],
            headers=self.inputs["test_01_get_access_token_success"]["headers"],
            data=self.inputs["test_01_get_access_token_success"]["admin"],
        )
        res2 = requests.post(
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
        IntegrationTests_Users.admin_token = res1.json()["access_token"]
        IntegrationTests_Users.user2_token = res2.json()["access_token"]

    # [get_access_token : GET : /token]
    def test_02_get_access_token_401(self):
        res = requests.post(
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
    def test_03_GetMe_success(self):
        self.inputs["test_03_GetMe_success"]["headers"]["Authorization"] = (
            self.inputs["test_03_GetMe_success"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = requests.get(
            self.urls["GetMe"], headers=self.inputs["test_03_GetMe_success"]["headers"]
        )
        assert res.status_code == self.outputs["test_03_GetMe_success"]["status_code"]
        assert res.json() == self.outputs["test_03_GetMe_success"]["json"]

    # [ListUsers : GET : /users]
    def test_04_ListUsers_success(self):
        self.inputs["test_04_ListUsers_success"]["headers"]["Authorization"] = (
            self.inputs["test_04_ListUsers_success"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = requests.get(
            self.urls["ListUsers"],
            headers=self.inputs["test_04_ListUsers_success"]["headers"],
        )
        assert (
            res.status_code == self.outputs["test_04_ListUsers_success"]["status_code"]
        )
        assert res.json() == self.outputs["test_04_ListUsers_success"]["json"]

    # [ListUsers : GET : /users]
    def test_05_ListUsers_401(self):
        self.inputs["test_05_ListUsers_401"]["headers"]["Authorization"] = (
            self.inputs["test_05_ListUsers_401"]["headers"]["Authorization"]
            % self.__class__.user2_token
        )
        res = requests.get(
            self.urls["ListUsers"],
            headers=self.inputs["test_05_ListUsers_401"]["headers"],
        )
        assert res.status_code == self.outputs["test_05_ListUsers_401"]["status_code"]
        assert res.json() == self.outputs["test_05_ListUsers_401"]["json"]

    # [GetAdmins : GET : /users/admins]
    def test_06_GetAdmins_success(self):
        self.inputs["test_06_GetAdmins_success"]["headers"]["Authorization"] = (
            self.inputs["test_06_GetAdmins_success"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = requests.get(
            self.urls["GetAdmins"],
            headers=self.inputs["test_06_GetAdmins_success"]["headers"],
        )
        assert (
            res.status_code == self.outputs["test_06_GetAdmins_success"]["status_code"]
        )
        assert res.json() == self.outputs["test_06_GetAdmins_success"]["json"]

    # [ListUsers : GET : /users]
    def test_07_GetAdmins_401(self):
        self.inputs["test_07_GetAdmins_401"]["headers"]["Authorization"] = (
            self.inputs["test_07_GetAdmins_401"]["headers"]["Authorization"]
            % self.__class__.user2_token
        )
        res = requests.get(
            self.urls["GetAdmins"],
            headers=self.inputs["test_07_GetAdmins_401"]["headers"],
        )
        assert res.status_code == self.outputs["test_07_GetAdmins_401"]["status_code"]
        assert res.json() == self.outputs["test_07_GetAdmins_401"]["json"]

    # [CreateUser : POST : /user]
    def test_08_CreateUser_success(self):
        self.inputs["test_08_CreateUser_success"]["headers"]["Authorization"] = (
            self.inputs["test_08_CreateUser_success"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = requests.post(
            self.urls["CreateUser"],
            headers=self.inputs["test_08_CreateUser_success"]["headers"],
            json=self.inputs["test_08_CreateUser_success"]["json"],
        )
        assert (
            res.status_code == self.outputs["test_08_CreateUser_success"]["status_code"]
        )
        assert res.json() == self.outputs["test_08_CreateUser_success"]["json"]

    # [CreateUser : POST : /user]
    def test_09_CreateUser_401(self):
        self.inputs["test_09_CreateUser_401"]["headers"]["Authorization"] = (
            self.inputs["test_09_CreateUser_401"]["headers"]["Authorization"]
            % self.__class__.user2_token
        )
        res = requests.post(
            self.urls["CreateUser"],
            headers=self.inputs["test_09_CreateUser_401"]["headers"],
            json=self.inputs["test_09_CreateUser_401"]["json"],
        )
        assert res.status_code == self.outputs["test_09_CreateUser_401"]["status_code"]
        assert res.json() == self.outputs["test_09_CreateUser_401"]["json"]

    # [CreateUser : POST : /user]
    def test_10_CreateUser_400(self):
        self.inputs["test_10_CreateUser_400"]["headers"]["Authorization"] = (
            self.inputs["test_10_CreateUser_400"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = requests.post(
            self.urls["CreateUser"],
            headers=self.inputs["test_10_CreateUser_400"]["headers"],
            json=self.inputs["test_10_CreateUser_400"]["json"],
        )
        assert res.status_code == self.outputs["test_10_CreateUser_400"]["status_code"]
        assert res.json() == self.outputs["test_10_CreateUser_400"]["json"]

    # [GetUser : GET : /user/{username}]
    def test_11_GetUser_success(self):
        self.inputs["test_11_GetUser_success"]["headers"]["Authorization"] = (
            self.inputs["test_11_GetUser_success"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = requests.get(
            (self.urls["GetUser"] % self.inputs["test_11_GetUser_success"]["name"]),
            headers=self.inputs["test_11_GetUser_success"]["headers"],
        )
        assert res.status_code == self.outputs["test_11_GetUser_success"]["status_code"]
        assert res.json() == self.outputs["test_11_GetUser_success"]["json"]

    # [GetUser : GET : /user/{username}]
    def test_12_GetUser_401(self):
        self.inputs["test_12_GetUser_401"]["headers"]["Authorization"] = (
            self.inputs["test_12_GetUser_401"]["headers"]["Authorization"]
            % self.__class__.user2_token
        )
        res = requests.get(
            (self.urls["GetUser"] % self.inputs["test_12_GetUser_401"]["name"]),
            headers=self.inputs["test_12_GetUser_401"]["headers"],
        )
        assert res.status_code == self.outputs["test_12_GetUser_401"]["status_code"]
        assert res.json() == self.outputs["test_12_GetUser_401"]["json"]

    # [GetUser : GET : /user/{username}]
    def test_13_GetUser_404(self):
        self.inputs["test_13_GetUser_404"]["headers"]["Authorization"] = (
            self.inputs["test_13_GetUser_404"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = requests.get(
            (self.urls["GetUser"] % self.inputs["test_13_GetUser_404"]["name"]),
            headers=self.inputs["test_13_GetUser_404"]["headers"],
        )
        assert res.status_code == self.outputs["test_13_GetUser_404"]["status_code"]
        assert res.json() == self.outputs["test_13_GetUser_404"]["json"]

    # [UpdateUser : PUT : /user/{username}/{set_admin}]
    def test_14_UpdateUser_success(self):
        self.inputs["test_14_UpdateUser_success"]["headers"]["Authorization"] = (
            self.inputs["test_14_UpdateUser_success"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = requests.put(
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
    def test_15_UpdateUser_401(self):
        self.inputs["test_15_UpdateUser_401"]["headers"]["Authorization"] = (
            self.inputs["test_15_UpdateUser_401"]["headers"]["Authorization"]
            % self.__class__.user2_token
        )
        res = requests.put(
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
    def test_16_UpdateUser_404(self):
        self.inputs["test_16_UpdateUser_404"]["headers"]["Authorization"] = (
            self.inputs["test_16_UpdateUser_404"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = requests.put(
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
    def test_17_Delete_success(self):
        self.inputs["test_17_Delete_success"]["headers"]["Authorization"] = (
            self.inputs["test_17_Delete_success"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = requests.delete(
            (
                self.urls["DeleteUser"]
                % (self.inputs["test_17_Delete_success"]["username"])
            ),
            headers=self.inputs["test_17_Delete_success"]["headers"],
        )
        assert res.status_code == self.outputs["test_17_Delete_success"]["status_code"]
        assert res.json() == self.outputs["test_17_Delete_success"]["json"]

    # [DeleteUser : Delete : /user/{username}]
    def test_18_Delete_401(self):
        self.inputs["test_18_Delete_401"]["headers"]["Authorization"] = (
            self.inputs["test_18_Delete_401"]["headers"]["Authorization"]
            % self.__class__.user2_token
        )
        res = requests.delete(
            (self.urls["DeleteUser"] % (self.inputs["test_18_Delete_401"]["username"])),
            headers=self.inputs["test_18_Delete_401"]["headers"],
        )
        assert res.status_code == self.outputs["test_18_Delete_401"]["status_code"]
        assert res.json() == self.outputs["test_18_Delete_401"]["json"]

    # [DeleteUser : Delete : /user/{username}]
    def test_19_Delete_404(self):
        self.inputs["test_19_Delete_404"]["headers"]["Authorization"] = (
            self.inputs["test_19_Delete_404"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = requests.delete(
            (self.urls["DeleteUser"] % (self.inputs["test_19_Delete_404"]["username"])),
            headers=self.inputs["test_19_Delete_404"]["headers"],
        )
        assert res.status_code == self.outputs["test_19_Delete_404"]["status_code"]
        assert res.json() == self.outputs["test_19_Delete_404"]["json"]
