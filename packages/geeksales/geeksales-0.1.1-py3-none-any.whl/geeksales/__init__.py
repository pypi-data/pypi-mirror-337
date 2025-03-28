"""
GeekSales - A PySpark utility package for sales data analysis and visualization.
"""

from .spark_utils import (
    create_spark_session,
    add_sales_metrics,
    get_sales_summary,
    plot_sales_by_region,
    plot_customer_order_distribution,
    plot_sales_trend,
    plot_product_sales,
    create_sales_dashboard,
)

__version__ = "0.1.0"
__all__ = [
    "create_spark_session",
    "add_sales_metrics",
    "get_sales_summary",
    "plot_sales_by_region",
    "plot_customer_order_distribution",
    "plot_sales_trend",
    "plot_product_sales",
    "create_sales_dashboard",
] 