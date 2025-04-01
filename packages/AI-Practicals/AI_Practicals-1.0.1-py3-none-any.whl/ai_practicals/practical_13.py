import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import silhouette_score

def Practical_13():
    print("\n" + "="*50)
    print("AI IN BUSINESS: CUSTOMER SEGMENTATION")
    print("="*50 + "\n")
    
    # Generate synthetic business data (customer spending habits)
    np.random.seed(42)
    n_customers = 100
    data = np.column_stack([
        np.random.normal(50, 15, n_customers),  # Annual spending ($1000s)
        np.random.normal(10, 4, n_customers)    # Website visits/month
    ])
    
    # Business context
    print("Business Problem:")
    print("Segment customers based on spending habits and engagement\n")
    
    # Determine optimal clusters using elbow method
    distortions = []
    silhouette_scores = []
    K_range = range(2, 6)
    
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(data)
        distortions.append(kmeans.inertia_)
        silhouette_scores.append(silhouette_score(data, kmeans.labels_))
    
    # Plot elbow curve
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(K_range, distortions, 'bx-')
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Distortion')
    plt.title('Elbow Method for Optimal k')
    
    plt.subplot(1, 2, 2)
    plt.plot(K_range, silhouette_scores, 'rx-')
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Silhouette Score')
    plt.title('Silhouette Analysis')
    
    plt.tight_layout()
    plt.show()
    
    # Final clustering with selected k
    optimal_k = 3
    kmeans = KMeans(n_clusters=optimal_k, random_state=42)
    kmeans.fit(data)
    
    # Create business-friendly cluster labels
    cluster_names = {
        0: "Low-Engagement Savers",
        1: "High-Spending Regulars",
        2: "Moderate Casual Shoppers"
    }
    
    # Visualize results
    plt.figure(figsize=(10, 6))
    colors = ['#FF5733', '#33FF57', '#3357FF']
    
    for i in range(optimal_k):
        cluster_data = data[kmeans.labels_ == i]
        plt.scatter(cluster_data[:, 0], cluster_data[:, 1], 
                   s=50, c=colors[i], 
                   label=cluster_names[i])
    
    plt.scatter(kmeans.cluster_centers_[:, 0], 
               kmeans.cluster_centers_[:, 1], 
               s=200, c='black', marker='X', 
               label='Cluster Centers')
    
    plt.title('Customer Segmentation Analysis')
    plt.xlabel('Annual Spending ($1000)')
    plt.ylabel('Monthly Website Visits')
    plt.legend()
    plt.grid(True)
    plt.show()
    
    # Business insights
    print("\nCluster Analysis Results:")
    cluster_stats = pd.DataFrame({
        'Segment': [cluster_names[i] for i in range(optimal_k)],
        'Avg Spending ($1000)': [np.round(data[kmeans.labels_ == i, 0].mean(), 1) for i in range(optimal_k)],
        'Avg Visits': [np.round(data[kmeans.labels_ == i, 1].mean(), 1) for i in range(optimal_k)],
        'Customer Count': [sum(kmeans.labels_ == i) for i in range(optimal_k)]
    })
    print(cluster_stats.to_string(index=False))
    
    print("\nRecommended Business Actions:")
    actions = [
        ("High-Spending Regulars", "Loyalty programs & premium offers"),
        ("Moderate Casual Shoppers", "Targeted promotions to increase frequency"),
        ("Low-Engagement Savers", "Re-engagement campaigns & value messaging")
    ]
    for segment, action in actions:
        print(f"- {segment:<25}: {action}")
    
    return {
        'model': kmeans,
        'cluster_stats': cluster_stats,
        'optimal_k': optimal_k
    }

# Call the function with:
# results = Practical_13()