import re

empty_name_pattern = r"empty name"
empty_class_name_pattern=r'class: empty name'
comment_pattern=r'comment:'
dummy_name_pattern = re.compile(r'^att(\s+[A-Za-z]|\s+\d+|[a-z0-9])?$', re.IGNORECASE)
dummy_class_pattern = re.compile(r'^class\s?[a-z0-9]$', re.IGNORECASE)  # Strictly match 'class 1', 'class a', etc.
general_class_pattern = re.compile(r'^[a-z]+', re.IGNORECASE)  # Match any class name
myclass_pattern = re.compile(r'^class:\s*my class\s?(\d+)?$', re.IGNORECASE)
numbered_pattern = re.compile(r'(.+?)[\s_]?(\d+)$', re.IGNORECASE)

DUMMY_KEYWORDS = {
    "my class",
    "class",
    "use case",
    "actor",
    "attribute",
    "association",
    "control flow",
    "activity",
    "decision node",
    "opaque action",
    "lifeline",
    "flow final node",
    "activity final node",
    "join node",
    "fork node",
    "initial node",
    "merge node",
    "action",
    "component",
    "ext point",
    "empty name",
    "package",
}


SEQUENTIAL_THRESHOLD = 0.75  # % of names that follow a sequential pattern
DUMMY_WORD_THRESHOLD = 0.82  # % of names that are generic dummy words
VOCABULARY_UNIQUENESS_THRESHOLD = 3  # Minimum unique words per model
GENERIC_PATTERN_THRESHOLD_COUNT = 2  # % of names that match a generic pattern
DUMMY_CLASSES_THRESHOLD = 0.5  # % of class names that are dummy classes
DUMMY_NAMES_THRESHOLD = 0.3  # % of class names that are dummy classes
SHORT_NAMES_UPPER_THRESHOLD = 0.35  # % of names that are shorter than 3 characters
SHORT_NAMES_LOWER_THRESHOLD = 0.25  # % of names that are longer than 3 characters
STOPWORDS_THRESHOLD = 0.4  # % of names that are stopwords
MIN_SHORT_NAME_LENGTH = 2  # Minimum length for short names

TFIDF_DUPLICATE_THRESHOLD = 0.8  # Threshold for TF-IDF similarity

FREQUENCT_NAMES = [
    'control flow',
    'control-flow'
]
