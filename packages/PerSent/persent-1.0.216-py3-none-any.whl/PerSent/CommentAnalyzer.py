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
    
    def __init__(self, model_dir='PerSent/model'):
        self.normalizer = Normalizer()
        self.stemmer = Stemmer()
        self.stopwords = set(stopwords_list())
        self.model_dir = model_dir
        self.vectorizer = None
        self.classifier = None
        
        # make /model Directory if not exist
        os.makedirs(self.model_dir, exist_ok=True)

    def _initialize_model(self):
        """Automatically load or train the model"""
        try:
            self.load_model()
            print("Model loaded successfully from:", self.model_dir)
        except (FileNotFoundError, Exception) as e:
            print(f"No trained model found: {str(e)}")
            self._train_from_default_dataset()

    def _train_from_default_dataset(self):
        """Train model using default dataset if available"""
        if not self.default_train_path.exists():
            warnings.warn(
                f"Default training file not found at: {self.default_train_path}\n"
                "Please provide training data or train manually using train() method",
                RuntimeWarning
            )
            return

        print(f"Training model from default dataset: {self.default_train_path}")
        
        try:
            # Load and validate dataset
            df = pd.read_csv(self.default_train_path)
            
            if not {'body', 'recommendation_status'}.issubset(df.columns):
                raise ValueError(
                    "Training file must contain 'body' and 'recommendation_status' columns"
                )
            
            # Add weight column if not exists
            if 'weight' not in df.columns:
                df['weight'] = 1.0  # Default weight
            
            # Train the model
            accuracy = self.train(
                train_csv=self.default_train_path,
                test_size=0.2,
                vector_size=100,
                window=5
            )
            
            print(f"Model trained successfully (accuracy: {accuracy:.2f})")
            self.save_model()
            
        except Exception as e:
            warnings.warn(
                f"Failed to train from default dataset: {str(e)}",
                RuntimeWarning
            )

    def _preprocess_text(self, text):
        """Preprocess Persian text (normalization, cleaning, tokenization)"""
        text = self.normalizer.normalize(str(text))
        text = re.sub(r'[!()-\[\]{};:\'",؟<>./?@#$%^&*_~۰-۹\d]+', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
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
            test_size (float): Test set proportion
            vector_size (int): Word2Vec vector size
            window (int): Word2Vec context window size
            random_state (int): Random seed
            
        Returns:
            float: Model accuracy
        """
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
        
        # Prepare features and labels
        X = np.array([self._sentence_vector(s, self.vectorizer) for s in df['tokens']])
        y = df['recommendation_status'].map({
            "no_idea": 2,
            "recommended": 1,
            "not_recommended": 0
        }).values
        
        # Train classifier
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        self.classifier = LogisticRegression(max_iter=1000, random_state=random_state)
        self.classifier.fit(X_train, y_train)
        
        return self.classifier.score(X_test, y_test)

    def predict(self, text):
        """Predict comment sentiment (recommended/not_recommended/no_idea)"""
        if not self.is_ready():
            raise Exception("Model not ready. Please train or load a model first.")
            
        tokens = self._preprocess_text(text)
        vector = self._sentence_vector(tokens, self.vectorizer)
        return {
            0: "not_recommended",
            1: "recommended",
            2: "no_idea"
        }[self.classifier.predict([vector])[0]]

    def save_model(self):
        """Save trained models to disk"""
        joblib.dump(self.classifier, self.model_dir / self.model_files['classifier'])
        self.vectorizer.save(str(self.model_dir / self.model_files['word2vec']))

    def load_model(self):
        """Load trained models from disk"""
        self.classifier = joblib.load(self.model_dir / self.model_files['classifier'])
        self.vectorizer = Word2Vec.load(str(self.model_dir / self.model_files['word2vec']))

    def is_ready(self):
        """Check if model is ready for predictions"""
        return self.classifier is not None and self.vectorizer is not None

    def analyze_csv(self, input_csv, output_path, text_column=0, summary_path=None):
        """
        Analyze sentiment for a CSV file of comments
        
        Args:
            input_csv (str): Input CSV path
            output_path (str): Output CSV path
            text_column: Column containing comments
            summary_path: Optional path for summary stats
        """
        df = pd.read_csv(input_csv)
        
        # Handle text column specification
        if isinstance(text_column, int):
            column_name = df.columns[text_column]
        else:
            column_name = text_column
            
        # Process comments
        tqdm.pandas(desc="Analyzing comments")
        df['sentiment'] = df[column_name].progress_apply(self.predict)
        
        # Save results
        df.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"Results saved to {output_path}")
        
        # Save summary if requested
        if summary_path:
            counts = df['sentiment'].value_counts()
            summary = pd.DataFrame({
                'Sentiment': ['Recommended', 'Not Recommended', 'No Idea'],
                'Count': [
                    counts.get('recommended', 0),
                    counts.get('not_recommended', 0), 
                    counts.get('no_idea', 0)
                ],
                'Percentage': [
                    f"{100*counts.get('recommended',0)/len(df):.1f}%",
                    f"{100*counts.get('not_recommended',0)/len(df):.1f}%",
                    f"{100*counts.get('no_idea',0)/len(df):.1f}%"
                ]
            })
            summary.to_csv(summary_path, index=False)
            print(f"Summary saved to {summary_path}")
