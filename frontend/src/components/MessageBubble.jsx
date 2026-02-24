/**
 * MessageBubble.jsx
 * ─────────────────
 * Renders one conversation turn — user question or assistant answer.
 * Assistant bubbles render Markdown + collapsible source citations.
 */

import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import styles from './MessageBubble.module.css'

/* ── User bubble ─────────────────────────────────────────────────────────── */
function UserBubble({ content }) {
    return (
        <div className={`${styles.row} ${styles.userRow}`}>
            <div className={`${styles.bubble} ${styles.userBubble}`}>
                <p className={styles.userText}>{content}</p>
            </div>
            <div className={`${styles.avatar} ${styles.userAvatar}`}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z" />
                </svg>
            </div>
        </div>
    )
}

/* ── Source card ─────────────────────────────────────────────────────────── */
function SourceCard({ source, index }) {
    const ext = source.filename.split('.').pop()?.toUpperCase() || 'FILE'

    return (
        <div className={styles.sourceCard}>
            <div className={styles.sourceCardHeader}>
                <span className={styles.sourceNum}>{index + 1}</span>
                <div className={styles.sourceInfo}>
                    <code className={styles.sourceFilename}>{source.filename}</code>
                    <span className={styles.sourceExt}>{ext}</span>
                </div>
            </div>
            <p className={styles.sourceSnippet}>{source.snippet}</p>
        </div>
    )
}

/* ── Assistant bubble ─────────────────────────────────────────────────────── */
function AssistantBubble({ content, sources, isError }) {
    const [showSources, setShowSources] = useState(false)
    const hasSources = sources?.length > 0

    return (
        <div className={`${styles.row} ${styles.assistantRow}`}>
            <div className={`${styles.avatar} ${styles.assistantAvatar}`}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
                    <circle cx="12" cy="12" r="9" />
                    <path d="M8 12h.01M12 12h.01M16 12h.01" />
                </svg>
            </div>

            <div className={`${styles.bubble} ${styles.assistantBubble} ${isError ? styles.errorBubble : ''}`}>
                {isError ? (
                    <div className={styles.errorContent}>
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" className={styles.errorIcon}>
                            <path d="M12 2a10 10 0 1 0 0 20A10 10 0 0 0 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z" />
                        </svg>
                        <div className="markdown-body">
                            <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
                        </div>
                    </div>
                ) : (
                    <div className="markdown-body">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
                    </div>
                )}

                {hasSources && (
                    <div className={styles.sourcesSection}>
                        <div className={styles.sourcesDivider} />
                        <button
                            className={styles.sourcesToggle}
                            onClick={() => setShowSources(v => !v)}
                        >
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
                                <polyline points="14 2 14 8 20 8" stroke="currentColor" fill="none" strokeWidth="2" />
                            </svg>
                            {sources.length} source{sources.length !== 1 ? 's' : ''} used
                            <svg
                                width="11" height="11" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" strokeWidth="2.5"
                                style={{ transform: showSources ? 'rotate(180deg)' : '', transition: 'transform 0.2s' }}
                            >
                                <polyline points="6 9 12 15 18 9" />
                            </svg>
                        </button>

                        {showSources && (
                            <div className={`${styles.sourcesGrid} fade-in`}>
                                {sources.map((s, i) => (
                                    <SourceCard key={i} source={s} index={i} />
                                ))}
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    )
}

/* ── Export ──────────────────────────────────────────────────────────────── */
export default function MessageBubble({ message }) {
    if (message.role === 'user') return <UserBubble content={message.content} />
    return (
        <AssistantBubble
            content={message.content}
            sources={message.sources}
            isError={message.isError}
        />
    )
}
