import type { Delta } from '@vueup/vue-quill'
import type { RouteParamsGeneric } from 'vue-router'

export * from './forums'
export * from './user'
export * from './threads'
export * from './comments'
export * from './accounts'

export type StringNull = string | null | undefined

export interface LoginAPIResponse {
  access: string
  refresh: string
}

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
