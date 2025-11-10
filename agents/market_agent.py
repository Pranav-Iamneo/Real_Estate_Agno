"""
Market Analysis Agent - Agno Framework
Analyzes market trends and comparable properties
"""

import logging
from typing import Dict, Any
from agno.agent import Agent
from agno.models.google.gemini import Gemini
from agno.db.sqlite import SqliteDb
from config import settings

logger = logging.getLogger(__name__)


class MarketAgent(Agent):
    """Market Analysis Agent using Agno"""

    def __init__(self):
        """Initialize Market Agent"""
        super().__init__(
            name="MarketAgent",
            model=Gemini(
                id=settings.AGENT_MODEL,
                api_key=settings.GEMINI_API_KEY
            ),
            db=SqliteDb(db_file=settings.DB_FILE),
            instructions="""You are an expert real estate market analyst.
            Your role is to:
            1. Analyze location and neighborhood market
            2. Identify comparable properties
            3. Assess market trends
            4. Evaluate location desirability
            5. Provide market insights

            Guidelines:
            - Consider location type and tier
            - Analyze neighborhood factors
            - Compare with similar properties
            - Identify market trends
            - Assess location risks
            - Provide market growth forecasts""",
            markdown=True
        )

    def analyze_market(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze market conditions

        Args:
            property_data: Property information

        Returns:
            Market analysis
        """
        prompt = f"""Analyze the market for this property:

Property Details:
- Address: {property_data.get('address', 'N/A')}
- Location Type: {property_data.get('location_type', 'suburban')}
- Neighborhood Rating: {property_data.get('neighborhood_rating', 'average')}
- Bedrooms: {property_data.get('bedrooms', 0)}
- SqFt: {property_data.get('sqft', 0)}

Please provide:
1. Location tier analysis (premium/good/average/developing)
2. Neighborhood desirability rating
3. Market growth trends (appreciating/stable/declining)
4. Expected market growth rate
5. Comparable properties analysis (3 similar properties with prices)
6. Price per sqft in the area
7. Location advantages
8. Location disadvantages
9. Future development potential
10. Market forecast (5-year outlook)

Format with clear sections and bullet points."""

        try:
            response = self.run(prompt)
            logger.info(f"Market analysis completed for: {property_data.get('address')}")
            return {
                "status": "success",
                "analysis": str(response)
            }
        except Exception as e:
            logger.error(f"Market analysis error: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }


# Create singleton instance
market_agent = MarketAgent()
