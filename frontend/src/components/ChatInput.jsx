/**
 * ChatInput.jsx
 * ─────────────
 * Auto-growing textarea + send button.
 * Submits on Enter (Shift+Enter for newline).
 */

import { useState, useRef, useEffect } from 'react'
import styles from './ChatInput.module.css'

const SUGGESTIONS = [
    'What is RAG?',
    'How does LangChain work?',
    'Explain the transformer attention mechanism',
    'What are the types of machine learning?',
    'Compare FAISS with other vector databases',
]

export default function ChatInput({ onSend, loading, disabled, showSuggestions }) {
    const [value, setValue] = useState('')
    const textareaRef = useRef(null)

    // Auto-resize textarea
    useEffect(() => {
        const el = textareaRef.current
        if (!el) return
        el.style.height = 'auto'
        el.style.height = Math.min(el.scrollHeight, 160) + 'px'
    }, [value])

    const handleSubmit = () => {
        const q = value.trim()
        if (!q || loading || disabled) return
        onSend(q)
        setValue('')
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSubmit()
        }
    }

    return (
        <div className={styles.wrapper}>
            {showSuggestions && (
                <div className={styles.suggestions}>
                    <p className={styles.suggestLabel}>Try asking:</p>
                    <div className={styles.chips}>
                        {SUGGESTIONS.map((s) => (
                            <button
                                key={s}
                                className={styles.chip}
                                onClick={() => { setValue(s); textareaRef.current?.focus() }}
                                disabled={loading || disabled}
                            >
                                {s}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            <div className={styles.inputRow}>
                <textarea
                    ref={textareaRef}
                    id="question-input"
                    className={styles.textarea}
                    placeholder="Ask anything about the knowledge base… (Enter to send)"
                    value={value}
                    onChange={(e) => setValue(e.target.value)}
                    onKeyDown={handleKeyDown}
                    disabled={loading || disabled}
                    rows={1}
                />
                <button
                    id="send-button"
                    className={`btn btn-primary ${styles.sendBtn}`}
                    onClick={handleSubmit}
                    disabled={!value.trim() || loading || disabled}
                    title="Send (Enter)"
                >
                    {loading ? (
                        <span className={styles.spinner} />
                    ) : (
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
                            <line x1="22" y1="2" x2="11" y2="13" />
                            <polygon points="22 2 15 22 11 13 2 9 22 2" />
                        </svg>
                    )}
                </button>
            </div>

            <p className={styles.hint}>
                <kbd>Enter</kbd> to send · <kbd>Shift+Enter</kbd> for a new line
            </p>
        </div>
    )
}
