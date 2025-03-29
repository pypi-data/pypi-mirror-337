# Import necessary libraries
import pandas as pd
from hazm import Normalizer, word_tokenize, Stemmer, stopwords_list
import re
from tqdm import tqdm
from gensim.models import Word2Vec
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import os
import joblib

class CommentAnalyzer:
    def __init__(self, model_dir='PerSent/model'):
        """
        Initialize the CommentAnalyzer with Persian text processing tools
        and model directory setup.
        """
        self.normalizer = Normalizer()
        self.stemmer = Stemmer()
        self.stopwords = set(stopwords_list())
        self.model_dir = model_dir
        self.vectorizer = None
        self.classifier = None
        
        # Create model directory if it doesn't exist
        os.makedirs(self.model_dir, exist_ok=True)
        
    def _preprocess_text(self, text):
        """
        Preprocess Persian text by:
        - Normalizing
        - Removing numbers and special characters
        - Tokenizing
        - Stemming
        - Removing stopwords
        """
        # Normalize Persian text
        text = self.normalizer.normalize(str(text))
        
        # Remove numbers and special characters
        text = re.sub(r'[!()-\[\]{};:\'",؟<>./?@#$%^&*_~۰-۹\d]+', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenize and stem words
        tokens = word_tokenize(text)
        processed_tokens = [
            self.stemmer.stem(token)
            for token in tokens
            if token not in self.stopwords and len(token) > 1
        ]
        
        return processed_tokens
    
    def _sentence_vector(self, sentence, model):
        """
        Convert a sentence to a vector by averaging word vectors
        from the Word2Vec model.
        """
        vectors = []
        for word in sentence:
            try:
                vectors.append(model.wv[word])
            except KeyError:
                vectors.append(np.zeros(100))  # Default vector for unknown words
        return np.mean(vectors, axis=0) if vectors else np.zeros(100)
    
    def train(self, train_csv, test_size=0.2, vector_size=100, window=5):
        """
        Train the sentiment analysis model:
        1. Preprocess training data
        2. Train Word2Vec embeddings
        3. Train Logistic Regression classifier
        """
        # Read and preprocess training data
        df = pd.read_csv(train_csv)
        df['tokens'] = df['body'].apply(self._preprocess_text)
        
        # Train Word2Vec model
        self.vectorizer = Word2Vec(
            sentences=df['tokens'],
            vector_size=vector_size,
            window=window,
            min_count=1,
            workers=4
        )
        
        # Convert sentences to vectors
        X = np.array([self._sentence_vector(s, self.vectorizer) for s in df['tokens']])
        y = df['recommendation_status'].map({
            "no_idea": 2,
            "recommended": 1,
            "not_recommended": 0
        }).values
        
        # Split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)

        # Train classifier
        self.classifier = LogisticRegression(max_iter=1000)
        self.classifier.fit(X_train, y_train)
        
        # Save trained models
        self.save_model()
        
        # Return model accuracy
        accuracy = self.classifier.score(X_test, y_test)
        return accuracy
    
    def predict(self, text):
        """
        Predict sentiment of a single text input.
        Returns one of: 'recommended', 'not_recommended', or 'no_idea'
        """
        if not self.classifier or not self.vectorizer:
            raise Exception("Model not trained! Call train() first or load a pretrained model.")
            
        tokens = self._preprocess_text(text)
        vector = self._sentence_vector(tokens, self.vectorizer)
        prediction = self.classifier.predict([vector])[0]
        
        return {
            0: "not_recommended",
            1: "recommended",
            2: "no_idea"
        }[prediction]
    
    def save_model(self):
        """Save trained models to disk"""
        joblib.dump(self.classifier, os.path.join(self.model_dir, 'classifier.joblib'))
        self.vectorizer.save(os.path.join(self.model_dir, 'word2vec.model'))
    
    def load_model(self):
        """Load trained models from disk"""
        self.classifier = joblib.load(os.path.join(self.model_dir, 'classifier.joblib'))
        self.vectorizer = Word2Vec.load(os.path.join(self.model_dir, 'word2vec.model'))
        
    def csvPredict(self, input_csv, output_path, summary_path=None, text_column=0):
        """
        Analyze sentiment for all comments in a CSV file and save results.
        
        Args:
            input_csv: Path to input CSV file
            output_path: Path to save results CSV
            summary_path: Optional path to save summary statistics
            text_column: Column name or index containing text to analyze
        """
        try:
            # Read input data
            df = pd.read_csv(input_csv)
            
            # Determine text column
            if isinstance(text_column, int):
                if text_column < 0:
                    text_column = len(df.columns) + text_column
                    
                if text_column >= len(df.columns) or text_column < 0:
                    raise ValueError(f"Column index {text_column} is out of range")
                    
                column_name = df.columns[text_column]
            else:
                if text_column not in df.columns:
                    raise ValueError(f"Column '{text_column}' not found in CSV file")
                column_name = text_column
            
            # Enable tqdm progress bar for pandas apply
            tqdm.pandas(desc="Analyzing comments")
            
            # Apply sentiment analysis with progress bar
            df['sentiment'] = df[column_name].progress_apply(self.predict)
            
            # Save results
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"Results saved to {output_path}")
            
            # Generate summary if requested
            if summary_path:
                summary = self._generate_summary(df)
                summary.to_csv(summary_path, index=False, encoding='utf-8-sig')
                print(f"Summary report saved to {summary_path}")
            
            return df
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return None

    def _generate_summary(self, df):
        """Generate summary statistics of sentiment predictions"""
        # Count sentiment distribution
        counts = df['sentiment'].value_counts().to_dict()
        
        # Create summary dataframe
        summary = pd.DataFrame({
            'Category': [
                'Recommended',
                'Not Recommended', 
                'No Idea',
                'Total',
                'Model Accuracy'
            ],
            'Count': [
                counts.get('recommended', 0),
                counts.get('not_recommended', 0),
                counts.get('no_idea', 0),
                len(df),
                'N/A'  # Accuracy is only available during training
            ],
            'Percentage': [
                f"{100 * counts.get('recommended', 0) / len(df):.2f}%",
                f"{100 * counts.get('not_recommended', 0) / len(df):.2f}%",
                f"{100 * counts.get('no_idea', 0) / len(df):.2f}%",
                '100%',
                'N/A'
            ]
        })
        
        return summary


