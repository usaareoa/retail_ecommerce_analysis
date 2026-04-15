
import pandas as pd
import numpy
import matplotlib.pyplot as plt
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
df = pd.read_csv("dataset/online.csv")
pd.set_option("display.float_format", "{:,.2f}".format)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

df["Revenue"] = df["Quantity"] * df["Price"]

df_full = df.copy()
df_clean = df[df["Customer ID"].notna()].copy()
df_clean = df_clean[df_clean["Quantity"] > 0]
df_clean = df_clean[df_clean ["Revenue"] > 0]


df_full["Month"] = df_full["InvoiceDate"].dt.to_period("M")
monthly_revenue = df_full.groupby("Month")["Revenue"].sum().reset_index()
monthly_revenue["Month"] = monthly_revenue["Month"].astype(str)

snapshot_date = df_clean["InvoiceDate"].max() + pd.Timedelta(days=1)

rfg = df_clean.groupby("Customer ID").agg(
recency=("InvoiceDate", lambda x: (snapshot_date - x.max()).days),
fre=("Invoice", "nunique"),
mone=("Revenue", "sum"),
).reset_index()



rfg["Rscore"] = pd.qcut(rfg["recency"], q=5, labels=[5,4,3,2,1])
rfg["Fscore"] = pd.qcut(rfg["fre"], q=5, labels=False, duplicates="drop") + 1
rfg["Mscore"] = pd.qcut(rfg["mone"], q=5, labels=[1,2,3,4,5])

rfg["rfm score"] = rfg["Rscore"].astype(str) + rfg["Fscore"].astype(str) + rfg["Mscore"].astype(str)

def segment(row):
    if row["Rscore"] >= 4 and row["Fscore"] >= 3:
        return "great"
    elif row["Rscore"] >= 3 and row["Fscore"] >= 2:
        return "returning"
    elif row["Rscore"] >= 4 and row["Fscore"] <= 1:
        return "new"
    elif row["Rscore"] <= 2 and row["Fscore"] <= 2:
        return "losing"
    else:
        return "help"
rfg["Segment"] = rfg.apply(segment, axis=1)
print(rfg["Segment"].value_counts())


#visualizer stuff below 

plt.figure(figsize=(24, 5))
plt.plot(monthly_revenue["Month"], monthly_revenue["Revenue"], marker="o", color=(27/255, 42/255, 74/255))
plt.title("Revenue per Month", fontsize=14)
plt.xlabel("Month")
plt.ylabel("Revenue in dollars")
plt.xticks(rotation=90)
plt.tight_layout()
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p:f"${x:,.0f}"))
plt.savefig("outputs/mrevenue.png", dpi=250, bbox_inches=("tight"))
plt.close()
print("saved")

countries = df_full.groupby("Country")["Revenue"].sum().sort_values(ascending=False).head(10)
print(countries)

fig, axes = plt.subplots(1, 2, figsize=(16, 5))
countries.plot(kind="bar", ax=axes[0], color="blue")
axes[0].set_title("Top 10 Countries by Revenue, including Britain", fontweight='extra bold')
axes[0].set_xlabel("")
axes[0].set_ylabel("Revenue ($)")
axes[0].tick_params(axis="x", rotation=90)
axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))

topcountries_sinUK = countries[countries.index!="United Kingdom"]
topcountries_sinUK.plot(kind="bar", ax=axes[1], color="Steelblue")
axes[1].set_title("Top 10 Countries by Revenue, not including Britain", fontweight='extra bold')
axes[1].set_xlabel("")  
axes[1].set_ylabel("")
axes[1].tick_params(axis="x", rotation=90)
axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x:,.0f}"))
plt.tight_layout(pad=2.0)
plt.savefig("outputs/top_countries.png", dpi=250, bbox_inches="tight")
plt.close()

rfg["Segment"].value_counts().plot(kind="bar", color="steelblue")
plt.title("Groups of Customers")
plt.xlabel("Segments")
plt.ylabel("Numbered")
plt.xticks( rotation=90)
plt.tight_layout()
plt.savefig("outputs/segments.png", dpi=250, bbox_inches="tight")
plt.close()
print("saved")

summary = rfg.groupby("Segment")[["recency", "fre", "mone"]].mean().round(2)
print(summary)
summary.to_csv("outputs/rfm_summary.csv", index=True)