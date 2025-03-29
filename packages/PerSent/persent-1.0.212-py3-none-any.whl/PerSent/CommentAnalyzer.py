#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Persian Comment Analyzer
A sentiment analysis tool for Persian comments with Word2Vec and Logistic Regression.
"""

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
import warnings
from pathlib import Path

class CommentAnalyzer:
    """Persian comment sentiment analyzer using Word2Vec and Logistic Regression"""
    
    def __init__(self, model_dir='PerSent/model/CommentAnalyzer', default_train_path=None):
        """
        Initialize the comment analyzer
        
        Args:
            model_dir (str): Directory to save/load models
            default_train_path (str): Path to default training CSV (optional)
        """
        # Initialize Persian NLP tools
        self.normalizer = Normalizer()
        self.stemmer = Stemmer()
        self.stopwords = set(stopwords_list())
        
        # Configure model paths
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        # Default model file names
        self.model_files = {
            'classifier': 'classifier.joblib',
            'word2vec': 'word2vec.model'
        }
        
        # Set default training path
        self.default_train_path = default_train_path or Path('PerSent/dataset/train.csv')
        
        # Model placeholders
        self.vectorizer = None
        self.classifier = None
        
        # Try to load existing models
        self._try_load_default_models()

    def _try_load_default_models(self):
        """Attempt to load default models if they exist"""
        try:
            classifier_path = self.model_dir / self.model_files['classifier']
            word2vec_path = self.model_dir / self.model_files['word2vec']
            
            if classifier_path.exists() and word2vec_path.exists():
                self.load_model()
                print("Models loaded successfully from:", self.model_dir)
            else:
                warnings.warn(
                    "Model files not found. You need to train or provide models.\n"
                    f"Expected paths:\n- {classifier_path}\n- {word2vec_path}",
                    RuntimeWarning
                )
                # Attempt to train from default dataset if exists
                if self.default_train_path.exists():
                    print("Training from default dataset...")
                    self.train(self.default_train_path)
        except Exception as e:
            warnings.warn(
                f"Failed to load models: {str(e)}",
                RuntimeWarning
            )

    def _preprocess_text(self, text):
        """
        Preprocess Persian text by:
        1. Normalizing
        2. Removing special characters and numbers
        3. Tokenizing and stemming
        """
        # Normalize Persian text
        text = self.normalizer.normalize(str(text))
        
        # Remove special characters and numbers
        text = re.sub(r'[!()-\[\]{};:\'",؟<>./?@#$%^&*_~۰-۹\d]+', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Tokenize and stem
        tokens = word_tokenize(text)
        return [
            self.stemmer.stem(token)
            for token in tokens
            if token not in self.stopwords and len(token) > 1
        ]
    
    def _sentence_vector(self, sentence, model):
        """Convert sentence to vector using Word2Vec model"""
        vectors = [
            model.wv[word] if word in model.wv else np.zeros(model.vector_size)
            for word in sentence
        ]
        return np.mean(vectors, axis=0) if vectors else np.zeros(model.vector_size)
    
    def train(self, train_csv, test_size=0.2, vector_size=100, window=5, random_state=42):
        """
        Train the comment analyzer model
        
        Args:
            train_csv (str): Path to training CSV
            test_size (float): Test set proportion (0-1)
            vector_size (int): Word2Vec vector dimensions
            window (int): Word2Vec context window size
            random_state (int): Random seed for reproducibility
            
        Returns:
            float: Model accuracy on test set
        """
        try:
            # Load and preprocess data
            df = pd.read_csv(train_csv)
            df['tokens'] = df['body'].progress_apply(self._preprocess_text)
            
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
            
            # Train/test split
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, 
                test_size=test_size,
                random_state=random_state
            )

            # Train classifier
            self.classifier = LogisticRegression(max_iter=1000, random_state=random_state)
            self.classifier.fit(X_train, y_train)
            
            # Save models
            self.save_model()
            
            # Return accuracy
            return self.classifier.score(X_test, y_test)
            
        except Exception as e:
            raise Exception(f"Training failed: {str(e)}")
    
    def predict(self, text):
        """
        Predict sentiment of a Persian comment
        
        Args:
            text (str): Persian text to analyze
            
        Returns:
            str: 'recommended', 'not_recommended', or 'no_idea'
            
        Raises:
            Exception: If model is not trained
        """
        if not self.is_ready():
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
        joblib.dump(self.classifier, self.model_dir / self.model_files['classifier'])
        self.vectorizer.save(str(self.model_dir / self.model_files['word2vec']))
    
    def load_model(self):
        """Load trained models from disk"""
        self.classifier = joblib.load(self.model_dir / self.model_files['classifier'])
        self.vectorizer = Word2Vec.load(str(self.model_dir / self.model_files['word2vec']))
    
    def is_ready(self):
        """Check if model is loaded and ready for predictions"""
        return self.classifier is not None and self.vectorizer is not None
    
    def analyze_csv(self, input_csv, output_path, text_column=0, summary_path=None):
        """
        Analyze sentiment for comments in a CSV file
        
        Args:
            input_csv (str): Path to input CSV
            output_path (str): Path to save results
            text_column (str/int): Column containing text (name or index)
            summary_path (str): Optional path to save summary stats
            
        Returns:
            pd.DataFrame: Results dataframe
        """
        if not self.is_ready():
            raise Exception("Model not ready for prediction")
            
        try:
            df = pd.read_csv(input_csv)
            
            # Determine text column
            if isinstance(text_column, int):
                if text_column < 0:
                    text_column = len(df.columns) + text_column
                if text_column >= len(df.columns):
                    raise ValueError(f"Column index {text_column} out of range")
                column_name = df.columns[text_column]
            else:
                if text_column not in df.columns:
                    raise ValueError(f"Column '{text_column}' not found")
                column_name = text_column
            
            # Process comments
            tqdm.pandas(desc="Analyzing comments")
            df['sentiment'] = df[column_name].progress_apply(self.predict)
            
            # Save results
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"Results saved to {output_path}")
            
            # Save summary if requested
            if summary_path:
                self._save_summary(df, summary_path)
            
            return df
            
        except Exception as e:
            raise Exception(f"CSV analysis failed: {str(e)}")
    
    def _save_summary(self, df, output_path):
        """Generate and save analysis summary statistics"""
        counts = df['sentiment'].value_counts().to_dict()
        
        summary = pd.DataFrame({
            'Category': ['Recommended', 'Not Recommended', 'No Idea', 'Total'],
            'Count': [
                counts.get('recommended', 0),
                counts.get('not_recommended', 0),
                counts.get('no_idea', 0),
                len(df)
            ],
            'Percentage': [
                f"{100 * counts.get('recommended', 0) / len(df):.2f}%",
                f"{100 * counts.get('not_recommended', 0) / len(df):.2f}%",
                f"{100 * counts.get('no_idea', 0) / len(df):.2f}%",
                '100%'
            ]
        })
        
        summary.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"Summary saved to {output_path}")

