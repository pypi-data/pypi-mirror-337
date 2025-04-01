from mcp4cm.uml.dataloading import load_dataset as load_uml_dataset
from base import DatasetType


def load_dataset(
    dataset_type: str, 
    path: str = 'modelset',
    uml_type: str = 'genmymodel',
    language_csv_path: str = 'categories_uml.csv'
):
    """
    Load a dataset based on the dataset type and path.
    
    Args:
        dataset_type (str): The type of dataset to load.
        path (str): The path to the dataset.
    
    Returns:
        Dataset: The loaded dataset.
    """
    if dataset_type == DatasetType.MODELSET.value:
        return load_uml_dataset(path, uml_type, language_csv_path)
    else:
        raise ValueError(f"Unknown dataset type: {dataset_type}")
    
    