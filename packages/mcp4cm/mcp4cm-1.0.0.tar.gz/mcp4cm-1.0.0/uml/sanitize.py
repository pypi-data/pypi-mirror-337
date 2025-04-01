from typing import Dict, List
import xml.etree.ElementTree as ET
from tqdm.auto import tqdm
from uml.data_extraction import extract_names_from_model
from uml.dataloading import UMLDataset, UMLModel


def filter_empty_or_invalid_files(dataset: UMLDataset) -> Dict[str, List[UMLModel]]:
    """
    Filter out empty or invalid files from the dataset.
    
    Args:
        dataset (Dataset): The dataset to filter.
    
    Returns:
        Dataset: The filtered dataset.
    """
    filtered_models = []
    empty_models, invalid_models = [], []
    for model in tqdm(dataset.models, desc="Filtering models"):
        if not model.model_xmi:
            continue
        
        # Check if the file is empty
        if len(model.model_xmi) == 0:
            empty_models.append(model)
            continue

        try:
            # Parse the XML file
            tree = ET.ElementTree(ET.fromstring(model.model_xmi))
            tree.getroot()
            # If parsing is successful, add the model to the filtered list
            filtered_models.append(model)
        except ET.ParseError:
            invalid_models.append(model)
    
    # dataset.models = filtered_models
    print(f"Filtered out {len(empty_models)} empty models and {len(invalid_models)} invalid models.")
    return {
        'empty': empty_models,
        'invalid': invalid_models    
    }


def filter_models_without_names(dataset: UMLDataset, empty_name_pattern='empty name') -> List[UMLModel]:
    """
    Get models without names from the dataset.
    
    Args:
        dataset (Dataset): The dataset to filter.
    
    Returns:
        Dataset: The filtered dataset containing models without names.
    """
    filtered_models = list()
    empty_models = list()
    for model in tqdm(dataset.models, desc="Filtering models without names"):
        if not model.model_xmi:
            continue
        
        names = extract_names_from_model(model)
        if any(name == empty_name_pattern for name in names):
            empty_models.append(model)
            continue
        filtered_models.append(model)
    
    # dataset.models = filtered_models
    print(f"Filtered out {len(empty_models)} models with empty names.")
    return empty_models


def find_models_with_empty_class_names(dataset: UMLDataset, empty_class_name_pattern='class: empty name') -> List[UMLModel]:
    """Finds and lists files that contain 'class: empty name' entries."""
    files_with_empty_class_names = []
    filtered_models = []

    # Iterate over all files in the given directory
    for model in tqdm(dataset.models, desc="Searching for empty class names", unit="file"):
        if not model.model_xmi:
            continue
        
        if any(name == empty_class_name_pattern for name in extract_names_from_model(model, use_types=True)):
            files_with_empty_class_names.append(model)
            continue
        
        filtered_models.append(model)
    
    # dataset.models = filtered_models
    
    print(f"Found {len(files_with_empty_class_names)} files with empty class names.")
            
    return files_with_empty_class_names



def find_files_with_comments(dataset: UMLDataset, comment_pattern='comment:') -> List[UMLModel]:
    """Finds and lists files that contain comments."""
    files_with_comments = []

    # Iterate through all files in the directory
    for model in tqdm(dataset.models, desc="Searching for comments", unit="file"):
        if not model.model_xmi:
            continue
        
        if any(comment_pattern in name for name in extract_names_from_model(model, use_types=True)):
            files_with_comments.append(model)
    
    print(f"Total files containing comments: {len(files_with_comments)}")
    # dataset.models = filtered_models
    return files_with_comments
