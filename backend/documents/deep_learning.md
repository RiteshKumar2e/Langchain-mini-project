# Deep Learning

## What is Deep Learning?

Deep Learning is a subfield of machine learning that uses artificial neural networks with multiple layers (hence "deep") to learn hierarchical representations of data. It has revolutionized fields like computer vision, natural language processing, and speech recognition.

Deep learning is inspired by the structure and function of the human brain, particularly the way neurons interconnect and communicate.

## Neural Network Fundamentals

### Artificial Neurons (Perceptrons)

The basic building block of neural networks:
- Takes weighted inputs
- Applies an activation function
- Produces an output

### Layers

- **Input Layer**: Receives raw data
- **Hidden Layers**: Learn intermediate representations
- **Output Layer**: Produces final predictions

### Activation Functions

- **ReLU (Rectified Linear Unit)**: max(0, x) - most common
- **Sigmoid**: Maps output between 0 and 1 (used for binary classification)
- **Tanh**: Maps output between -1 and 1
- **Softmax**: Maps output to probability distribution (used for multi-class classification)

### Backpropagation

The algorithm used to train neural networks:
1. Forward pass: compute predictions
2. Calculate loss
3. Backward pass: compute gradients
4. Update weights using gradient descent

## Types of Neural Networks

### Convolutional Neural Networks (CNNs)

Specialized for processing grid-like data (images):
- **Convolutional layers**: Apply filters to detect features
- **Pooling layers**: Reduce spatial dimensions
- **Fully connected layers**: Make final predictions

**Applications:** Image classification, object detection, medical imaging

### Recurrent Neural Networks (RNNs)

Designed for sequential data:
- Maintain hidden state across time steps
- Suffer from vanishing gradient problem

**Variants:**
- **LSTM (Long Short-Term Memory)**: Solves vanishing gradient using gates
- **GRU (Gated Recurrent Unit)**: Simplified version of LSTM

**Applications:** Text generation, machine translation, time series forecasting

### Transformers

State-of-the-art architecture for NLP and beyond:

- **Self-Attention Mechanism**: Allows every token to attend to every other token
- **Multi-Head Attention**: Multiple attention heads capture different relationships
- **Positional Encoding**: Injects position information into embeddings
- **Encoder-Decoder Architecture**: Used in translation tasks

**Key Models:**
- **BERT**: Bidirectional encoder for understanding tasks
- **GPT**: Decoder-only model for generation tasks
- **T5**: Encoder-decoder for text-to-text tasks
- **ViT**: Vision Transformer for image tasks

### Generative Models

- **GANs (Generative Adversarial Networks)**: Generator vs. Discriminator
- **VAEs (Variational Autoencoders)**: Learn latent space representations
- **Diffusion Models**: State-of-the-art image generation (Stable Diffusion, DALL-E)

## Training Deep Learning Models

### Loss Functions

- **Cross-Entropy Loss**: Classification tasks
- **Mean Squared Error (MSE)**: Regression tasks
- **Binary Cross-Entropy**: Binary classification

### Optimizers

- **SGD (Stochastic Gradient Descent)**: Basic optimizer
- **Adam**: Adaptive learning rate optimizer (most popular)
- **AdaGrad**: Adapts learning rate per parameter
- **RMSprop**: Running average of squared gradients

### Regularization Techniques

- **Dropout**: Randomly deactivate neurons during training
- **Batch Normalization**: Normalize layer inputs
- **L1/L2 Regularization**: Add penalty for large weights
- **Data Augmentation**: Artificially increase training data

### Hyperparameters

- Learning rate
- Batch size
- Number of layers and neurons
- Dropout rate
- Number of epochs

## Deep Learning Frameworks

- **TensorFlow/Keras**: Google's framework, great for production
- **PyTorch**: Facebook's framework, popular in research
- **JAX**: Google's high-performance numerical computing
- **MXNet**: Apache's scalable deep learning framework
