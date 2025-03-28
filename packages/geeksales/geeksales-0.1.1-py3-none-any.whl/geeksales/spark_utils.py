from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, count, avg, round
from pyspark.sql.window import Window
from pyspark.sql.types import DoubleType

def create_spark_session(app_name):
    """
    Create and return a Spark session with the given application name.
    
    Args:
        app_name (str): Name of the Spark application
        
    Returns:
        SparkSession: Configured Spark session
    """
    return (SparkSession.builder
            .appName(app_name)
            .config("spark.driver.memory", "2g")
            .config("spark.executor.memory", "4g")
            .getOrCreate())

def add_sales_metrics(df):
    """
    Add sales metrics to the DataFrame including total amount and order count.
    
    Args:
        df (DataFrame): Input DataFrame with sales data
        
    Returns:
        DataFrame: DataFrame with added metrics
    """
    # Calculate total amount for each order
    df_with_total = df.withColumn(
        "total_amount",
        col("quantity") * col("unit_price")
    )
    
    # Add order count per customer
    window_spec = Window.partitionBy("customer_id")
    df_with_metrics = df_with_total.withColumn(
        "customer_order_count",
        count("order_id").over(window_spec)
    )
    
    return df_with_metrics

def get_sales_summary(df):
    """
    Generate a summary of sales metrics grouped by region.
    
    Args:
        df (DataFrame): Input DataFrame with sales data and metrics
        
    Returns:
        DataFrame: Summary DataFrame with aggregated metrics
    """
    return (df.groupBy("region")
            .agg(
                count("order_id").alias("total_orders"),
                sum("total_amount").alias("total_sales"),
                avg("total_amount").alias("average_order_value"),
                count("customer_id").alias("unique_customers")
            )
            .withColumn("average_order_value", round(col("average_order_value"), 2))
            .orderBy(col("total_sales").desc()))

def plot_sales_by_region(df, title="Sales by Region"):
    """
    Create a bar plot of total sales by region.
    
    Args:
        df (DataFrame): DataFrame with sales data
        title (str): Plot title
        
    Returns:
        matplotlib.figure.Figure: The generated plot
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Get the data
    sales_data = df.groupBy("region").agg(sum("total_amount").alias("total_sales")).toPandas()
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    sns.barplot(data=sales_data, x="region", y="total_sales")
    plt.title(title)
    plt.xticks(rotation=45)
    plt.xlabel("Region")
    plt.ylabel("Total Sales")
    plt.tight_layout()
    
    return plt.gcf()

def plot_customer_order_distribution(df, title="Customer Order Distribution"):
    """
    Create a histogram of customer order counts.
    
    Args:
        df (DataFrame): DataFrame with sales data
        title (str): Plot title
        
    Returns:
        matplotlib.figure.Figure: The generated plot
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Get the data
    order_data = df.select("customer_order_count").toPandas()
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    sns.histplot(data=order_data, x="customer_order_count", bins=30)
    plt.title(title)
    plt.xlabel("Number of Orders per Customer")
    plt.ylabel("Count")
    plt.tight_layout()
    
    return plt.gcf()

def plot_sales_trend(df, date_column="order_date", title="Sales Trend Over Time"):
    """
    Create a line plot showing sales trend over time.
    
    Args:
        df (DataFrame): DataFrame with sales data
        date_column (str): Name of the date column
        title (str): Plot title
        
    Returns:
        matplotlib.figure.Figure: The generated plot
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Get the data
    trend_data = (df.groupBy(date_column)
                 .agg(sum("total_amount").alias("daily_sales"))
                 .orderBy(date_column)
                 .toPandas())
    
    # Create the plot
    plt.figure(figsize=(15, 6))
    sns.lineplot(data=trend_data, x=date_column, y="daily_sales")
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Daily Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return plt.gcf()

def plot_product_sales(df, top_n=10, title="Top Products by Sales"):
    """
    Create a horizontal bar plot of top products by sales.
    
    Args:
        df (DataFrame): DataFrame with sales data
        top_n (int): Number of top products to show
        title (str): Plot title
        
    Returns:
        matplotlib.figure.Figure: The generated plot
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Get the data
    product_data = (df.groupBy("product_name")
                   .agg(sum("total_amount").alias("product_sales"))
                   .orderBy(col("product_sales").desc())
                   .limit(top_n)
                   .toPandas())
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    sns.barplot(data=product_data, y="product_name", x="product_sales")
    plt.title(title)
    plt.xlabel("Total Sales")
    plt.ylabel("Product Name")
    plt.tight_layout()
    
    return plt.gcf()

def create_sales_dashboard(df):
    """
    Create a comprehensive sales dashboard with multiple visualizations.
    
    Args:
        df (DataFrame): DataFrame with sales data
        
    Returns:
        matplotlib.figure.Figure: The dashboard figure
    """
    import matplotlib.pyplot as plt
    
    # Create a 2x2 grid of plots
    fig = plt.figure(figsize=(20, 16))
    
    # Plot 1: Sales by Region
    plt.subplot(2, 2, 1)
    plot_sales_by_region(df)
    
    # Plot 2: Customer Order Distribution
    plt.subplot(2, 2, 2)
    plot_customer_order_distribution(df)
    
    # Plot 3: Sales Trend
    plt.subplot(2, 2, 3)
    plot_sales_trend(df)
    
    # Plot 4: Top Products
    plt.subplot(2, 2, 4)
    plot_product_sales(df)
    
    plt.tight_layout()
    return fig 