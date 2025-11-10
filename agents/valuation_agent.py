"""
Property Valuation Agent - Agno Framework
Analyzes property features and calculates estimated value
"""

import logging
from typing import Dict, Any
from agno.agent import Agent
from agno.models.google.gemini import Gemini
from agno.db.sqlite import SqliteDb
from config import settings

logger = logging.getLogger(__name__)


class ValuationAgent(Agent):
    """Property Valuation Agent using Agno"""

    def __init__(self):
        """Initialize Valuation Agent"""
        super().__init__(
            name="ValuationAgent",
            model=Gemini(
                id=settings.AGENT_MODEL,
                api_key=settings.GEMINI_API_KEY
            ),
            db=SqliteDb(db_file=settings.DB_FILE),
            instructions="""You are an expert real estate valuation specialist.
            Your role is to:
            1. Analyze property details (size, age, condition, location)
            2. Consider market factors and comparable properties
            3. Calculate estimated property value
            4. Provide price per square foot
            5. Give valuation confidence score

            Guidelines:
            - Consider location premium/discount
            - Factor in property age and condition
            - Compare with market data
            - Provide realistic valuations
            - Include confidence percentage (70-95%)""",
            markdown=True
        )

    def valuate_property(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valuate property based on input data

        Args:
            property_data: Property information

        Returns:
            Valuation analysis
        """
        prompt = f"""Analyze and valuate this property:

Property Details:
- Address: {property_data.get('address', 'N/A')}
- Bedrooms: {property_data.get('bedrooms', 0)}
- Bathrooms: {property_data.get('bathrooms', 0)}
- Square Feet: {property_data.get('sqft', 0)}
- Age (Years): {property_data.get('age_years', 0)}
- Location Type: {property_data.get('location_type', 'suburban')}
- Condition: {property_data.get('condition', 'fair')}
- Neighborhood Rating: {property_data.get('neighborhood_rating', 'average')}

Please provide:
1. Estimated property value
2. Price per square foot
3. Valuation confidence (percentage)
4. Key factors affecting value
5. Market comparison insights"""

        try:
            response = self.run(prompt)
            logger.info(f"Valuation completed for: {property_data.get('address')}")
            return {
                "status": "success",
                "analysis": str(response)
            }
        except Exception as e:
            logger.error(f"Valuation error: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }


# Create singleton instance
valuation_agent = ValuationAgent()
