# Part B — the curriculum tasks
# TASK 02
# Word frequency with Counter

from collections import Counter
import string


# ------------------------------------------------------------
# STEP 1: Read the text file
# ------------------------------------------------------------

with open("text.txt", "r", encoding="utf-8") as f:
    text = f.read()

print("Original text:")
print(text)


# ------------------------------------------------------------
# STEP 2: Count words the hard way
# Using a normal dictionary, a loop, and .get()
# ------------------------------------------------------------

# Convert everything to lowercase
text_lower = text.lower()

# Split text into words
words = text_lower.split()

counts = {}

for word in words:
    counts[word] = counts.get(word, 0) + 1

print("\nWord counts using dictionary:")
print(counts)

print("\nNumber of unique words:", len(counts))


# ------------------------------------------------------------
# STEP 3: Count words using Counter
# ------------------------------------------------------------

counts_counter = Counter(words)

print("\nWord counts using Counter:")
print(counts_counter)

print("\nNumber of unique words:", len(counts_counter))


# ------------------------------------------------------------
# STEP 4: Print the 10 most common words
# ------------------------------------------------------------

print("\n10 most common words:")
print(counts_counter.most_common(10))


# ------------------------------------------------------------
# STEP 5: Understand punctuation problem
# ------------------------------------------------------------

# Example:
# "the" and "the." are considered different words.

print("\nPunctuation example:")

example = ["the", "the.", "the", "the."]

example_counts = Counter(example)

print(example_counts)

# Output:
# Counter({'the': 2, 'the.': 2})


# ------------------------------------------------------------
# STEP 6: Properly normalise the text
# Lowercase + remove punctuation
# ------------------------------------------------------------

# Remove punctuation
clean_text = text.lower().translate(
    str.maketrans("", "", string.punctuation)
)

# Split into words
clean_words = clean_text.split()

# Count words
clean_counts = Counter(clean_words)

print("\n10 most common words after normalisation:")
print(clean_counts.most_common(10))


# ------------------------------------------------------------
# STEP 7: Remove stopwords
# ------------------------------------------------------------

stopwords = {
    "the",
    "a",
    "an",
    "and",
    "is",
    "of",
    "to",
    "in",
    "on",
    "for",
    "with",
    "this",
    "that",
    "it",
    "as",
    "are",
    "was",
    "were",
    "be",
    "by"
}

filtered_words = [
    word for word in clean_words
    if word not in stopwords
]

filtered_counts = Counter(filtered_words)

print("\n10 most common words after removing stopwords:")
print(filtered_counts.most_common(10))


# ------------------------------------------------------------
# STEP 8: Compare the results
# ------------------------------------------------------------

print("\nComparison:")
print("Unique words using dictionary:", len(counts))
print("Unique words using Counter:", len(counts_counter))
print("Unique words after normalisation:", len(clean_counts))
print("Unique words after removing stopwords:", len(filtered_counts))