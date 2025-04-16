
import numpy as np
import math
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from scipy.stats import kurtosis, skew

from generators.dft import dft
from generators.dct import dct
from generators.dst import dst
from generators.polynomial_regression import polynomial_regression

def extract_features(x, y):
    try:
        y_poly = polynomial_regression(x, y)
        poly_r2 = r2_score(y, y_poly)
        poly_mse = mean_squared_error(y, y_poly)
        rmse = np.sqrt(poly_mse)
    except:
        poly_r2 = 0
        poly_mse = float('inf')
        rmse = float('inf')

    diff = np.diff(y)
    skewness = skew(y)
    kurt = kurtosis(y)

    try:
        y_dft = dft(y)
        dft_mse = mean_squared_error(y, y_dft)
    except:
        dft_mse = float('inf')

    curvature = np.mean(np.diff(np.diff(y)))

    features = [
        np.mean(y),
        np.std(y),
        np.max(y),
        np.min(y),
        np.ptp(y),
        np.mean(diff),
        np.std(diff),
        poly_r2,
        poly_mse,
        rmse,
        skewness,
        kurt,
        dft_mse,
        curvature
    ]

    features = [0 if np.isnan(f) or np.isinf(f) else f for f in features]
    return features

def is_definitely_polynomial(x, y):
    try:
        y_poly = polynomial_regression(x, y)
        r2 = r2_score(y, y_poly)
        mse = mean_squared_error(y, y_poly)
        return r2 > 0.98 and mse < 1e-2
    except:
        return False

def label_best(x, y):
    if is_definitely_polynomial(x, y):
        return 'polynomial_regression'

    methods = [
        lambda x, y: dft(y),
        lambda x, y: dct(y),
        lambda x, y: dst(y),
        polynomial_regression
    ]
    names = ['dft', 'dct', 'dst', 'polynomial_regression']

    errors = []
    for method in methods:
        try:
            y_hat = method(x, y)
            mse = mean_squared_error(y, y_hat)
        except:
            mse = float('inf')
        errors.append(mse)

    return names[np.argmin(errors)]

# --- Generate training data ---

X_data, y_labels = [], []

# Add clean polynomial samples
for _ in range(100):
    x = np.linspace(0, 10, 100)
    coeffs = np.random.uniform(-3, 3, size=np.random.randint(2, 5))
    y = np.polyval(coeffs, x)
    features = extract_features(x, y)
    label = 'polynomial_regression'
    X_data.append(features)
    y_labels.append(label)

# Noisy/randomized samples
for _ in range(400):
    x = np.linspace(0, 2 * np.pi, 100)

    if np.random.rand() < 0.5:
        y = np.sin(np.random.randint(1, 4) * x) + 0.1 * np.random.randn(100)
    else:
        coeffs = np.random.uniform(-3, 3, size=np.random.randint(2, 5))
        y = np.polyval(coeffs, x - np.pi) + 0.1 * np.random.randn(100)

    features = extract_features(x, y)
    label = label_best(x, y)

    X_data.append(features)
    y_labels.append(label)

# --- Train Model training
clf = RandomForestClassifier()
X_train, X_test, y_train, y_test = train_test_split(X_data, y_labels, test_size=0.2, random_state=42)
clf.fit(X_train, y_train)



def predict_best_approximator(x, y):
    if is_definitely_polynomial(x, y):
        return 'polynomial_regression'
    features = extract_features(x, y)
    return clf.predict([features])[0]

# --- Test ---

if __name__ == "__main__":
    x = np.linspace(0, 10, 100)
    y = x - (x**3) / math.factorial(3) + (x**5) / math.factorial(5) - (x**7) / math.factorial(7) + (x**9) / math.factorial(9)
    print("Predicted:", predict_best_approximator(x, y))
