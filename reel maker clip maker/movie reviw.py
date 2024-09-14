import nltk
from nltk.corpus import movie_reviews
import random
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.pipeline import make_pipeline

# Download the necessary NLTK resources
nltk.download('movie_reviews')
nltk.download('punkt')

# Load and shuffle the movie reviews
documents = [(movie_reviews.raw(fileid), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]
random.shuffle(documents)

# Create a DataFrame
df = pd.DataFrame(documents, columns=['review', 'label'])

# Prepare the data for training and testing
X_train, X_test, y_train, y_test = train_test_split(df['review'], df['label'], test_size=0.25, random_state=42)

# Create a pipeline that includes TF-IDF vectorization and SVM classification
pipeline = make_pipeline(TfidfVectorizer(min_df=5, max_df=0.8, sublinear_tf=True, use_idf=True), SVC(kernel='linear'))

# Train the model
pipeline.fit(X_train, y_train)

# Predict and evaluate the model
y_pred = pipeline.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
