import numpy as np
import nltk
from textblob import TextBlob
from sklearn.preprocessing import MinMaxScaler

class PsychologicalHarmAssessment:
    def __init__(self):
        # Predefined psychological harm indicators
        self.harm_indicators = {
            'emotional_distress': {
                'weight': 0.25,
                'assessment_method': self._assess_emotional_distress
            },
            'autonomy_violation': {
                'weight': 0.20,
                'assessment_method': self._assess_autonomy_violation
            },
            'identity_impact': {
                'weight': 0.15,
                'assessment_method': self._assess_identity_impact
            },
            'power_dynamics': {
                'weight': 0.20,
                'assessment_method': self._assess_power_dynamics
            },
            'trauma_potential': {
                'weight': 0.20,
                'assessment_method': self._assess_trauma_potential
            }
        }
        
        # Sentiment and linguistic analysis resources
        nltk.download('vader_lexicon')
        self.sentiment_analyzer = nltk.sentiment.SentimentIntensityAnalyzer()
        
        # Normalization scaler
        self.scaler = MinMaxScaler()
        
        # Predefined psychological harm dictionaries
        self.trauma_keywords = self._load_trauma_keywords()
        self.power_abuse_terms = self._load_power_abuse_terms()
        self.autonomy_violation_terms = self._load_autonomy_violation_terms()
    
    def assess_psychological_harm(self, context, action_details):
        # Comprehensive psychological harm evaluation
        harm_scores = {}
        
        for indicator, config in self.harm_indicators.items():
            harm_scores[indicator] = {
                'raw_score': config['assessment_method'](context, action_details),
                'weight': config['weight']
            }
        
        # Normalize and weight scores
        normalized_scores = self._normalize_harm_scores(harm_scores)
        
        # Calculate composite psychological harm score
        psychological_harm_score = self._calculate_weighted_harm_score(normalized_scores)
        
        return psychological_harm_score
    
    def _normalize_harm_scores(self, harm_scores):
        # Normalize harm scores
        raw_scores = [score['raw_score'] for score in harm_scores.values()]
        normalized_array = self.scaler.fit_transform(
            np.array(raw_scores).reshape(-1, 1)
        )
        
        normalized_scores = {}
        for (indicator, config), norm_score in zip(
            self.harm_indicators.items(), 
            normalized_array
        ):
            normalized_scores[indicator] = {
                'normalized_score': norm_score[0],
                'weight': config['weight']
            }
        
        return normalized_scores
    
    def _calculate_weighted_harm_score(self, normalized_scores):
        # Calculate weighted psychological harm score
        weighted_sum = sum(
            scores['normalized_score'] * scores['weight'] 
            for scores in normalized_scores.values()
        )
        
        return weighted_sum
    
    def _assess_emotional_distress(self, context, action_details):
        # Analyze emotional impact
        sentiment_scores = self.sentiment_analyzer.polarity_scores(str(action_details))
        
        # Sentiment analysis
        negative_sentiment = sentiment_scores['neg']
        
        # Linguistic complexity and emotional intensity
        text_complexity = self._measure_text_complexity(str(action_details))
        
        # Combine factors
        emotional_distress_score = (
            negative_sentiment * 0.6 + 
            text_complexity * 0.4
        )
        
        return emotional_distress_score
    
    def _assess_autonomy_violation(self, context, action_details):
        # Check for autonomy violation indicators
        autonomy_violation_count = sum(
            1 for term in self.autonomy_violation_terms
            if term.lower() in str(action_details).lower()
        )
        
        # Contextual autonomy assessment
        context_autonomy_score = self._evaluate_context_autonomy(context)
        
        return min(1, autonomy_violation_count * 0.3 + context_autonomy_score * 0.7)
    
    def _assess_identity_impact(self, context, action_details):
        # Analyze potential identity-based harm
        identity_keywords = ['gender', 'race', 'sexuality', 'disability']
        identity_mention_count = sum(
            1 for keyword in identity_keywords
            if keyword in str(action_details).lower()
        )
        
        # Sentiment around identity-related terms
        identity_sentiment = self._analyze_identity_sentiment(str(action_details))
        
        return min(1, identity_mention_count * 0.4 + identity_sentiment * 0.6)
    
    def _assess_power_dynamics(self, context, action_details):
        # Evaluate power imbalance indicators
        power_abuse_count = sum(
            1 for term in self.power_abuse_terms
            if term.lower() in str(action_details).lower()
        )
        
        # Contextual power dynamics assessment
        context_power_score = self._evaluate_context_power_dynamics(context)
        
        return min(1, power_abuse_count * 0.4 + context_power_score * 0.6)
    
    def _assess_trauma_potential(self, context, action_details):
        # Identify potential trauma-inducing elements
        trauma_keyword_count = sum(
            1 for keyword in self.trauma_keywords
            if keyword.lower() in str(action_details).lower()
        )
        
        # Sentiment analysis of potentially traumatic content
        trauma_sentiment = self._analyze_trauma_sentiment(str(action_details))
        
        return min(1, trauma_keyword_count * 0.5 + trauma_sentiment * 0.5)
    
    def _measure_text_complexity(self, text):
        # Assess linguistic complexity
        blob = TextBlob(text)
        return min(1, len(blob.words) / 100)  # Normalization
    
    def _analyze_identity_sentiment(self, text):
        # Specialized sentiment analysis for identity-related content
        sentiment_scores = self.sentiment_analyzer.polarity_scores(text)
        return abs(sentiment_scores['compound'])
    
    def _analyze_trauma_sentiment(self, text):
        # Specialized sentiment analysis for potentially traumatic content
        sentiment_scores = self.sentiment_analyzer.polarity_scores(text)
        return abs(sentiment_scores['neg'])
    
    def _evaluate_context_autonomy(self, context):
        # Contextual autonomy assessment logic
        # Placeholder for more complex contextual analysis
        return 0.5
    
    def _evaluate_context_power_dynamics(self, context):
        # Contextual power dynamics assessment logic
        # Placeholder for more complex contextual analysis
        return 0.5
    
    def _load_trauma_keywords(self):
        # Predefined trauma-related keywords
        return [
            'abuse', 'violence', 'assault', 'harassment', 
            'trauma', 'ptsd', 'psychological damage'
        ]
    
    def _load_power_abuse_terms(self):
        # Predefined power abuse terminology
        return [
            'manipulation', 'coercion', 'intimidation', 
            'control', 'domination'
        ]
    
    def _load_autonomy_violation_terms(self):
        # Predefined autonomy violation terms
        return [
            'force', 'compel', 'restrict', 'deny choice', 
            'remove agency'
        ]

# Example usage
def assess_psychological_harm(context, action_details):
    harm_assessor = PsychologicalHarmAssessment()
    return harm_assessor.assess_psychological_harm(context, action_details)
