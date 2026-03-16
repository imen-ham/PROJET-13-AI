import streamlit as st
import json
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="FormExtract",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Imports internes
from app.extractor.pdf_extractor import PDFExtractor
from app.extractor.image_extractor import ImageExtractor
from app.extractor.ai_extractor import AIExtractor
from app.extractor.schema_manager import SchemaManager
from app.validator.data_validator import DataValidator
from app.ui.components import confidence_badge, status_icon, metric_card, render_header
from app.config import Config

# ─── CSS global ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background: #f0f4ff; color: #2c2c3e; }
    .stSidebar { background: #ffffff; border-right: 2px solid #dde3f5; }

    .stButton > button {
        background: #7c9ef5;
        color: white; border: none; border-radius: 8px;
        padding: 10px 24px; font-weight: 600; width: 100%;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background: #6b8ef0;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(124,158,245,0.4);
    }

    .field-card {
        background: #ffffff;
        border-radius: 10px; padding: 16px;
        margin: 8px 0; border: 1px solid #dde3f5;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }

    .stTextInput input, .stSelectbox select, .stTextArea textarea {
        background: #ffffff !important;
        color: #2c2c3e !important;
        border: 1px solid #c8d3f0 !important;
        border-radius: 8px !important;
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border-radius: 10px; padding: 16px;
        border: 1px solid #dde3f5;
        box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    }

    h1, h2, h3 { color: #5b7ee5 !important; }

    .stTabs [data-baseweb="tab"] {
        background: #e8eeff;
        border-radius: 8px 8px 0 0;
        font-weight: 500;
        color: #5b7ee5;
    }

    .stTabs [aria-selected="true"] {
        background: #7c9ef5 !important;
        color: white !important;
    }

    .stAlert { border-radius: 10px; }
    .stDataFrame { border-radius: 10px; box-shadow: 0 1px 4px rgba(0,0,0,0.04); }
    .stExpander { border: 1px solid #dde3f5 !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ─── Init session state ──────────────────────────────────────────────────────
for key in ["extracted_data", "validated_data", "selected_schema", "raw_text", "corrections"]:
    if key not in st.session_state:
        st.session_state[key] = None
if "corrections" not in st.session_state:
    st.session_state.corrections = {}

# ─── Instances ───────────────────────────────────────────────────────────────
pdf_extractor = PDFExtractor()
img_extractor = ImageExtractor()
ai_extractor = AIExtractor()
schema_manager = SchemaManager()
validator = DataValidator()

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📋 FormExtract")
    st.markdown("---")

    st.markdown("### 📊 Statut du système")
    if Config.AI_PROVIDER == "mock":
        st.info("⚙️ Mode standard actif")
    elif Config.AI_PROVIDER == "groq" and Config.GROQ_API_KEY:
        st.success("✅ Système connecté")
    elif Config.AI_PROVIDER == "anthropic" and Config.ANTHROPIC_API_KEY:
        st.success("✅ Système connecté")
    else:
        st.warning("⚠️ Configuration manquante")

    st.markdown("---")
    st.markdown("### 📖 Guide rapide")
    st.markdown("""
    1. 📤 **Uploadez** votre formulaire
    2. 📋 **Choisissez** un modèle de champs
    3. 🔍 **Lancez** l'analyse
    4. ✏️ **Corrigez** si besoin
    5. 💾 **Exportez** le résultat
    """)

    st.markdown("---")
    st.markdown("### 📁 Formats supportés")
    st.markdown("""
    - 📄 PDF
    - 📝 TXT
    - 🖼️ PNG / JPG / WEBP
    """)

# ─── Header ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background: linear-gradient(135deg, #7c9ef5 0%, #a5b8f8 100%);
            padding: 28px 32px; border-radius: 14px; margin-bottom: 24px;">
    <h1 style="color: white; margin: 0; font-size: 2em;">📋 FormExtract</h1>
    <p style="color: rgba(255,255,255,0.9); margin: 6px 0 0 0; font-size: 1em;">
        Extraction et traitement automatique de données depuis vos formulaires
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Tabs ────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload & Analyse", "📋 Schéma", "✏️ Résultats & Correction", "📥 Export"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Upload & Analyse
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📤 Importer un document")
        uploaded_file = st.file_uploader(
            "Glissez votre formulaire ici",
            type=["pdf", "txt", "png", "jpg", "jpeg", "webp"],
            help="Formats supportés : PDF, TXT, PNG, JPG"
        )

        if uploaded_file:
            file_ext = Path(uploaded_file.name).suffix.lower()
            file_bytes = uploaded_file.read()

            st.markdown(f"""
            <div class="field-card">
                📄 <b>{uploaded_file.name}</b><br>
                📦 Taille : {len(file_bytes)/1024:.1f} KB &nbsp;|&nbsp;
                🏷️ Type : {uploaded_file.type}
            </div>
            """, unsafe_allow_html=True)

            with st.spinner("🔍 Lecture du document..."):
                if file_ext == ".pdf":
                    extracted_doc = pdf_extractor.extract_from_bytes(file_bytes, uploaded_file.name)
                    raw_text = extracted_doc.get("text", "")
                    method = extracted_doc.get("method", "pdfplumber")
                    if "error_pdfplumber" in extracted_doc:
                        st.warning(f"⚠️ {extracted_doc['error_pdfplumber']}")
                elif file_ext == ".txt":
                    raw_text = file_bytes.decode("utf-8", errors="replace")
                    method = "texte brut"
                elif file_ext in [".png", ".jpg", ".jpeg", ".webp"]:
                    ocr_result = img_extractor.extract_text(file_bytes)
                    raw_text = ocr_result.get("text", "")
                    method = f"Reconnaissance optique (confiance : {ocr_result.get('confidence', 0):.0%})"
                    if "error" in ocr_result:
                        st.error(f"❌ Erreur : {ocr_result['error']}")
                else:
                    raw_text = ""
                    method = "non supporté"

                st.session_state.raw_text = raw_text

            st.success(f"✅ Document lu via **{method}**")

            with st.expander("👁️ Aperçu du contenu détecté"):
                if raw_text.strip():
                    st.text_area("", raw_text[:3000], height=200, disabled=True)
                else:
                    st.error("❌ Aucun contenu détecté. Vérifiez le fichier.")

    with col2:
        st.markdown("### 🔍 Lancer l'analyse")

        schemas = schema_manager.get_default_schemas()
        selected_name = st.selectbox("📋 Modèle de formulaire", list(schemas.keys()))
        st.session_state.selected_schema = schemas[selected_name]

        schema_df = pd.DataFrame(schema_manager.schema_to_display(st.session_state.selected_schema))
        st.dataframe(schema_df, use_container_width=True, hide_index=True)

        if st.session_state.raw_text:
            if st.button("⚡ Analyser le document", type="primary"):
                with st.spinner("🔍 Analyse en cours..."):
                    result = ai_extractor.extract(
                        st.session_state.raw_text,
                        st.session_state.selected_schema
                    )
                    validated = validator.validate_and_enrich(
                        result,
                        st.session_state.selected_schema
                    )
                    st.session_state.extracted_data = result
                    st.session_state.validated_data = validated
                    st.session_state.corrections = {
                        k: v.get("value") for k, v in validated.get("validated_fields", {}).items()
                    }

                st.success("✅ Analyse terminée ! Consultez l'onglet **Résultats & Correction**")

                vd = st.session_state.validated_data
                c1, c2, c3, c4 = st.columns(4)
                metric_card(c1, "Total champs", vd["total_fields"], color="#7c9ef5")
                metric_card(c2, "Détectés", vd["extracted_count"], color="#6bc8a0")
                metric_card(c3, "Valides", vd["valid_count"], color="#5bc4d4")
                metric_card(c4, "À vérifier", vd["review_count"], color="#f87c7c")
        else:
            st.info("👆 Uploadez d'abord un document")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Schéma
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 📋 Éditeur de modèle de formulaire")
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("#### Modèle actuel")
        schema_json = st.text_area(
            "Éditez votre modèle JSON",
            value=json.dumps(
                st.session_state.selected_schema or schema_manager.get_default_schemas()["Formulaire générique"],
                indent=2, ensure_ascii=False
            ),
            height=400
        )

        if st.button("✅ Valider et appliquer ce modèle"):
            try:
                parsed = schema_manager.load_from_json(schema_json)
                ok, msg = schema_manager.validate_schema(parsed)
                if ok:
                    st.session_state.selected_schema = parsed
                    st.success(f"✅ {msg}")
                else:
                    st.error(f"❌ {msg}")
            except json.JSONDecodeError as e:
                st.error(f"❌ Format invalide : {e}")

    with col2:
        st.markdown("#### Ajouter un champ")
        new_field_name = st.text_input("Nom du champ", placeholder="ex : numero_contrat")
        new_field_type = st.selectbox("Type", ["string", "number", "boolean"])
        new_field_desc = st.text_input("Description", placeholder="ex : Numéro de contrat")
        new_field_format = st.selectbox("Format (optionnel)", ["", "date", "email", "uri"])
        new_required = st.checkbox("Obligatoire")

        if st.button("➕ Ajouter ce champ"):
            if new_field_name and st.session_state.selected_schema:
                field_def = {"type": new_field_type}
                if new_field_desc:
                    field_def["description"] = new_field_desc
                if new_field_format:
                    field_def["format"] = new_field_format
                st.session_state.selected_schema["properties"][new_field_name] = field_def
                if new_required:
                    req = st.session_state.selected_schema.get("required", [])
                    if new_field_name not in req:
                        req.append(new_field_name)
                    st.session_state.selected_schema["required"] = req
                st.success(f"✅ Champ '{new_field_name}' ajouté !")
                st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Résultats & Correction
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    if not st.session_state.validated_data:
        st.info("⏳ Lancez d'abord une analyse dans l'onglet **Upload & Analyse**")
    else:
        vd = st.session_state.validated_data
        fields = vd.get("validated_fields", {})

        st.markdown("### 📊 Résumé de l'analyse")
        c1, c2, c3, c4, c5 = st.columns(5)
        metric_card(c1, "Total", vd["total_fields"], color="#7c9ef5")
        metric_card(c2, "Détectés", vd["extracted_count"], color="#6bc8a0")
        metric_card(c3, "Valides", vd["valid_count"], color="#5bc4d4")
        metric_card(c4, "À vérifier", vd["review_count"], color="#f87c7c")
        metric_card(c5, "Fiabilité", f"{vd['overall_confidence']:.0%}", color="#b39cf5")

        notes = vd.get("notes", "")
        if notes and "mock" not in notes.lower() and "api" not in notes.lower():
            st.info(f"ℹ️ {notes}")

        if vd.get("global_issues"):
            with st.expander(f"⚠️ {len(vd['global_issues'])} problème(s) détecté(s)"):
                for issue in vd["global_issues"]:
                    st.markdown(f"• {issue}")

        st.markdown("---")
        st.markdown("### ✏️ Champs détectés — Vérification et correction")

        for field_name, field_data in fields.items():
            status = field_data.get("status", "missing")
            conf = field_data.get("confidence", 0)
            value = field_data.get("value")
            is_valid = field_data.get("is_valid", True)

            border_color = {
                "high_confidence": "#6bc8a0",
                "medium_confidence": "#f5c97a",
                "low_confidence": "#f5a27a",
                "invalid": "#f87c7c",
                "missing": "#c8d3f0"
            }.get(status, "#dde3f5")

            st.markdown(f"""
            <div style="background:#ffffff;border-left:4px solid {border_color};
                        border-radius:8px;padding:12px;margin:6px 0;
                        box-shadow:0 1px 4px rgba(0,0,0,0.05)">
                <span style="font-weight:700;color:#5b7ee5">{field_name}</span>
                &nbsp;&nbsp;{status_icon(status)}&nbsp;
                <span style="font-size:0.8em">{confidence_badge(conf)}</span>
                {f'<span style="color:#f87c7c;font-size:0.8em"> — {field_data.get("validation_message","")}</span>' if not is_valid else ''}
            </div>
            """, unsafe_allow_html=True)

            corrected = st.text_input(
                f"Valeur pour {field_name}",
                value=str(value) if value is not None else "",
                key=f"correction_{field_name}",
                label_visibility="collapsed"
            )
            st.session_state.corrections[field_name] = corrected if corrected else None

        if st.button("💾 Enregistrer les corrections"):
            st.success("✅ Corrections sauvegardées !")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — Export
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    if not st.session_state.validated_data:
        st.info("⏳ Lancez d'abord une analyse")
    else:
        st.markdown("### 📥 Export des données")

        corrections = st.session_state.corrections or {}
        vd = st.session_state.validated_data
        fields = vd.get("validated_fields", {})

        final_data = {}
        for field_name, field_data in fields.items():
            corrected_value = corrections.get(field_name, field_data.get("value"))
            final_data[field_name] = {
                "value": corrected_value,
                "confidence": field_data.get("confidence", 0),
                "status": field_data.get("status", "unknown"),
                "is_valid": field_data.get("is_valid", False),
                "manually_corrected": corrected_value != field_data.get("value")
            }

        export_json = {
            "metadata": {
                "overall_confidence": vd.get("overall_confidence", 0),
                "total_fields": vd.get("total_fields", 0),
                "extracted_count": vd.get("extracted_count", 0),
                "valid_count": vd.get("valid_count", 0),
            },
            "data": {k: v["value"] for k, v in final_data.items()},
            "details": final_data
        }

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📄 Aperçu des données extraites")
            st.json(export_json["data"])

        with col2:
            st.markdown("#### 💾 Télécharger")

            json_str = json.dumps(export_json, indent=2, ensure_ascii=False)
            st.download_button(
                "⬇️ JSON complet",
                data=json_str,
                file_name="formulaire_extrait.json",
                mime="application/json"
            )

            csv_data = pd.DataFrame([
                {"Champ": k, "Valeur": v["value"], "Fiabilité": f'{v["confidence"]:.0%}', "Statut": v["status"]}
                for k, v in final_data.items()
            ])
            st.download_button(
                "⬇️ Export CSV",
                data=csv_data.to_csv(index=False),
                file_name="formulaire_extrait.csv",
                mime="text/csv"
            )

            simple_json = json.dumps(export_json["data"], indent=2, ensure_ascii=False)
            st.download_button(
                "⬇️ JSON simplifié",
                data=simple_json,
                file_name="donnees.json",
                mime="application/json"
            )

            st.markdown("---")
            st.markdown("##### 📊 Tableau récapitulatif")
            st.dataframe(csv_data, use_container_width=True, hide_index=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:20px;color:#a0aec0;margin-top:40px;
            border-top:1px solid #dde3f5;font-size:0.85em">
    FormExtract — Projet 13 | Traitement automatique de formulaires
</div>
""", unsafe_allow_html=True)