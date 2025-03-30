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
"import matplotlib.pyplot as plt"

"def sigmoid(x):"
"    return 1 / (1 + np.exp(-x))"

"def sigmoid_derivative(x):"
"    return x * (1 - x)"

"def mean_squared_error(y_true, y_pred):"
"    return np.mean((y_true - y_pred) ** 2)"

"def mean_squared_error_derivative(y_true, y_pred):"
"    return 2 * (y_pred - y_true) / len(y_true)"
"class NeuralNetwork:"
"    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.1):"
"        self.input_size = input_size"
"        self.hidden_size = hidden_size"
"        self.output_size = output_size"
"        self.learning_rate = learning_rate"
"        self.W1 = np.random.randn(self.input_size, self.hidden_size)"
"        self.b1 = np.zeros((1, self.hidden_size))"
"        self.W2 = np.random.randn(self.hidden_size, self.output_size)"
"        self.b2 = np.zeros((1, self.output_size))"

"    def forward(self, X):"
"        self.z1 = np.dot(X, self.W1) + self.b1"
"        self.a1 = sigmoid(self.z1)"
"        self.z2 = np.dot(self.a1, self.W2) + self.b2"
"        self.a2 = sigmoid(self.z2)"
"        return self.a2"

"    def backward(self, X, y, y_pred):"
"        output_error = mean_squared_error_derivative(y, y_pred)"
"        d_z2 = output_error * sigmoid_derivative(self.a2)"
"        d_W2 = np.dot(self.a1.T, d_z2)"
"        d_b2 = np.sum(d_z2, axis=0, keepdims=True)"
"        d_a1 = np.dot(d_z2, self.W2.T)"
"        d_z1 = d_a1 * sigmoid_derivative(self.a1)"
"        d_W1 = np.dot(X.T, d_z1)"
"        d_b1 = np.sum(d_z1, axis=0, keepdims=True)"
"        self.W1 -= self.learning_rate * d_W1"
"        self.b1 -= self.learning_rate * d_b1"
"        self.W2 -= self.learning_rate * d_W2"
"        self.b2 -= self.learning_rate * d_b2"

"    def train(self, X, y, epochs=10000):"
"        for epoch in range(epochs):"
"            y_pred = self.forward(X)"
"            self.backward(X, y, y_pred)"
"            if epoch % 1000 == 0:"
"                loss = mean_squared_error(y, y_pred)"
"                f'Epoch {epoch}, Loss: {loss:.5f}'"
"    def predict(self, X):"
"        return self.forward(X)"

"X = np.array([[0, 0],"
"              [0, 1],"
"              [1, 0],"
"              [1, 1]])"

"y = np.array([[0],"
"              [1],"
"              [1],"
"              [0]])"

"nn = NeuralNetwork(input_size=2, hidden_size=2, output_size=1, learning_rate=0.1)"
"nn.train(X, y, epochs=10000)"
"predictions = nn.predict(X)"
"plt.plot(predictions, label='Predictions', marker='o')"
"plt.plot(y, label='Actual', linestyle='dashed', marker='s')"
"plt.legend()"
"plt.title('Neural Network XOR Predictions vs Actual')"
"plt.show()"

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
