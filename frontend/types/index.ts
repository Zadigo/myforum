export * from './forums'
export * from './user'
export * from './threads'
export * from './comments'

export type StringNull = string | null | undefined

export interface LoginAPIResponse {
    access: string
    refresh: string
}

export type RefreshAPIResponse = Exclude<LoginAPIResponse, 'access'>

export interface EditorData {
    delta: object | null
    html: string
    text: string
}
