import { getJson, postJson } from './services'
import { API_URL } from './constants'
import { schemaToFormFields } from '@/tools/helpers'
import type { Schema } from './interfaces'

export async function getFeatures(): Promise<any[]> {
    const endpoint = "/features"
    const schema = await getJson<Schema>(`${API_URL}${endpoint}`)
    return schema ? schemaToFormFields(schema) : []
}

export async function sendEntry(entry: Record<string, unknown>): Promise<any> {
    const endpoint = "/predict"
    return await postJson(`${API_URL}${endpoint}`, entry)
}