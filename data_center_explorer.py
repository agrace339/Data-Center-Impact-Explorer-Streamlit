from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st
import us
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parent
IMAGES = ROOT / "images"
DATA = ROOT / "data"

PRESSURE_CSV = DATA / "data_center_pipeline_grid_pressure.csv"
MODELED_CSV = DATA / "data_center_pipeline_pressure_regression_summary.csv"
AHR_ALL_RANKS = DATA / "AHR_avg_rankings.csv"
LOCATIONS = DATA / "FracTrackers_Data_Centers_Database.xlsx - FracTracker Data Centers.csv"

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
      .block-container { max-width: 1180px; padding-top: 5.5rem; padding-bottom: 4rem; }
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
def load_results() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    pressure = pd.read_csv(PRESSURE_CSV).set_index("state")
    modeled = pd.read_csv(MODELED_CSV).set_index("state")
    avghealth = pd.read_csv(AHR_ALL_RANKS)
    locations = pd.read_csv(LOCATIONS)
    return pressure, modeled, avghealth, locations


def show_plot(filename: str, caption: str) -> None:
    path = IMAGES / filename
    if path.exists():
        st.image(str(path), use_container_width=True)
        st.markdown(f'<p class="caption">{caption}</p>', unsafe_allow_html=True)
    else:
        st.warning(f"Plot asset not found: {filename}")


pressure, modeled, avghealth, locations = load_results()
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

st.write("Roughly 75% to 90% of data centers use water as their primary cooling method, in which many "
         "evaporate the water as part of the cooling process (Hedge, 2026). Since the number of data centers "
         "built and being planned to be built has increased dramatically in the past 10 years, it begs the "
         "question:")

st.write("**How are drought rates being impacted by data center construction?**")

st.write("For this section, we examine the data provided by the U.S. Drought Monitor and its correlation "
         "to recent data center construction.")

st.subheader("How has drought changed over time?")

show_plot(
    "drought_1.png",
    "Source: U.S. Drought Monitor (n.d.).",
)

st.write("From the graph, the year 2012 stands out as a year when all drought rates increase at a rapid rate. "
         "This is due to the Drought of 2012, which occurred due to low rates of snowfall. In "
         "addition, it appears that drought rates have been less steady from 2020 onwards versus before 2020, "
         "but this is not conclusive, as the graph has a lot of variations, and furthermore, there is no "
         "direct correlation shown between drought rates and the years that data centers started being "
         "constructed at a more rapid rate.")

st.subheader("What are the drought rates around where data centers are located?")

col1, col2 = st.columns(2)

with col1:
    show_plot(
        "drought_2.png",
        "Average drought severity between 2016-2021 with data center locations. Source: U.S. Drought Monitor, FracTracker",
    )

with col2:
    show_plot(
        "drought_3.png",
        "Average drought severity between 2021-2026 with data center locations. U.S. Drought Monitor, FracTracker",
    )
    
st.write("Above, the average drought severity is compared between two 5-year time periods, 2016 to 2021 "
         "and 2022 to 2026. The blue dots are data center locations. Overall, it seems that the average "
         "drought severity has increased across the nation. From these maps there seems to be no correlation "
         "between data center location and drought severity. Many data centers are located in the Virginia, "
         "Maryland and D.C. area, but based on these maps, the severity of drought rates has not increased "
         "significantly. On the other hand, in Texas, which is home to the second largest amount of data "
         "centers, we can see the drought has increased, including around areas where data centers are "
         "located. In contract, drought in southern New Mexico and Arizona has also noticeably increased, "
         "but data centers are sparse in that area.")

st.write("Although no specific conclusions can be drawn from this data, it is worth monitoring for future "
         "correlation as droughts are a slow-moving hazard but can be catastrophic none the less.")

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
st.markdown(
    '<p class="lede">While studies have yet to release concretely linking data centers to poor health outcomes, '
    'we do know that the pollutants they release can exacerbate the symptoms experienced by individuals '
    'with respiratory and cardiovascular conditions, as well as increase the risk of developing cancer with '
    'prolonged exposure (Pavlinich, 2026).</p>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="finding"><strong>Main finding.</strong> States with a high frequency of planned data '
    'centers also tend to have middling to poor health rankings with regards to conditions that could '
    'potentially be exacerbated by their presence (FracTracker Alliance, 2026; '
    'United Health Foundation, 2025).</div>',
    unsafe_allow_html=True,
)

st.subheader("What is a 'health ranking'? How is it used here?")
st.write("In order to understand the health and wellness of a state, we utilized data from the United Health "
         "Foundation's America's Health Rankings 2025 Annual Report (United Health Foundation, 2025). "
         "In this report, large quantities of health data were collected, compiled, and made publically "
         "available for charitable use. To visually demonstrate how preexisting health conditions may interact "
         "with data center locations, location data from the FracTracker Alliance U.S. Data Centers Tracker "
         "(FracTracker Alliance, 2026) was also used. "
         "Using emerging literature as a guideline (Pavlinich, 2026; Han et al., 2024), we selected three diagnoses "
         "as our points of focus: asthma, cardiovascular disease, and cancer. The average ranking per "
         "state across all included demographics for each diagnosis was then calculated, giving us the "
         "rankings you see below. **Select a state to see how they currently rank across these three metrics:**")

us_states = [state.name for state in us.states.STATES]

selected_state = st.selectbox(
    "Choose a U.S. state:",
    options=us_states,
    index=us_states.index("Alabama"),
    placeholder="Select a state..."
)

if selected_state:
    st.write(f"You selected: {selected_state}")
    selected_abbr = us.states.lookup(selected_state).abbr
    state_AHRdf = avghealth[avghealth["state"] == selected_abbr]
else:
    state_AHRdf = avghealth.iloc[0:0]
    
measures = ["Asthma", "Cancer", "Cardiovascular Disease"]

col1, col2, col3 = st.columns(3)

for col, measure in zip([col1, col2, col3], measures):
    with col:
        match = state_AHRdf.loc[state_AHRdf["Measure"] == measure, "Rank"]
        value = match.iloc[0] if not match.empty else "N/A"
        st.metric(label=measure, value=value)
        
st.subheader("How do these health rankings line up with data center locations?")
st.write("For states whose citizens are currently experiencing complications related to asthma, cardiovascular "
         "conditions, or cancer, allowing a high volume of data centers to be built or expanded could very well "
         "have an impact on the symptoms those individuals are experiencing. Take, for example, Virginia "
         "(home of the now-famous 'data-center alley'), which is consistently middle of the pack compared "
         "to other states. While there are a myriad of extraneous factors that contribute to the health "
         "challenges a state faces, the pollutants released by data centers have the potential to actively "
         "harm residents that are already vulnerable--and whose presence has heretofore been overlooked. "
         "**Select a condition to see how each state ranks comparatively, along with data center locations:**")

measures = sorted(avghealth["Measure"].unique())
selected_measure = st.selectbox("Select a condition", measures)

measure_df = avghealth[avghealth["Measure"] == selected_measure].copy()

pipeline_statuses = {
    "Proposed",
    "Approved/Permitted/Under construction",
    "Expanding",
}
facility_context = locations.copy()
facility_context["state"] = facility_context["state"].astype("string").str.strip().str.upper()
facility_context["is_operating_or_expanding"] = facility_context["status"].isin(
    {"Operating", "Expanding"}
)
facility_context["is_pipeline"] = facility_context["status"].isin(pipeline_statuses)

state_facility_counts = (
    facility_context.groupby("state")
    .agg(
        total_data_centers=("facility_name", "size"),
        operating_or_expanding=("is_operating_or_expanding", "sum"),
        pipeline_projects=("is_pipeline", "sum"),
    )
)

measure_df = measure_df.merge(
    state_facility_counts,
    left_on="state",
    right_index=True,
    how="left",
)
measure_df[["total_data_centers", "operating_or_expanding", "pipeline_projects"]] = (
    measure_df[["total_data_centers", "operating_or_expanding", "pipeline_projects"]]
    .fillna(0)
    .astype(int)
)
measure_df["State name"] = measure_df["state"].map(
    lambda abbreviation: us.states.lookup(abbreviation).name
    if us.states.lookup(abbreviation)
    else abbreviation
)


def rank_context(rank: float) -> str:
    if rank <= 10:
        return "Among the 10 best-ranked states"
    if rank <= 20:
        return "Above the middle of the rankings"
    if rank <= 30:
        return "Near the middle of the rankings"
    if rank <= 40:
        return "Below the middle of the rankings"
    return "Among the 10 lowest-ranked states"


measure_df["Rank context"] = measure_df["Rank"].map(rank_context)

custom_colorscale = [
    [0.0, "red"],
    [0.5, "gold"],
    [1.0, "green"],
]

fig = go.Figure()

fig.add_trace(go.Choropleth(
    locations=measure_df["state"],
    z=measure_df["Rank"],
    locationmode="USA-states",
    colorscale=custom_colorscale,
    reversescale=True,
    colorbar_title="Rank",
    marker_line_color="white",
    marker_line_width=0.5,
    customdata=measure_df[
        [
            "State name",
            "Measure",
            "Rank context",
            "Data Year(s)",
            "total_data_centers",
            "operating_or_expanding",
            "pipeline_projects",
        ]
    ].to_numpy(),
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "%{customdata[1]} rank: <b>%{z:.0f}</b><br>"
        "%{customdata[2]}<br>"
        "Health data year: %{customdata[3]}<br><br>"
        "Data centers in tracker: %{customdata[4]:,.0f}<br>"
        "Operating or expanding: %{customdata[5]:,.0f}<br>"
        "Development pipeline: %{customdata[6]:,.0f}"
        "<extra></extra>"
    ),
))

facility_context["Facility"] = facility_context["facility_name"].fillna("Unnamed facility")
facility_context["Location"] = (
    facility_context["city"].fillna("Unknown city").astype(str)
    + ", "
    + facility_context["state"].fillna("Unknown state").astype(str)
)
facility_context["Status"] = facility_context["status"].fillna("Unknown")
facility_context["Operator"] = facility_context["operator_name"].fillna("Not reported")
facility_context["Reported MW"] = facility_context["mw"].fillna("Not reported").astype(str)

fig.add_trace(go.Scattergeo(
    lon=facility_context["long"],
    lat=facility_context["lat"],
    mode="markers",
    marker=dict(
        size=8,
        color="black",
        symbol="circle",
        line=dict(width=1, color="white"),
    ),
    customdata=facility_context[
        ["Facility", "Location", "Status", "Operator", "Reported MW"]
    ].to_numpy(),
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "%{customdata[1]}<br>"
        "Status: %{customdata[2]}<br>"
        "Operator: %{customdata[3]}<br>"
        "Reported capacity: %{customdata[4]} MW"
        "<extra></extra>"
    ),
))

fig.update_layout(
    geo=dict(
        scope="usa",
        projection=go.layout.geo.Projection(type="albers usa"),
    ),
    margin=dict(l=0, r=0, t=30, b=0),
    height=600,
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Why does this matter? Who is affected?")
st.write("Although we're looking at rather generalized versions of these three conditions, the health burden "
         "created by data center pollutants is far greater and more complex than what we are able to wholly present. "
         "Firstly, populations vulnerable to air pollution come in many different forms--children, "
         "fetuses in utero, pregnant folks, and the elderly are all considered to be high risk (Pavlinich, 2026). "
         "Black Americans are also disproporrtionately affected by the health impacts of data centers, "
         "with low-income, rural Black communities in particular often being targeted for their ample land and "
         "low energy costs at the expense of long-time residents (Mahoney, 2025). Outside of individual or "
         "community-wide impacts is also the reality of the financial health burden these data centers "
         "could cause. Recent studies have projected that by 2028, the demand for technologies made possible "
         "by data centers (such as AI) may push the total annual public health burden of U.S. data centers to "
         "over $20 billion; personal health costs are also anticipated to be unevenly distributed, with "
         "the average household health cost in affected counties expected to reach 7x the national average "
         "(Han et al., 2024).")
         
st.write("We've provided a glimpse into which states are struggling most with these conditions "
         "and how data centers may impact their residents, but it is important to remember that there are real "
         "people behind these numbers. Many states are actively considering moritoriums or banning the "
         "construction of data centers outright (National Conference of State Legislatures, 2026), but "
         "concerns regarding resident health have yet to be officially cited despite ever-increasing "
         "evidence for its inclusion in the conversation. Although we cannot decisively say with the data at "
         "hand that data centers themselves are causing health problems to manifest, public health is still a "
         "worthwhile, yet neglected, angle for policymakers, politicians, and residents to consider.")

st.divider()
st.markdown('<h2 class="section-title" id="politics">Politics</h2>', unsafe_allow_html=True)
st.write("Here, we examine the connections between data center presence and political factors at the county "
         "level based on data from the FracTracker Alliance U.S. Data Centers Tracker (FracTracker Alliance, 2026) "
         "and the National Neighborhood Data Archive (ICPSR 38506) (Clary et al., 2024); "
         "for geographic code matching to make this analysis possible, we used Row Zero FIPS code lists "
         "and location mapping (Row Zero, 2025). NaNDA provides information about voter registration, turnout, and "
         "partisanship in 2022, whereas the data center dataset is updated as of summer 2026; so, "
         "these visualizations represent how past political trends may correspond to current data "
         "center presence."
         )
st.subheader("Voting Populations")
st.write("Histograms show that the data centers in the FracTracker dataset tend to be located in counties "
         "with higher voting populations. However, the data center dataset is partially crowd-sourced and "
         "does not present a comprehensive record of all data centers in the U.S., and so is likely biased "
         "towards higher-population areas.")

col1, col2 = st.columns(2)

with col1:
    show_plot(
        "political_histogram_1.png",
        "Registered voters per county by data center presence (with/without). Source: National Neighborhood Data Archive, FracTracker",
    )

with col2:
    show_plot(
        "political_histogram_2.png",
        "Registered voters per county by number of data centers (1-6+). Source: National Neighborhood Data Archive, FracTracker",
    )

st.subheader("Partisanship")
st.write("Based on the available data, a larger presence of data centers in a county corresponds to a "
         "comparatively greater Democrat partisanship and lower Republican partisanship (measured by "
         "averaging presidential and senate vote ratios in each county from 2016 to 2022). However, the "
         "FracTracker data center dataset is likely biased towards data centers located in higher-population "
         "areas, which skews the distribution.")

col1, col2 = st.columns(2)

with col1:
    show_plot(
        "partisanship_1.png",
        "Average Republican/Democrat county partisanship by data center presence. Source: National Neighborhood Data Archive, FracTracker",
    )

with col2:
    show_plot(
        "partisanship_2.png",
        "Distribution of Republican/Democrat county partisanship by data center presence. Source: National Neighborhood Data Archive, FracTracker",
    )

st.write("Despite differences in county partisanship and county voting populations, the distribution of "
         "voter turnout across counties with varying data center presences remains remarkably similar.")

col1, col2 = st.columns(2)

with col1:
    show_plot(
        "turnout_1.png",
        "Voter turnout percentage by data center presence (with/without). Source: National Neighborhood Data Archive, FracTracker",
    )

with col2:
    show_plot(
        "turnout_2.png",
        "Voter turnout percentage by data center presence (0-6+). Source: National Neighborhood Data Archive, FracTracker",
    )

st.divider()
st.header("Sources")
st.markdown(
    """
- Clary, W., Gomez-Lopez, I. N., Chenoweth, M., Gypin, L., Clarke, P., Noppert, G., Li, M., & Kollman, K. (2024). [*National Neighborhood Data Archive (NaNDA): Voter registration, turnout, and partisanship by county, United States, 2004–2022*](https://www.icpsr.umich.edu/web/ICPSR/studies/38506/versions/V2) [Data set]. Inter-university Consortium for Political and Social Research.

- Commonwealth of Pennsylvania. (2026, August 18). [*Governor Shapiro signs executive order demanding data center developers comply with strict requirements and blocking speculative, irresponsible data center projects*](https://www.pa.gov/governor/newsroom/2026-press-releases/governor-shapiro-signs-executive-order-on-data-center-developmen).

- FracTracker Alliance. (2026, July). [*U.S. Data Centers Tracker*](https://experience.arcgis.com/experience/5a4d072ad01449bba5698a80103fb909/page/Demographics) [Data set].

- Han, Y., Wu, Z., Li, P., Wierman, A., & Ren, S. (2024). [*Health-informed computing: Estimating and addressing the public health impact of data centers*](https://arxiv.org/abs/2412.06288).

- Hedge, G. (2026). [*Myths vs. reality: Data centers and water usage*](https://www.fwpcoa.org/content.aspx?page_id=5&club_id=859275&item_id=130961). Florida Water and Pollution Control Operators Association.

- Mahoney, A. (2025). [*How the data center boom could harm Black communities*](https://www.canarymedia.com/articles/fossil-fuels/how-the-data-center-boom-could-harm-black-communities). Canary Media.

- National Conference of State Legislatures. (2026). [*Which states are banning data centers?*](https://www.ncsl.org/fiscal/which-states-are-banning-data-centers).

- Pavlinich, E. J. (2026). [*The dangers of data centers*](https://www.environmentalhealthproject.org/post/the-dangers-of-data-centers). Environmental Health Project.

- Row Zero. (2025, March 6). [*FIPS codes for all U.S. locations in a spreadsheet*](https://rowzero.com/datasets/fips-codes-lookup#zip-code-mappings) [Data set].

- United Health Foundation. (2025). [*America’s Health Rankings 2025 annual report*](https://www.americashealthrankings.org/publications/reports/2025-annual-report) [Data set].

- U.S. Drought Monitor. (n.d.). [*Data tables*](https://droughtmonitor.unl.edu/DmData/DataTables.aspx) [Data set]. Retrieved June 30, 2026.

- U.S. Energy Information Administration. (2025). [*EIA bulk data: Electricity*](https://www.eia.gov/opendata/v1/bulkfiles.php) [Data set].

- Wilder, D. (2026, July 24). [*How Loudoun County data centers are linked to power flickering across half the U.S.*](https://www.nbcwashington.com/news/local/northern-virginia/how-loudoun-county-data-centers-are-linked-to-power-flickering-across-half-the-u-s/4134124/). NBC Washington.
"""
)
