# GeekSales

A powerful PySpark utility package for sales data analysis and visualization.

## Features

- Create and configure Spark sessions with optimized settings
- Calculate sales metrics and aggregations
- Generate comprehensive sales dashboards
- Create various sales visualizations:
  - Sales by region
  - Customer order distribution
  - Sales trends over time
  - Top products by sales

## Installation

```bash
pip install geeksales
```

## Usage

```python
from geeksales import spark_utils

# Create a Spark session
spark = spark_utils.create_spark_session("Sales Analysis")

# Load your sales data
df = spark.read.csv("sales_data.csv", header=True, inferSchema=True)

# Add sales metrics
df_with_metrics = spark_utils.add_sales_metrics(df)

# Generate sales summary
summary = spark_utils.get_sales_summary(df_with_metrics)

# Create visualizations
spark_utils.plot_sales_by_region(df_with_metrics)
spark_utils.plot_customer_order_distribution(df_with_metrics)
spark_utils.plot_sales_trend(df_with_metrics)
spark_utils.plot_product_sales(df_with_metrics)

# Create a complete dashboard
dashboard = spark_utils.create_sales_dashboard(df_with_metrics)
```

## Requirements

- Python 3.7 or higher
- PySpark 3.0 or higher
- Matplotlib 3.0 or higher
- Seaborn 0.11 or higher
- Pandas 1.0 or higher

## License

This project is licensed under the MIT License - see the LICENSE file for details. 