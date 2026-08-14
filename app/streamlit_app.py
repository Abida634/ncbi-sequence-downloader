"""Streamlit web GUI for the NCBI Sequence Downloader."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
import logging

from downloader.config import Config
from downloader.downloader import Downloader
from downloader.exceptions import DownloaderError
from downloader.history import HistoryManager
from downloader.logger import setup_logging
from downloader.metadata import extract_metadata
from downloader.statistics import compute_stats

setup_logging(level=logging.INFO)

st.set_page_config(
    page_title="NCBI Sequence Downloader",
    page_icon="🧬",
    layout="centered",
    initial_sidebar_state="expanded",
)


def inject_custom_css() -> None:
    """Inject custom CSS to override Streamlit's default styling.

    This must be called once, early in the script, before other elements
    are rendered — CSS applies globally regardless of injection order,
    but keeping it first makes the script easier to read top-to-bottom.
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        html, body, [class*="css"] {
            font-family: 'Space Grotesk', sans-serif;
        }

        /* Hero header with gradient background */
        .hero {
            background: linear-gradient(135deg, #134E4A 0%, #312E81 100%);
            padding: 2.2rem 2rem;
            border-radius: 18px;
            margin-bottom: 1.8rem;
            border: 1px solid rgba(45, 212, 191, 0.25);
        }
        .hero h1 {
            font-size: 2.1rem;
            margin: 0;
            background: linear-gradient(90deg, #2DD4BF, #A78BFA);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero p {
            color: #94A3B8;
            margin-top: 0.4rem;
            margin-bottom: 0;
        }

        /* Card container used for result panels */
        .card {
            background: #1E293B;
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 14px;
            padding: 1.4rem 1.5rem;
            margin-bottom: 1rem;
        }
        .card h4 {
            margin-top: 0;
            color: #2DD4BF;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* Monospace styling for sequence-related text */
        .mono {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            color: #CBD5E1;
        }

        /* Primary download button */
        div.stButton > button[kind="primary"] {
            background: linear-gradient(90deg, #2DD4BF, #14B8A6);
            border: none;
            border-radius: 10px;
            font-weight: 600;
            transition: transform 0.15s ease;
        }
        div.stButton > button[kind="primary"]:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 14px rgba(45, 212, 191, 0.35);
        }

        /* Sidebar tweaks */
        section[data-testid="stSidebar"] {
            background: #0B1220;
            border-right: 1px solid rgba(148, 163, 184, 0.1);
        }

        /* Metric styling */
        div[data-testid="stMetric"] {
            background: #1E293B;
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 12px;
            padding: 0.8rem 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource
def get_downloader() -> Downloader | None:
    """Build (and cache) a single Downloader instance for the app's lifetime."""
    try:
        config = Config.from_env()
        return Downloader(config)
    except DownloaderError:
        return None


def render_header() -> None:
    """Render the gradient hero header."""
    st.markdown(
        """
        <div class="hero">
            <h1>🧬 NCBI Sequence Downloader</h1>
            <p>Fetch DNA, RNA, and protein sequences directly from NCBI — fast, validated, documented.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_download_form(downloader: Downloader) -> None:
    """Render the accession/format input form and handle the download action."""
    with st.container():
        st.markdown('<div class="card"><h4>Search NCBI</h4>', unsafe_allow_html=True)

        col_input, col_format = st.columns([2, 1])
        with col_input:
            accession = st.text_input(
                "Accession number",
                placeholder="e.g. NM_001301717",
                label_visibility="collapsed",
            )
        with col_format:
            fmt = st.selectbox("Format", options=["fasta", "genbank"], label_visibility="collapsed")

        download_clicked = st.button("⬇ Download Sequence", type="primary", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    if download_clicked:
        if not accession:
            st.warning("Please enter an accession number.")
            return

        with st.spinner(f"Contacting NCBI for {accession}..."):
            try:
                result = downloader.download(accession=accession, fmt=fmt)
            except DownloaderError as exc:
                st.error(f"Download failed: {exc}")
                return

        st.success(f"Saved to `{result.saved_path}`")
        render_result(result, fmt)


def render_result(result, fmt: str) -> None:
    """Render sequence statistics and metadata for a completed download."""
    stats = compute_stats(result.record)

    st.markdown('<div class="card"><h4>Sequence Statistics</h4></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    col1.metric("Length", f"{stats.length:,} bp")
    col2.metric("GC Content", f"{stats.gc_content:.1f}%")
    col3.metric("AT Content", f"{stats.at_content:.1f}%")

    if fmt == "genbank":
        meta = extract_metadata(result.record)
        st.markdown(
            f"""
            <div class="card">
                <h4>Metadata</h4>
                <p><b>Organism:</b> <span class="mono">{meta.organism}</span></p>
                <p><b>Gene:</b> <span class="mono">{meta.gene_name or 'N/A'}</span></p>
                <p><b>Definition:</b> {meta.definition}</p>
                <p><b>Molecule type:</b> <span class="mono">{meta.molecule_type or 'N/A'}</span></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with open(result.saved_path, "rb") as f:
        st.download_button(
            label="📥 Save file to my computer",
            data=f.read(),
            file_name=result.saved_path.name,
            use_container_width=True,
        )


def render_history() -> None:
    """Render the download history as a table in the sidebar."""
    history = HistoryManager()
    entries = history.load_all()

    st.sidebar.markdown("### 📜 Download History")

    if not entries:
        st.sidebar.caption("No downloads yet — your history will appear here.")
        return

    st.sidebar.metric("Total downloads", len(entries))
    st.sidebar.divider()

    for entry in reversed(entries[-8:]):
        st.sidebar.markdown(
            f"""
            <div style="padding:0.5rem 0; border-bottom:1px solid rgba(148,163,184,0.1);">
                <span class="mono" style="color:#2DD4BF;">{entry.accession}</span><br>
                <span style="font-size:0.75rem; color:#64748B;">{entry.format} · {entry.timestamp[:19].replace('T', ' ')}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


def main() -> None:
    """The Streamlit app's entry point."""
    inject_custom_css()
    render_header()

    downloader = get_downloader()
    if downloader is None:
        st.error(
            "Configuration error: could not load settings. "
            "Make sure your .env file exists with a valid ENTREZ_EMAIL."
        )
        return

    render_download_form(downloader)
    render_history()


main()