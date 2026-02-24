/**
 * WelcomeBanner.jsx
 * ─────────────────
 * Shown when no messages exist. Displays branding, capability pills,
 * and clickable suggestion prompts.
 */

import styles from './WelcomeBanner.module.css'

const SUGGESTIONS = [
    { icon: '🧠', text: 'What is Retrieval-Augmented Generation?' },
    { icon: '🔗', text: 'How does LangChain work?' },
    { icon: '⚡', text: 'Explain the Transformer attention mechanism' },
    { icon: '🌳', text: 'What are the types of machine learning?' },
    { icon: '🗄️', text: 'Compare FAISS with Pinecone and Chroma' },
    { icon: '🐍', text: 'What are key features of Python?' },
]

const CAPABILITIES = [
    { label: 'LangChain RAG', color: 'blue' },
    { label: 'FAISS Vector DB', color: 'purple' },
    { label: 'Groq LLM', color: 'green' },
    { label: 'Source Citations', color: 'orange' },
    { label: 'Follow-up Questions', color: 'teal' },
]

export default function WelcomeBanner({ onSuggestion }) {
    return (
        <div className={styles.wrapper}>
            {/* ── Hero ── */}
            <div className={styles.hero}>
                <div className={styles.logoWrap}>
                    <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
                        <rect width="36" height="36" rx="10" fill="var(--color-primary)" />
                        <circle cx="18" cy="18" r="4" fill="white" opacity="0.9" />
                        <path d="M18 9v4M18 23v4M9 18h4M23 18h4" stroke="white" strokeWidth="2" strokeLinecap="round" />
                        <path d="M11.5 11.5l2.8 2.8M21.7 21.7l2.8 2.8M11.5 24.5l2.8-2.8M21.7 14.3l2.8-2.8"
                            stroke="white" strokeWidth="1.5" strokeLinecap="round" opacity="0.6" />
                    </svg>
                </div>
                <h1 className={styles.title}>RAG Knowledge Assistant</h1>
                <p className={styles.subtitle}>
                    Ask questions and get grounded answers from a curated knowledge base.
                    Every response cites its sources so you can verify and explore further.
                </p>

                <div className={styles.capabilities}>
                    {CAPABILITIES.map(c => (
                        <span key={c.label} className={`${styles.pill} ${styles[`pill_${c.color}`]}`}>
                            {c.label}
                        </span>
                    ))}
                </div>
            </div>

            {/* ── Suggestions ── */}
            <div className={styles.suggestSection}>
                <p className={styles.suggestLabel}>
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2a10 10 0 1 0 0 20A10 10 0 0 0 12 2zm1 14.5h-2v-6h2v6zm0-8h-2V6h2v2.5z" />
                    </svg>
                    Try one of these prompts
                </p>
                <div className={styles.grid}>
                    {SUGGESTIONS.map((s) => (
                        <button
                            key={s.text}
                            className={styles.suggestionCard}
                            onClick={() => onSuggestion(s.text)}
                        >
                            <span className={styles.cardIcon}>{s.icon}</span>
                            <span className={styles.cardText}>{s.text}</span>
                            <svg className={styles.cardArrow} width="14" height="14" viewBox="0 0 24 24"
                                fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                                <path d="M5 12h14M12 5l7 7-7 7" />
                            </svg>
                        </button>
                    ))}
                </div>
            </div>
        </div>
    )
}
