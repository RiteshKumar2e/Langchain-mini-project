/**
 * ChatInput.jsx
 * ─────────────
 * Auto-growing textarea + send button at the bottom of the screen.
 * Enter to send, Shift+Enter for newlines.
 */

import { useState, useRef, useEffect } from 'react'
import styles from './ChatInput.module.css'

export default function ChatInput({ onSend, loading }) {
    const [value, setValue] = useState('')
    const textareaRef = useRef(null)

    /* Auto-resize */
    useEffect(() => {
        const el = textareaRef.current
        if (!el) return
        el.style.height = 'auto'
        el.style.height = Math.min(el.scrollHeight, 160) + 'px'
    }, [value])

    const canSend = value.trim().length > 0 && !loading

    const handleSubmit = () => {
        if (!canSend) return
        onSend(value.trim())
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
            <div className={styles.container}>
                <div className={`${styles.inputBox} ${loading ? styles.inputLoading : ''}`}>
                    <textarea
                        ref={textareaRef}
                        id="question-input"
                        className={styles.textarea}
                        placeholder="Ask a question… (Enter ↵ to send)"
                        value={value}
                        onChange={e => setValue(e.target.value)}
                        onKeyDown={handleKeyDown}
                        disabled={loading}
                        rows={1}
                    />

                    <button
                        id="send-button"
                        className={`${styles.sendBtn} ${canSend ? styles.sendActive : ''}`}
                        onClick={handleSubmit}
                        disabled={!canSend}
                        title="Send (Enter)"
                    >
                        {loading ? (
                            <span className={styles.spinner} />
                        ) : (
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
                                stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                                <line x1="22" y1="2" x2="11" y2="13" />
                                <polygon points="22 2 15 22 11 13 2 9 22 2" />
                            </svg>
                        )}
                    </button>
                </div>

                <p className={styles.hint}>
                    <kbd>Enter</kbd> send &nbsp;·&nbsp; <kbd>Shift+Enter</kbd> newline
                    {loading && <span className={styles.hintLoading}> · Generating answer…</span>}
                </p>
            </div>
        </div>
    )
}
