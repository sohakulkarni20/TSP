import time
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from core.distance import distance_matrix, route_distance, random_cities
from core.benchmark import run_algorithm
from ui.styles import apply_styles
from ui.dashboard import render_metrics, render_comparison

st.set_page_config(page_title="RouteLab | TSP Studio", page_icon="🧭", layout="wide")
apply_styles()

if "cities" not in st.session_state:
    st.session_state.cities = random_cities(10, seed=7)
if "results" not in st.session_state:
    st.session_state.results = {}
if "history" not in st.session_state:
    st.session_state.history = []

st.markdown("""
<div class="hero">
  <div class="eyebrow">DESIGN & ANALYSIS OF ALGORITHMS</div>
  <h1>RouteLab <span>↗</span></h1>
  <p>Traveling Salesman Problem · Interactive Algorithm Studio</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🧭 Route controls")
    st.caption("Create a city set, then run or compare algorithms.")
    city_count = st.slider("Number of cities", min_value=4, max_value=11, value=len(st.session_state.cities))
    seed = st.number_input("Random seed", min_value=0, max_value=99999, value=7, step=1)
    if st.button("🎲 Generate new map", use_container_width=True):
        st.session_state.cities = random_cities(city_count, int(seed))
        st.session_state.results = {}
        st.rerun()
    if st.button("↻ Reset demo map", use_container_width=True):
        st.session_state.cities = random_cities(10, seed=7)
        st.session_state.results = {}
        st.rerun()
    st.divider()
    algorithm = st.selectbox(
        "Algorithm",
        ["Nearest Neighbor", "Nearest Neighbor + 2-opt", "Brute Force", "Held–Karp DP"]
    )
    st.caption({
        "Nearest Neighbor": "Fast heuristic · O(n²)",
        "Nearest Neighbor + 2-opt": "Heuristic improvement · typically O(n²) per pass",
        "Brute Force": "Exact search · O(n!)",
        "Held–Karp DP": "Exact dynamic programming · O(n² · 2ⁿ)"
    }[algorithm])
    animate = st.checkbox("Show step-by-step route", value=True)
    run_btn = st.button("▶ Run selected algorithm", type="primary", use_container_width=True)
    compare_btn = st.button("⚖ Compare algorithms", use_container_width=True)
    st.divider()
    st.markdown("### How to use")
    st.markdown("1. Choose the number of cities.\n2. Generate a map.\n3. Run an algorithm.\n4. Compare the route and metrics.")

cities = st.session_state.cities
dm = distance_matrix(cities)

if run_btn:
    with st.spinner("Solving the route…"):
        result = run_algorithm(algorithm, cities, animate=animate)
    st.session_state.results[algorithm] = result
    st.session_state.history.append({
        "Algorithm": algorithm,
        "Cities": len(cities),
        "Distance": round(result["distance"], 2),
        "Runtime (ms)": round(result["runtime_ms"], 3),
        "States explored": result["states_explored"]
    })

if compare_btn:
    compare_names = ["Nearest Neighbor", "Nearest Neighbor + 2-opt"]
    if len(cities) <= 10:
        compare_names += ["Brute Force", "Held–Karp DP"]
    else:
        compare_names += ["Held–Karp DP"]
    comparison = []
    for name in compare_names:
        if name == "Brute Force" and len(cities) > 9:
            continue
        with st.spinner(f"Running {name}…"):
            res = run_algorithm(name, cities, animate=False)
        st.session_state.results[name] = res
        comparison.append({
            "Algorithm": name,
            "Distance": round(res["distance"], 2),
            "Runtime (ms)": round(res["runtime_ms"], 3),
            "States explored": res["states_explored"],
            "Optimal": "Yes" if res["optimal"] else "No guarantee"
        })
    st.session_state.comparison = comparison

# Top summary metrics
latest = next(iter(st.session_state.results.values()), None)
if st.session_state.results:
    latest_name = list(st.session_state.results.keys())[-1]
    latest = st.session_state.results[latest_name]
    render_metrics(len(cities), latest["distance"], latest["runtime_ms"], latest_name)
else:
    render_metrics(len(cities), None, None, "No run yet")

left, right = st.columns([1.65, 1])
with left:
    st.markdown('<div class="section-title">01 / Route canvas</div>', unsafe_allow_html=True)
    st.caption("Each point is a city. Lines show the current tour; hover over a point to see its label and coordinates.")
    selected_name = list(st.session_state.results.keys())[-1] if st.session_state.results else None
    selected_result = st.session_state.results.get(selected_name) if selected_name else None

    fig = go.Figure()
    # faint all-pairs links for context
    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            fig.add_trace(go.Scatter(
                x=[cities[i][0], cities[j][0]], y=[cities[i][1], cities[j][1]],
                mode="lines", line=dict(color="rgba(100,116,139,0.12)", width=1),
                hoverinfo="skip", showlegend=False
            ))
    if selected_result:
        route = selected_result["route"]
        rx = [cities[i][0] for i in route]
        ry = [cities[i][1] for i in route]
        fig.add_trace(go.Scatter(
            x=rx, y=ry, mode="lines+markers",
            line=dict(color="#42e8d4", width=3),
            marker=dict(size=7, color="#42e8d4"),
            name="Tour", hoverinfo="skip"
        ))
    fig.add_trace(go.Scatter(
        x=[p[0] for p in cities], y=[p[1] for p in cities],
        mode="markers+text",
        text=[f"C{i}" for i in range(len(cities))],
        textposition="top center",
        marker=dict(size=15, color="#a78bfa", line=dict(color="#f5f3ff", width=1.5)),
        textfont=dict(color="#f8fafc", size=11),
        customdata=[[i, p[0], p[1]] for i, p in enumerate(cities)],
        hovertemplate="<b>City C%{customdata[0]}</b><br>x=%{customdata[1]:.1f}<br>y=%{customdata[2]:.1f}<extra></extra>",
        name="Cities"
    ))
    fig.update_layout(
        height=480, margin=dict(l=10, r=10, t=15, b=10),
        paper_bgcolor="#101522", plot_bgcolor="#101522",
        font=dict(color="#dbe4f0"),
        xaxis=dict(visible=False, range=[-5, 105], fixedrange=True),
        yaxis=dict(visible=False, range=[-5, 105], fixedrange=True, scaleanchor="x", scaleratio=1),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    if selected_result:
        st.success(f"Current tour: {' → '.join('C'+str(i) for i in selected_result['route'])} → C{selected_result['route'][0]}")
    else:
        st.info("Run an algorithm to draw its tour on the canvas.")

with right:
    st.markdown('<div class="section-title">02 / Algorithm insights</div>', unsafe_allow_html=True)
    if selected_result:
        st.markdown(f"### {selected_name}")
        st.write(selected_result["description"])
        st.markdown("**Route order**")
        st.code(" → ".join("C"+str(i) for i in selected_result["route"]) + f" → C{selected_result['route'][0]}")
        st.markdown("**Complexity**")
        st.write(selected_result["complexity"])
        st.markdown("**Search states / candidates**")
        st.metric("Count", f"{selected_result['states_explored']:,}")
        st.markdown("**Optimality**")
        st.write("Optimal for this input." if selected_result["optimal"] else "Heuristic result; optimality is not guaranteed.")
    else:
        st.markdown("### Ready to optimize")
        st.write("Choose an algorithm in the sidebar and run it to inspect the tour, complexity, and search metrics.")
        st.markdown("- Cyan lines: current tour\n- Purple points: cities\n- Grey lines: possible connections")

st.markdown('<div class="section-title">03 / Benchmark comparison</div>', unsafe_allow_html=True)
if "comparison" in st.session_state and st.session_state.comparison:
    render_comparison(st.session_state.comparison)
else:
    st.info("Click **Compare algorithms** in the sidebar to run a benchmark on the same city set.")

if st.session_state.history:
    with st.expander("Run history"):
        hist = pd.DataFrame(st.session_state.history)
        st.dataframe(hist, use_container_width=True, hide_index=True)
        st.download_button("Download run history as CSV", hist.to_csv(index=False), "routelab_history.csv", "text/csv")

st.markdown("""
<div class="footer">ROUTELAB · Educational TSP visualizer · Distances are Euclidean units, not real road distances.</div>
""", unsafe_allow_html=True)
