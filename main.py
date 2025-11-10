"""
Real Estate Intelligence System - Integrated Streamlit + FastAPI
Single-port application combining UI and API
"""

import streamlit as st
import pandas as pd
import logging
from datetime import datetime
from typing import Dict, Any
from config import settings
from agents.orchestrator import orchestrator
from pydantic import BaseModel
from human_intervention.feedback_handler import FeedbackHandler
from human_intervention.validation_manager import ValidationManager
from human_intervention.approval_workflow import ApprovalWorkflow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# DATA MODELS
# ============================================================================

class PropertyInput(BaseModel):
    """Property input model"""
    address: str
    bedrooms: int
    bathrooms: float
    sqft: int
    age_years: int
    location_type: str = "suburban"
    condition: str = "fair"
    neighborhood_rating: str = "average"


class AnalysisRequest(BaseModel):
    """Property analysis request"""
    property: PropertyInput


class RealEstateIntelligence:
    """Real Estate Intelligence System with Agno Agents"""

    def __init__(self):
        """Initialize system"""
        logger.info("Initializing Real Estate Intelligence System with Agno Agents")
        self.orchestrator = orchestrator
        logger.info("Real Estate Intelligence System initialized successfully")

    def analyze_property(self, request: AnalysisRequest) -> Dict[str, Any]:
        """
        Analyze property using Agno agents

        Args:
            request: Analysis request with property data

        Returns:
            Complete property analysis
        """
        logger.info(f"Starting analysis for: {request.property.address}")

        # Prepare property data
        property_data = {
            "address": request.property.address,
            "bedrooms": request.property.bedrooms,
            "bathrooms": request.property.bathrooms,
            "sqft": request.property.sqft,
            "age_years": request.property.age_years,
            "location_type": request.property.location_type,
            "condition": request.property.condition,
            "neighborhood_rating": request.property.neighborhood_rating
        }

        try:
            # Use Agno orchestrator with fallback to mock
            analysis = self.orchestrator.analyze_property(property_data)
            logger.info(f"Analysis completed for: {request.property.address}")
            return analysis

        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "analysis_summary": {
                    "property_name": request.property.address,
                    "status": "failed"
                }
            }


# ============================================================================
# INITIALIZE APPLICATION
# ============================================================================

intelligence_system = RealEstateIntelligence()
feedback_handler = FeedbackHandler()
validation_manager = ValidationManager()
approval_workflow = ApprovalWorkflow()

# Configure Streamlit page
st.set_page_config(
    page_title="Real Estate Intelligence",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
STYLES = """
<style>
.card {
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 16px;
    background: #fff;
    margin: 8px 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    margin: 10px 0;
}

.success-card {
    background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
    color: white;
}

.warning-card {
    background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    color: white;
}

.h3 {
    font-weight: 600;
    margin: 18px 0 8px;
}

.pills {
    margin: 6px 0;
}

.pill {
    display: inline-block;
    background: #f1f3f5;
    border: 1px solid #e6e8eb;
    padding: 4px 10px;
    border-radius: 999px;
    margin: 3px;
    font-size: 13px;
}

.risk-high {
    color: #dc3545;
    font-weight: 600;
}

.risk-moderate {
    color: #ffc107;
    font-weight: 600;
}

.risk-low {
    color: #28a745;
    font-weight: 600;
}
</style>
"""

st.markdown(STYLES, unsafe_allow_html=True)


# ============================================================================
# MAIN STREAMLIT APP
# ============================================================================

def main():
    """Main Streamlit application"""

    st.title("🏠 Real Estate Intelligence System")
    st.caption("AI-powered property analysis, valuation, and investment recommendations")

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Property Analysis", "📊 Comparison", "ℹ️ System Info", "👤 Human Intervention"])

    # ============ TAB 1: PROPERTY ANALYSIS ============
    with tab1:
        st.header("Property Analysis & Valuation")

        # Sidebar actions
        with st.sidebar:
            st.header("⚙️ Quick Actions")

            if st.button("📋 Run Sample Analysis", width="stretch"):
                with st.spinner("Running sample analysis..."):
                    try:
                        sample_property = PropertyInput(
                            address="123 Oak Street, Downtown District",
                            bedrooms=3,
                            bathrooms=2.5,
                            sqft=2500,
                            age_years=8,
                            location_type="urban",
                            condition="good",
                            neighborhood_rating="good"
                        )

                        request = AnalysisRequest(property=sample_property)
                        analysis = intelligence_system.analyze_property(request)

                        if "status" in analysis and analysis["status"] == "success":
                            st.session_state.last_analysis = {
                                "status": "success",
                                "analysis": analysis,
                                "timestamp": datetime.now().isoformat()
                            }
                            st.success("✅ Sample analysis completed!")
                            st.rerun()
                        else:
                            st.error(f"Error: {analysis.get('error', 'Unknown error')}")
                    except Exception as e:
                        st.error(f"Failed: {str(e)}")

        # Two-column layout
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("🏘️ Property Details")

            property_address = st.text_input("Property Address", value="123 Oak Street, Downtown", key="address")
            bedrooms = st.number_input("Bedrooms", min_value=1, max_value=10, value=3, key="beds")
            bathrooms = st.number_input("Bathrooms", min_value=0.5, max_value=10.0, value=2.5, step=0.5, key="baths")
            sqft = st.number_input("Square Footage", min_value=500, max_value=10000, value=2500, key="sqft")

        with col2:
            st.subheader("📍 Property Characteristics")

            age = st.number_input("Age (Years)", min_value=0, max_value=100, value=8, key="age")
            location = st.selectbox(
                "Location Type",
                ["downtown", "urban", "suburban", "rural"],
                index=1,
                key="location"
            )
            condition = st.selectbox(
                "Property Condition",
                ["excellent", "good", "fair", "needs_repair", "poor"],
                index=2,
                key="condition"
            )
            neighborhood = st.selectbox(
                "Neighborhood Rating",
                ["excellent", "good", "average", "developing", "poor"],
                index=2,
                key="neighborhood"
            )

        # Analysis button
        st.divider()

        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            analyze_button = st.button(
                "🔍 Analyze Property",
                type="primary",
                width="stretch",
                key="analyze_btn"
            )

        # Run analysis
        if analyze_button:
            # Validate input
            if not property_address:
                st.error("Please enter property address")
                st.stop()

            # Prepare request
            property_obj = PropertyInput(
                address=property_address,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                sqft=sqft,
                age_years=age,
                location_type=location,
                condition=condition,
                neighborhood_rating=neighborhood
            )

            request = AnalysisRequest(property=property_obj)

            # Call analysis
            with st.spinner("🔄 Analyzing property..."):
                try:
                    analysis = intelligence_system.analyze_property(request)

                    if "status" in analysis and analysis["status"] == "success":
                        st.session_state.last_analysis = {
                            "status": "success",
                            "analysis": analysis,
                            "timestamp": datetime.now().isoformat()
                        }
                        st.success("✅ Analysis completed!")
                        st.balloons()

                        # Display results
                        st.header("📊 Analysis Results")

                        # Key metrics
                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            valuation = analysis.get("valuation", {}).get("estimated_value", "N/A")
                            st.metric("Estimated Value", f"${valuation:,.0f}" if isinstance(valuation, (int, float)) else valuation)

                        with col2:
                            roi = analysis.get("investment_analysis", {}).get("roi_percentage", 0)
                            st.metric("Expected ROI", f"{roi:.1f}%" if isinstance(roi, (int, float)) else roi)

                        with col3:
                            score = analysis.get("investment_analysis", {}).get("investment_score", 0)
                            st.metric("Investment Score", f"{score}/10" if isinstance(score, (int, float)) else score)

                        with col4:
                            price_sqft = analysis.get("valuation", {}).get("price_per_sqft", 0)
                            st.metric("Price/SqFt", f"${price_sqft:.0f}" if isinstance(price_sqft, (int, float)) else price_sqft)

                        # Recommendation
                        st.divider()
                        st.subheader("💡 Investment Recommendation")

                        recommendation = analysis.get("investment_analysis", {}).get("recommendation", "N/A")
                        investment_score = analysis.get("investment_analysis", {}).get("investment_score", 0)

                        if investment_score >= 8:
                            st.success(f"✅ {recommendation}")
                        elif investment_score >= 6:
                            st.info(f"ℹ️ {recommendation}")
                        else:
                            st.warning(f"⚠️ {recommendation}")

                        # Valuation details
                        st.subheader("💰 Valuation Analysis")

                        valuation_col1, valuation_col2, valuation_col3 = st.columns(3)

                        with valuation_col1:
                            est_value = analysis.get("valuation", {}).get("estimated_value", 0)
                            st.write(f"**Estimated Value:** ${est_value:,.0f}")

                        with valuation_col2:
                            confidence = analysis.get("valuation", {}).get("confidence_score", 0)
                            st.write(f"**Confidence:** {confidence:.1%}")

                        with valuation_col3:
                            trend = analysis.get("market_analysis", {}).get("market_trend", "N/A")
                            st.write(f"**Market Trend:** {trend.capitalize() if isinstance(trend, str) else trend}")

                        # Investment metrics
                        st.subheader("📈 Investment Metrics")

                        invest_col1, invest_col2, invest_col3 = st.columns(3)

                        with invest_col1:
                            rental = analysis.get("investment_analysis", {}).get("annual_rental_potential", 0)
                            st.write(f"**Annual Rental:** ${rental:,.0f}")

                        with invest_col2:
                            appreciation = analysis.get("investment_analysis", {}).get("annual_appreciation", 0)
                            st.write(f"**Annual Appreciation:** ${appreciation:,.0f}")

                        with invest_col3:
                            payback = analysis.get("investment_analysis", {}).get("payback_period_years", 0)
                            st.write(f"**Payback Period:** {payback:.1f} years")

                        # Risk assessment
                        st.subheader("⚠️ Risk Assessment")

                        risk_col1, risk_col2, risk_col3 = st.columns(3)

                        risk_data = analysis.get("risk_assessment", {})

                        with risk_col1:
                            loc_risk = risk_data.get("location_risk", "N/A")
                            st.write(f"**Location Risk:** {loc_risk}")

                        with risk_col2:
                            maint_risk = risk_data.get("maintenance_risk", "N/A")
                            st.write(f"**Maintenance Risk:** {maint_risk}")

                        with risk_col3:
                            overall_risk = risk_data.get("overall_risk", "N/A")
                            st.write(f"**Overall Risk:** {overall_risk}")

                        # Property features
                        st.subheader("🏡 Property Features")

                        features = analysis.get("property_features", {})

                        feat_col1, feat_col2 = st.columns(2)

                        with feat_col1:
                            st.write("**Amenities:**")
                            amenities = features.get("amenities", [])
                            for amenity in amenities:
                                st.write(f"✓ {amenity}")

                        with feat_col2:
                            st.write("**Nearby Facilities:**")
                            facilities = features.get("nearby_facilities", [])
                            for facility in facilities:
                                st.write(f"✓ {facility}")

                        # Market comparison
                        st.subheader("🔄 Comparable Properties")

                        comparables = analysis.get("market_analysis", {}).get("comparable_properties", [])
                        if comparables:
                            comp_df = pd.DataFrame([
                                {
                                    "Address": c.get("address", "N/A"),
                                    "Price": f"${c.get('price', 0):,.0f}",
                                    "SqFt": c.get("sqft", 0),
                                    "Price/SqFt": f"${c.get('price_per_sqft', 0):.2f}"
                                }
                                for c in comparables
                            ])
                            st.dataframe(comp_df, use_container_width=True, hide_index=True)

                        # Future projections
                        st.subheader("🚀 5-Year Projections")

                        projections = analysis.get("future_projections", {})

                        proj_col1, proj_col2, proj_col3 = st.columns(3)

                        with proj_col1:
                            proj_value = projections.get("projected_value_5years", 0)
                            st.write(f"**Projected Value:** ${proj_value:,.0f}")

                        with proj_col2:
                            proj_rental = projections.get("projected_rental_income_5years", 0)
                            st.write(f"**Projected Rental:** ${proj_rental:,.0f}")

                        with proj_col3:
                            proj_total = projections.get("projected_total_value_5years", 0)
                            st.write(f"**Total Value:** ${proj_total:,.0f}")

                        # Recommendations
                        st.subheader("💼 Recommendations")

                        recommendations = analysis.get("recommendations", [])
                        for idx, rec in enumerate(recommendations, 1):
                            st.write(f"{idx}. {rec}")

                        # Full data view
                        with st.expander("📄 View Full Analysis Data"):
                            st.json(analysis)

                    else:
                        st.error(f"Analysis failed: {analysis.get('error', 'Unknown error')}")

                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")

    # ============ TAB 2: COMPARISON ============
    with tab2:
        st.header("Property Comparison")

        if "last_analysis" in st.session_state:
            analysis = st.session_state.last_analysis

            if analysis.get("status") == "success":
                property_analysis = analysis.get("analysis", {})
                summary = property_analysis.get("analysis_summary", {})

                st.subheader(f"Analysis for: {summary.get('property_name', 'Unknown')}")

                # Comparison metrics
                comp_col1, comp_col2, comp_col3 = st.columns(3)

                with comp_col1:
                    value = summary.get("estimated_value", 0)
                    st.metric("Property Value", f"${value:,.0f}")

                with comp_col2:
                    roi = summary.get("roi", 0)
                    st.metric("ROI", f"{roi:.1f}%")

                with comp_col3:
                    score = summary.get("investment_score", 0)
                    st.metric("Score", f"{score}/10")

                # Comparable properties table
                st.subheader("Market Comparables")

                comparables = property_analysis.get("market_analysis", {}).get("comparable_properties", [])
                if comparables:
                    comp_data = []
                    for comp in comparables:
                        comp_data.append({
                            "Property": comp.get("address", "N/A"),
                            "Price": comp.get("price", 0),
                            "SqFt": comp.get("sqft", 0),
                            "Beds": comp.get("beds", 0),
                            "Price/SqFt": comp.get("price_per_sqft", 0)
                        })

                    comp_df = pd.DataFrame(comp_data)
                    st.dataframe(comp_df, use_container_width=True, hide_index=True)
            else:
                st.info("No analysis data available. Run an analysis first!")
        else:
            st.info("No analysis history yet. Run an analysis to see comparisons!")

    # ============ TAB 3: SYSTEM INFO ============
    with tab3:
        st.header("System Information")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Name", "Real Estate Intelligence System")
            st.metric("Version", "1.0.0")
            st.metric("Framework", "Agno Framework + Streamlit")

        with col2:
            st.metric("Model", settings.AGENT_MODEL)
            st.metric("Database", settings.DB_FILE)
            st.metric("Currency", settings.CURRENCY)

        st.subheader("Features")
        features = [
            "Property Valuation",
            "Market Analysis",
            "Investment Scoring",
            "Risk Assessment",
            "Future Projections",
            "Multi-Agent Analysis"
        ]
        for feature in features:
            st.write(f"✓ {feature}")

        # Health check
        st.divider()
        st.subheader("Health Status")
        st.success("✅ System is healthy and running")

    # ============ TAB 4: HUMAN INTERVENTION ============
    with tab4:
        st.header("Human Intervention & Approval")

        st.subheader("Analysis Management")

        # Section 1: Validation
        with st.expander("🔍 Validate Analysis", expanded=True):
            st.write("Validate the last analysis result")

            if "last_analysis" in st.session_state:
                analysis = st.session_state.last_analysis.get("analysis", {})

                # Run validation
                is_valid, issues = validation_manager.validate_analysis(analysis)

                if is_valid:
                    st.success("✅ Analysis validation PASSED - No issues found")
                else:
                    st.warning(f"⚠️ Analysis validation FAILED - {len(issues)} issue(s) found")
                    for issue in issues:
                        st.write(f"• {issue}")

                # Validation report
                report = validation_manager.get_validation_report(analysis)
                with st.expander("📋 Full Validation Report"):
                    st.json(report)
            else:
                st.info("No analysis available. Run an analysis first.")

        # Section 2: Feedback
        with st.expander("💬 Submit Feedback"):
            st.write("Provide feedback on the analysis")

            if "last_analysis" in st.session_state:
                property_name = st.session_state.last_analysis.get("analysis", {}).get("analysis_summary", {}).get("property_name", "Unknown")

                col1, col2 = st.columns(2)

                with col1:
                    analyst_name = st.text_input("Analyst Name", value="Analyst", key="feedback_analyst")
                    feedback_type = st.selectbox(
                        "Feedback Type",
                        ["correction", "clarification", "approval", "rejection"],
                        key="feedback_type_select"
                    )

                with col2:
                    confidence_adj = st.slider(
                        "Confidence Adjustment",
                        min_value=-1.0,
                        max_value=1.0,
                        value=0.0,
                        step=0.1,
                        key="confidence_slider"
                    )

                feedback_text = st.text_area(
                    "Feedback Content",
                    placeholder="Provide detailed feedback here...",
                    height=100,
                    key="feedback_text"
                )

                if st.button("Submit Feedback", type="primary", key="submit_feedback_btn"):
                    feedback_record = feedback_handler.submit_feedback(
                        property_address=property_name,
                        feedback_type=feedback_type,
                        feedback_content=feedback_text,
                        analyst_name=analyst_name,
                        confidence_adjustment=confidence_adj
                    )
                    st.success(f"✅ Feedback submitted (ID: {feedback_record['id']})")
                    st.json(feedback_record)
            else:
                st.info("No analysis available. Run an analysis first.")

        # Section 3: Approval Workflow
        with st.expander("✅ Approval Workflow"):
            st.write("Manage analysis approvals")

            approval_action = st.radio(
                "Approval Action",
                ["View Pending", "Approve Analysis", "Reject Analysis", "Request Revisions"],
                key="approval_action"
            )

            if approval_action == "View Pending":
                pending = approval_workflow.get_pending_approvals()
                if pending:
                    st.write(f"Found {len(pending)} pending approval(s)")
                    for approval in pending:
                        st.write(f"- **{approval['property_address']}** (ID: {approval['analysis_id']})")
                else:
                    st.info("No pending approvals")

            elif approval_action == "Approve Analysis":
                if "last_analysis" in st.session_state:
                    analysis = st.session_state.last_analysis.get("analysis", {})
                    property_name = analysis.get("analysis_summary", {}).get("property_name", "Unknown")

                    col1, col2 = st.columns(2)
                    with col1:
                        reviewer = st.text_input("Reviewer Name", value="Reviewer", key="approver_name")
                    with col2:
                        analysis_id = st.text_input("Analysis ID", value=f"PROP_{hash(property_name) % 10000}", key="analysis_id_approve")

                    approval_notes = st.text_area("Approval Notes", key="approval_notes")

                    if st.button("Approve Analysis", type="primary", key="approve_btn"):
                        result = approval_workflow.approve_analysis(
                            analysis_id=analysis_id,
                            reviewer_name=reviewer,
                            approval_notes=approval_notes
                        )
                        st.success("✅ Analysis approved!")
                        st.json(result)
                else:
                    st.info("No analysis available.")

            elif approval_action == "Reject Analysis":
                if "last_analysis" in st.session_state:
                    analysis = st.session_state.last_analysis.get("analysis", {})
                    property_name = analysis.get("analysis_summary", {}).get("property_name", "Unknown")

                    col1, col2 = st.columns(2)
                    with col1:
                        reviewer = st.text_input("Reviewer Name", value="Reviewer", key="rejector_name")
                    with col2:
                        analysis_id = st.text_input("Analysis ID", value=f"PROP_{hash(property_name) % 10000}", key="analysis_id_reject")

                    rejection_reason = st.text_area("Rejection Reason", key="rejection_reason")

                    if st.button("Reject Analysis", type="primary", key="reject_btn"):
                        result = approval_workflow.reject_analysis(
                            analysis_id=analysis_id,
                            reviewer_name=reviewer,
                            rejection_reason=rejection_reason
                        )
                        st.warning("❌ Analysis rejected!")
                        st.json(result)
                else:
                    st.info("No analysis available.")

            elif approval_action == "Request Revisions":
                if "last_analysis" in st.session_state:
                    analysis = st.session_state.last_analysis.get("analysis", {})
                    property_name = analysis.get("analysis_summary", {}).get("property_name", "Unknown")

                    col1, col2 = st.columns(2)
                    with col1:
                        reviewer = st.text_input("Reviewer Name", value="Reviewer", key="revisions_reviewer")
                    with col2:
                        analysis_id = st.text_input("Analysis ID", value=f"PROP_{hash(property_name) % 10000}", key="analysis_id_revisions")

                    revision_notes = st.text_area("Revision Notes", key="revision_notes")

                    if st.button("Request Revisions", type="primary", key="revisions_btn"):
                        result = approval_workflow.request_revisions(
                            analysis_id=analysis_id,
                            reviewer_name=reviewer,
                            revision_notes=revision_notes
                        )
                        st.info("📝 Revision request submitted!")
                        st.json(result)
                else:
                    st.info("No analysis available.")

        # Section 4: Statistics
        with st.expander("📊 Statistics"):
            col1, col2, col3 = st.columns(3)

            with col1:
                feedback_stats = feedback_handler.get_feedback_summary()
                st.metric("Total Feedback", feedback_stats["total_feedback"])
                st.write(f"Unique Properties: {feedback_stats['unique_properties']}")
                st.write(f"Unique Analysts: {feedback_stats['unique_analysts']}")

            with col2:
                approval_stats = approval_workflow.get_approval_statistics()
                st.metric("Total Approvals", approval_stats["total_approvals"])
                st.write(f"Approved: {approval_stats['approved_count']}")
                st.write(f"Rejected: {approval_stats['rejected_count']}")

            with col3:
                st.metric("Pending Approvals", approval_stats["pending_count"])
                st.write(f"Revisions Needed: {approval_stats['revisions_needed_count']}")


if __name__ == "__main__":
    logger.info("Starting Real Estate Intelligence System with Streamlit")
    main()
