# Install dependencies (Colab users only need to run this once)
!pip install transformers torch pandas --quiet

import pandas as pd
from transformers import pipeline

# Load sample data
df = pd.read_csv("sentiment_sample.csv")

# Load sentiment analysis model
nlp = pipeline("sentiment-analysis")

# Run sentiment analysis
df["sentiment"] = df["text"].apply(lambda x: nlp(x)[0]["label"])
df["score"] = df["text"].apply(lambda x: nlp(x)[0]["score"])

# Display results
print(df)
