from collections import defaultdict
from langdetect import detect, DetectorFactory

from mcp4cm.uml.dataloading import UMLDataset, UMLModel


def process_file(model: UMLModel) -> dict:
    """Process a single txt file to detect language."""
    if model.model_txt.strip():  # Ensure it's not empty or whitespace
        return detect(model.model_txt)
    return None

def detect_dataset_languages(dataset: UMLDataset) -> dict:
    """
    Detect the language of each model in the dataset.
    
    Args:
        dataset (UMLDataset): The dataset containing UML models.
    
    Returns:
        dict: A dictionary with detected languages for each model.
    """
    DetectorFactory.seed = 0  # Set seed for reproducibility
    language_dict = defaultdict(list)
    
    for model in dataset.models:
        if model.model_txt is None:
            continue
        lang = process_file(model)
        if lang:
            language_dict[lang].append(model)
    
    print("Language Distribution Across Models:")
    for lang, models in language_dict.items():
        print(f"Language: {lang}, Count: {len(models)}")
    
    return language_dict

def extract_non_english_models(dataset: UMLDataset) -> UMLDataset:
    """
    Extract non-English models from the dataset.
    
    Args:
        dataset (UMLDataset): The dataset containing UML models.
    
    Returns:
        UMLDataset: A new dataset containing only non-English models.
    """
    non_english_models = []
    
    for model in dataset.models:
        if model.model_txt is None:
            continue
        lang = process_file(model)
        if lang != 'en':
            non_english_models.append(model)
    
    return UMLDataset(models=non_english_models)

