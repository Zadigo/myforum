import type { Delta } from '@vueup/vue-quill'
import type { RouteParamsGeneric } from 'vue-router'
import type { RouteMeta } from '#vue-router'

export type * from './graphql'
export type * from './restapi'
export * from './motions'
export type * from './live_discussions'
export { SortMethods, type SortMethodNames, type SortMenuItem, sortMethodNames } from './forums'

export type Arrayable<T> = T[]

export type Nullable<T> = T | null

export type Undefineable<T> = T | undefined

export type TypeNull<T> = T | Nullable<T> | Undefineable<T>

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

export interface EditorData {
  delta: string | Delta | undefined
  html: string
  text: string
}

type RouteMetaNames = 'Create Thread' | 'Edit Thread' | 'Thread Details'

export interface CustomRouteMeta extends RouteMeta {
  name?: RouteMetaNames
}
