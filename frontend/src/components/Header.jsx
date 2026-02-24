/**
 * Header.jsx
 * ──────────
 * Top navigation bar with app branding and health status indicator.
 */

import { useEffect, useState } from 'react'
import { getHealth } from '../api'
import styles from './Header.module.css'

export default function Header({ onClearChat }) {
    const [health, setHealth] = useState(null)

    useEffect(() => {
        getHealth()
            .then(setHealth)
            .catch(() => setHealth({ status: 'error' }))
    }, [])

    const ready = health?.vector_store_ready
    const statusLabel = !health
        ? 'Checking…'
        : !health.vector_store_ready
            ? 'Index not built'
            : 'Ready'

    const statusColor = !health ? 'warning' : !health.vector_store_ready ? 'error' : 'success'

    return (
        <header className={styles.header}>
            <div className={styles.inner}>
                {/* Brand */}
                <div className={styles.brand}>
                    <div className={styles.logo}>
                        <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                            <rect width="28" height="28" rx="8" fill="var(--color-primary)" />
                            <path d="M7 14h5m9 0h-5m-4-4v8" stroke="#fff" strokeWidth="2" strokeLinecap="round" />
                            <circle cx="14" cy="14" r="2.5" fill="#fff" />
                        </svg>
                    </div>
                    <div>
                        <h1 className={styles.title}>RAG Knowledge Assistant</h1>
                        <p className={styles.subtitle}>Powered by LangChain · FAISS · Groq ({health?.llm_model ?? '…'})</p>
                    </div>
                </div>

                {/* Right side */}
                <div className={styles.right}>
                    <div className={`${styles.status} ${styles[statusColor]}`}>
                        <span className={`${styles.dot} ${styles[`dot_${statusColor}`]}`} />
                        {statusLabel}
                    </div>
                    {onClearChat && (
                        <button className="btn btn-ghost" onClick={onClearChat} title="Clear conversation">
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                                <polyline points="3 6 5 6 21 6" />
                                <path d="M19 6l-1 14H6L5 6" />
                                <path d="M10 11v6M14 11v6" />
                            </svg>
                            Clear chat
                        </button>
                    )}
                </div>
            </div>
        </header>
    )
}
