
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="CPM / PERT + Gantt", layout="wide")
st.title("Gestão do Cronograma: CPM / PERT e Gráfico de Gantt")

with st.sidebar:
    st.header("Parâmetros")
    ru = st.text_input("Seu RU (ex.: 5020930)", value="5020930")
    last_digit = int(ru[-1]) if ru and ru[-1].isdigit() else 0
    o_duration = last_digit + 10
    st.write(f"**Duração da Atividade O = {last_digit} + 10 = {o_duration} dias**")
    st.caption("O valor é calculado automaticamente pelo último dígito do RU.")
    st.markdown("---")
    st.download_button("Baixar modelo CSV", data=open("activities.csv","rb").read(),
                       file_name="activities.csv", mime="text/csv")

df = pd.read_csv("activities.csv")
df.loc[df["Activity"]=="O","Duration"] = o_duration
st.markdown("### 1) Tabela de Atividades")
df = st.data_editor(df, num_rows="fixed", use_container_width=True)

activities = {}
for _, r in df.iterrows():
    preds = [] if r["Predecessors"] == "-" else [p.strip() for p in str(r["Predecessors"]).split(",")]
    activities[r["Activity"]] = {"duration": int(r["Duration"]), "pred": preds}

# Topological order
order, temp, perm = [], set(), set()
def visit(n):
    if n in perm: return
    if n in temp: raise ValueError("Ciclo detectado.")
    temp.add(n)
    for p in activities[n]["pred"]:
        visit(p)
    temp.remove(n); perm.add(n); order.append(n)
for a in activities: visit(a)

ES = {a:0 for a in activities}; EF = {a:0 for a in activities}
for a in order:
    ES[a] = max([EF[p] for p in activities[a]["pred"]], default=0)
    EF[a] = ES[a] + activities[a]["duration"]
project_duration = max(EF.values())

succ = {a:[] for a in activities}
for a,info in activities.items():
    for p in info["pred"]:
        succ[p].append(a)

LF = {a:project_duration for a in activities}; LS = {a:0 for a in activities}
for a in reversed(order):
    LF[a] = min([LS[s] for s in succ[a]], default=project_duration)
    LS[a] = LF[a] - activities[a]["duration"]
slack = {a: LS[a]-ES[a] for a in activities}

out = pd.DataFrame({
    "Activity": list(activities.keys()),
    "Duration": [activities[a]["duration"] for a in activities],
    "Predecessors": [", ".join(activities[a]["pred"]) if activities[a]["pred"] else "-" for a in activities],
    "ES": [ES[a] for a in activities],
    "EF": [EF[a] for a in activities],
    "LS": [LS[a] for a in activities],
    "LF": [LF[a] for a in activities],
    "Slack": [slack[a] for a in activities],
    "Critical": [("Yes" if np.isclose(slack[a],0) else "No") for a in activities],
}).sort_values("ES").reset_index(drop=True)

st.markdown("### 2) Quadro CPM")
st.dataframe(out, use_container_width=True)

st.markdown("### 3) Gantt")
fig, ax = plt.subplots(figsize=(10,6))
y = np.arange(len(out))
ax.barh(y, out["Duration"], left=out["ES"])
ax.set_yticks(y); ax.set_yticklabels(out["Activity"]); ax.invert_yaxis()
ax.set_xlabel("Dias"); ax.set_title("Gantt")
for i,(es,dur,ef,crit) in enumerate(zip(out["ES"], out["Duration"], out["EF"], out["Critical"])):
    ax.text(es+dur/2, i, f"{es}-{ef}" + (" *" if crit=="Yes" else ""), ha="center", va="center", fontsize=8)
st.pyplot(fig)

st.markdown("### 4) Diagrama de Redes")
layers = {}
for a in out["Activity"]:
    layers.setdefault(ES[a], []).append(a)
sorted_layers = sorted(layers.keys())
pos = {}; x_gap=3; y_gap=1.3
for li,k in enumerate(sorted_layers):
    for ai,a in enumerate(sorted(layers[k])):
        pos[a] = (li*x_gap, -ai*y_gap)

fig2, ax2 = plt.subplots(figsize=(12,7))
for a,info in activities.items():
    for p in info["pred"]:
        x1,y1 = pos[p]; x2,y2 = pos[a]
        ax2.plot([x1+0.8, x2-0.8],[y1,y2], lw=1)
        ax2.annotate("", xy=(x2-0.8,y2), xytext=(x1+0.8,y1), arrowprops=dict(arrowstyle="->", lw=1))
for a,(x,y) in pos.items():
    rect = plt.Rectangle((x-0.8,y-0.4),1.6,0.8, fill=False, lw=1.5)
    ax2.add_patch(rect)
    ax2.text(x, y+0.12, a, ha="center", va="center", fontsize=10, fontweight="bold")
    ax2.text(x, y-0.18, f"D={activities[a]['duration']}", ha="center", va="center", fontsize=8)
    ax2.text(x-0.95, y, f"ES {ES[a]}", ha="left", va="center", fontsize=7)
    ax2.text(x+0.95, y, f"EF {EF[a]}", ha="right", va="center", fontsize=7)
    if np.isclose(slack[a],0):
        ax2.text(x, y-0.35, "CRÍTICO", ha="center", va="center", fontsize=7)
ax2.axis("off"); ax2.set_title("Diagrama de Redes (PERT/CPM)")
st.pyplot(fig2)
