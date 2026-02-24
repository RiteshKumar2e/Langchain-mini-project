# Machine Learning Basics

## What is Machine Learning?

Machine Learning (ML) is a subset of artificial intelligence (AI) that provides systems the ability to automatically learn and improve from experience without being explicitly programmed. Machine learning focuses on the development of computer programs that can access data and use it to learn for themselves.

## Types of Machine Learning

### 1. Supervised Learning

In supervised learning, the algorithm is trained on labeled data. The model learns the mapping between inputs and outputs.

**Common algorithms:**
- Linear Regression
- Logistic Regression
- Decision Trees
- Random Forest
- Support Vector Machines (SVM)
- Neural Networks

**Applications:**
- Email spam detection
- Image classification
- Price prediction
- Medical diagnosis

### 2. Unsupervised Learning

In unsupervised learning, the algorithm is trained on unlabeled data and must find structure on its own.

**Common algorithms:**
- K-Means Clustering
- Hierarchical Clustering
- Principal Component Analysis (PCA)
- Autoencoders

**Applications:**
- Customer segmentation
- Anomaly detection
- Topic modeling
- Dimensionality reduction

### 3. Reinforcement Learning

In reinforcement learning, an agent learns by interacting with its environment and receiving rewards or punishments.

**Key concepts:**
- Agent
- Environment
- State
- Action
- Reward

**Applications:**
- Game playing (Chess, Go)
- Robotics
- Autonomous vehicles
- Resource management

## Key Machine Learning Concepts

### Training and Testing

- **Training Set**: Data used to train the model
- **Validation Set**: Data used to tune hyperparameters
- **Test Set**: Data used to evaluate final model performance

### Overfitting and Underfitting

- **Overfitting**: Model performs well on training data but poorly on new data (too complex)
- **Underfitting**: Model performs poorly on both training and test data (too simple)
- **Bias-Variance Tradeoff**: Balancing model complexity to achieve good generalization

### Model Evaluation Metrics

- **Accuracy**: Percentage of correct predictions
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)
- **F1-Score**: Harmonic mean of precision and recall
- **RMSE**: Root Mean Square Error for regression tasks

### Feature Engineering

Feature engineering is the process of using domain knowledge to extract features from raw data:
- Feature selection
- Feature scaling (normalization, standardization)
- Feature creation
- Handling missing values
- Encoding categorical variables

## Popular Machine Learning Frameworks

- **Scikit-learn**: General purpose ML library for Python
- **TensorFlow**: Deep learning framework by Google
- **PyTorch**: Deep learning framework by Facebook
- **Keras**: High-level neural network API
- **XGBoost**: Gradient boosting library
