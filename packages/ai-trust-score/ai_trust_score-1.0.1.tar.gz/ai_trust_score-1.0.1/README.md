# AI Trust Score Client

A Python client for accessing the Tumeryk AI Trust Score API, which provides comprehensive trust and safety metrics for various AI models.

## Features

- 🔒 Secure authentication with the Tumeryk API
- 📊 Retrieve trust scores for multiple AI models
- 🎯 Detailed category-specific scores
- 🚀 Easy-to-use singleton client
- 🔄 Environment variable support for credentials
- 📝 Comprehensive scoring categories

## Installation

```bash
pip install ai-trust-score
```

## Quick Start

```python
from ai_trust_score import trust_score

# Using environment variables
# Set TUMERYK_USERNAME and TUMERYK_PASSWORD in your environment

# The client will auto-login if environment variables are set
scores = trust_score.get_trust_scores()
print(scores)

# Or login explicitly
trust_score.login(username="your_username", password="your_password")
scores = trust_score.get_trust_scores()
```

## Advanced Usage

```python
from ai_trust_score import TumerykTrustScoreClient

# Create a custom client instance
client = TumerykTrustScoreClient(
    base_url="https://trust-score.tmryk.com/",
    auth_url="https://chat.tmryk.com"
)

# Login
client.login(username="your_username", password="your_password")

# Get trust scores
scores = client.get_trust_scores()

# Access specific model scores
for model_id, data in scores["data"]["total_score"].items():
    print(f"Model: {model_id}")
    print(f"Total Score: {data['score']}")
    print("Information Codes:")
    for code, message in data["information_codes"].items():
        print(f"  {code}: {message}")
    
    # Print category scores
    category_scores = scores["data"]["category_score"][model_id]
    print("Category Scores:")
    for category, score in category_scores.items():
        print(f"  {category}: {score}")
```

## Score Categories

The trust score evaluation includes the following categories:

- **Prompt Injection**: Measures resistance to malicious prompts
- **Security**: Overall security assessment
- **Sensitive Information Disclosure**: Evaluation of data privacy
- **Insecure Output Handling**: Assessment of output safety
- **Supply Chain Vulnerabilities**: Analysis of dependencies
- **Hallucination**: Measurement of response accuracy
- **Psychological Safety**: Evaluation of emotional impact
- **Fairness**: Assessment of bias and equality
- **Toxicity**: Measurement of harmful content

## Information Codes

The API may return various information codes indicating areas for improvement:

- 301: Low Security Score
- 303: Low Sensitive Information Disclosure Score
- 307: Low Insecure Output Handling Score
- 308: Low Supply Chain Vulnerabilities Score
- 309: Low Hallucination Score

## Environment Variables

- `TUMERYK_USERNAME`: Your Tumeryk API username
- `TUMERYK_PASSWORD`: Your Tumeryk API password
- `TUMERYK_BASE_URL`: Base URL for the trust score service (default: https://trust-score.tmryk.com/)
- `TUMERYK_AUTH_URL`: Authentication URL (default: https://chat.tmryk.com)

## Response Format

```python
{
    "status": "success",
    "data": {
        "total_score": {
            "model_id": {
                "score": 800,
                "information_codes": {
                    "307": "Low Insecure Output Handling Score",
                    "308": "Low Supply Chain Vulnerabilities Score"
                }
            }
        },
        "category_score": {
            "model_id": {
                "Prompt Injection": 766,
                "Security": 925,
                "Sensitive Information Disclosure": 687,
                "Insecure Output Handling": 462,
                "Supply Chain Vulnerabilities": 780,
                "Hallucination": 637,
                "Psychological Safety": 833,
                "Fairness": 997,
                "Toxicity": 997
            }
        }
    }
}
```

## Error Handling

The client includes built-in error handling for API requests. If a request fails, it will return a dictionary with an error message:

```python
{
    "error": "Request failed: <error details>"
}
```

## Contributing

We welcome contributions! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Support

For support, please contact support@tmryk.com or visit our website at https://tmryk.com.