import pandas as pd
import plotly.express as px
import streamlit as st


def render_metrics(city_count, distance, runtime_ms, algorithm):
    cols = st.columns(4)
    cols[0].metric("CITIES", city_count)
    cols[1].metric("BEST TOUR DISTANCE", f"{distance:.2f}" if distance is not None else "—")
    cols[2].metric("RUNTIME", f"{runtime_ms:.3f} ms" if runtime_ms is not None else "—")
    cols[3].metric("ACTIVE ALGORITHM", algorithm)


def render_comparison(rows):
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)
    chart_df = df[["Algorithm", "Distance"]].copy()
    fig = px.bar(chart_df, x="Algorithm", y="Distance", color="Algorithm",
                 title="Tour distance by algorithm", template="plotly_dark")
    fig.update_layout(
        paper_bgcolor="#0b0f19", plot_bgcolor="#101522",
        font_color="#dbe4f0", showlegend=False, height=350,
        margin=dict(l=10, r=10, t=55, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)
