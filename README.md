retail\_ecommerce\_analysis
Overview
---

This repository contains the code, output and dataset for an analysis on a publicly available UK-based online retail dataset, including RFM scoring. It cleans the data, scores it across these 3 behavioral dimensions, assigns it to a segment, and visualizes useful information such as geographic distribution, trends, and the segmentation itself.

## Dataset

This analysis was conducted on the UCI Online Retail II, with around 1M transactions recorded from a UK retailer. The recorded data tracks from December 2009 to December 2011.

## Requirements

Python 3.8, pandas, numpy, matplotlib

## Methods

Two dataframes are maintained throughout the pipeline: df\_full, which includes all rows from the original dataset being a clone, and was used for a monthly revenue and geographic-trends chart. This was used alongside df\_clean, which was filtered to rows with a valid customer ID, valid quantity, and valid, positive revenue, which was applied to the RFM calculations.


|Recency|Days since the last purchase from a specific customer ID|Lower is better|
|-|-|-|
|Frequency|Number of unique invoices from a specific customer ID|Higher is better|
|Monetary|Total revenue from a specific customer ID|Higher is better|



## Outputs

|File|Description|
|-|-|
|outputs/mrevenue.png|A revenue line chart ordered by dt.monthly|
|outputs/top\_countries.png|Top 10 countries by revenue, 2 charts. One includes the UK, One does not. This is because the story is a UK-based online retail store, and excluding the UK allows the analysis of other areas of interest.|
|outputs/segments.png|The distribution of customer segments in a bar chart.|
|outputs/rfm\_summary.csv|The mean RFM values per segment.|



