from enum import Enum
from pydantic import BaseModel
from typing import List, Optional, Union, Dict

class Model(BaseModel):
    id: str
    file_path: str
    hash: str
    model_json: Optional[Union[List, Dict]] = None
    model_xmi: Optional[str] = None
    model_txt: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None


class Dataset(BaseModel):
    """
    Base class for datasets.
    """
    name: str
    models: List[Model]



class DatasetType(Enum):
    """
    Enum for different datasets.
    """
    MODELSET = "modelset"
