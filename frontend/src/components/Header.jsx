/**
 * Header.jsx
 * ──────────
 * Sticky top nav — branding, backend health indicator, action buttons.
 */

import { useEffect, useState } from 'react'
import { getHealth } from '../api'
import styles from './Header.module.css'

function StatusDot({ ready }) {
    return (
        <span className={`${styles.statusDot} ${ready ? styles.ready : styles.notReady}`} />
    )
}

export default function Header({ onHistoryOpen, onClearChat }) {
    const [health, setHealth] = useState(null)

    useEffect(() => {
        getHealth()
            .then(setHealth)
            .catch(() => setHealth({ status: 'error', vector_store_ready: false }))
    }, [])

    const isReady = health?.vector_store_ready === true
    const model = health?.llm_model ?? '…'

    return (
        <header className={styles.header}>
            <div className={styles.inner}>

                {/* ── Brand ── */}
                <div className={styles.brand}>
                    <div className={styles.logoBox}>
                        <svg width="20" height="20" viewBox="0 0 36 36" fill="none">
                            <rect width="36" height="36" rx="10" fill="var(--color-primary)" />
                            <circle cx="18" cy="18" r="4" fill="white" opacity="0.95" />
                            <path d="M18 9v4M18 23v4M9 18h4M23 18h4" stroke="white" strokeWidth="2.2" strokeLinecap="round" />
                        </svg>
                    </div>
                    <div className={styles.brandText}>
                        <span className={styles.brandName}>RAG Assistant</span>
                        <span className={styles.brandSub}>
                            LangChain · FAISS · Groq
                        </span>
                    </div>
                </div>

                {/* ── Right actions ── */}
                <div className={styles.right}>
                    {/* Health pill */}
                    <div className={`${styles.healthPill} ${isReady ? styles.pillReady : styles.pillWaiting}`}>
                        <StatusDot ready={isReady} />
                        <span>{isReady ? `${model}` : (health ? 'Index missing' : 'Connecting…')}</span>
                    </div>

                    {/* History button */}
                    <button
                        id="history-btn"
                        className={`btn btn-ghost ${styles.iconBtn}`}
                        onClick={onHistoryOpen}
                        title="View history"
                    >
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <circle cx="12" cy="12" r="9" />
                            <polyline points="12 6 12 12 16 14" />
                        </svg>
                        <span className={styles.btnLabel}>History</span>
                    </button>

                    {/* Clear button */}
                    {onClearChat && (
                        <button
                            className={`btn btn-ghost ${styles.iconBtn}`}
                            onClick={onClearChat}
                            title="Clear conversation"
                        >
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                                <polyline points="3 6 5 6 21 6" />
                                <path d="M19 6l-1 14H6L5 6" />
                                <path d="M10 11v6M14 11v6" />
                            </svg>
                            <span className={styles.btnLabel}>Clear</span>
                        </button>
                    )}
                </div>
            </div>
        </header>
    )
}
