import subprocess
import getpass
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="NEXUS | Web Analytics",
    page_icon="⚡",
    layout="wide"
)

# Futuristic dark UI
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Inter:wght@400;500;700&display=swap');

.stApp {
    background:
      radial-gradient(ellipse at 10% 0%, #172554 0%, transparent 40%),
      radial-gradient(ellipse at 90% 10%, #3b0764 0%, transparent 35%),
      #070b16;
    color: #e5f0ff;
    font-family: 'Inter', sans-serif;
}
.block-container {
    padding-top: 2rem;
    max-width: 1500px;
}
h1, h2, h3 {
    color: #f0f7ff !important;
}
.hero {
    padding: 28px;
    border: 1px solid #263d66;
    border-radius: 22px;
    background: linear-gradient(120deg, #101b35dd, #17112ddd);
    box-shadow: 0 0 35px #2563eb18;
    margin-bottom: 24px;
}
.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(25px, 4vw, 42px);
    font-weight: 700;
    letter-spacing: 2px;
    background: linear-gradient(90deg, #67e8f9, #a78bfa, #f0abfc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    color: #9fb4d7;
    margin-top: 10px;
}
.kpi {
    background: linear-gradient(145deg, #111c32, #0c1325);
    border: 1px solid #253b60;
    border-radius: 18px;
    padding: 20px;
    min-height: 125px;
    box-shadow: 0 0 22px #06b6d410;
    transition: 0.25s ease;
}
.kpi:hover {
    border-color: #22d3ee;
    transform: translateY(-3px);
    box-shadow: 0 0 25px #06b6d425;
}
.kpi-label {
    color: #93a9cc;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
.kpi-value {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(20px, 2.5vw, 30px);
    color: #67e8f9;
    margin-top: 14px;
    overflow-wrap: anywhere;
}
.panel {
    background: #0c1425;
    border: 1px solid #233858;
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 15px;
}
div[data-testid="stDataFrame"] {
    border: 1px solid #263d60;
    border-radius: 12px;
}
.stButton button {
    background: linear-gradient(90deg, #0891b2, #7c3aed);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 700;
}
.stButton button:hover {
    border: 1px solid #67e8f9;
    color: white;
}
[data-testid="stSidebar"] {
    background: #090f1d;
    border-right: 1px solid #1e3150;
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# Read actual Hadoop output from HDFS
@st.cache_data(ttl=15)
def load_data():
    result = subprocess.run(
        [
            "hdfs", "dfs", "-cat",
            f"/user/{__import__('getpass').getuser()}/weblogs_out/part-00000"
        ],
        capture_output=True,
        text=True,
        timeout=60
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stderr.strip()
            or "Could not read the Hadoop output."
        )

    rows = []
    for line in result.stdout.splitlines():
        parts = line.strip().split("\t")
        if len(parts) == 2:
            try:
                rows.append((parts[0], int(parts[1])))
            except ValueError:
                continue

    if not rows:
        raise ValueError("No URL counts found in the Hadoop output.")

    df = pd.DataFrame(rows, columns=["URL", "Requests"])
    return df.sort_values("Requests", ascending=False)


# Sidebar
with st.sidebar:
    st.markdown("## ⚡ NEXUS")
    st.caption("WEB INTELLIGENCE SYSTEM")
    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        ["Overview", "URL Explorer", "Project Info"]
    )

    st.markdown("---")
    top_n = st.slider(
        "URLs shown in chart",
        min_value=5,
        max_value=15,
        value=10
    )

    st.caption("DATA SOURCE")
    st.markdown("Hadoop HDFS")
    st.markdown("MapReduce + Python")

    if st.button("⟳ Refresh Hadoop Data", use_container_width=True):
        load_data.clear()
        st.rerun()


# Header
st.markdown("""
<div class="hero">
    <div style="color:#67e8f9; letter-spacing:3px; font-size:12px;">
        ● WEB TRAFFIC INTELLIGENCE / SYSTEM ONLINE
    </div>
    <div class="hero-title">NEXUS ANALYTICS</div>
    <div class="hero-sub">
        Hadoop-powered web log analysis · Request intelligence · URL performance
    </div>
</div>
""", unsafe_allow_html=True)


try:
    df = load_data()
except Exception as e:
    st.error("Unable to load Hadoop output.")
    st.markdown("### Check your setup")
    st.code("""
jps
hdfs dfs -ls /user/$USER/weblogs_out
hdfs dfs -cat /user/$USER/weblogs_out/part-00000
""", language="bash")
    st.warning(
        "Run this dashboard from the same terminal environment "
        "where Hadoop and HDFS are configured."
    )
    st.caption(f"Technical details: {e}")
    st.stop()


total_requests = int(df["Requests"].sum())
unique_urls = len(df)
top_url = df.iloc[0]["URL"]
top_count = int(df.iloc[0]["Requests"])


if page == "Overview":
    # Summary cards
    c1, c2, c3, c4 = st.columns(4)

    cards = [
        (c1, "TOTAL REQUESTS", f"{total_requests:,}"),
        (c2, "UNIQUE URL PATHS", f"{unique_urls:,}"),
        (c3, "MOST VISITED URL", top_url),
        (c4, "TOP URL REQUESTS", f"{top_count:,}")
    ]

    for col, label, value in cards:
        with col:
            st.markdown(
                f'<div class="kpi">'
                f'<div class="kpi-label">{label}</div>'
                f'<div class="kpi-value">{value}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.write("")

    left, right = st.columns([1.65, 1])

    with left:
        st.markdown("### ◈ URL Traffic Matrix")
        chart_df = df.head(top_n).sort_values("Requests")

        fig = px.bar(
            chart_df,
            x="Requests",
            y="URL",
            orientation="h",
            color="Requests",
            color_continuous_scale=["#312e81", "#2563eb", "#22d3ee"],
            template="plotly_dark"
        )

        fig.update_layout(
            height=470,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=15, b=10),
            xaxis_title="Total requests",
            yaxis_title="URL path"
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("### ◈ Traffic Distribution")
        pie_df = df.head(top_n).copy()
        pie_df["URL"] = pie_df["URL"].astype(str)

        fig2 = px.pie(
            pie_df,
            names="URL",
            values="Requests",
            hole=0.62,
            color_discrete_sequence=[
                "#22d3ee", "#818cf8", "#c084fc",
                "#f472b6", "#60a5fa", "#34d399",
                "#fbbf24", "#fb7185", "#a3e635"
            ],
            template="plotly_dark"
        )
        fig2.update_layout(
            height=390,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(font=dict(size=10)),
            margin=dict(l=0, r=0, t=15, b=10)
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown(
            f'<div class="panel">'
            f'<div style="color:#93a9cc;font-size:12px;">'
            f'HIGHEST TRAFFIC PATH</div>'
            f'<h2 style="color:#67e8f9;">{top_url}</h2>'
            f'<div style="color:#a5b4fc;">'
            f'{top_count:,} requests recorded</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown("### ◈ Top URL Records")
    display_df = df.head(5).copy()
    display_df.insert(0, "Rank", range(1, len(display_df) + 1))
    st.dataframe(display_df, hide_index=True, use_container_width=True)


elif page == "URL Explorer":
    st.markdown("### ◈ URL Explorer")
    st.caption("Search, sort, and inspect the aggregated Hadoop results.")

    search = st.text_input(
        "Search URL path",
        placeholder="Try /login, /products, /cart..."
    )

    min_requests = st.number_input(
        "Minimum request count",
        min_value=0,
        value=0,
        step=100
    )

    filtered = df[df["Requests"] >= min_requests].copy()

    if search:
        filtered = filtered[
            filtered["URL"].str.contains(search, case=False, na=False)
        ]

    st.write(f"**{len(filtered)} URL paths found**")

    st.dataframe(
        filtered.reset_index(drop=True),
        hide_index=True,
        use_container_width=True,
        height=480
    )

    st.download_button(
        "⬇ Export results as CSV",
        data=filtered.to_csv(index=False),
        file_name="web_log_analysis.csv",
        mime="text/csv"
    )


else:
    st.markdown("### ◈ Project Architecture")

    st.markdown("""
    <div class="panel">
      <h3 style="color:#67e8f9;">01 / HDFS</h3>
      Stores the raw web server access log.
    </div>
    <div class="panel">
      <h3 style="color:#818cf8;">02 / Python Mapper</h3>
      Extracts URL paths and emits (URL, 1).
    </div>
    <div class="panel">
      <h3 style="color:#c084fc;">03 / Hadoop Reducer</h3>
      Adds counts for each URL path.
    </div>
    <div class="panel">
      <h3 style="color:#f0abfc;">04 / Streamlit Dashboard</h3>
      Visualizes request counts and supports URL search and CSV export.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Current Dataset Summary")
    st.write(f"- Total counted requests: **{total_requests:,}**")
    st.write(f"- Distinct URL paths: **{unique_urls:,}**")
    st.write(f"- Most requested path: **{top_url}**")
    st.write("- Processing method: **Hadoop Streaming MapReduce**")

