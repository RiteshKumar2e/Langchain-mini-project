# Transformers and Attention Mechanism

## Introduction

The Transformer architecture, introduced in the seminal 2017 paper "Attention Is All You Need" by Vaswani et al., has revolutionized natural language processing and beyond. It replaced recurrent architectures with a purely attention-based mechanism, enabling massive parallelization and better capture of long-range dependencies.

## The Attention Mechanism

### Intuition

Attention allows a model to focus on the most relevant parts of the input when producing each part of the output. Think of it like how humans read — when understanding a word, we pay more attention to related words in context.

### Scaled Dot-Product Attention

The core attention formula:

```
Attention(Q, K, V) = softmax(QK^T / √d_k) * V
```

Where:
- **Q (Query)**: What we are looking for
- **K (Key)**: What we have to offer
- **V (Value)**: The actual content
- **d_k**: Dimension of the key vectors (scaling factor)

### Multi-Head Attention

Instead of a single attention function, multi-head attention runs attention multiple times in parallel:

```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) * W_O
where head_i = Attention(Q*W_Qi, K*W_Ki, V*W_Vi)
```

Each head can focus on different aspects of the input.

### Self-Attention

When Q, K, and V all come from the same sequence, it is called self-attention. This allows each token to attend to all other tokens in the same sequence to build contextual representations.

### Cross-Attention

In encoder-decoder models, the decoder uses cross-attention where:
- Q comes from the decoder
- K and V come from the encoder

## Transformer Architecture

### Encoder

The encoder processes the input sequence:

1. **Input Embeddings + Positional Encoding**
2. **N × Encoder Blocks**, each containing:
   - Multi-Head Self-Attention
   - Feed-Forward Network
   - Layer Normalization (applied with residual connections)

### Decoder

The decoder generates the output sequence:

1. **Output Embeddings + Positional Encoding**
2. **N × Decoder Blocks**, each containing:
   - Masked Multi-Head Self-Attention
   - Multi-Head Cross-Attention (attending to encoder output)
   - Feed-Forward Network
   - Layer Normalization

### Positional Encoding

Since transformers have no recurrence, positional information must be injected:
- **Sinusoidal Encoding**: Fixed based on position and dimension
- **Learned Positional Embeddings**: Trained alongside the model
- **Relative Position Encoding**: RoPE, ALiBi

### Feed-Forward Networks

Each transformer block contains a position-wise feed-forward network:
```
FFN(x) = max(0, x*W_1 + b_1)*W_2 + b_2
```

### Residual Connections and Layer Normalization

Each sub-layer has a residual connection:
```
output = LayerNorm(x + Sublayer(x))
```

## Key Transformer Variants

### Encoder-Only (BERT-style)
- Good for understanding tasks
- Uses bidirectional attention
- Used for classification, NER, QA

### Decoder-Only (GPT-style)
- Good for generation tasks
- Uses causal (left-to-right) attention
- Used for text generation, chat

### Encoder-Decoder (T5/BART style)
- Good for seq-to-seq tasks
- Translation, summarization

## Pre-training and Fine-tuning

### Pre-training Objectives

- **Masked Language Modeling (MLM)**: BERT masks 15% of tokens and predicts them
- **Causal Language Modeling (CLM)**: GPT predicts the next token autoregressively
- **Span Corruption**: T5 replaces spans of text and reconstructs them

### Fine-tuning

After pre-training, models are fine-tuned on specific tasks:
- Add a task-specific head
- Train on labeled data
- Often only a few epochs needed

### Parameter-Efficient Fine-Tuning (PEFT)

- **LoRA**: Low-Rank Adaptation — only trains small rank-decomposition matrices
- **Prompt Tuning**: Learns soft prompts while keeping model frozen
- **Adapter Layers**: Adds small bottleneck layers

## Scaling Laws

Research has shown that model performance scales predictably with:
- Number of parameters
- Amount of training data
- Compute budget

This has motivated the development of increasingly large models from GPT-2 (1.5B) to GPT-4 (estimated ~1.8T parameters).
