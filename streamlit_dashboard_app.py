"""
Streamlit dashboard: marketing intelligence with Tableau-style cross-filters (Plotly on_select).

Local: streamlit run streamlit_dashboard_app.py
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

from project_paths import PROJECT_ROOT
from shared_cleaning_rules import DEFAULT_CLEAN_FILENAME

try:
    from shared_cleaning_rules import add_revised_sentiment, add_trends_keyword
except ImportError:

    def add_revised_sentiment(df: pd.DataFrame) -> pd.DataFrame:
        """Fallback if shared_cleaning_rules predates add_revised_sentiment (e.g. unsynced copy)."""
        out = df.copy()
        if "sentiment_label" not in out.columns:
            out["sentiment_revised_label"] = None
            return out
        action = out["customer_action"].astype(str)
        orig = out["sentiment_label"].fillna("neutral").astype(str)
        out["sentiment_revised_label"] = orig
        out.loc[action == "formal_complaint", "sentiment_revised_label"] = "negative"
        return out

    def add_trends_keyword(df: pd.DataFrame) -> pd.DataFrame:
        return df

BASE = PROJECT_ROOT
JOIN_KEY_CANDIDATES = ("record_id", "id", "complaint_id")

KEY_CHART_COMPANY = "chart_sel_company"
KEY_CHART_ISSUE = "chart_sel_issue"
KEY_CHART_PRODUCT = "chart_sel_product"
KEY_CHART_ACTION = "chart_sel_action"

KEY_SB_YEAR = "sb_year_range"
KEY_SB_COMPANY = "sb_company"
KEY_SB_ISSUE = "sb_issue"
KEY_SB_PRODUCT = "sb_product"
KEY_SB_ACTION = "sb_customer_action"
KEY_SB_SRC = "sb_source"

# Primary MI dimension: observable behavior (not supplier NLP sentiment — often misleading on short text).
ACTION_COL = "customer_action"

CHART_H = 260
TREND_H = 300

# Plotly's floating modebar (top-right) overlaps the first rows of horizontal bar charts and steals clicks.
PLOTLY_CONFIG_SELECT = {"displayModeBar": False, "scrollZoom": False}
PLOTLY_CONFIG_TREND = {"displayModeBar": "hover", "scrollZoom": False}

# Bump to remount Plotly charts so selections clear (read-only in session state)
KEY_CHART_GEN = "chart_gen"


def chart_widget_key(base: str) -> str:
    return f"{base}_{st.session_state.get(KEY_CHART_GEN, 0)}"


def resolve_csv_path() -> Path:
    override = os.environ.get("DASHBOARD_CSV_PATH", "").strip()
    if override:
        return Path(override)
    return BASE / DEFAULT_CLEAN_FILENAME


def resolve_aux_csv_path() -> Path | None:
    aux = os.environ.get("DASHBOARD_AUX_CSV", "").strip()
    return Path(aux) if aux else None


def _parse_issue(raw: object) -> str | None:
    if pd.isna(raw) or not isinstance(raw, str):
        return None
    try:
        d = json.loads(raw)
        v = d.get("issue")
        return str(v) if v is not None else None
    except (json.JSONDecodeError, TypeError):
        return None


@st.cache_data(show_spinner=False)
def load_main_csv(path_str: str) -> pd.DataFrame:
    p = Path(path_str)
    if not p.is_file():
        raise FileNotFoundError(f"CSV not found: {p}")
    df = pd.read_csv(p, low_memory=False, encoding="utf-8-sig")
    if "issue" not in df.columns or df["issue"].isna().all():
        df["issue"] = df["raw_metadata"].apply(_parse_issue)
    df = add_revised_sentiment(df)
    if "trends_keyword" not in df.columns:
        df = add_trends_keyword(df)
    return df


def merge_aux_csv(df: pd.DataFrame) -> tuple[pd.DataFrame, str | None]:
    aux_path = resolve_aux_csv_path()
    if not aux_path or not aux_path.is_file():
        return df, None
    aux = pd.read_csv(aux_path, low_memory=False, encoding="utf-8-sig")
    key = next((k for k in JOIN_KEY_CANDIDATES if k in df.columns and k in aux.columns), None)
    if not key:
        return df, f"Could not join aux CSV (need a shared id column): {aux_path.name}"
    drop_overlap = [c for c in aux.columns if c in df.columns and c != key]
    aux = aux.drop(columns=drop_overlap, errors="ignore")
    return df.merge(aux, on=key, how="left"), None


def init_session_state(y_min: int, y_max: int) -> None:
    if KEY_CHART_GEN not in st.session_state:
        st.session_state[KEY_CHART_GEN] = 0
    if KEY_SB_YEAR not in st.session_state:
        st.session_state[KEY_SB_YEAR] = (y_min, y_max)
    if KEY_SB_COMPANY not in st.session_state:
        st.session_state[KEY_SB_COMPANY] = []
    if KEY_SB_ISSUE not in st.session_state:
        st.session_state[KEY_SB_ISSUE] = []
    if KEY_SB_PRODUCT not in st.session_state:
        st.session_state[KEY_SB_PRODUCT] = []
    if KEY_SB_ACTION not in st.session_state:
        st.session_state[KEY_SB_ACTION] = []
    if KEY_SB_SRC not in st.session_state:
        st.session_state[KEY_SB_SRC] = []


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    y0, y1 = st.session_state[KEY_SB_YEAR]
    out = out[(out["year"] >= y0) & (out["year"] <= y1)]

    if st.session_state[KEY_SB_COMPANY]:
        out = out[out["company"].isin(st.session_state[KEY_SB_COMPANY])]
    if st.session_state[KEY_SB_ISSUE]:
        out = out[out["issue"].isin(st.session_state[KEY_SB_ISSUE])]
    if st.session_state[KEY_SB_PRODUCT]:
        out = out[out["product_service"].isin(st.session_state[KEY_SB_PRODUCT])]
    if st.session_state[KEY_SB_ACTION] and ACTION_COL in out.columns:
        out = out[out[ACTION_COL].astype(str).isin(st.session_state[KEY_SB_ACTION])]
    if st.session_state[KEY_SB_SRC]:
        out = out[out["source"].isin(st.session_state[KEY_SB_SRC])]

    return out


def main() -> None:
    st.set_page_config(
        page_title="ISYS 812 · Customer intelligence",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
<style>
    .block-container { padding-top: 0.6rem; padding-bottom: 0.4rem; }
    /* Main page title (see markdown h1 below); keep any other h1 consistent */
    h1 { font-size: 1.15rem; font-weight: 600; line-height: 1.35; margin-top: 0.85rem; margin-bottom: 0.35rem;
         word-wrap: break-word; letter-spacing: normal; }
    h3 { font-size: 0.9rem; margin-top: 0.2rem; margin-bottom: 0.05rem; }
</style>
""",
        unsafe_allow_html=True,
    )

    csv_path = resolve_csv_path()
    try:
        df_all = load_main_csv(str(csv_path))
    except FileNotFoundError as e:
        st.error(str(e))
        st.info(
            "Generate `master_customer_behavior_clean.csv` via **notebook_export_clean_csv.ipynb** "
            "or: `python -c \"from shared_cleaning_rules import export_clean_csv; export_clean_csv()\"`"
        )
        return

    df_all, aux_warn = merge_aux_csv(df_all)
    df_all = add_revised_sentiment(df_all)
    if "trends_keyword" not in df_all.columns:
        df_all = add_trends_keyword(df_all)
    if aux_warn:
        st.warning(aux_warn)

    years = sorted(df_all["year"].dropna().unique().tolist())
    y_min, y_max = int(min(years)), int(max(years))
    init_session_state(y_min, y_max)

    src_opts = sorted(df_all["source"].dropna().unique().tolist()) if "source" in df_all.columns else []

    y0, y1 = st.session_state[KEY_SB_YEAR]
    src_sel = st.session_state.get(KEY_SB_SRC) or []
    df_opts = df_all[(df_all["year"] >= y0) & (df_all["year"] <= y1)]
    if src_sel:
        df_opts = df_opts[df_opts["source"].isin(src_sel)]

    def _prune_multiselect(key: str, allowed: list[str]) -> None:
        if key not in st.session_state or not allowed:
            return
        allow = set(allowed)
        cur = st.session_state[key]
        if isinstance(cur, list) and cur:
            st.session_state[key] = [x for x in cur if x in allow]

    companies_opts = sorted(df_opts["company"].dropna().unique().tolist()) if "company" in df_opts.columns else []
    issues_opts = sorted(df_opts["issue"].dropna().unique().tolist()) if "issue" in df_opts.columns else []
    prods_opts = (
        sorted(df_opts["product_service"].dropna().unique().tolist()) if "product_service" in df_opts.columns else []
    )
    action_opts = (
        sorted(df_opts[ACTION_COL].dropna().astype(str).unique().tolist()) if ACTION_COL in df_opts.columns else []
    )

    _prune_multiselect(KEY_SB_COMPANY, companies_opts)
    _prune_multiselect(KEY_SB_ISSUE, issues_opts)
    _prune_multiselect(KEY_SB_PRODUCT, prods_opts)
    _prune_multiselect(KEY_SB_ACTION, action_opts)

    with st.sidebar:
        st.markdown("##### Filters (use these)")
        st.slider("Year range", y_min, y_max, key=KEY_SB_YEAR)
        st.caption("All slicing is done here — not Tableau-style chart clicks.")

        if src_opts:
            st.multiselect(
                "Source",
                src_opts,
                key=KEY_SB_SRC,
                help="Choose source(s) first — Company / Issue lists only show values that exist in those sources.",
            )

        if companies_opts:
            st.multiselect(
                "Company",
                companies_opts,
                key=KEY_SB_COMPANY,
            )
        if issues_opts:
            st.multiselect("Issue", issues_opts, key=KEY_SB_ISSUE)
        if prods_opts:
            st.multiselect("Product / service", prods_opts, key=KEY_SB_PRODUCT)
        if action_opts:
            st.multiselect(
                "Customer action",
                action_opts,
                key=KEY_SB_ACTION,
                help="What the record represents (e.g. formal_complaint vs churning). Clearer for MI than NLP sentiment.",
            )

        if st.button("Clear all filters", use_container_width=True):
            st.session_state[KEY_SB_COMPANY] = []
            st.session_state[KEY_SB_ISSUE] = []
            st.session_state[KEY_SB_PRODUCT] = []
            st.session_state[KEY_SB_ACTION] = []
            st.session_state[KEY_SB_SRC] = []
            st.session_state[KEY_SB_YEAR] = (y_min, y_max)
            st.session_state[KEY_CHART_GEN] = st.session_state.get(KEY_CHART_GEN, 0) + 1
            st.rerun()

    df = filter_dataframe(df_all)

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(
        "<h1>ISYS 812<br/>Customer intelligence</h1>",
        unsafe_allow_html=True,
    )
    st.info(
        "**Use the left sidebar to filter.** **Source** + **year** control which values appear in "
        "**Company / Issue / Product** lists. Empty Source = all channels (Trends theme tags can still "
        "show under Company). Charts are read-only. **Clear all filters** resets."
    )
    st.caption("Trend chart: year range follows the sidebar slider only.")

    if len(df) == 0:
        st.warning("No rows match. Widen year range or clear filters.")
        return

    n = len(df)
    fc_share = (
        (df[ACTION_COL].astype(str) == "formal_complaint").mean() if ACTION_COL in df.columns else 0.0
    )
    n_issues = df["issue"].nunique() if "issue" in df.columns else 0
    top_issue_share = 0.0
    if "issue" in df.columns and n > 0:
        vc = df["issue"].value_counts()
        if len(vc) > 0:
            top_issue_share = vc.iloc[0] / n

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Events", f"{n:,}")
    k2.metric("Formal complaint %", f"{fc_share:.1%}")
    k3.metric("Issue types", f"{n_issues:,}")
    k4.metric("Top issue share", f"{top_issue_share:.1%}")

    # Trend: no on_select (subplots + selection are flaky in Streamlit)
    st.markdown("##### Volume & formal complaints over time")
    if "year" in df.columns and "month" in df.columns and ACTION_COL in df.columns:
        ts = (
            df.groupby(["year", "month"])
            .agg(
                events=("record_id", "count"),
                fc_rate=(
                    ACTION_COL,
                    lambda s: (s.astype(str) == "formal_complaint").mean(),
                ),
            )
            .reset_index()
        )
        ts["period"] = pd.to_datetime(dict(year=ts["year"], month=ts["month"], day=1))
        ts = ts.sort_values("period")
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(
            go.Bar(x=ts["period"], y=ts["events"], name="Events", marker_color="#4e79a7"),
            secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(
                x=ts["period"],
                y=ts["fc_rate"],
                name="Formal complaint rate",
                mode="lines+markers",
                line=dict(color="#e15759", width=2),
            ),
            secondary_y=True,
        )
        ev_max = max(float(ts["events"].max()), 1.0) if len(ts) else 1.0
        fig.update_yaxes(
            title_text="Events",
            secondary_y=False,
            showgrid=False,
            rangemode="tozero",
            range=[0, ev_max * 1.08],
        )
        # Lock 0–100% on the right axis; otherwise tiny y (0–1) can render like the bottom of the events scale.
        fig.update_yaxes(
            title_text="Formal complaint rate",
            tickformat=".0%",
            secondary_y=True,
            showgrid=False,
            rangemode="tozero",
            range=[0, 1],
        )
        fig.update_layout(
            height=TREND_H,
            margin=dict(l=40, r=40, t=28, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            hovermode="x unified",
        )
        st.plotly_chart(
            fig,
            width="stretch",
            on_select="ignore",
            key="trend_subplot",
            config=PLOTLY_CONFIG_TREND,
        )
    else:
        yc = df.groupby("year").size().reset_index(name="count")
        fig = px.line(yc, x="year", y="count", markers=True)
        fig.update_layout(height=TREND_H, margin=dict(t=28, b=40))
        st.plotly_chart(
            fig,
            width="stretch",
            on_select="ignore",
            key="trend_line",
            config=PLOTLY_CONFIG_TREND,
        )

    r1, r2 = st.columns(2)
    with r1:
        st.markdown("##### Customer action (top 12)")
        if ACTION_COL in df.columns:
            ac = df[ACTION_COL].dropna().astype(str)
            if len(ac) > 0:
                top_a = ac.value_counts().head(12).reset_index()
                top_a.columns = ["customer_action", "count"]
                fig_a = px.bar(
                    top_a,
                    x="count",
                    y="customer_action",
                    orientation="h",
                )
                fig_a.update_layout(height=CHART_H, margin=dict(l=10, r=10, t=14, b=10))
                fig_a.update_yaxes(autorange="reversed")
                st.plotly_chart(
                    fig_a,
                    width="stretch",
                    on_select="ignore",
                    key=chart_widget_key(KEY_CHART_ACTION),
                    config=PLOTLY_CONFIG_SELECT,
                )
            else:
                st.info("No customer_action values.")
        else:
            st.info("Column customer_action not found.")
    with r2:
        st.markdown("##### Issues (top 12)")
        iss = df["issue"].dropna()
        if len(iss) > 0:
            top_i = iss.value_counts().head(12).reset_index()
            top_i.columns = ["issue", "count"]
            fig_i = px.bar(
                top_i,
                x="count",
                y="issue",
                orientation="h",
            )
            fig_i.update_layout(height=CHART_H, margin=dict(l=10, r=10, t=14, b=10))
            fig_i.update_yaxes(autorange="reversed")
            st.plotly_chart(
                fig_i,
                width="stretch",
                on_select="ignore",
                key=chart_widget_key(KEY_CHART_ISSUE),
                config=PLOTLY_CONFIG_SELECT,
            )
        else:
            st.info("No issues.")

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("##### Companies (top 12)")
        if "company" in df.columns:
            if ACTION_COL in df.columns:
                co = (
                    df.groupby("company")
                    .agg(
                        events=("record_id", "count"),
                        fc_rate=(
                            ACTION_COL,
                            lambda s: (s.astype(str) == "formal_complaint").mean(),
                        ),
                    )
                    .reset_index()
                    .sort_values("events", ascending=False)
                    .head(12)
                )
                fig_c = px.bar(
                    co,
                    x="events",
                    y="company",
                    orientation="h",
                    color="fc_rate",
                    color_continuous_scale="Reds",
                    labels={"fc_rate": "Formal complaint rate", "events": "Events"},
                )
            else:
                co = (
                    df.groupby("company")
                    .agg(events=("record_id", "count"))
                    .reset_index()
                    .sort_values("events", ascending=False)
                    .head(12)
                )
                fig_c = px.bar(co, x="events", y="company", orientation="h")
            fig_c.update_layout(height=CHART_H, margin=dict(l=10, r=10, t=14, b=10), coloraxis_showscale=False)
            fig_c.update_yaxes(autorange="reversed")
            st.plotly_chart(
                fig_c,
                width="stretch",
                on_select="ignore",
                key=chart_widget_key(KEY_CHART_COMPANY),
                config=PLOTLY_CONFIG_SELECT,
            )
    with c4:
        st.markdown("##### Products (top 10)")
        if "product_service" in df.columns:
            if ACTION_COL in df.columns:
                pr = (
                    df.groupby("product_service")
                    .agg(
                        events=("record_id", "count"),
                        fc_rate=(
                            ACTION_COL,
                            lambda s: (s.astype(str) == "formal_complaint").mean(),
                        ),
                    )
                    .reset_index()
                    .sort_values("events", ascending=False)
                    .head(10)
                )
                fig_p = px.bar(
                    pr,
                    x="events",
                    y="product_service",
                    orientation="h",
                    color="fc_rate",
                    color_continuous_scale="OrRd",
                    labels={"fc_rate": "Formal complaint rate", "events": "Events"},
                )
            else:
                pr = (
                    df.groupby("product_service")
                    .agg(events=("record_id", "count"))
                    .reset_index()
                    .sort_values("events", ascending=False)
                    .head(10)
                )
                fig_p = px.bar(pr, x="events", y="product_service", orientation="h")
            fig_p.update_layout(height=CHART_H, margin=dict(l=10, r=10, t=14, b=10), coloraxis_showscale=False)
            fig_p.update_yaxes(autorange="reversed")
            st.plotly_chart(
                fig_p,
                width="stretch",
                on_select="ignore",
                key=chart_widget_key(KEY_CHART_PRODUCT),
                config=PLOTLY_CONFIG_SELECT,
            )

    with st.expander("Notes & limits"):
        st.markdown(
            """
**How filtering works (read this):** Use the **left sidebar** multiselects and year slider. Every chart
and KPI uses the **same** filtered table. **Do not rely on clicking** chart elements to filter —
this is **not Tableau**; Streamlit’s Plotly integration does not reliably wire those clicks into the
sidebar. The modebar is off on bar charts to reduce clutter; the trend chart shows its toolbar on **hover**.

**Google Trends rows:** The `company` column is a **short theme tag** (e.g. `not worth`, `plan change`),
not a bank. The full search phrase is in **`trends_keyword`** (from metadata) — e.g. *subscription not worth*
means interest in searches about whether a subscription is worth it, not a company named “Not Worth.”
**CFPB** rows use real firm names in `company`. For finance MI, keep **Source = CFPB**.

**Customer action vs sentiment:** Filters and charts use **`customer_action`** (what the row represents —
e.g. `formal_complaint`, `churning`, reviews). **Formal complaint %** and the **formal complaint rate**
in trends and bar colors measure **escalation to the CFPB complaint channel**, not NLP “happiness.”
The CSV still contains **`sentiment_label` / `sentiment_score`** and, when exported, **`sentiment_revised_label`**
for research and audit; the dashboard does **not** treat NLP sentiment as a headline KPI because short
category text is often mislabeled.

**Fit on screen:** Layout is tightened; very small monitors may still scroll slightly.
            """
        )

    with st.expander("Multiple CSVs (advanced)"):
        st.markdown(
            "Set **`DASHBOARD_AUX_CSV`** to merge a second file on `record_id`. "
            "Otherwise merge offline into one CSV."
        )


if __name__ == "__main__":
    main()
