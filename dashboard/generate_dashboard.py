"""
generate_dashboard.py — Generates multi-panel KPI dashboard and Excel report.
"""
import pandas as pd, numpy as np, matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec, os

np.random.seed(42)
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(BASE,"outputs"); os.makedirs(OUT,exist_ok=True)

# ── GENERATE SAMPLE DATA ──────────────────────────────────────────
n=200
df=pd.DataFrame({
    "site_id":[f"SITE_{i:03d}" for i in np.random.randint(1,51,n)],
    "region":np.random.choice(["Lagos","Abuja","PH","Kano","Enugu"],n),
    "vendor":np.random.choice(["FastFuel","NigerDiesel","SwiftHaul","PrimeLogistics"],n),
    "month":np.random.choice(pd.period_range("2023-01","2023-12",freq="M").astype(str),n),
    "qty_ordered":np.random.randint(500,5000,n),
    "qty_delivered":np.random.randint(400,5100,n),
    "on_time":np.random.choice([0,1],n,p=[0.18,0.82]),
    "downtime_hrs":np.random.exponential(2,n),
    "fuel_autonomy_days":np.random.uniform(0.5,10,n).round(1),
})
df["accurate"]=(abs(df["qty_delivered"]-df["qty_ordered"])/df["qty_ordered"]<=0.05).astype(int)
TOTAL_MINS=43800
df["availability_pct"]=((TOTAL_MINS-df["downtime_hrs"]*60)/TOTAL_MINS*100).clip(90,100).round(2)

# ── COMPUTE KPIs ──────────────────────────────────────────────────
kpis={
    "Total Sites":         df["site_id"].nunique(),
    "Total Deliveries":    len(df),
    "Avg Delivery Accuracy":f"{df['accurate'].mean()*100:.1f}%",
    "Avg On-Time Rate":    f"{df['on_time'].mean()*100:.1f}%",
    "Avg Availability":    f"{df['availability_pct'].mean():.2f}%",
    "High Risk Sites":     (df["fuel_autonomy_days"]<2).sum(),
}
print("=== EXECUTIVE KPI SUMMARY ===")
for k,v in kpis.items(): print(f"  {k}: {v}")

# ── DASHBOARD CHART ───────────────────────────────────────────────
fig=plt.figure(figsize=(18,12))
fig.suptitle("Telecom Operations — KPI Dashboard", fontsize=16,fontweight="bold",y=0.98)
gs=gridspec.GridSpec(2,3,figure=fig,hspace=0.45,wspace=0.35)

# 1 Availability by region
ax1=fig.add_subplot(gs[0,0])
reg=df.groupby("region")["availability_pct"].mean().sort_values()
ax1.barh(reg.index,reg.values,color="steelblue")
ax1.axvline(99.5,color="red",linestyle="--",alpha=0.7,label="SLA 99.5%")
ax1.set_title("Avg Availability by Region"); ax1.legend(fontsize=8)

# 2 On-time by vendor
ax2=fig.add_subplot(gs[0,1])
vot=df.groupby("vendor")["on_time"].mean()*100
ax2.bar(vot.index,vot.values,color=["#27ae60","#f1c40f","#e67e22","#e74c3c"])
ax2.axhline(80,color="red",linestyle="--",alpha=0.7)
ax2.set_title("On-Time Delivery by Vendor"); ax2.set_ylabel("%"); ax2.tick_params(axis="x",rotation=20)

# 3 Monthly accuracy trend
ax3=fig.add_subplot(gs[0,2])
mt=df.groupby("month")["accurate"].mean()*100
ax3.plot(mt.index,mt.values,marker="o",color="steelblue")
ax3.fill_between(mt.index,mt.values,alpha=0.1,color="steelblue")
ax3.axhline(95,color="red",linestyle="--",alpha=0.7)
ax3.set_title("Monthly Delivery Accuracy"); ax3.tick_params(axis="x",rotation=45)

# 4 Risk sites
ax4=fig.add_subplot(gs[1,0])
risk=df[df["fuel_autonomy_days"]<2]["region"].value_counts()
ax4.bar(risk.index,risk.values,color="tomato")
ax4.set_title("Supply Risk Events by Region"); ax4.set_ylabel("Events")

# 5 Autonomy distribution
ax5=fig.add_subplot(gs[1,1])
ax5.hist(df["fuel_autonomy_days"],bins=20,color="steelblue",edgecolor="white",alpha=0.85)
ax5.axvline(2,color="red",linestyle="--",label="Risk threshold"); ax5.legend()
ax5.set_title("Fuel Autonomy Distribution"); ax5.set_xlabel("Days")

# 6 KPI text box
ax6=fig.add_subplot(gs[1,2])
ax6.axis("off")
kpi_text="\n".join([f"{'●'} {k}: {v}" for k,v in kpis.items()])
ax6.text(0.1,0.5,kpi_text,transform=ax6.transAxes,fontsize=11,va="center",
         bbox=dict(boxstyle="round",facecolor="#EBF5FB",alpha=0.8))
ax6.set_title("Executive KPI Summary")

plt.savefig(f"{OUT}/kpi_dashboard.png",dpi=150,bbox_inches="tight")
print(f"\n✅ Dashboard saved to {OUT}/kpi_dashboard.png")

# ── EXCEL REPORT ──────────────────────────────────────────────────
try:
    with pd.ExcelWriter(f"{OUT}/kpi_report.xlsx",engine="openpyxl") as w:
        pd.DataFrame(list(kpis.items()),columns=["KPI","Value"]).to_excel(w,sheet_name="Summary",index=False)
        df.groupby("region").agg(sites=("site_id","nunique"),deliveries=("qty_ordered","count"),
            avg_accuracy=("accurate","mean"),avg_ontime=("on_time","mean")).round(3).to_excel(w,sheet_name="By Region")
        df.groupby("vendor").agg(deliveries=("qty_ordered","count"),
            on_time_rate=("on_time","mean"),accuracy=("accurate","mean")).round(3).to_excel(w,sheet_name="By Vendor")
    print(f"✅ Excel report saved to {OUT}/kpi_report.xlsx")
except Exception as e:
    print(f"Excel export skipped: {e}")
