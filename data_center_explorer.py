from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


ROOT = Path(__file__).resolve().parent
IMAGES = ROOT / "images"
DATA = ROOT / "data"

PRESSURE_CSV = DATA / "data_center_pipeline_grid_pressure.csv"
MODELED_CSV = DATA / "data_center_pipeline_pressure_regression_summary.csv"


st.set_page_config(
    page_title="Findings | Data Center Impact Explorer",
    page_icon="🏢",
    layout="wide",
)

st.markdown(
    """
    <style>
      :root { --ink:#17324d; --teal:#2f858d; --coral:#dc5c45; --paper:#f7f4ee; }
      .stApp { background: linear-gradient(180deg, #f7f4ee 0%, #ffffff 32%); }
      .stApp * { border-radius:0 !important; box-shadow:none !important; }
      .block-container { max-width: 1180px; padding-top: 2.2rem; padding-bottom: 4rem; }
      h1, h2, h3 { color: var(--ink); letter-spacing: -0.02em; }
      h1 { font-size: clamp(2.4rem, 5vw, 4.5rem) !important; line-height: .98 !important; }
      .section-title { margin-top:2.5rem; padding:.65rem 0 .55rem;
                       border-bottom:1px solid #cfd8dd; font-size:2.55rem; color:var(--ink); }
      .eyebrow { color:var(--teal); font-weight:800; letter-spacing:.14em; text-transform:uppercase; }
      .lede { color:#445565; font-size:1.2rem; line-height:1.65; max-width:820px; }
      .finding { border-left:5px solid var(--coral); background:#fff8f5; padding:1rem 1.2rem;
                 margin:1rem 0 1.5rem; }
      .finding strong { color:var(--ink); }
      .caption { color:#66727c; font-size:.86rem; line-height:1.45; }
      [data-testid="stMetric"] { background:rgba(255,255,255,.82); border:1px solid #dfe5e8;
                                 padding:1rem; border-radius:0; box-shadow:none; }
      [data-testid="stMetricValue"] { color:var(--ink); }
      [data-testid="stImage"] img { border-radius:0; border:1px solid #e7e7e7; }
      [data-baseweb="select"] > div,
      [data-testid="stExpander"],
      .stButton button,
      .stDownloadButton button { border-radius:0 !important; box-shadow:none !important; }
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
    path = IMAGES / filename
    if path.exists():
        st.image(str(path), use_container_width=True)
        st.markdown(f'<p class="caption">{caption}</p>', unsafe_allow_html=True)
    else:
        st.warning(f"Plot asset not found: {filename}")


pressure, modeled = load_results()
pipeline = pressure[pressure["pipeline_projects"] >= 10]

st.markdown('<div class="eyebrow">Data Center Impact Explorer · Findings</div>', unsafe_allow_html=True)
st.title("What surrounds America’s data-center boom?")
st.markdown(
    '<p class="lede">Digital computation may seem weightless, but every data center occupies a physical '
    'place. Here we examine how those places intersect with electricity systems, drought, public health, '
    'and local politics.</p>',
    unsafe_allow_html=True,
)

st.markdown("**Explore:** [Drought](#drought) · [Electricity](#electricity) · [Health](#health) · [Politics](#politics)")

st.markdown('<h2 class="section-title" id="drought">Drought</h2>', unsafe_allow_html=True)
st.caption("Drought findings and visualizations will be added here.")

st.divider()

st.markdown('<h2 class="section-title" id="electricity">Electricity</h2>', unsafe_allow_html=True)
st.markdown(
    '<p class="lede">To understand the electrical demands of data centers, we first asked a simple question: '
    'How large is the development pipeline when compared with the power systems that must sustain it?</p>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="finding"><strong>Main finding.</strong> In several states, the reported capacity of the '
    'data-center pipeline approaches—and in some cases exceeds—the state’s average electricity generation '
    'in 2024, revealing the scale of the planning challenge ahead (FracTracker Alliance, 2026; '
    'U.S. Energy Information Administration, 2025).</div>',
    unsafe_allow_html=True,
)

st.subheader("Where is data-center development concentrated?")
st.write(
    "The emerging geography is strikingly uneven. Among facilities classified as proposed, approved, "
    "under construction, or expanding, Virginia alone contains 263 projects. Texas and Georgia follow. "
    "Thus, a national technological transition is being concentrated within a relatively small number of "
    "state and local power systems (FracTracker Alliance, 2026)."
)
show_plot(
    "pipeline_facilities.png",
    "Source: FracTracker Alliance (2026).",
)

st.subheader("How has electricity generation changed?")
st.write(
    "The states attracting data centers did not arrive at the present moment by a common path. Their "
    "electricity generation rose, fell, or remained comparatively stable over the past decade. To make "
    "these different trajectories comparable, the figure assigns each state’s 2015 generation a value of "
    "100 (U.S. Energy Information Administration, 2025)."
)
show_plot(
    "leading_state_generation.png",
    "Source: U.S. Energy Information Administration (2025). The latest year may be incomplete for some states.",
)

st.subheader("How large is the pipeline relative to state power systems?")
st.write(
    "We compared two quantities: reported pipeline megawatts and the state’s average rate of electricity "
    "generation in 2024, calculated as annual megawatt-hours divided by 8,760 hours. In Ohio and Nevada, "
    "the resulting ratio exceeds 100 percent; in Virginia and Indiana, it comes close. The ratio is useful "
    "because it places unfamiliar project numbers against the scale of an existing electrical system "
    "(FracTracker Alliance, 2026; U.S. Energy Information Administration, 2025)."
)

default_states = ["OH", "NV", "VA", "IN", "TX", "GA", "PA"]
chart_states = st.multiselect(
    "States shown",
    options=pipeline.sort_values(
        "pipeline_share_of_average_generation_pct", ascending=False
    ).index.tolist(),
    default=default_states,
    help="Select one or more states with at least 10 pipeline projects.",
)

if chart_states:
    interactive_chart = pressure.loc[chart_states].sort_values(
        "pipeline_share_of_average_generation_pct", ascending=False
    )
    reporting = (
        interactive_chart["projects_reporting_mw"].astype(int).astype(str)
        + "/"
        + interactive_chart["pipeline_projects"].astype(int).astype(str)
        + " projects report MW"
    )

    chart_rows = []
    for state, row in interactive_chart.iterrows():
        for category, share_column, mw_column in [
            (
                "Supply unknown",
                "reported_no_onsite_share_of_generation_pct",
                "reported_no_onsite_evidence_mw",
            ),
            (
                "Dedicated/hybrid",
                "reported_onsite_share_of_generation_pct",
                "reported_onsite_mw",
            ),
        ]:
            chart_rows.append(
                {
                    "State": state,
                    "Power supply": category,
                    "Share": row[share_column],
                    "MW": row[mw_column],
                    "Reporting": reporting.loc[state],
                    "Total share": row["pipeline_share_of_average_generation_pct"],
                }
            )

    chart_data = pd.DataFrame(chart_rows)
    state_order = interactive_chart.index.tolist()
    bars = (
        alt.Chart(chart_data)
        .mark_bar()
        .encode(
            x=alt.X(
                "sum(Share):Q",
                title="Reported pipeline MW as a share of 2024 average state generation",
                axis=alt.Axis(labelExpr="datum.value + '%'", gridColor="#DCE2E6"),
            ),
            y=alt.Y("State:N", sort=state_order, title="State"),
            color=alt.Color(
                "Power supply:N",
                scale=alt.Scale(
                    domain=["Supply unknown", "Dedicated/hybrid"],
                    range=["#315A7D", "#3A8B75"],
                ),
                legend=alt.Legend(title=None, orient="top"),
            ),
            order=alt.Order("Power supply:N", sort="descending"),
            tooltip=[
                alt.Tooltip("State:N"),
                alt.Tooltip("Power supply:N"),
                alt.Tooltip("MW:Q", title="Reported MW", format=",.0f"),
                alt.Tooltip("Share:Q", title="Share of generation", format=".1f"),
                alt.Tooltip("Total share:Q", title="Total pipeline share", format=".1f"),
                alt.Tooltip("Reporting:N", title="Coverage"),
            ],
        )
    )
    reference = (
        alt.Chart(pd.DataFrame({"Reference": [100]}))
        .mark_rule(color="#B43C2E", strokeDash=[7, 5], strokeWidth=2)
        .encode(x="Reference:Q")
    )
    interactive_fig = (
        (bars + reference)
        .properties(height=max(320, 48 * len(interactive_chart)))
        .configure_view(strokeWidth=0)
        .configure_axis(labelColor="#17324D", titleColor="#17324D")
    )
    st.altair_chart(interactive_fig, use_container_width=True)
    st.caption(
        "A facility is classified as dedicated/hybrid only when the source data provide explicit evidence. "
        "Blank power-source fields remain unknown."
    )
else:
    st.info("Select at least one state to display the chart.")

st.subheader("Why separate dedicated and hybrid generation?")
st.write(
    "The distinction separates two related but different questions: how much electricity a facility may "
    "require, and how much of that electricity the public grid may have to provide. A project with dedicated "
    "generation may supply part of its own demand; a hybrid project may alternate or combine onsite and grid "
    "power. Treating all reported capacity as grid supplied would therefore exaggerate what the data establish. "
    "Yet self-generation does not make a facility electrically invisible. It may still depend on the grid and "
    "may introduce consequences involving fuel, emissions, transmission, and reliability."
)

st.subheader("Why does missing MW matter?")
st.write(
    "A measurement can mislead not only through what it records, but also through what it omits. Nearly "
    "two-thirds of pipeline facilities report no megawatt capacity. Where facility area was available, we "
    "used a log-log regression to estimate the missing value. These estimates are a sensitivity analysis: "
    "they reveal how incomplete reporting could alter the state comparisons."
)
show_plot(
    "data_center_pipeline_pressure_with_regression.png",
    "Light blue represents regression-estimated missing MW. Facilities explicitly associated with dedicated or hybrid generation were not imputed.",
)

st.subheader("What do these pressures look like in practice?")
st.write(
    "A July 2026 incident in Loudoun County illustrates why the size and behavior of data-center loads matter, "
    "not merely the amount of electricity they consume. NBC Washington reported that equipment failed on a "
    "high-voltage transmission line serving data centers, after which the facilities’ control systems briefly "
    "transferred them to backup power. Monitoring data cited by NBC showed repeated voltage changes across much "
    "of the eastern United States, linking the widespread flicker to the abrupt load transfer (Wilder, 2026)."
)
st.write(
    "Pennsylvania has responded to the broader planning problem with explicit conditions on new development. "
    "Executive Order 2026-05 requires qualifying developers to accept the state’s Responsible Infrastructure "
    "Development requirements and obtain local approval. Among other provisions, developers must bear the full "
    "cost of the generation and grid infrastructure needed for their projects, disclose energy and water use, "
    "and satisfy standards for environmental protection and community engagement. The order also directs state "
    "officials to pursue reliability protocols and more transparent demand forecasts. These measures reflect a "
    "simple principle: growth in computational infrastructure must be accompanied by growth in accountability "
    "for the physical systems that support it (Commonwealth of Pennsylvania, 2026)."
)

st.divider()
st.markdown('<h2 class="section-title" id="health">Health</h2>', unsafe_allow_html=True)
st.caption("Health findings and visualizations will be added here.")

st.divider()
st.markdown('<h2 class="section-title" id="politics">Politics</h2>', unsafe_allow_html=True)
st.caption("Politics findings and visualizations will be added here.")

st.divider()
st.header("Sources")
st.markdown(
    "- FracTracker Alliance. (2026, July). [*U.S. Data Centers Tracker*]"
    "(https://experience.arcgis.com/experience/5a4d072ad01449bba5698a80103fb909/page/Demographics).\n"
    "- Commonwealth of Pennsylvania. (2026, August 18). [*Governor Shapiro signs executive order "
    "demanding data center developers comply with strict requirements and blocking speculative, irresponsible "
    "data center projects*](https://www.pa.gov/governor/newsroom/2026-press-releases/"
    "governor-shapiro-signs-executive-order-on-data-center-developmen).\n"
    "- U.S. Energy Information Administration. (2025). [*EIA Bulk Data: Electricity*]"
    "(https://www.eia.gov/opendata/v1/bulkfiles.php).\n"
    "- Wilder, D. (2026, July 24). [*How Loudoun County data centers are linked to power flickering across "
    "half the U.S.*](https://www.nbcwashington.com/news/local/northern-virginia/"
    "how-loudoun-county-data-centers-are-linked-to-power-flickering-across-half-the-u-s/4134124/). "
    "NBC Washington."
)
