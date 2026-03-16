import streamlit as st

def confidence_badge(confidence: float) -> str:
    """Retourne HTML pour badge de confiance coloré."""
    if confidence >= 0.9:
        color, label = "#00c851", "🟢 Élevée"
    elif confidence >= 0.7:
        color, label = "#ffbb33", "🟡 Moyenne"
    elif confidence > 0:
        color, label = "#ff4444", "🔴 Faible"
    else:
        color, label = "#aaaaaa", "⚪ Absent"
    return f'<span style="color:{color};font-weight:bold">{label} ({confidence:.0%})</span>'

def status_icon(status: str) -> str:
    icons = {
        "high_confidence": "✅",
        "medium_confidence": "⚠️",
        "low_confidence": "🔴",
        "invalid": "❌",
        "missing": "⬜"
    }
    return icons.get(status, "❓")

def metric_card(col, title, value, delta=None, color="#667eea"):
    with col:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,{color}22,{color}11);
                    border-left:4px solid {color};border-radius:8px;
                    padding:16px;margin:4px 0">
            <div style="font-size:0.8em;color:#888;text-transform:uppercase;letter-spacing:1px">{title}</div>
            <div style="font-size:2em;font-weight:700;color:{color}">{value}</div>
            {f'<div style="font-size:0.8em;color:#888">{delta}</div>' if delta else ''}
        </div>
        """, unsafe_allow_html=True)

def render_header():
    st.markdown("""
    <div style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);
                padding:32px;border-radius:16px;margin-bottom:24px;text-align:center">
        <h1 style="color:white;margin:0;font-size:2.2em">📄 FormExtract AI</h1>
        <p style="color:rgba(255,255,255,0.85);margin:8px 0 0 0;font-size:1.1em">
            Extraction intelligente de données depuis vos formulaires
        </p>
    </div>
    """, unsafe_allow_html=True)