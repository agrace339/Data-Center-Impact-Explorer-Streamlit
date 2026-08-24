from pathlib import Path

import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "report_assets"
OUTPUTS = ROOT / "analysis_outputs"

PRESSURE_CSV = OUTPUTS / "data_center_pipeline_grid_pressure.csv"
MODELED_CSV = OUTPUTS / "data_center_pipeline_pressure_regression_summary.csv"


st.set_page_config(
    page_title="Electricity EDA | Data Center Impact Explorer",
    page_icon="⚡",
    layout="wide",
)

st.markdown(
    """
    <style>
      :root { --ink:#17324d; --teal:#2f858d; --coral:#dc5c45; --paper:#f7f4ee; }
      .stApp { background: linear-gradient(180deg, #f7f4ee 0%, #ffffff 32%); }
      .block-container { max-width: 1180px; padding-top: 2.2rem; padding-bottom: 4rem; }
      h1, h2, h3 { color: var(--ink); letter-spacing: -0.02em; }
      h1 { font-size: clamp(2.4rem, 5vw, 4.5rem) !important; line-height: .98 !important; }
      .eyebrow { color:var(--teal); font-weight:800; letter-spacing:.14em; text-transform:uppercase; }
      .lede { color:#445565; font-size:1.2rem; line-height:1.65; max-width:820px; }
      .finding { border-left:5px solid var(--coral); background:#fff8f5; padding:1rem 1.2rem;
                 border-radius:0 12px 12px 0; margin:1rem 0 1.5rem; }
      .finding strong { color:var(--ink); }
      .caption { color:#66727c; font-size:.86rem; line-height:1.45; }
      [data-testid="stMetric"] { background:rgba(255,255,255,.82); border:1px solid #dfe5e8;
                                 padding:1rem; border-radius:14px; }
      [data-testid="stMetricValue"] { color:var(--ink); }
      [data-testid="stImage"] img { border-radius:14px; border:1px solid #e7e7e7; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_results() -> tuple[pd.DataFrame, pd.DataFrame]:
    pressure = pd.read_csv(PRESSURE_CSV).set_index("state")
    modeled = pd.read_csv(MODELED_CSV).set_index("state")
    return pressure, modeled


def show_plot(filename: str, caption: str) -> None:
    path = ASSETS / filename
    if not path.exists():
        path = OUTPUTS / filename
    if path.exists():
        st.image(str(path), use_container_width=True)
        st.markdown(f'<p class="caption">{caption}</p>', unsafe_allow_html=True)
    else:
        st.warning(f"Plot asset not found: {filename}")


pressure, modeled = load_results()
pipeline = pressure[pressure["pipeline_projects"] >= 10]

st.markdown('<div class="eyebrow">Data Center Impact Explorer · Electricity</div>', unsafe_allow_html=True)
st.title("How large is the data-center power pipeline?")
st.markdown(
    '<p class="lede">A state-level exploration of data-center development, electricity generation, '
    'and the limits of what current public data can tell us about future grid pressure.</p>',
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("Pipeline projects", "943")
m2.metric("Projects reporting MW", f"{int(pressure.projects_reporting_mw.sum()):,}", "37.6% of pipeline")
m3.metric("Ohio reported pressure", "105.7%", "of 2024 avg. generation")
m4.metric("Virginia modeled pressure", "471.7%", "sensitivity estimate")

st.markdown(
    '<div class="finding"><strong>Main finding.</strong> In several states, reported pipeline capacity '
    'is comparable to an entire state’s average 2024 electricity generation. This is a planning signal, '
    'not a forecast of electricity use, shortages, or outages.</div>',
    unsafe_allow_html=True,
)

st.header("1 · Where development is concentrated")
st.write(
    "The pipeline includes facilities listed as proposed, approved or under construction, or expanding. "
    "Virginia alone accounts for 263 projects, followed by Texas and Georgia."
)
show_plot(
    "pipeline_facilities.png",
    "Source: FracTracker U.S. Data Centers Tracker. Counts describe projects, not realized electricity demand.",
)

st.header("2 · Generation has not moved uniformly")
st.write(
    "Electricity generation followed very different paths across leading data-center states. The index "
    "below sets each state's 2015 generation to 100, making relative change comparable across states."
)
show_plot(
    "leading_state_generation.png",
    "Source: U.S. Energy Information Administration. The latest year may be incomplete for some states.",
)

st.header("3 · Concentration is associated with different outcomes")
st.write(
    "When states are grouped into quartiles by operating data-center concentration, the highest quartile "
    "shows stronger median generation growth and a lower median industrial price. These are descriptive "
    "associations; fuel mix, regulation, market structure, weather, and other factors also shape both outcomes."
)
show_plot(
    "quartile_comparison.png",
    "Source: FracTracker and EIA. Quartile comparisons do not establish that data centers caused either outcome.",
)

st.header("4 · The pipeline is large relative to existing systems")
st.write(
    "For each state, reported pipeline megawatts were divided by average 2024 generation "
    "(annual MWh ÷ 8,760). Ohio and Nevada exceed 100%; Virginia and Indiana approach it."
)
show_plot(
    "data_center_pipeline_grid_pressure.png",
    "Only reported MW are shown. Nameplate or requested capacity is not the same as continuous realized load.",
)

with st.expander("Why missing MW matters", expanded=True):
    st.write(
        "Nearly two-thirds of pipeline facilities do not report capacity. A log-log regression estimated "
        "missing MW from facility square footage where possible. The results are best read as a sensitivity "
        "test: they show how much the reported totals could omit, not what utilities should expect as load."
    )
    show_plot(
        "data_center_pipeline_pressure_with_regression.png",
        "Light blue represents regression-estimated missing MW. Facilities explicitly associated with dedicated or hybrid generation were not imputed.",
    )

st.header("Explore a state")
eligible_states = pipeline.sort_values("pipeline_projects", ascending=False).index.tolist()
selected = st.selectbox("State", eligible_states, index=eligible_states.index("VA"))
row = pressure.loc[selected]
estimate = modeled.loc[selected]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Pipeline projects", f"{int(row.pipeline_projects):,}")
c2.metric("Reporting MW", f"{int(row.projects_reporting_mw):,}", f"{row.mw_reporting_rate_pct:.1f}%")
c3.metric("Reported pipeline", f"{row.reported_pipeline_mw:,.0f} MW")
c4.metric("Reported pressure", f"{row.pipeline_share_of_average_generation_pct:.1f}%")

chart_data = pd.DataFrame(
    {
        "Share of average 2024 generation (%)": [
            row.pipeline_share_of_average_generation_pct,
            estimate.combined_share_pct,
        ]
    },
    index=["Reported MW", "Reported + eligible estimated MW"],
)
st.bar_chart(chart_data, horizontal=True, color="#315a7d")

st.markdown(
    f"**{selected} in context:** {int(estimate.projects_with_imputed_mw):,} projects received an estimate; "
    f"{int(estimate.projects_still_missing_mw):,} still lacked usable MW. The modeled pressure is "
    f"**{estimate.combined_share_pct:.1f}%** of average 2024 generation."
)

st.header("How to read these results")
left, right = st.columns(2)
with left:
    st.subheader("What the indicator shows")
    st.write(
        "It compares the scale of the development pipeline with the scale of electricity currently generated "
        "in the same state. High values identify places where grid planning deserves closer examination."
    )
with right:
    st.subheader("What it does not show")
    st.write(
        "It is not peak demand, installed capacity, reserve margin, locally deliverable power, or a reliability "
        "forecast. Projects may change, use dedicated generation, import power, or never become operational."
    )

st.divider()
st.markdown(
    "**Sources:** FracTracker Alliance, *U.S. Data Centers Tracker* (2026); "
    "U.S. Energy Information Administration, ELEC Bulk Data (2025).  \\n"
    "Analysis and figures: Team JAMA, Drexel University DSCI 591."
)
