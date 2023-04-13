from sklearn.cluster import KMeans

def classify_sleep_states(features):
    # Cluster the feature vectors using K-means
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(features)
    labels = kmeans.labels_
    return labels
