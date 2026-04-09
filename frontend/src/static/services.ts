export async function getJson<T = unknown>(
    url?: string,
    init: RequestInit = {}
): Promise<T | null> {
    if (!url) return null

    try {
        const response = await fetch(url, { ...init, method: 'GET' })
        if (!response.ok) {
            throw new Error(`GET request failed (${response.status})`)
        }

        const text = await response.text()
        return text ? (JSON.parse(text) as T) : null
    } catch (error) {
        console.error(error)
        return null
    }
}

export async function postJson<T = unknown, U = unknown>(
    url?: string,
    data?: U,
    init: RequestInit = {}
): Promise<T | null> {
    if (!url) return null

    try {
        const response = await fetch(url, {
            ...init,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...(init.headers ?? {}),
            },
            body: data !== undefined ? JSON.stringify(data) : undefined,
        })

        if (!response.ok) {
            throw new Error(`POST request failed (${response.status})`)
        }

        const text = await response.text()
        return text ? (JSON.parse(text) as T) : null
    } catch (error) {
        console.error(error)
        return null
    }
}