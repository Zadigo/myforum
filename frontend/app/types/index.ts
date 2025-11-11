import type { Delta } from '@vueup/vue-quill'
import type { RouteParamsGeneric } from 'vue-router'

export * from './forums'
export * from './user'
export * from './threads'
export * from './comments'
export * from './accounts'

export type Arrayable<T> = T[]

export type Nullable<T> = T | null

export type Undefineableable<T> = T | undefined

export type TypeNull<T> = T | Nullable<T> | Undefineableable<T>

/**
 * @deprecated
 */
export interface LoginAPIResponse {
  access: string
  refresh: string
}

/**
 * @deprecated
 */
export type RefreshAPIResponse = Exclude<LoginAPIResponse, 'access'>

export interface EditorData {
  delta: string | Delta | undefined
  html: string
  text: string
}

export interface CustomRouteParamsGeneric extends RouteParamsGeneric {
  q: string
}

export interface CustomRouteIdParamsGeneric extends RouteParamsGeneric {
  id: string
}

export interface BaseApiResponse<R> {
  results: R[]
}
