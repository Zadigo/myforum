import type { Delta } from '@vueup/vue-quill'
import type { RouteParamsGeneric } from 'vue-router'
import type { RouteMeta } from 'vue-router/dist/router-BbqN7H95.mjs'

export type * from './forums'
export type * from './user'
export type * from './threads'
export type * from './comments'
export type * from './accounts'

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

export interface UserSearch {
  q?: string
  title_only?: string
  posted_by?: string
  from_date?: string
  to_date?: string
  search_in_forums?: string
  sub_forums?: string
}

export type RouteSearchParamsGeneric = RouteParamsGeneric & UserSearch

export interface RouteIdParamsGeneric extends RouteParamsGeneric {
  id: string
}

export interface BaseApiResponse<R> {
  count: number
  next: null
  previous: null
  results: R[]
}

type RouteMetaNames = 'Create Thread' | 'Edit Thread' | 'Thread Details'

export interface CustomRouteMeta extends RouteMeta {
  name?: RouteMetaNames
}
