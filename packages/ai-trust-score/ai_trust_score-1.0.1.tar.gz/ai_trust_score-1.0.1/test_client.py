import os
from tumeryk_ai_trust_score import trust_score

def test_with_credentials(username: str, password: str):
    """Test the client with specific credentials."""
    print(f"\nTesting with account: {username}")
    print("=" * 50)
    
    # Login with provided credentials
    print(f"Logging in as {username}...")
    trust_score.login(username=username, password=password)
    
    # Fetch trust scores
    print("\nFetching trust scores...")
    response = trust_score.get_trust_scores()
    
    # Process response
    if isinstance(response, dict) and response.get('status') == 'success' and 'data' in response:
        data = response['data']
        total_scores = data.get('total_score', {})
        category_scores = data.get('category_score', {})
        
        print("\nTrust Scores:")
        print("=" * 50)
        
        # Print total scores and information codes for each model
        for model, model_data in total_scores.items():
            print(f"\nModel: {model}")
            print(f"Total Score: {model_data['score']}")
            
            # Print information codes if any
            if model_data.get('information_codes'):
                print("\nInformation Codes:")
                for code, message in model_data['information_codes'].items():
                    print(f"  {code}: {message}")
            
            # Print category scores if available
            if model in category_scores:
                print("\nCategory Scores:")
                for category, score in category_scores[model].items():
                    print(f"  {category}: {score}")
            
            print("-" * 50)
    else:
        print("\nError: Invalid response format or error in response")
        print(f"Raw response: {response}")

def main():
    # Test accounts
    test_accounts = [
        ("nirmit", "nirmit"),
        ("demoTumeryk", "abc123")
    ]
    
    print("Starting Tumeryk AI Trust Score Client Tests")
    print("=" * 50)
    
    # Test each account
    for username, password in test_accounts:
        try:
            test_with_credentials(username, password)
        except Exception as e:
            print(f"\nError testing account {username}: {str(e)}")
            print("-" * 50)

if __name__ == "__main__":
    main() 