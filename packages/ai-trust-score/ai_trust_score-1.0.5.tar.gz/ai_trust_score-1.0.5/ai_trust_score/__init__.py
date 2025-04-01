from .client import TumerykTrustScoreClient

# Create a singleton instance
trust_score = TumerykTrustScoreClient()

__all__ = ['TumerykTrustScoreClient', 'trust_score'] 