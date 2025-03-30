# aimlab/programs.py

class ProgramLibrary:
    def __init__(self):
        self.programs = {}

    def add_program(self, x, function):
       
        self.programs[x] = function

    def fetch_and_run(self, x):
      
        if x in self.programs:
            print(f"Running program {x}...")
            self.programs[x]()
        else:
            print(f"Program {x} not found.")


# Example programs
def program_5():
    print(
      
      "import numpy as np"
"from sklearn.datasets import load_iris"
"from sklearn.model_selection import train_test_split"
"from sklearn.preprocessing import StandardScaler"
"from collections import Counter"
"import math"

"# Euclidean distance function"
"def euclidean_distance(x1, x2):"
"    return math.sqrt(sum((x - y) ** 2 for x, y in zip(x1, x2)))"

"# k-Nearest Neighbors Classifier"
"class KNNClassifier:"
"    def __init__(self, k=3):"
"        self.k = k"

"    def fit(self, X_train, y_train):"
"        self.X_train = X_train"
"        self.y_train = y_train"

"    def predict(self, X_test):"
"        predictions = []"
"        for x_test in X_test:"
"            distances = [euclidean_distance(x_test, x_train) for x_train in self.X_train]"
"            k_indices = np.argsort(distances)[:self.k]"
"            k_nearest_labels = [self.y_train[i] for i in k_indices]"
"            most_common = Counter(k_nearest_labels).most_common(1)"
"            predictions.append(most_common[0][0])"

"        return np.array(predictions)"

"# Load Iris dataset"
"iris = load_iris()"
"X = iris.data"
"y = iris.target"

"# Split the data"
"X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)"

"# Standardize the features"
"scaler = StandardScaler()"
"X_train = scaler.fit_transform(X_train)"
"X_test = scaler.transform(X_test)"

"# Initialize KNN Classifier"
"knn = KNNClassifier(k=3)"

"# Train the model"
"knn.fit(X_train, y_train)"

"# Make predictions"
"y_pred = knn.predict(X_test)"

"# Evaluate and print results"
"correct = 0"
"incorrect = 0"

"for i in range(len(y_test)):"
"    if y_pred[i] == y_test[i]:"
"        correct += 1"
"        print(f'Correct: Predicted {iris.target_names[y_pred[i]]} for sample {i} (True label: {iris.target_names[y_test[i]]})')"
"    else:"
"        incorrect += 1"
"        print(f'Incorrect: Predicted {iris.target_names[y_pred[i]]} for sample {i} (True label: {iris.target_names[y_test[i]]})')"

"# Print the final summary"
"print('\\nResults Summary:')"
"print(f'Correct Predictions: {correct}')"
"print(f'Incorrect Predictions: {incorrect}')"
"print(f'Accuracy: {correct / len(y_test) * 100:.2f}%')"
              )
def program_8():
    print(

 "import numpy as np" 
"from sklearn.datasets import load_iris"
"from sklearn.model_selection import train_test_split"
"from sklearn.preprocessing import StandardScaler"
"from collections import Counter"
"import math"
"# Euclidean distance function"
"def euclidean_distance(x1, x2):"
"    return math.sqrt(sum((x - y) ** 2 for x, y in zip(x1, x2)))"

"# k-Nearest Neighbors Classifier"
"class KNNClassifier:"
"    def __init__(self, k=3):"
"        self.k = k  # Number of neighbors to use for classification"
"    "
"    def fit(self, X_train, y_train):"
"        self.X_train = X_train"
"        self.y_train = y_train"
"    "
"    def predict(self, X_test):"
"        predictions = []"
"        for x_test in X_test:"
"            # Calculate distances between the test point and all training points"
"            distances = [euclidean_distance(x_test, x_train) for x_train in self.X_train]"
"            # Get the indices of the k nearest neighbors"
"            k_indices = np.argsort(distances)[:self.k]"
"            # Get the labels of the k nearest neighbors"
"            k_nearest_labels = [self.y_train[i] for i in k_indices]"
"            # Predict the most common class among the k nearest neighbors"
"            most_common = Counter(k_nearest_labels).most_common(1)"
"            predictions.append(most_common[0][0])"
"        return np.array(predictions)"
"# Load Iris dataset"
"iris = load_iris()"
"X = iris.data  # Features"
"y = iris.target  # Target labels (species)"

"# Split the data into training and testing sets (80% train, 20% test)"
"X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)"

"# Standardize the features (important for distance-based algorithms like KNN)"
"scaler = StandardScaler()"
"X_train = scaler.fit_transform(X_train)"
"X_test = scaler.transform(X_test)"

"# Initialize the KNN Classifier with k=3"
"knn = KNNClassifier(k=3)"

"# Train the model"
"knn.fit(X_train, y_train)"

"# Make predictions"
"y_pred = knn.predict(X_test)"
"correct = 0"
"incorrect = 0"
"for i in range(len(y_test)):"
"    if y_pred[i] == y_test[i]:"
"        correct += 1"
"    else:"
"        incorrect += 1"

"# Print the final results"
"results_summary = "
"Results Summary:"
"Correct Predictions: {correct}"
"Incorrect Predictions: {incorrect}"
"Accuracy: {correct / len(y_test) * 100:.2f}%"





    )

def program_9():
    print(
      


      "import numpy as np"
"import matplotlib.pyplot as plt"

"# Function to perform Locally Weighted Linear Regression (LWLR)"
"def locally_weighted_linear_regression(X, y, tau=1.0):"
"    m = X.shape[0]"
"    y_pred = []"
"    for i in range(m):"
"        # Calculate the weights for the point xi"
"        weights = np.exp(-np.linalg.norm(X[i] - X, axis=1) ** 2 / (2 * tau ** 2))"
"        W = np.diag(weights) # Convert weights into a diagonal matrix"

"        # Perform weighted least squares (WLS) to compute the coefficients"
"        X_weighted = X.T @ W @ X # Weighted X"
"        y_weighted = X.T @ W @ y # Weighted y"

"        # Solve for the weights (beta coefficients)"
"        beta = np.linalg.pinv(X_weighted) @ y_weighted # Use pseudo-inverse for stability"

"        # Predict the value for the point"
"        y_pred.append(X[i] @ beta)"
"    return np.array(y_pred)"

"# Generate some synthetic data for demonstration (sine wave + noise)"
"np.random.seed(42)"
"X = np.linspace(0, 10, 100).reshape(-1, 1) # 100 data points between 0 and 10"
"y = np.sin(X).flatten() + np.random.normal(0, 0.1, X.shape[0]) # Sine wave with noise"

"# Add a bias term (column of ones) to the X data for linear regression"
"X_bias = np.c_[np.ones((X.shape[0], 1)), X]"

"# Perform Locally Weighted Linear Regression (LWLR)"
"tau = 0.5 # Smoothing parameter"
"y_pred = locally_weighted_linear_regression(X_bias, y, tau)"

"# Plot the results"
"plt.figure(figsize=(10, 6))"
"plt.scatter(X, y, color='blue', label='Data points')"
"plt.plot(X, y_pred, color='red', label='LWLR predictions', linewidth=2)"
"plt.title(f'Locally Weighted Linear Regression ( = {tau})')"
"plt.xlabel('X')"
"plt.ylabel('y')"
"plt.legend()"
"plt.show()"

    )


# Create an instance of ProgramLibrary
lib = ProgramLibrary()

# Add predefined programs
lib.add_program(5, program_5)
lib.add_program(8, program_8)
lib.add_program(9, program_9)


def getprogram(x):

    lib.fetch_and_run(x)


# with open("main.py", "w") as f:
#     f.write(programs_code)
