/**
 * HistoryPanel.jsx
 * ────────────────
 * Slide-in side panel showing recent Q&A history from the backend.
 * Supports clearing all history and deleting individual entries.
 */

import { useState, useEffect } from 'react'
import { getHistory, clearHistory, deleteHistoryEntry } from '../api'
import styles from './HistoryPanel.module.css'

function HistoryItem({ entry, index, absoluteIndex, onDelete }) {
    const [expanded, setExpanded] = useState(false)
    const [deleting, setDeleting] = useState(false)
    const date = new Date(entry.timestamp).toLocaleString()

    const handleDelete = async (e) => {
        e.stopPropagation()
        setDeleting(true)
        try {
            await onDelete(absoluteIndex)
        } finally {
            setDeleting(false)
        }
    }

    return (
        <div className={`${styles.item} ${entry.error ? styles.itemError : ''} ${deleting ? styles.itemDeleting : ''}`}>
            <button className={styles.itemHeader} onClick={() => setExpanded(v => !v)}>
                <div className={styles.itemMeta}>
                    <div className={styles.itemLeft}>
                        <span className={styles.itemIndex}>#{index + 1}</span>
                        <span className={styles.itemDate}>{date}</span>
                    </div>
                    <div className={styles.itemRight}>
                        <button
                            className={styles.deleteBtn}
                            onClick={handleDelete}
                            disabled={deleting}
                            title="Delete this entry"
                        >
                            {deleting
                                ? <span className={styles.deletingSpinner} />
                                : (
                                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
                                        <polyline points="3 6 5 6 21 6" />
                                        <path d="M19 6l-1 14H6L5 6" />
                                        <path d="M10 11v6M14 11v6" />
                                    </svg>
                                )
                            }
                        </button>
                        <svg
                            className={`${styles.chevron} ${expanded ? styles.chevronOpen : ''}`}
                            width="13" height="13" viewBox="0 0 24 24" fill="none"
                            stroke="currentColor" strokeWidth="2.5"
                        >
                            <polyline points="6 9 12 15 18 9" />
                        </svg>
                    </div>
                </div>
                <p className={styles.itemQuestion}>{entry.question}</p>
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

    const fetchEntries = async () => {
        setLoading(true)
        try {
            const data = await getHistory(20)
            setEntries([...(data.entries || [])].reverse())
        } catch { /* silent */ }
        finally { setLoading(false) }
    }

    useEffect(() => { if (isOpen) fetchEntries() }, [isOpen])

    const handleClear = async () => {
        if (!confirm('Clear all history?')) return
        setClearing(true)
        try { await clearHistory(); setEntries([]) }
        catch { /* silent */ }
        finally { setClearing(false) }
    }

    // absoluteIndex = position in the full JSONL file (not reversed)
    // entries is reversed, so entry at display-position i has absoluteIndex = (total - 1 - i)
    const handleDelete = async (absoluteIndex) => {
        try {
            await deleteHistoryEntry(absoluteIndex)
            // Remove from local state without refetch
            setEntries(prev => {
                const totalBefore = prev.length
                return prev.filter((_, i) => {
                    const absIdx = totalBefore - 1 - i
                    return absIdx !== absoluteIndex
                })
            })
        } catch {
            // silently ignore — could toast here
        }
    }

    return (
        <>
            {/* Overlay */}
            {isOpen && <div className={styles.overlay} onClick={onClose} />}

            {/* Panel */}
            <aside className={`${styles.panel} ${isOpen ? styles.open : ''}`}>
                <div className={styles.panelHeader}>
                    <div className={styles.panelTitleGroup}>
                        <div className={styles.panelTitleRow}>
                            <svg className={styles.panelIcon} width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <circle cx="12" cy="12" r="9" />
                                <polyline points="12 6 12 12 16 14" />
                            </svg>
                            <h2 className={styles.panelTitle}>History</h2>
                        </div>
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
                            <div className={styles.emptyIcon}>
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
                                    <path d="M12 20h9" /><path d="M16.5 3.5a2.121 2.121 0 013 3L7 19l-4 1 1-4L16.5 3.5z" />
                                </svg>
                            </div>
                            <div>
                                <p className={styles.emptyTitle}>No history yet</p>
                                <p className={styles.emptyHint}>Ask a question to get started.<br />Your conversations will appear here.</p>
                            </div>
                        </div>
                    ) : (
                        <div className={styles.list}>
                            {entries.map((e, i) => (
                                <HistoryItem
                                    key={`${e.timestamp}-${i}`}
                                    entry={e}
                                    index={entries.length - 1 - i}
                                    absoluteIndex={entries.length - 1 - i}
                                    onDelete={handleDelete}
                                />
                            ))}
                        </div>
                    )}
                </div>
            </aside>
        </>
    )
}
