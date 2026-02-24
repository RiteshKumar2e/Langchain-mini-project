/**
 * useChat.js
 * ──────────
 * Custom hook that manages the entire chat / conversation state,
 * including follow-up question support via conversation_history.
 */

import { useState, useCallback, useRef } from 'react'
import { askQuestion } from '../api'

export function useChat() {
    const [messages, setMessages] = useState([])  // {role, content, sources?, isError?}
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const historyRef = useRef([])  // raw history for the API [{role, content}]

    const sendMessage = useCallback(async (question) => {
        if (!question.trim() || loading) return

        const userMsg = { role: 'user', content: question }
        setMessages(prev => [...prev, userMsg])
        setLoading(true)
        setError(null)

        try {
            const data = await askQuestion(question, historyRef.current)

            const assistantMsg = {
                role: 'assistant',
                content: data.answer,
                sources: data.sources || [],
            }
            setMessages(prev => [...prev, assistantMsg])

            // Keep rolling history for follow-ups
            historyRef.current = [
                ...historyRef.current,
                { role: 'user', content: question },
                { role: 'assistant', content: data.answer },
            ]
        } catch (err) {
            const errMsg = {
                role: 'assistant',
                content: `Sorry, I encountered an error: **${err.message}**`,
                isError: true,
                sources: [],
            }
            setMessages(prev => [...prev, errMsg])
            setError(err.message)
        } finally {
            setLoading(false)
        }
    }, [loading])

    const clearChat = useCallback(() => {
        setMessages([])
        setError(null)
        historyRef.current = []
    }, [])

    return { messages, loading, error, sendMessage, clearChat }
}
