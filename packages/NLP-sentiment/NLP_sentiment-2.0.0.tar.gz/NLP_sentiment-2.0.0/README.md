# Sentiment Analyzer

A simple sentiment analysis tool that assigns a sentiment score to a given text based on predefined positive and negative words.

## Features
- Uses a predefined list of positive and negative words.
- Assigns a sentiment score between -1 (negative) and 1 (positive).
- Lightweight and easy to use.

## Installation
You can install the package using pip:

```sh
pip install https://github.com/rupayan-23/NLP_sentiment.git
```

## Usage

```python
from sentiment_analyzer import Sentiment

text = "This is an amazing and fantastic experience!"
score = Sentiment(text)
print("Sentiment Score:", score)
```

## Sentiment Scoring
- **1.0** → Strongly positive sentiment
- **0.5 to 0.9** → Moderately positive sentiment
- **0.0** → Neutral
- **-0.5 to -0.9** → Moderately negative sentiment
- **-1.0** → Strongly negative sentiment

## Requirements
- Python 3.6+
- NumPy

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Author
[Rupayan Sarker](https://github.com/rupayan-23)
