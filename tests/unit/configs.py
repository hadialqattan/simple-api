from starlette.testclient import TestClient
from unittest.mock import patch
import unittest

# local import
from ..IO import BASE_URL, URLs, INPUTS_CONFIGS, OUTPUTS_CONFIGS, MOCK_CONFIGS
from app.main import app


class UnitTests_Configs(unittest.TestCase):
    """
    Unit tests class using unittest (Configs endpoints)
    """

    def __init__(self, *args, **kwargs):
        """
        self.inputs: dict (standard tests inputs from input.py @tests dir)

        self.outputs: dict (expected tests outputs)

        self.urls: dict (base urls)

        self.client: starlette.testclient.TestClient
        """
        super(UnitTests_Configs, self).__init__(*args, **kwargs)
        self.inputs = INPUTS_CONFIGS()
        self.outputs = OUTPUTS_CONFIGS()
        self.urls = URLs(True)
        self.client = TestClient(app=app)
        self.mockdb = MOCK_CONFIGS()

    # [get_access_token : GET : /token]
    @patch("app.auth.authenticate_user") #1
    @patch("app.auth.get_user") #2
    def test_00_create_access_token_for_admin_and_user2(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = self.mockdb["admin"]
        res1 = self.client.post(
            self.urls["get_access_token"],
            headers=self.inputs["test_00_create_access_token_for_admin_and_user2"]["headers"],
            data=self.inputs["test_00_create_access_token_for_admin_and_user2"]["admin"],
        )
        patch1.return_value = self.mockdb["user2"]
        patch2.return_value = self.mockdb["user2"]
        res2 = self.client.post(
            self.urls["get_access_token"],
            headers=self.inputs["test_00_create_access_token_for_admin_and_user2"]["headers"],
            data=self.inputs["test_00_create_access_token_for_admin_and_user2"]["user2"],
        )
        assert res1.status_code == self.outputs["test_00_create_access_token_for_admin_and_user2"]["status_code"]
        assert res2.status_code == self.outputs["test_00_create_access_token_for_admin_and_user2"]["status_code"]
        UnitTests_Configs.admin_token = res1.json()["access_token"]
        UnitTests_Configs.user2_token = res2.json()["access_token"]

    # [List : GET : /configs]
    @patch("app.auth.get_user") #1
    @patch("app.crud.get_configs") #2
    def test_01_List_success(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = [self.mockdb["datacenter-1"], self.mockdb["datacenter-2"]]
        self.inputs["test_01_List_success"]["headers"]["Authorization"] = (
            self.inputs["test_01_List_success"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.get(
            self.urls["List"], 
            headers = self.inputs["test_01_List_success"]["headers"]
        )
        assert res.status_code == self.outputs["test_01_List_success"]["status_code"]
        assert res.json() == self.outputs["test_01_List_success"]["json"]

    # [List : GET : /configs]
    @patch("app.auth.get_user") #1
    @patch("app.crud.get_configs") #2
    def test_02_List_success_owner(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = [self.mockdb["datacenter-2"]]
        self.inputs["test_02_List_success_owner"]["headers"]["Authorization"] = (
            self.inputs["test_02_List_success_owner"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.get(
            self.urls["List"] + '?owner=' + self.inputs["test_02_List_success_owner"]["owner"], 
            headers = self.inputs["test_02_List_success_owner"]["headers"]
        )
        assert res.status_code == self.outputs["test_02_List_success_owner"]["status_code"]
        assert res.json() == self.outputs["test_02_List_success_owner"]["json"]

    # [List : GET : /configs]
    @patch("app.auth.get_user") #1
    def test_03_List_401(self, patch1):
        patch1.return_value = self.mockdb["user2"]
        self.inputs["test_03_List_401"]["headers"]["Authorization"] = (
            self.inputs["test_03_List_401"]["headers"]["Authorization"]
            % self.__class__.user2_token
        )
        res = self.client.get(
            self.urls["List"] + '?owner=' + self.inputs["test_03_List_401"]["owner"], 
            headers= self.inputs["test_03_List_401"]["headers"]
        )
        assert res.status_code == self.outputs["test_03_List_401"]["status_code"]
        assert res.json() == self.outputs["test_03_List_401"]["json"]

    # [Create : POST : /configs]
    @patch("app.auth.get_user") #1
    @patch("app.crud.get_config") #2
    @patch("app.crud.create_config") #3
    def test_04_Create_success(self, patch3, patch2, patch1):
        patch1.return_value = self.mockdb["user2"]
        patch2.return_value = None
        patch3.return_value = self.mockdb["datacenter-3"]
        self.inputs["test_04_Create_success"]["headers"]["Authorization"] = (
            self.inputs["test_04_Create_success"]["headers"]["Authorization"]
            % self.__class__.user2_token
        )
        res = self.client.post(
            self.urls["Create"], 
            headers= self.inputs["test_04_Create_success"]["headers"], 
            json= self.inputs["test_04_Create_success"]["json"]
        )
        assert res.status_code == self.outputs["test_04_Create_success"]["status_code"]
        assert res.json() == self.outputs["test_04_Create_success"]["json"]


    # [Create : POST : /configs]
    @patch("app.auth.get_user") #1
    @patch("app.crud.get_config") #2
    def test_05_Create_400(self, patch2, patch1): 
        patch1.return_value = self.mockdb["user2"]
        patch2.return_value = self.mockdb["datacenter-3"]
        self.inputs["test_05_Create_400"]["headers"]["Authorization"] = (
            self.inputs["test_05_Create_400"]["headers"]["Authorization"]
            % self.__class__.user2_token
        )
        res = self.client.post(
            self.urls["Create"], 
            headers= self.inputs["test_05_Create_400"]["headers"], 
            json= self.inputs["test_05_Create_400"]["json"]
        )
        assert res.status_code == self.outputs["test_05_Create_400"]["status_code"]
        assert res.json() == self.outputs["test_05_Create_400"]["json"]

    # [Get : GET : /configs/{name}]
    @patch("app.auth.get_user") #1
    @patch("app.crud.get_config") #2
    def test_06_Get_success(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = self.mockdb["datacenter-1"]
        self.inputs["test_06_Get_success"]["headers"]["Authorization"] = (
            self.inputs["test_06_Get_success"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.get(
            (self.urls["Get"] % self.inputs["test_06_Get_success"]["name"]), 
            headers= self.inputs["test_06_Get_success"]["headers"]
        )
        assert res.status_code == self.outputs["test_06_Get_success"]["status_code"]
        assert res.json() == self.outputs["test_06_Get_success"]["json"]

    # [Get : GET : /configs/{name}]
    @patch("app.auth.get_user") #1
    @patch("app.crud.get_config") #2
    def test_07_Get_success_owner(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = self.mockdb["datacenter-1"]
        self.inputs["test_07_Get_success_owner"]["headers"]["Authorization"] = (
            self.inputs["test_07_Get_success_owner"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.get(
            (self.urls["Get"] % (self.inputs["test_07_Get_success_owner"]["name"]) + '?owner=' + self.inputs["test_07_Get_success_owner"]["owner"]), 
            headers= self.inputs["test_07_Get_success_owner"]["headers"]
        )
        assert res.status_code == self.outputs["test_07_Get_success_owner"]["status_code"]
        assert res.json() == self.outputs["test_07_Get_success_owner"]["json"]

    # [Get : GET : /configs/{name}]
    @patch("app.auth.get_user") #1
    def test_08_Get_401(self, patch1):
        patch1.return_value = self.mockdb["user2"]
        self.inputs["test_08_Get_401"]["headers"]["Authorization"] = (
            self.inputs["test_08_Get_401"]["headers"]["Authorization"]
            % self.__class__.user2_token
        )
        res = self.client.get(
            (self.urls["Get"] % (self.inputs["test_08_Get_401"]["name"]) + '?owner=' + self.inputs["test_07_Get_success_owner"]["owner"]), 
            headers= self.inputs["test_08_Get_401"]["headers"]
        )
        assert res.status_code == self.outputs["test_08_Get_401"]["status_code"]
        assert res.json() == self.outputs["test_08_Get_401"]["json"]

    # [Get : GET : /configs/{name}]
    @patch("app.auth.get_user") #1
    def test_09_Get_404(self, patch1):
        patch1.return_value = self.mockdb["admin"]
        self.inputs["test_09_Get_404"]["headers"]["Authorization"] = (
            self.inputs["test_09_Get_404"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.get(
            (self.urls["Get"] % (self.inputs["test_09_Get_404"]["name"]) + '?owner=' + self.inputs["test_07_Get_success_owner"]["owner"]), 
            headers= self.inputs["test_09_Get_404"]["headers"]
        )
        assert res.status_code == self.outputs["test_09_Get_404"]["status_code"]
        assert res.json() == self.outputs["test_09_Get_404"]["json"]

    # [Update : PUT : /configs/{name}]
    @patch("app.auth.get_user") #1
    @patch("app.crud.update_config") #2
    def test_10_Update_success(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = self.mockdb["datacenter-32"]
        self.inputs["test_10_Update_success"]["headers"]["Authorization"] = (
            self.inputs["test_10_Update_success"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.put(
            (self.urls["Update"] % self.inputs["test_10_Update_success"]["name"]), 
            headers= self.inputs["test_10_Update_success"]["headers"], 
            json=self.inputs["test_10_Update_success"]["json"]
        )
        assert res.status_code == self.outputs["test_10_Update_success"]["status_code"]
        assert res.json() == self.outputs["test_10_Update_success"]["json"]

    # [Update : PUT : /configs/{name}]
    @patch("app.auth.get_user") #1
    @patch("app.crud.update_config") #2
    def test_11_Update_success_owner(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = self.mockdb["datacenter-33"]
        self.inputs["test_11_Update_success_owner"]["headers"]["Authorization"] = (
            self.inputs["test_11_Update_success_owner"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.put(
            (self.urls["Update"] % self.inputs["test_11_Update_success_owner"]["name"]) + '?owner=' + self.inputs["test_11_Update_success_owner"]["owner"], 
            headers= self.inputs["test_11_Update_success_owner"]["headers"], 
            json=self.inputs["test_11_Update_success_owner"]["json"]
        )
        assert res.status_code == self.outputs["test_11_Update_success_owner"]["status_code"]
        assert res.json() == self.outputs["test_11_Update_success_owner"]["json"]

    # [Update : PUT : /configs/{name}]
    @patch("app.auth.get_user") #1
    def test_12_Update_401(self, patch1):
        patch1.return_value = self.mockdb["user2"]
        self.inputs["test_12_Update_401"]["headers"]["Authorization"] = (
            self.inputs["test_12_Update_401"]["headers"]["Authorization"]
            % self.__class__.user2_token
        )
        res = self.client.put(
            (self.urls["Update"] % (self.inputs["test_12_Update_401"]["name"]) + '?owner=' + self.inputs["test_12_Update_401"]["owner"]), 
            headers= self.inputs["test_12_Update_401"]["headers"], 
            json=self.inputs["test_12_Update_401"]["json"]
        )
        assert res.status_code == self.outputs["test_12_Update_401"]["status_code"]
        assert res.json() == self.outputs["test_12_Update_401"]["json"]

    # [Update : PUT : /configs/{name}]
    @patch("app.auth.get_user") #1
    def test_13_Update_404(self, patch1):
        patch1.return_value = self.mockdb["admin"]
        self.inputs["test_13_Update_404"]["headers"]["Authorization"] = (
            self.inputs["test_13_Update_404"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.put(
            (self.urls["Update"] % (self.inputs["test_13_Update_404"]["name"]) + '?owner=' + self.inputs["test_13_Update_404"]["owner"]), 
            headers= self.inputs["test_13_Update_404"]["headers"], 
            json=self.inputs["test_13_Update_404"]["json"]
        )
        assert res.status_code == self.outputs["test_13_Update_404"]["status_code"]
        assert res.json() == self.outputs["test_13_Update_404"]["json"]

    # [Delete : Delete : /configs/{name}]
    @patch("app.auth.get_user") #1
    @patch("app.crud.delete_config") #2
    def test_14_Delete_success(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = True
        self.inputs["test_14_Delete_success"]["headers"]["Authorization"] = (
            self.inputs["test_14_Delete_success"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.delete(
            (self.urls["Delete"] % self.inputs["test_14_Delete_success"]["name"]), 
            headers= self.inputs["test_14_Delete_success"]["headers"]
        )
        assert res.status_code == self.outputs["test_14_Delete_success"]["status_code"]
        assert res.json() == self.outputs["test_14_Delete_success"]["json"]

    # [Delete : Delete : /configs/{name}]
    @patch("app.auth.get_user") #1
    @patch("app.crud.delete_config") #2
    def test_15_Delete_success_owner(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = True
        self.inputs["test_15_Delete_success_owner"]["headers"]["Authorization"] = (
            self.inputs["test_15_Delete_success_owner"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.delete(
            (self.urls["Delete"] % self.inputs["test_15_Delete_success_owner"]["name"]) + '?owner=' + self.inputs["test_15_Delete_success_owner"]["owner"], 
            headers= self.inputs["test_15_Delete_success_owner"]["headers"]
        )
        assert res.status_code == self.outputs["test_15_Delete_success_owner"]["status_code"]
        assert res.json() == self.outputs["test_15_Delete_success_owner"]["json"]

    # [Delete : Delete : /configs/{name}]
    @patch("app.auth.get_user") #1
    def test_16_Delete_401(self, patch1):
        patch1.return_value = self.mockdb["user2"]
        self.inputs["test_16_Delete_401"]["headers"]["Authorization"] = (
            self.inputs["test_16_Delete_401"]["headers"]["Authorization"]
            % self.__class__.user2_token
        )
        res = self.client.delete(
            (self.urls["Delete"] % (self.inputs["test_16_Delete_401"]["name"]) + '?owner=' + self.inputs["test_16_Delete_401"]["owner"]), 
            headers= self.inputs["test_16_Delete_401"]["headers"]
        )
        assert res.status_code == self.outputs["test_16_Delete_401"]["status_code"]
        assert res.json() == self.outputs["test_16_Delete_401"]["json"]

    # [Delete : Delete : /configs/{name}]
    @patch("app.auth.get_user") #1
    @patch("app.crud.delete_config") #2
    def test_17_Delete_404(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = False
        self.inputs["test_17_Delete_404"]["headers"]["Authorization"] = (
            self.inputs["test_17_Delete_404"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.delete(
            (self.urls["Delete"] % (self.inputs["test_17_Delete_404"]["name"]) + '?owner=' + self.inputs["test_17_Delete_404"]["owner"]), 
            headers= self.inputs["test_17_Delete_404"]["headers"]
        )
        assert res.status_code == self.outputs["test_17_Delete_404"]["status_code"]
        assert res.json() == self.outputs["test_17_Delete_404"]["json"]
        
    # [Query : GET : /search/metadata.{key}={value}]
    @patch("app.auth.get_user") #1
    @patch("app.crud.query_metadata") #2
    def test_18_Query_success(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = [self.mockdb["datacenter-1"]]
        self.inputs["test_18_Query_success"]["headers"]["Authorization"] = (
            self.inputs["test_18_Query_success"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.get(
            (self.urls["Query"] % (self.inputs["test_18_Query_success"]["key"], self.inputs["test_18_Query_success"]["value"]) + "?all=" + self.inputs["test_18_Query_success"]["all"]), 
            headers= self.inputs["test_18_Query_success"]["headers"]
        )
        assert res.status_code == self.outputs["test_18_Query_success"]["status_code"]
        assert res.json() == self.outputs["test_18_Query_success"]["json"]

    # [Query : GET : /search/metadata.{key}={value}]
    @patch("app.auth.get_user") #1
    @patch("app.crud.query_metadata") #2
    def test_19_Query_success_all(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = [self.mockdb["datacenter-1"]]
        self.inputs["test_19_Query_success_all"]["headers"]["Authorization"] = (
            self.inputs["test_19_Query_success_all"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.get(
            (self.urls["Query"] % (self.inputs["test_19_Query_success_all"]["key"], self.inputs["test_19_Query_success_all"]["value"]) + "?all=" + self.inputs["test_19_Query_success_all"]["all"]), 
            headers= self.inputs["test_19_Query_success_all"]["headers"]
        )
        assert res.status_code == self.outputs["test_19_Query_success_all"]["status_code"]
        assert res.json() == self.outputs["test_19_Query_success_all"]["json"]

    # [Query : GET : /search/metadata.{key}={value}]
    @patch("app.auth.get_user") #1
    @patch("app.crud.query_metadata") #2
    def test_20_Query_success_owner(self, patch2, patch1):
        patch1.return_value = self.mockdb["admin"]
        patch2.return_value = [self.mockdb["datacenter-1"]]
        self.inputs["test_20_Query_success_owner"]["headers"]["Authorization"] = (
            self.inputs["test_20_Query_success_owner"]["headers"]["Authorization"]
            % self.__class__.admin_token
        )
        res = self.client.get(
            (self.urls["Query"] % (self.inputs["test_20_Query_success_owner"]["key"], self.inputs["test_20_Query_success_owner"]["value"])) + "?all=" + self.inputs["test_20_Query_success_owner"]["all"] + "&owner=" + self.inputs["test_20_Query_success_owner"]["owner"], 
            headers= self.inputs["test_20_Query_success_owner"]["headers"]
        )
        assert res.status_code == self.outputs["test_20_Query_success_owner"]["status_code"]
        assert res.json() == self.outputs["test_20_Query_success_owner"]["json"]

    # [Query : GET : /search/metadata.{key}={value}]
    @patch("app.auth.get_user") #1
    def test_21_Query_401(self, patch1):
        patch1.return_value = self.mockdb["user2"]
        self.inputs["test_21_Query_401"]["headers"]["Authorization"] = (
            self.inputs["test_21_Query_401"]["headers"]["Authorization"]
            % self.__class__.user2_token
        )
        res = self.client.get(
            (self.urls["Query"] % (self.inputs["test_21_Query_401"]["key"], self.inputs["test_21_Query_401"]["value"]) + "?all=" + self.inputs["test_21_Query_401"]["all"]), 
            headers= self.inputs["test_21_Query_401"]["headers"]
        )
        assert res.status_code == self.outputs["test_21_Query_401"]["status_code"]
        assert res.json() == self.outputs["test_21_Query_401"]["json"]
