/**
 * HistoryPanel.jsx
 * ────────────────
 * Slide-in side panel showing recent Q&A history from the backend.
 * Supports clearing history and re-fetching.
 */

import { useState, useEffect } from 'react'
import { getHistory, clearHistory } from '../api'
import styles from './HistoryPanel.module.css'

function HistoryItem({ entry, index }) {
    const [expanded, setExpanded] = useState(false)
    const date = new Date(entry.timestamp).toLocaleString()

    return (
        <div className={`${styles.item} ${entry.error ? styles.itemError : ''}`}>
            <button className={styles.itemHeader} onClick={() => setExpanded(v => !v)}>
                <div className={styles.itemMeta}>
                    <span className={styles.itemIndex}>#{index + 1}</span>
                    <span className={styles.itemDate}>{date}</span>
                </div>
                <p className={styles.itemQuestion}>{entry.question}</p>
                <svg
                    width="13" height="13" viewBox="0 0 24 24" fill="none"
                    stroke="currentColor" strokeWidth="2.5"
                    style={{ transform: expanded ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s', flexShrink: 0 }}
                >
                    <polyline points="6 9 12 15 18 9" />
                </svg>
            </button>

            {expanded && (
                <div className={`${styles.itemBody} fade-in`}>
                    {entry.error ? (
                        <p className={styles.itemErrorText}>⚠ Error: {entry.error}</p>
                    ) : (
                        <p className={styles.itemAnswer}>{entry.answer?.slice(0, 400)}{entry.answer?.length > 400 ? '…' : ''}</p>
                    )}
                    {entry.sources?.length > 0 && (
                        <div className={styles.itemSources}>
                            {entry.sources.map((s, i) => (
                                <span key={i} className="badge badge-primary">{s.filename}</span>
                            ))}
                        </div>
                    )}
                </div>
            )}
        </div>
    )
}

export default function HistoryPanel({ isOpen, onClose }) {
    const [entries, setEntries] = useState([])
    const [loading, setLoading] = useState(false)
    const [clearing, setClearing] = useState(false)

    const fetch = async () => {
        setLoading(true)
        try {
            const data = await getHistory(20)
            setEntries([...(data.entries || [])].reverse())
        } catch { /* silent */ }
        finally { setLoading(false) }
    }

    useEffect(() => { if (isOpen) fetch() }, [isOpen])

    const handleClear = async () => {
        if (!confirm('Clear all history?')) return
        setClearing(true)
        try { await clearHistory(); setEntries([]) }
        catch { /* silent */ }
        finally { setClearing(false) }
    }

    return (
        <>
            {/* Overlay */}
            {isOpen && <div className={styles.overlay} onClick={onClose} />}

            {/* Panel */}
            <aside className={`${styles.panel} ${isOpen ? styles.open : ''}`}>
                <div className={styles.panelHeader}>
                    <div>
                        <h2 className={styles.panelTitle}>History</h2>
                        <p className={styles.panelSub}>{entries.length} recent interaction{entries.length !== 1 ? 's' : ''}</p>
                    </div>
                    <div className={styles.panelActions}>
                        {entries.length > 0 && (
                            <button className="btn btn-danger" onClick={handleClear} disabled={clearing}>
                                {clearing ? 'Clearing…' : 'Clear all'}
                            </button>
                        )}
                        <button className="btn btn-ghost" onClick={onClose} title="Close">
                            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                                <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
                            </svg>
                        </button>
                    </div>
                </div>

                <div className={styles.panelBody}>
                    {loading ? (
                        <div className={styles.center}>
                            <span className={styles.loader} />
                            <p>Loading history…</p>
                        </div>
                    ) : entries.length === 0 ? (
                        <div className={styles.empty}>
                            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="var(--color-border-strong)" strokeWidth="1.5">
                                <path d="M12 20h9" /><path d="M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z" />
                            </svg>
                            <p>No history yet. Ask a question to get started.</p>
                        </div>
                    ) : (
                        <div className={styles.list}>
                            {entries.map((e, i) => <HistoryItem key={i} entry={e} index={entries.length - 1 - i} />)}
                        </div>
                    )}
                </div>
            </aside>
        </>
    )
}
