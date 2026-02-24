/**
 * App.jsx
 * ───────
 * Root component that stitches together:
 *   • Header with health indicator
 *   • Scrollable chat message area
 *   • Typing / loading indicator
 *   • Chat input with suggestion chips (first load only)
 *   • Slide-in history panel
 */

import { useEffect, useRef, useState } from 'react'
import Header from './components/Header'
import MessageBubble from './components/MessageBubble'
import ChatInput from './components/ChatInput'
import HistoryPanel from './components/HistoryPanel'
import { useChat } from './hooks/useChat'
import styles from './App.module.css'

function TypingIndicator() {
    return (
        <div className={styles.typingRow}>
            <div className={styles.typingAvatar}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="9" />
                    <path d="M9 9h.01M15 9h.01M9.5 14.5s1 1.5 2.5 1.5 2.5-1.5 2.5-1.5" />
                </svg>
            </div>
            <div className={styles.typingBubble}>
                <span className={styles.dot} />
                <span className={styles.dot} />
                <span className={styles.dot} />
            </div>
        </div>
    )
}

function EmptyState() {
    return (
        <div className={styles.empty}>
            <div className={styles.emptyIcon}>
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
                    <circle cx="12" cy="12" r="10" stroke="var(--color-primary)" strokeWidth="1.5" />
                    <path d="M8 12h8M12 8v8" stroke="var(--color-primary)" strokeWidth="1.5" strokeLinecap="round" />
                </svg>
            </div>
            <h2 className={styles.emptyTitle}>Ask your knowledge base</h2>
            <p className={styles.emptyText}>
                This assistant uses Retrieval-Augmented Generation (RAG) to answer questions
                from a curated set of documents. Every answer is grounded with source citations.
            </p>
            <div className={styles.emptyPills}>
                {['LangChain', 'FAISS', 'FastAPI', 'React'].map(t => (
                    <span key={t} className="badge badge-primary">{t}</span>
                ))}
            </div>
        </div>
    )
}

export default function App() {
    const { messages, loading, sendMessage, clearChat } = useChat()
    const [historyOpen, setHistoryOpen] = useState(false)
    const bottomRef = useRef(null)

    // Auto-scroll to the latest message
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages, loading])

    const showSuggestions = messages.length === 0

    return (
        <div className={styles.layout}>
            <Header onClearChat={messages.length > 0 ? clearChat : undefined} />

            <div className={styles.toolbar}>
                <button
                    id="history-btn"
                    className="btn btn-ghost"
                    onClick={() => setHistoryOpen(true)}
                >
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <circle cx="12" cy="12" r="9" />
                        <polyline points="12 6 12 12 16 14" />
                    </svg>
                    History
                </button>

                <span className={styles.docsCount}>
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
                    </svg>
                    10+ knowledge documents
                </span>
            </div>

            {/* ── Messages ── */}
            <main className={styles.main} id="chat-area">
                <div className={styles.feed}>
                    {messages.length === 0 && <EmptyState />}

                    {messages.map((msg, i) => (
                        <MessageBubble key={i} message={msg} />
                    ))}

                    {loading && <TypingIndicator />}
                    <div ref={bottomRef} />
                </div>
            </main>

            {/* ── Input ── */}
            <ChatInput
                onSend={sendMessage}
                loading={loading}
                showSuggestions={showSuggestions}
            />

            {/* ── History panel ── */}
            <HistoryPanel
                isOpen={historyOpen}
                onClose={() => setHistoryOpen(false)}
            />
        </div>
    )
}
