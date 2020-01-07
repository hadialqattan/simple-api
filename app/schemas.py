from pydantic import BaseModel


class ConfigBase(BaseModel):
    """
    To avoid confusion between the SQLAlchemy models and the Pydantic models, 
    we will have models with the SQLAlchemy models, and schemas with the Pydantic models.
    These Pydantic models define more or less a "schema" (a valid data shape).
    So this will help us avoiding confusion while using both. 
    """

    name: str
    metadata: dict


class ConfigRead(ConfigBase):
    """ Child class for reading operation """

    name: str
    metadata: dict

    class Config:
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
    """ Child class for create operation, it does not has any additional data """

    pass


class ConfigUpdate(ConfigBase):
    """ Child class for update operation, it does not has any additional data """

    pass
