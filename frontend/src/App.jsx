/**
 * App.jsx
 * ───────
 * Root component — stitches Header, chat feed, input, history panel together.
 */

import { useEffect, useRef, useState } from 'react'
import Header from './components/Header'
import MessageBubble from './components/MessageBubble'
import ChatInput from './components/ChatInput'
import HistoryPanel from './components/HistoryPanel'
import WelcomeBanner from './components/WelcomeBanner'
import { useChat } from './hooks/useChat'
import styles from './App.module.css'

/* ── Typing dots ─────────────────────────────────────────────────────────── */
function TypingIndicator() {
    return (
        <div className={styles.typingRow}>
            <div className={styles.typingAvatar}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="9" />
                    <path d="M8 12h.01M12 12h.01M16 12h.01" />
                </svg>
            </div>
            <div className={styles.typingBubble}>
                <span className={styles.dot} />
                <span className={styles.dot} />
                <span className={styles.dot} />
                <span className={styles.typingLabel}>Thinking…</span>
            </div>
        </div>
    )
}

export default function App() {
    const { messages, loading, sendMessage, clearChat } = useChat()
    const [historyOpen, setHistoryOpen] = useState(false)
    const bottomRef = useRef(null)
    const hasMessages = messages.length > 0

    /* Auto-scroll on new messages */
    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages, loading])

    return (
        <div className={styles.layout}>

            {/* ── Top bar ── */}
            <Header
                onHistoryOpen={() => setHistoryOpen(true)}
                onClearChat={hasMessages ? clearChat : undefined}
            />

            {/* ── Chat area ── */}
            <main className={styles.main} id="chat-area">
                <div className={styles.feed}>

                    {!hasMessages && <WelcomeBanner onSuggestion={sendMessage} />}

                    {messages.map((msg, i) => (
                        <MessageBubble key={i} message={msg} index={i} />
                    ))}

                    {loading && <TypingIndicator />}
                    <div ref={bottomRef} className={styles.anchor} />
                </div>
            </main>

            {/* ── Input bar ── */}
            <ChatInput
                onSend={sendMessage}
                loading={loading}
            />

            {/* ── Side panel ── */}
            <HistoryPanel
                isOpen={historyOpen}
                onClose={() => setHistoryOpen(false)}
            />
        </div>
    )
}
