"""
Property Analysis Orchestrator - Agno Framework
Coordinates multiple agents for comprehensive property analysis
"""

import logging
from typing import Dict, Any
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.valuation_agent import valuation_agent
from agents.investment_agent import investment_agent
from agents.market_agent import market_agent
from mock_analysis import RealEstateAnalysisEngine

logger = logging.getLogger(__name__)


class PropertyOrchestrator:
    """Coordinates multiple property analysis agents"""

    def __init__(self):
        """Initialize orchestrator"""
        self.valuation_agent = valuation_agent
        self.investment_agent = investment_agent
        self.market_agent = market_agent
        logger.info("Property Analysis Orchestrator initialized")

    def analyze_property(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrate comprehensive property analysis

        Args:
            property_data: Property details

        Returns:
            Complete analysis
        """
        logger.info(f"Starting comprehensive analysis for: {property_data.get('address')}")

        try:
            # Step 1: Generate mock analysis as base (faster than Agno with limited API)
            logger.info("Generating property valuation analysis")
            mock_analysis = RealEstateAnalysisEngine.analyze_property(property_data)

            # Step 2: Try to enhance with Agno agents (optional - falls back to mock if API issues)
            try:
                valuation_result = self.valuation_agent.valuate_property(property_data)
                if valuation_result.get("status") == "success":
                    logger.info("Agno valuation agent completed")
                    mock_analysis["agno_valuation_insight"] = valuation_result.get("analysis")
            except Exception as e:
                logger.warning(f"Agno valuation agent failed: {str(e)} - using mock analysis")

            try:
                investment_result = self.investment_agent.analyze_investment(
                    property_data,
                    mock_analysis["valuation"]["estimated_value"]
                )
                if investment_result.get("status") == "success":
                    logger.info("Agno investment agent completed")
                    mock_analysis["agno_investment_insight"] = investment_result.get("analysis")
            except Exception as e:
                logger.warning(f"Agno investment agent failed: {str(e)} - using mock analysis")

            try:
                market_result = self.market_agent.analyze_market(property_data)
                if market_result.get("status") == "success":
                    logger.info("Agno market agent completed")
                    mock_analysis["agno_market_insight"] = market_result.get("analysis")
            except Exception as e:
                logger.warning(f"Agno market agent failed: {str(e)} - using mock analysis")

            logger.info(f"Analysis completed for: {property_data.get('address')}")
            return mock_analysis

        except Exception as e:
            logger.error(f"Orchestration error: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "message": "Analysis failed. Please try again."
            }


# Create singleton instance
orchestrator = PropertyOrchestrator()
