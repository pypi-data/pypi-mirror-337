import numpy as np
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

class SMK:
    def __init__(self, n_clusters=2, kernel='rbf', C=1.0, gamma='scale'):
        self.n_clusters = n_clusters
        self.kernel = kernel
        self.C = C
        self.gamma = gamma
        self.kmeans = KMeans(n_clusters=self.n_clusters, n_init=10, random_state=42)
        self.svm = SVC(kernel=self.kernel, C=self.C, gamma=self.gamma, probability=True, random_state=42)
        self.scaler = StandardScaler()
        self.mode = None  # 'classification' or 'clustering'
    
    def fit(self, X, y=None):
        X_scaled = self.scaler.fit_transform(X)
        
        if y is None:
            self.mode = 'clustering'
            self.kmeans.fit(X_scaled)
        else:
            self.mode = 'classification'
            self.svm.fit(X_scaled, y)
        
    def predict(self, X):
        X_scaled = self.scaler.transform(X)
        
        if self.mode == 'classification':
            return self.svm.predict(X_scaled)
        elif self.mode == 'clustering':
            return self.kmeans.predict(X_scaled)
        else:
            raise ValueError("Model has not been trained yet.")
    
    def predict_proba(self, X):
        X_scaled = self.scaler.transform(X)
        if self.mode == 'classification':
            return self.svm.predict_proba(X_scaled)
        else:
            raise ValueError("Probability prediction is only available for classification mode.")
    
    def evaluate(self, X, y):
        predictions = self.predict(X)
        return accuracy_score(y, predictions)

# Example Usage
if __name__ == "__main__":
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split
    
    data = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)
    
    model = SMK(n_clusters=3)
    model.fit(X_train, y_train)
    accuracy = model.evaluate(X_test, y_test)
    print(f"SMK Accuracy: {accuracy * 100:.2f}%")
