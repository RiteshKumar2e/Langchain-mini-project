/**
 * MessageBubble.jsx
 * ─────────────────
 * Renders a single conversation turn — user question or assistant answer.
 * Assistant messages render Markdown and include collapsible source citations.
 */

import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import styles from './MessageBubble.module.css'

function UserBubble({ content }) {
    return (
        <div className={`${styles.row} ${styles.userRow}`}>
            <div className={`${styles.bubble} ${styles.userBubble}`}>
                <p className={styles.userText}>{content}</p>
            </div>
            <div className={`${styles.avatar} ${styles.userAvatar}`}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 12c2.7 0 4.8-2.1 4.8-4.8S14.7 2.4 12 2.4 7.2 4.5 7.2 7.2 9.3 12 12 12zm0 2.4c-3.2 0-9.6 1.6-9.6 4.8v2.4h19.2v-2.4c0-3.2-6.4-4.8-9.6-4.8z" />
                </svg>
            </div>
        </div>
    )
}

function SourceCard({ source, index }) {
    return (
        <div className={styles.sourceCard}>
            <div className={styles.sourceHeader}>
                <span className={`badge badge-primary ${styles.sourceBadge}`}>
                    <svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
                        <polyline points="14 2 14 8 20 8" stroke="currentColor" fill="none" strokeWidth="2" />
                    </svg>
                    {index + 1}
                </span>
                <code className={styles.sourceFile}>{source.filename}</code>
            </div>
            <p className={styles.sourceSnippet}>{source.snippet}</p>
        </div>
    )
}

function AssistantBubble({ content, sources, isError }) {
    const [showSources, setShowSources] = useState(false)
    const hasSources = sources && sources.length > 0

    return (
        <div className={`${styles.row} ${styles.assistantRow}`}>
            <div className={`${styles.avatar} ${styles.assistantAvatar}`}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="9" />
                    <path d="M9 9h.01M15 9h.01M9.5 14.5s1 1.5 2.5 1.5 2.5-1.5 2.5-1.5" />
                </svg>
            </div>

            <div className={`${styles.bubble} ${styles.assistantBubble} ${isError ? styles.errorBubble : ''}`}>
                <div className="markdown-body">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
                </div>

                {hasSources && (
                    <div className={styles.sourcesSection}>
                        <button
                            className={styles.sourcesToggle}
                            onClick={() => setShowSources(v => !v)}
                        >
                            <svg
                                width="13" height="13" viewBox="0 0 24 24" fill="currentColor"
                                style={{ transform: showSources ? 'rotate(90deg)' : 'none', transition: 'transform 0.2s' }}
                            >
                                <path d="M9 18l6-6-6-6" />
                            </svg>
                            {sources.length} source{sources.length > 1 ? 's' : ''}
                            {showSources ? ' ▴' : ' ▾'}
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
