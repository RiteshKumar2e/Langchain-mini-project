/**
 * api.js
 * ──────
 * Thin wrapper around the backend API. All fetch calls live here so
 * components never deal with raw URLs or error-handling boilerplate.
 */

const BASE = '/api'

async function handleResponse(res) {
    if (!res.ok) {
        let detail = `HTTP ${res.status}`
        try {
            const json = await res.json()
            detail = json.detail || JSON.stringify(json)
        } catch {/* ignore parse errors */ }
        throw new Error(detail)
    }
    return res.json()
}

/** POST /api/ask */
export async function askQuestion(question, conversationHistory = []) {
    const res = await fetch(`${BASE}/ask`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question, conversation_history: conversationHistory }),
    })
    return handleResponse(res)
}

/** GET /api/health */
export async function getHealth() {
    const res = await fetch(`${BASE}/health`)
    return handleResponse(res)
}

/** GET /api/history */
export async function getHistory(limit = 10) {
    const res = await fetch(`${BASE}/history?limit=${limit}`)
    return handleResponse(res)
}

/** POST /api/history/clear */
export async function clearHistory() {
    const res = await fetch(`${BASE}/history/clear`, { method: 'POST' })
    return handleResponse(res)
}

/** POST /api/ingest */
export async function triggerIngest(force = true) {
    const res = await fetch(`${BASE}/ingest?force=${force}`, { method: 'POST' })
    return handleResponse(res)
}
