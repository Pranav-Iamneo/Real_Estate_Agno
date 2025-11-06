"""
Real Estate Intelligence System - Streamlit Frontend
Interactive property analysis and investment evaluation
"""

import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime
import traceback

# Configure page
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

# API Configuration
API_BASE_URL = "http://localhost:8082"
API_TIMEOUT = 120

def call_api(endpoint: str, method: str = "GET", data: dict = None) -> dict:
    """Call FastAPI backend"""
    try:
        url = f"{API_BASE_URL}{endpoint}"

        if method == "GET":
            response = requests.get(url, timeout=API_TIMEOUT)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=API_TIMEOUT)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to backend. Is the server running on port 8082?"}
    except Exception as e:
        return {"error": str(e)}

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main Streamlit application"""

    st.title("🏠 Real Estate Intelligence System")
    st.caption("AI-powered property analysis, valuation, and investment recommendations")

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["🔍 Property Analysis", "📊 Comparison", "ℹ️ System Info"])

    # ============ TAB 1: PROPERTY ANALYSIS ============
    with tab1:
        st.header("Property Analysis & Valuation")

        # Sidebar actions
        with st.sidebar:
            st.header("⚙️ Quick Actions")

            if st.button("📋 Run Sample Analysis", width="stretch"):
                with st.spinner("Running sample analysis..."):
                    try:
                        result = call_api("/sample-analyze", method="POST")

                        if "error" in result:
                            st.error(f"Error: {result['error']}")
                        else:
                            st.session_state.last_analysis = result
                            st.success("✅ Sample analysis completed!")
                            st.rerun()
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
            analysis_request = {
                "property": {
                    "address": property_address,
                    "bedrooms": bedrooms,
                    "bathrooms": bathrooms,
                    "sqft": sqft,
                    "age_years": age,
                    "location_type": location,
                    "condition": condition,
                    "neighborhood_rating": neighborhood
                }
            }

            # Call API
            with st.spinner("🔄 Analyzing property..."):
                try:
                    result = call_api("/analyze", method="POST", data=analysis_request)

                    if "error" in result:
                        st.error(f"Error: {result['error']}")
                    else:
                        st.session_state.last_analysis = result
                        st.success("✅ Analysis completed!")
                        st.balloons()

                        if result.get("status") == "success":
                            analysis = result.get("analysis", {})

                            if analysis and analysis.get("analysis_summary"):
                                summary = analysis["analysis_summary"]

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
                                    st.metric("Investment Score", f"{score}/10" if isinstance(score, int) else score)

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
                                    st.write(f"**Market Trend:** {trend.capitalize()}")

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

                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
                    st.write(traceback.format_exc())

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

        with st.spinner("Loading system info..."):
            info = call_api("/info", method="GET")

            if "error" not in info:
                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Name", info.get("name", "N/A"))
                    st.metric("Version", info.get("version", "N/A"))
                    st.metric("Framework", info.get("framework", "N/A"))

                with col2:
                    st.metric("Model", info.get("model", "N/A"))
                    st.metric("Database", info.get("database", "N/A"))
                    st.metric("Currency", info.get("currency", "N/A"))

                st.subheader("Features")
                features = info.get("features", [])
                for feature in features:
                    st.write(f"✓ {feature}")
            else:
                st.error(f"Error: {info.get('error', 'Unknown')}")

        # Health check
        st.divider()
        st.subheader("Health Status")

        with st.spinner("Checking health..."):
            health = call_api("/health", method="GET")

            if "error" not in health:
                status = health.get("status", "unknown")
                if status == "healthy":
                    st.success(f"✅ {health.get('message', 'System is healthy')}")
                else:
                    st.warning(f"⚠️ {health.get('message', 'Status unknown')}")
            else:
                st.error(f"Error: {health.get('error', 'Unknown')}")

if __name__ == "__main__":
    main()
