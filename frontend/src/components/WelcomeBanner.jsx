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
                    <svg width="38" height="38" viewBox="0 0 36 36" fill="none">
                        <circle cx="18" cy="18" r="5" fill="white" opacity="0.95" />
                        <path d="M18 7v5M18 24v5M7 18h5M24 18h5" stroke="white" strokeWidth="2.2" strokeLinecap="round" />
                        <path d="M10.5 10.5l3.5 3.5M22 22l3.5 3.5M10.5 25.5l3.5-3.5M22 14l3.5-3.5"
                            stroke="white" strokeWidth="1.6" strokeLinecap="round" opacity="0.65" />
                    </svg>
                </div>

                <div className={styles.headingGroup}>
                    <span className={styles.eyebrow}>AI-Powered Knowledge Base</span>
                    <h1 className={styles.title}>RAG Knowledge Assistant</h1>
                    <p className={styles.subtitle}>
                        Ask questions and get grounded answers from a curated knowledge base.
                        Every response cites its sources so you can verify and explore further.
                    </p>
                </div>

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
