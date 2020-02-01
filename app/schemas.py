from typing import List
from pydantic import BaseModel


class ConfigBase(BaseModel):
    """
    ConfigBase model columns:

        - metadata: nested key:value (json like)

        - note: str

    """

    metadata: dict
    note: str

    class ConfigBase:
        """ 
        Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict,
        but an ORM model (or any other arbitrary object with attributes).
        
        This way, instead of only trying to get the id value from a dict, as in:
        name = data['name']

        it will also try to get it from an attribute, as in:
        name = data.name
        """

        orm_mode = True


class ConfigCreate(ConfigBase):
    """
    ConfigCreate model columns:

        - name: str (config name (unique))

        - metadata: nested key:value (json like) ::fromBase

        - note: str ::fromBase

    """

    name: str


class ConfigRead(ConfigBase):
    """
    ConfigRead model columns:

        - owner: str (config owner username)

        - name: str (config name (unique))

        - metadata: nested key:value (json like) ::fromBase

        - note: str ::fromBase

    """

    owner: str
    name: str


class ConfigUpdate(ConfigBase):
    """
    ConfigUpdate model columns:

        - metadata: nested key:value (json like) ::fromBase

        - note: str ::fromBase

    """

    pass


class ConfigDelete(BaseModel):
    """
    ConfigDelete model columns:

        - owner: str (owner username)

        - name: str (config name (unique))

    """

    owner: str
    name: str


class UserBase(BaseModel):
    """
    UserBase model columns:

        - username: str (user name)

        - isadmin: bool

    """

    username: str
    isadmin: bool

    class ConfigBase:
        """ 
        Pydantic's orm_mode will tell the Pydantic model to read the data even if it is not a dict,
        but an ORM model (or any other arbitrary object with attributes).
        
        This way, instead of only trying to get the id value from a dict, as in:
        name = data['name']

        it will also try to get it from an attribute, as in:
        name = data.name
        """

        orm_mode = True


class UserCreate(UserBase):
    """
    UserCreate model columns:

        - username: str (user name) ::fromBase
 
        - password: str (user password)

        - isadmin: bool ::fromBase

    """

    password: str


class UserRead(UserBase):
    """
    UserRead model columns:

        - username: str (user name) ::fromBase

        - isadmin: bool ::fromBase

        - configs: List[ConfigBase] 

    """

    configs: List[ConfigBase] = []


class UserUpdate(UserBase):
    """
    UserUpdate model columns:

        - username: str (user name) ::fromBase

        - isadmin: bool ::fromBase

    """

    pass


class UserDelete(BaseModel):
    """
    UserDelete model columns:

        - username: str (user name)

    """

    username: str


class Token(BaseModel):
    """
    Token model used for basic auth:

        - access_token: str

        - token_type: str

    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    TokenData contain token data: 
    
        - id: int (user id)
        
    """

    username: str = None
