# style.py — Visual styling for the app
#
# Streamlit has a default look. This file overrides it with custom CSS
# to create a dark, minimal theme. Each page calls style.inject() to apply it.

import streamlit as st

# All the CSS lives in this one big string.
# It gets injected into the page as raw HTML via st.markdown().
CSS = """
<style>
/* Load the 'Inter' font from Google Fonts (a clean, modern sans-serif) */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400&display=swap');

/* Apply Inter font to everything in the app */
html, body, [class*="css"], [class*="st-"], .stApp {
    font-family: 'Inter', sans-serif !important;
    font-weight: 300 !important;
}

/* Keep Streamlit's built-in icons working (they use a special icon font) */
[data-testid="stIconMaterial"],
[data-testid="collapsedControl"],
.material-symbols-rounded,
[class*="icon"] span[aria-hidden],
header[data-testid="stHeader"] {
    font-family: 'Material Symbols Rounded' !important;
    visibility: hidden;
}

/* Dark background for the top header bar */
header[data-testid="stHeader"] {
    background: #1a1a1a !important;
}

/* Main app background and text color */
.stApp {
    background-color: #1a1a1a;
    color: #d4d4d4;
}

/* Sidebar (left panel with navigation links) */
section[data-testid="stSidebar"] {
    background-color: #141414;
    border-right: 1px solid #2a2a2a;
}

section[data-testid="stSidebar"] * {
    color: #999 !important;
}

/* Headings (h1 = page title, h2 = section headers, etc.) */
h1, h2, h3, h4, h5, h6,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 300 !important;
    color: #e0e0e0 !important;
}

/* Regular paragraph/label text */
p, span, label, .stMarkdown, .stText, .stCaption {
    font-family: 'Inter', sans-serif !important;
    font-weight: 300 !important;
    color: #b0b0b0 !important;
}

/* The flashcard display area (dark card with subtle border) */
.card-panel {
    background: #222;
    border: 1px solid #333;
    border-radius: 2px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.3);
    padding: 2rem 2.5rem;
    margin: 1.5rem auto;
    max-width: 640px;
}

/* Front of the flashcard (the question) */
.card-front {
    font-family: 'Inter', sans-serif;
    font-weight: 300;
    font-size: 1.3em;
    color: #e0e0e0;
    line-height: 1.6;
}

/* Bold text within the front (e.g., the key word) */
.card-front b {
    font-weight: 400;
    color: #fff;
}

/* Back of the flashcard (the answer), shown after clicking "Show Answer" */
.card-back {
    font-family: 'Inter', sans-serif;
    font-weight: 400;
    font-size: 1.15em;
    color: #999;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #333; /* Divider line between front and back */
}

/* Small metadata text (e.g., "Box 3") */
.card-meta {
    font-family: 'Inter', sans-serif;
    font-weight: 300;
    font-size: 0.85em;
    color: #666;
    margin-top: 0.5rem;
}

/* All buttons: transparent with a subtle border */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 300 !important;
    background: transparent !important;
    color: #999 !important;
    border: 1px solid #444 !important;
    border-radius: 2px !important;
    box-shadow: none !important;
    transition: border-color 0.2s, color 0.2s, background 0.2s;
}

/* Button hover effect: slightly brighter */
.stButton > button:hover {
    border-color: #777 !important;
    color: #ddd !important;
    background: #2a2a2a !important;
}

/* Button when clicked or focused */
.stButton > button:active,
.stButton > button:focus {
    border-color: #777 !important;
    color: #ddd !important;
    background: #333 !important;
    box-shadow: none !important;
}

/* Form submit buttons (same style as regular buttons) */
.stFormSubmitButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 300 !important;
    background: transparent !important;
    color: #999 !important;
    border: 1px solid #444 !important;
    border-radius: 2px !important;
    box-shadow: none !important;
}

.stFormSubmitButton > button:hover {
    border-color: #777 !important;
    color: #ddd !important;
    background: #2a2a2a !important;
}

/* Text input fields and text areas */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    font-family: 'Inter', sans-serif !important;
    font-weight: 300 !important;
    border: 1px solid #333 !important;
    border-radius: 2px !important;
    background: #1e1e1e !important;
    color: #d4d4d4 !important;
}

/* Input fields when focused (typing) */
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #555 !important;
    box-shadow: none !important;
}

/* Dropdown select boxes */
.stSelectbox > div > div {
    font-family: 'Inter', sans-serif !important;
    font-weight: 300 !important;
    border-radius: 2px !important;
    background: #1e1e1e !important;
    color: #d4d4d4 !important;
}

/* Progress bar (shows how far through the review session you are) */
.stProgress > div > div > div {
    background-color: #555 !important;
    border-radius: 1px !important;
}

/* Expandable sections (used on the Browse page for each card) */
.streamlit-expanderHeader {
    font-family: 'Inter', sans-serif !important;
    font-weight: 300 !important;
    color: #b0b0b0 !important;
    background: #222 !important;
    border: 1px solid #333 !important;
    border-radius: 2px !important;
}

/* File upload widget */
.stFileUploader {
    font-family: 'Inter', sans-serif !important;
}

/* Small keyboard shortcut hints at the bottom of the study page */
.shortcut-hint {
    text-align: center;
    font-size: 0.8em;
    color: #555 !important;
    margin-top: 2rem;
    letter-spacing: 0.02em;
}

/* Info/success/warning notification boxes */
.stAlert {
    font-family: 'Inter', sans-serif !important;
    font-weight: 300 !important;
    border-radius: 2px !important;
}
</style>
"""


def inject():
    """Inject the custom CSS into the current Streamlit page.
    Must be called once per page (Streamlit re-runs the whole script on each interaction).
    """
    st.markdown(CSS, unsafe_allow_html=True)