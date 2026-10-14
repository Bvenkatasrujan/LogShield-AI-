import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

from src.analyzer import analyze_logs

# Page Config & Title
st.set_page_config(
    page_title="LogShield AI - Log File Analyzer",
    page_icon="🛡️",
    layout="wide"
)

# Custom Styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #555;
        margin-bottom: 30px;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-left: 5px solid #1E88E5;
        padding: 15px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">🛡️ LOGSHIELD AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Based Log File Analyzer Using Python & Machine Learning</div>', unsafe_allow_html=True)

# Sidebar Options
st.sidebar.header("📁 Data Source Selection")
data_option = st.sidebar.radio(
    "Choose Log Data Source:",
    [
        "Upload CSV File",
        "Load Sample Logs (Mixed)",
        "Load Normal Logs",
        "Load Test Attack Logs",
        "Load Brute Force Attack Logs",
        "Load High Frequency API Logs",
        "Load 10,000 Benchmark Dataset"
    ]
)

uploaded_file = None
if data_option == "Upload CSV File":
    uploaded_file = st.sidebar.file_uploader("Upload a .csv log file", type=["csv"])
elif data_option == "Load Sample Logs (Mixed)":
    uploaded_file = os.path.join("data", "sample_logs.csv")
elif data_option == "Load Normal Logs":
    uploaded_file = os.path.join("data", "normal_logs.csv")
elif data_option == "Load Test Attack Logs":
    uploaded_file = os.path.join("data", "test_logs.csv")
elif data_option == "Load Brute Force Attack Logs":
    uploaded_file = os.path.join("data", "brute_force_logs.csv")
elif data_option == "Load High Frequency API Logs":
    uploaded_file = os.path.join("data", "high_frequency_logs.csv")
elif data_option == "Load 10,000 Benchmark Dataset":
    uploaded_file = os.path.join("data", "benchmark_10k.csv")


if uploaded_file is not None:
    try:
        # Run Pipeline
        analysis = analyze_logs(uploaded_file)
        results = analysis["results"]
        raw_logs = analysis["raw_logs"]

        # Top Overview Cards
        st.subheader("📌 Key Security Metrics")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Events Processed", analysis["total_events"])
        col2.metric("Unique IP Addresses", analysis["unique_ips"])
        
        suspicious_rules = (results["rule_result"] == "Suspicious").sum() if not results.empty else 0
        col3.metric("Rule Violations", int(suspicious_rules))
        col4.metric("AI Anomalies Detected", analysis["anomaly_count"])

        st.markdown("---")

        # Visualizations & Risk Summary
        col_chart, col_risk = st.columns([1, 1])

        with col_chart:
            st.subheader("📊 Risk Distribution")
            if not results.empty and "final_risk" in results.columns:
                risk_counts = results["final_risk"].value_counts().reindex(["LOW", "MEDIUM", "HIGH"]).fillna(0)
                
                fig, ax = plt.subplots(figsize=(6, 3.5))
                colors = ["#2ecc71", "#f39c12", "#e74c3c"]
                bars = ax.bar(risk_counts.index, risk_counts.values, color=colors)
                ax.set_ylabel("IP Count")
                ax.set_title("Threat Risk Distribution")
                for bar in bars:
                    height = bar.get_height()
                    ax.annotate(f'{int(height)}',
                                xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, 3),  # 3 points vertical offset
                                textcoords="offset points",
                                ha='center', va='bottom')
                st.pyplot(fig)
            else:
                st.info("No data available for risk breakdown.")

        with col_risk:
            st.subheader("🔍 AI vs Rule Classification Matrix")
            if not results.empty:
                assessment_counts = results["final_assessment"].value_counts()
                st.dataframe(pd.DataFrame({
                    "Assessment Category": assessment_counts.index,
                    "Count": assessment_counts.values
                }), use_container_width=True)
                
                st.caption(
                    "• **High Attention**: Triggered both Rule threshold AND AI anomaly detector.\n"
                    "• **Investigate**: Novel unusual behavior detected by AI (no rule match).\n"
                    "• **Suspicious**: Known rule threshold exceeded."
                )

        st.markdown("---")

        # Detailed Security Findings Table
        st.subheader("⚠️ Detailed IP Analysis Findings")
        if not results.empty:
            # Color highlighting function for Risk
            def highlight_risk(val):
                if val == "HIGH":
                    return "background-color: #ffcccc; color: #900; font-weight: bold;"
                elif val == "MEDIUM":
                    return "background-color: #fff0bb; color: #8a6d3b; font-weight: bold;"
                elif val == "LOW":
                    return "background-color: #d4edda; color: #155724;"
                return ""

            if hasattr(results.style, "map"):
                styled_results = results.style.map(highlight_risk, subset=["final_risk"])
            else:
                styled_results = results.style.applymap(highlight_risk, subset=["final_risk"])
            st.dataframe(styled_results, use_container_width=True)

            # Download Analysis Report CSV
            report_csv = results.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Complete Analysis Report (CSV)",
                data=report_csv,
                file_name="analysis_report.csv",
                mime="text/csv",
                key="download_report"
            )
        else:
            st.warning("No records to display.")

        # Raw Logs Expander
        with st.expander("📄 View Cleaned Raw Event Logs"):
            st.dataframe(raw_logs, use_container_width=True)

    except Exception as e:
        st.error(f"Error analyzing log file: {str(e)}")
else:
    st.info("👈 Please upload a CSV log file or choose a pre-loaded sample dataset from the sidebar to begin analysis.")
