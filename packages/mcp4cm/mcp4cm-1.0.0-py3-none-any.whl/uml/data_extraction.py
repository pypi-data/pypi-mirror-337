from collections import Counter
import re
from typing import Dict, List
import xml.etree.ElementTree as ET

import numpy as np
from uml.dataloading import UMLDataset, UMLModel
from uml.utils import ns
from matplotlib import pyplot as plt
from tqdm.auto import tqdm
from uml.filtering_patterns import (
    DUMMY_CLASSES_THRESHOLD,
    DUMMY_NAMES_THRESHOLD,
    DUMMY_WORD_THRESHOLD,
    FREQUENCT_NAMES,
    GENERIC_PATTERN_THRESHOLD_COUNT,
    MIN_SHORT_NAME_LENGTH,
    SEQUENTIAL_THRESHOLD,
    SHORT_NAMES_LOWER_THRESHOLD,
    SHORT_NAMES_UPPER_THRESHOLD,
    STOPWORDS_THRESHOLD,
    VOCABULARY_UNIQUENESS_THRESHOLD,
    empty_name_pattern,    
    empty_class_name_pattern,
    comment_pattern,
    dummy_name_pattern,
    dummy_class_pattern,
    general_class_pattern,
    myclass_pattern,
    numbered_pattern,
    DUMMY_KEYWORDS
)


def filter_empty_or_invalid_files(dataset: UMLDataset, inplace: bool = False) -> Dict[str, List[UMLModel]]:
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
    # return {
    #     'empty': empty_models,
    #     'invalid': invalid_models    
    # }
    if inplace:
        dataset.models = filtered_models
        return dataset
    return UMLDataset(name=dataset.name, models=filtered_models)


def filter_models_without_names(dataset: UMLDataset, inplace: bool = False) -> List[UMLModel]:
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
        if any(re.fullmatch(empty_name_pattern, name) for name in names):
            empty_models.append(model)
            continue
        filtered_models.append(model)
    
    # dataset.models = filtered_models
    print(f"Filtered out {len(empty_models)} models with empty names.")
    if inplace:
        dataset.models = filtered_models
        return dataset
    return UMLDataset(name=dataset.name, models=filtered_models)


def filter_models_by_name_count(dataset: UMLDataset, min_count: int = 25, max_count: int = 2000, inplace: bool = False) -> list:
    """Filter models by name count."""
    filtered_models = [
        model for model in dataset.models
        if min_count <= (len(extract_names_from_model(model)) if not model.names else len(model.names)) <= max_count
    ]
    
    print(f"Filtered models with name counts between {min_count} and {max_count}: {len(dataset.models) - len(filtered_models)}")
    if inplace:
        dataset.models = filtered_models
        return dataset
    return UMLDataset(name=dataset.name, models=filtered_models)


def filter_models_with_empty_class_names(dataset: UMLDataset, inplace: bool = False) -> List[UMLModel]:
    """Finds and lists files that contain 'class: empty name' entries."""
    files_with_empty_class_names = []
    filtered_models = []

    # Iterate over all files in the given directory
    for model in tqdm(dataset.models, desc="Searching for empty class names", unit="file"):
        if not model.model_xmi:
            continue
        
        if any(re.fullmatch(empty_class_name_pattern, name) for name in extract_names_from_model(model, use_types=True)):
            files_with_empty_class_names.append(model)
            continue
        
        filtered_models.append(model)
    
    # dataset.models = filtered_models
    
    print(f"Found {len(files_with_empty_class_names)} files with empty class names.")
            
    if inplace:
        dataset.models = filtered_models
        return dataset
    return files_with_empty_class_names



def find_files_with_comments(dataset: UMLDataset) -> List[UMLModel]:
    """Finds and lists files that contain comments."""
    files_with_comments = []

    # Iterate through all files in the directory
    for model in tqdm(dataset.models, desc="Searching for comments", unit="file"):
        if not model.model_xmi:
            continue
        
        if any(re.fullmatch(comment_pattern, name) for name in extract_names_from_model(model, use_types=True)):
            files_with_comments.append(model)
    
    print(f"Total files containing comments: {len(files_with_comments)}")
    return files_with_comments


def extract_names_from_model(model: UMLModel, use_types: bool = False, empty_name_pattern='empty name') -> list:
    """Extract names from a single XMI file, including all types of artifacts."""
    
    def split_name(name):
        """Splits camelCase, PascalCase, and snake_case names into words and converts them to lowercase."""
        name = re.sub('([a-z0-9])([A-Z])', r'\1 \2', name)
        name = re.sub('([A-Z]+)([A-Z][a-z])', r'\1 \2', name)
        name = name.replace("_", " ").lower()
        return name

    
    extracted_info = []

    try:
        tree = ET.ElementTree(ET.fromstring(model.model_xmi))
        root = tree.getroot()

        for elem in root.iter():
            xsi_type = elem.get(f"{{{ns['xsi']}}}type", None)
            if not xsi_type:
                tag_type = elem.tag.split('}')[-1]
                xsi_type = f"uml:{tag_type}"

            artifact_type = xsi_type.split(":")[-1].lower()
            if 'name' in elem.attrib:
                name = elem.attrib['name'].strip()
                name_entry = split_name(name) if name else empty_name_pattern
                formatted_name = f"{artifact_type}: {name_entry}" if use_types else name_entry
                extracted_info.append(formatted_name)

            if elem.tag.endswith('ownedComment') and 'body' in elem.attrib:
                comment = elem.attrib['body'].strip()
                formatted_comment = f"comment: {split_name(comment)}"
                content = formatted_comment if use_types else f"{split_name(comment)}"
                extracted_info.append(content)
        
        if use_types:
            model.names_with_types = extracted_info
        else:
            model.names = extracted_info

    except Exception as e:
        print(f"Error processing model {model.id}: {e}")
    return extracted_info
    

def extract_names_counts_from_dataset(dataset: UMLDataset, ascending: bool=False, plt_figs: bool= False) -> dict:
    """Extract names from all models in the dataset."""
    
    for model in dataset.models:
        if not model.names:
            extract_names_from_model(model)
    
    file_counts = {
        model.id: model.names
        for model in dataset.models
    }
    sorted_counts = dict(sorted(file_counts.items(), key=lambda item: item[1], reverse=not ascending))
    
    if plt_figs:
        plt.figure(figsize=(10, 6))
        plt.boxplot(sorted_counts.values(), vert=False)
        plt.title('Boxplot of Name Counts of Models')
        plt.xlabel('Number of Names')
        plt.show()
        
        plt.figure(figsize=(10, 6))
        plt.hist(sorted_counts.values(), bins=30, color='blue', alpha=0.7, log=True)
        plt.title('Histogram of Name Counts in Models (Log Scale)')
        plt.xlabel('Number of Names')
        plt.ylabel('Log Frequency of Models')
        plt.grid(True)
        plt.show()
    
    return sorted_counts


def get_word_counts_from_dataset(dataset: UMLDataset, plt_fig: bool = True, topk: int = 20) -> dict:
    """Get the most frequent names from the dataset."""
    models: List[UMLModel] = dataset.models
    for model in models:
        if not model.names:
            extract_names_from_model(model)
    
    print(f"Total models: {len(models)}")
    names = sum([list(set([n.strip().lower() for n in model.names if n.strip()])) for model in models], [])
    print(f"Total names: {len(names)}")
    name_counts = Counter(names)
    most_common_names = name_counts.most_common(topk)  # Get the top 20 most common names

    if plt_fig:
        plt.figure(figsize=(10, 8))
        names, counts = zip(*most_common_names)
        plt.bar(names, counts)
        plt.xlabel('Names')
        plt.ylabel('Frequency')
        plt.title(f'Top {topk} Most Frequent Names')
        plt.xticks(rotation=90)
        plt.show()

    return dict(most_common_names)


def get_name_length_distribution(dataset: UMLDataset, plt_fig: bool = True) -> dict:
    """Get the distribution of name lengths in the dataset."""
    
    def get_model_name_lengths(model: UMLModel) -> tuple:
        """Retrieve the mean and median length of names from a file."""
        names = model.names if model.names else extract_names_from_model(model)
        
        mean_length, median_length = 0, 0
        if not names:
            print(f"No names found in model {model.id}.")
        else:
            lengths = [len(name) for name in names]  # Calculate lengths of each name
            mean_length = np.mean(lengths)
            median_length = np.median(lengths)

        return {
            'mean_length': mean_length,
            'median_length': median_length
        }

    
    name_lengths = {
        model.id: get_model_name_lengths(model)
        for model in dataset.models
    }
    
    mean_lengths = [length[0] for length in name_lengths]
    median_lengths = [length[1] for length in name_lengths]

    if plt_fig:
        plt.figure(figsize=(10, 6))
        plt.hist(mean_lengths, bins=30, color='blue', alpha=0.7, label='Mean Lengths')
        plt.hist(median_lengths, bins=30, color='orange', alpha=0.7, label='Median Lengths')
        plt.title('Distribution of Name Lengths in Models')
        plt.xlabel('Length of Names')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True)
        plt.show()

    return name_lengths


def filter_models_by_name_length_or_stopwords(
    dataset: UMLDataset, 
    length_upper_threshold: float = SHORT_NAMES_UPPER_THRESHOLD, 
    length_lower_threshold: float = SHORT_NAMES_LOWER_THRESHOLD, 
    stopword_threshold: float = STOPWORDS_THRESHOLD,
    min_name_length: int = MIN_SHORT_NAME_LENGTH,
    inplace: bool = False
) -> list:
    
    def analyze_names(names: List[str]) -> bool:
        """ Analyze the names to categorize files based on criteria """
        short_names = [name for name in names if len(name.strip()) <= min_name_length]
        stopwords_count = sum(1 for name in names if any(stopword in name.lower() for stopword in FREQUENCT_NAMES))
        
        short_name_ratio = len(short_names) / len(names)
        stopwords_ratio = stopwords_count / len(names)
        

        criteria_1 = short_name_ratio > length_upper_threshold
        criteria_2 = short_name_ratio >= length_lower_threshold and stopwords_ratio >= stopword_threshold

        return criteria_1, criteria_2

    criteria_one_models, criteria_two_models = list(), list()
    filtered_models = list()
    # Iterate over files in the directory
    models: List[UMLModel] = dataset.models
    for model in models:
        names = model.names if model.names else extract_names_from_model(model)        

        c1, c2 = analyze_names(names)
        if c1:
            criteria_one_models.append(model.id)
        if c2:
            criteria_two_models.append(model.id)
        
        if not c1 and not c2:
            filtered_models.append(model)
            
        

    # Output results
    print(f"Flagged models with > {length_upper_threshold*100}% short names: {len(criteria_one_models)}")
    print(f"Flagged models with >= {length_lower_threshold*100}% short names and >= {stopword_threshold*100}% of stopwords: {len(criteria_two_models)}")
    
    print(f"Filtered models: {len(filtered_models)}")
    # dataset.models = filtered_models
    if inplace:
        dataset.models = filtered_models
        return dataset
    return UMLDataset(name=dataset.name, models=filtered_models)


def filter_dummy_names(dataset: UMLDataset, threshold: float = DUMMY_NAMES_THRESHOLD, inplace: bool = False) -> list:
    """Filter models with dummy names."""
    filtered_models = []
    dummy_models = []

    for model in tqdm(dataset.models, desc="Filtering dummy names"):
        if not model.model_xmi:
            continue
        
        names = extract_names_from_model(model)
        dummy_names_count = sum(1 for name in names if dummy_name_pattern.match(name))
        dummy_ratio = dummy_names_count / len(names) if names else 0
        
        if dummy_ratio >= threshold:
            dummy_models.append((model.id, len(names), dummy_names_count, dummy_ratio))
            continue
        filtered_models.append(model)
    
    # Output results
    dummy_models.sort(key=lambda x: x[3], reverse=True)
    print(f"Flagged models based on dummy name percentage (Threshold: {threshold*100}%)\nShowing Top 10")
    for file, total, dummy, ratio in dummy_models[:10]:  # Show first 10 for preview
        print(f"{file} - {dummy}/{total} names ({ratio:.2%} dummy)")

    if inplace:
        dataset.models = filtered_models
        return dataset
    return UMLDataset(name=dataset.name, models=filtered_models)


def filter_dummy_classes(dataset: UMLDataset, threshold: float = DUMMY_CLASSES_THRESHOLD, inplace: bool = False) -> list:
    """Filter models with dummy class names."""
    filtered_models = []
    files_fully_dummy = []
    files_mostly_valid = []
    files_mixed_classes = []

    for model in tqdm(dataset.models, desc="Filtering dummy classes"):
        if not model.model_xmi:
            continue
        
        names = extract_names_from_model(model, use_types=True) if not model.names_with_types else model.names_with_types
        
        dummy_count, valid_count, dummy_found = 0, 0, False
        for name in names:
            
            type_name = name.strip().split(':')  # Splitting line into type and name
            if len(type_name) < 2:  # Ensure there is a type and a name
                continue
            
            artifact_type, name = type_name[0].strip().lower(), type_name[1].strip()
            if artifact_type == "class":  # Only process class types
                if dummy_class_pattern.match(name):
                    dummy_count += 1
                    dummy_found = True  # Set flag on finding a dummy name
                elif general_class_pattern.match(name):
                    valid_count += 1
                    
            if dummy_found:  # Only process further if a dummy name was found
                # Evaluate file based on counts
                total_classes = dummy_count + valid_count
                if total_classes == 0:
                    continue  # Avoid division by zero, handle files with no class definitions

                dummy_ratio = dummy_count / total_classes
                # Define thresholds
                if dummy_ratio > threshold:
                    files_fully_dummy.append(model.id)
                elif dummy_count > 0 and dummy_ratio <= 0.13:  # Less than 10% dummy names
                    files_mixed_classes.append(model.id)
                else:
                    files_mostly_valid.append(model.id)
            else:
                filtered_models.append(model)
    
    # Output results
    print(f"Flagged models based on dummy class percentage (Threshold: {threshold*100}%)")
    print(f"Files fully dummy: {len(files_fully_dummy)}")
    print(f"Files mostly valid (with few dummy classes): {len(files_mostly_valid)}")
    print(f"Files with a mix of dummy and non-dummy classes: {len(files_mixed_classes)}")
    print(f"Filtered models: {len(filtered_models)}")
    
    if inplace:
        dataset.models = filtered_models
        return dataset
    return UMLDataset(name=dataset.name, models=filtered_models)


def filter_classes_by_generic_pattern(dataset: UMLDataset, threshold_count: int = GENERIC_PATTERN_THRESHOLD_COUNT, inplace: bool = False) -> list:
    """Filter models with generic class names."""
    filtered_models = []
    generic_classes = []

    for model in tqdm(dataset.models, desc="Filtering generic classes"):
        if not model.model_xmi:
            continue
        
        names = extract_names_from_model(model, use_types=True) if not model.names_with_types else model.names_with_types
        
        name_count = sum(1 for name in names if myclass_pattern.match(name))
        if name_count >= threshold_count:
            generic_classes.append((model.id, len(names), name_count))
            continue
        filtered_models.append(model)
    
    # Output results
    print("Files containing more than one 'class: my class' or 'class: my class' followed by a number:")
    print(f"Filtered models based on generic class names (Threshold: {threshold_count})")
    for file, total, count in generic_classes:
        print(f"{file} - {count}/{total} names")
    
    print(f"Filtered models: {len(filtered_models)}")
    
    if inplace:
        dataset.models = filtered_models
        return dataset
    return UMLDataset(name=dataset.name, models=filtered_models)


def filter_models_by_sequential_and_dummy_words(
    dataset: UMLDataset, 
    sequential_threshold: float = SEQUENTIAL_THRESHOLD,
    dummy_word_threshold: float = DUMMY_WORD_THRESHOLD,
    vocabulary_uniqueness_threshold: int = VOCABULARY_UNIQUENESS_THRESHOLD,
    inplace: bool = False
) -> list:
    """Filter models by sequential and dummy words."""
    filtered_models = []
    flagged_models = []
    

    for model in tqdm(dataset.models, desc="Filtering sequential and dummy words"):
        if not model.model_xmi:
            continue
        
        names = extract_names_from_model(model)
        
        # Check for sequential patterns
        sequential_count = sum(1 for name in names if numbered_pattern.match(name))
        sequential_ratio = sequential_count / len(names)
        
        # Check for dummy words
        dummy_count = sum(1 for name in names if any(dw in name for dw in DUMMY_KEYWORDS))
        dummy_ratio = dummy_count / len(names)
        
        # Check for vocabulary uniqueness
        words = [word for name in names for word in name.split()]
        unique_words = set(words)
        # Flagging condition
        if (
            sequential_ratio >= sequential_threshold or  # Too many numbered names
            dummy_ratio >= dummy_word_threshold or  # Too many generic words
            len(unique_words) <= vocabulary_uniqueness_threshold  # Low vocabulary richness
        ):
            flagged_models.append((model.id, len(names), sequential_ratio, dummy_ratio, len(unique_words)))
        else:
            filtered_models.append(model)
    
    # Output results
    print(f"Flagged models based on sequential patterns (Threshold: {sequential_threshold*100}%)")
    print(f"Flagged models based on dummy word percentage (Threshold: {dummy_word_threshold*100}%)")
    print(f"Flagged models based on vocabulary uniqueness (Threshold: {vocabulary_uniqueness_threshold})")
    
    for file, total, seq_ratio, dummy_ratio, vocab_count in flagged_models:
        print(f"{file} - {total} names, {seq_ratio:.2%} sequential, {dummy_ratio:.2%} dummy words, {vocab_count} unique words")
    print(f"Filtered models: {len(filtered_models)}")
    if inplace:
        dataset.models = filtered_models
        return dataset
    return UMLDataset(name=dataset.name, models=filtered_models)