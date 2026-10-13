"""Side decorations for HerMetrics Ranking only. No change to data or charts."""
from pathlib import Path
import base64
import streamlit as st


def render_ranking_side_art():
    folder = Path(__file__).resolve().parent / "assets" / "vietnam_art"
    left = folder / "ranking_left_art.png"
    right = folder / "ranking_right_bamboo.png"
    if not (left.is_file() and right.is_file()):
        return
    def uri(path):
        return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode("ascii")
    st.markdown("""<style>
    /* Visible on large desktop screens; never obstruct content or navigation. */
    @media (min-width: 1500px) {
      [data-testid="stAppViewContainer"]::before,
      [data-testid="stAppViewContainer"]::after {
        content: ""; position: fixed; pointer-events: none; z-index: 0;
        background-repeat: no-repeat; background-size: contain;
        bottom: 0; opacity: .88;
      }
      [data-testid="stAppViewContainer"]::before {
        left: 280px; width: min(23vw, 400px); height: 75vh;
        background-position: left bottom;
        background-image: url('""" + uri(left) + """');
      }
      [data-testid="stAppViewContainer"]::after {
        right: 0; width: min(25vw, 410px); height: 94vh;
        background-position: right bottom;
        background-image: url('""" + uri(right) + """');
      }
      [data-testid="stMainBlockContainer"] {position: relative; z-index: 1;}
    }
    @media (max-width: 1499px) {
      [data-testid="stAppViewContainer"]::before,
      [data-testid="stAppViewContainer"]::after {display:none!important;}
    }
    </style>""", unsafe_allow_html=True)
