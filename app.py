import streamlit as st
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Hospital Referral Network", layout="wide")

st.title("🏥 Hospital Referral Network System")
st.markdown("### Analyze Doctor Referral Patterns with Graph + Centrality")

# -----------------------------
# INPUT SECTION
# -----------------------------
st.sidebar.header("➕ Add Referral Data")

doctor_from = st.sidebar.text_input("Referring Doctor")
doctor_to = st.sidebar.text_input("Referred To")

if "edges" not in st.session_state:
    st.session_state.edges = [
        ("Dr A", "Dr B"),
        ("Dr A", "Dr C"),
        ("Dr B", "Dr D"),
        ("Dr C", "Dr D"),
    ]

# Add new referral
if st.sidebar.button("Add Referral"):
    if doctor_from and doctor_to:
        st.session_state.edges.append((doctor_from, doctor_to))
        st.sidebar.success("Referral Added!")
    else:
        st.sidebar.error("Enter both doctors!")

# -----------------------------
# GRAPH CREATION
# -----------------------------
G = nx.DiGraph()
G.add_edges_from(st.session_state.edges)

# -----------------------------
# MENU
# -----------------------------
menu = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Graph View", "Centrality Analysis", "Doctor Lookup"]
)

# -----------------------------
# DASHBOARD
# -----------------------------
if menu == "Dashboard":
    st.header("📊 Overview")

    st.write(f"Total Doctors: {len(G.nodes())}")
    st.write(f"Total Referrals: {len(G.edges())}")

    df = pd.DataFrame(st.session_state.edges, columns=["From", "To"])
    st.dataframe(df)

# -----------------------------
# GRAPH VIEW
# -----------------------------
elif menu == "Graph View":
    st.header("🔗 Referral Network Graph")

    fig, ax = plt.subplots()
    pos = nx.spring_layout(G)

    # Highlight top doctor
    degree = nx.degree_centrality(G)
    top_doc = max(degree, key=degree.get)

    node_colors = ["red" if node == top_doc else "lightblue" for node in G.nodes()]

    nx.draw(
        G, pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2000,
        font_size=10,
        ax=ax
    )

    st.pyplot(fig)

    st.success(f"Top Referral Hub: {top_doc}")

# -----------------------------
# CENTRALITY ANALYSIS
# -----------------------------
elif menu == "Centrality Analysis":
    st.header("📊 Centrality Measures")

    degree = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)
    closeness = nx.closeness_centrality(G)

    df = pd.DataFrame({
        "Doctor": list(G.nodes()),
        "Degree": list(degree.values()),
        "Betweenness": list(betweenness.values()),
        "Closeness": list(closeness.values())
    })

    st.dataframe(df)

    st.subheader("🏆 Key Doctor")

    top_doc = max(degree, key=degree.get)
    st.success(f"Most Important Doctor: {top_doc}")

# -----------------------------
# DOCTOR LOOKUP
# -----------------------------
elif menu == "Doctor Lookup":
    st.header("🔍 Doctor Referral Details")

    doctor = st.selectbox("Select Doctor", list(G.nodes()))

    outgoing = list(G.successors(doctor))
    incoming = list(G.predecessors(doctor))

    st.write(f"➡ Refers to: {outgoing}")
    st.write(f"⬅ Referred by: {incoming}")
