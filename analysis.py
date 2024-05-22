import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.sentiment import SentimentIntensityAnalyzer
import spacy

# Load spaCy English model
# Load spaCy English model
nlp = spacy.load('en_core_web_sm')

# Load the CSV file
df = pd.read_csv('preprocessed_data.csv')

# Verify column names
print("Data columns:", df.columns)

# Generate a word cloud from the 'Preprocessed Text' column
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(df['Preprocessed Text']))

# Plot the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Preprocessed Text')
plt.show()

# Initialize VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Calculate sentiment scores for each preprocessed text
df['sentiment_score'] = df['Preprocessed Text'].apply(lambda x: sia.polarity_scores(x)['compound'])

# Plot the sentiment score distribution
plt.figure(figsize=(10, 5))
df['sentiment_score'].hist(bins=30, alpha=0.7, color='blue')
plt.title('Distribution of Sentiment Scores')
plt.xlabel('Sentiment Score')
plt.ylabel('Frequency')
plt.show()

# Named Entity Recognition (NER) function
def named_entity_recognition(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

# Apply NER to each row of preprocessed text and store the entities in a new column
df['entities'] = df['Preprocessed Text'].apply(named_entity_recognition)

# Calculate entity frequency
entity_freq = {}
for entity_list in df['entities']:
    for entity, label in entity_list:
        key = (entity, label)
        if key in entity_freq:
            entity_freq[key] += 1
        else:
            entity_freq[key] = 1

# Convert the dictionary of entity frequencies to a list of tuples
entity_freq_data = [(entity, label, frequency) for (entity, label), frequency in entity_freq.items()]

# Create a DataFrame for entity frequency data
entity_freq_df = pd.DataFrame(entity_freq_data, columns=['Entity', 'Label', 'Frequency'])

# Plot entity frequencies
entity_freq_df.plot(kind='bar', x='Entity', y='Frequency', figsize=(12, 8))
plt.xlabel('Entity')
plt.ylabel('Frequency')
plt.title('Frequency of Named Entities by Label')
plt.show()

# Combine sentiment scores and named entities
entity_sentiment_scores = []

for idx, row in df.iterrows():
    entities = row['entities']
    sentiment_score = row['sentiment_score']
    
    for entity, label in entities:
        entity_sentiment_scores.append({
            'entity': entity,
            'label': label,
            'sentiment_score': sentiment_score
        })

# Convert the entity sentiment scores to a DataFrame
entity_sentiment_df = pd.DataFrame(entity_sentiment_scores)

# Calculate average sentiment scores by entity
avg_sentiment_by_entity = entity_sentiment_df.groupby('entity')['sentiment_score'].mean()

# Plot average sentiment scores for each entity
avg_sentiment_by_entity.plot(kind='bar', figsize=(12, 8))
plt.xlabel('Entity')
plt.ylabel('Average Sentiment Score')
plt.title('Average Sentiment Score by Entity')
plt.show()


