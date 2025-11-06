"""
Investment Analysis Agent - Agno Framework
Evaluates investment potential and ROI
"""

import logging
from typing import Dict, Any
from agno.agent import Agent
from agno.models.google.gemini import Gemini
from agno.db.sqlite import SqliteDb
from config import settings

logger = logging.getLogger(__name__)


class InvestmentAgent(Agent):
    """Investment Analysis Agent using Agno"""

    def __init__(self):
        """Initialize Investment Agent"""
        super().__init__(
            name="InvestmentAgent",
            model=Gemini(
                id=settings.AGENT_MODEL,
                api_key=settings.GEMINI_API_KEY
            ),
            db=SqliteDb(db_file=settings.DB_FILE),
            instructions="""You are an expert real estate investment analyst.
            Your role is to:
            1. Evaluate investment potential and ROI
            2. Calculate rental yield and appreciation
            3. Assess risk factors
            4. Provide investment recommendations
            5. Compare with market standards

            Guidelines:
            - Realistic rental yield (5-8%)
            - Market appreciation (3-6%)
            - Consider location and condition
            - Factor in holding costs
            - Provide investment score (1-10)
            - Give clear BUY/HOLD/PASS recommendations""",
            markdown=True
        )

    def analyze_investment(self, property_data: Dict[str, Any], valuation: float) -> Dict[str, Any]:
        """
        Analyze investment potential

        Args:
            property_data: Property information
            valuation: Estimated property value

        Returns:
            Investment analysis
        """
        prompt = f"""Analyze the investment potential of this property:

Property Details:
- Address: {property_data.get('address', 'N/A')}
- Bedrooms: {property_data.get('bedrooms', 0)}
- Location Type: {property_data.get('location_type', 'suburban')}
- Condition: {property_data.get('condition', 'fair')}
- Estimated Value: ${valuation:,.0f}

Please provide:
1. Expected annual rental income
2. Annual appreciation potential
3. Total expected annual return (%)
4. Payback period (years)
5. Risk assessment (low/moderate/high)
6. Investment recommendation (HIGHLY RECOMMENDED/RECOMMENDED/CONSIDER/NOT RECOMMENDED)
7. Investment score (1-10)
8. Key investment factors
9. Potential risks
10. Comparison with market standards

Format the response with clear sections."""

        try:
            response = self.run(prompt)
            logger.info(f"Investment analysis completed for: {property_data.get('address')}")
            return {
                "status": "success",
                "analysis": str(response)
            }
        except Exception as e:
            logger.error(f"Investment analysis error: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }


# Create singleton instance
investment_agent = InvestmentAgent()
