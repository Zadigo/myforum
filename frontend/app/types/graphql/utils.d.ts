type GraphQlError = {
  errors: Array<{
    message: string
    locations?: Array<{ line: number; column: number }>
    path?: Array<string | number>
    extensions?: Record<string, unknown>
  }>
}

/**
 * Type for GraphQL pagination info using Relay-style pagination
 */
export interface GraphQlPaginationInfo {
  pageInfo: Partial<{
    /**
     * The cursor representing the start of the current page
     */
    startCursor: string
    /**
     * The cursor representing the end of the current page
     */
    endCursor: string
    /**
     * Indicates if there is a next page available
     * @default false
     */
    hasNextPage: boolean
    /**
     * Indicates if there is a previous page available
     * @default false
     */
    hasPreviousPage: boolean
  }>
}

/**
 * Type for Relay Node structure
 * @example
 * ```ts
 * const relayNode: RelayNode<Video> = { node: Video }
 * ```
 */
export type RelayNode<N> = {
  node: N
}

/**
 * Type for Relay Edge structure
 * @example
 * ```ts
 * const relayEdge: RelayEdge<Video> = {
 *   edges: [{ node: Video1 }, { node: Video2 }],
 *   pageInfo: { hasNextPage: true }
 * }
 * ```
 */
export type RelayEdge<E> = { edges: Array<RelayNode<E>> } & Partial<GraphQlPaginationInfo>

/**
 * Type for GraphQL response data
 * @example
 * ```ts
 * 
 * // With relay nodes (edges)
 * const response = $fetch<GraphQlData<'allvideos', RelayEdge<Video>>>(...)
 * 
 * // With single data
 * const response = $fetch<GraphQlData<'videoDetails', VideoDetails>>(...)
 * 
 * // With array of data
 * const response = $fetch<GraphQlData<'searchvideos', Video[]>>(...)
 * ```
 */
export interface GraphQlData<K extends string, R> {
  data: {
    [key in K]: R
  }
}

/**
 * Type for GraphQL response data where the data can have multiple keys 
 * based on the query, and may also include errors
 * @example
 * ```ts
 * // With multiple data keys
 * const response = $fetch<GraphQlMultiData<{ allvideos: RelayEdge<Video>, videoDetails: VideoDetails }>>(...)
 * ```
 */
export interface GraphQlMultiData<T extends Record<string, unknown>> {
  data: {
    [K in keyof T]: T[K]
  }
}

/**
 * Type for GraphQL response data where the data can be located under
 * different keys based on the query, and may also include errors
 * @example
 * ```ts
 * // With relay nodes (edges)
 * const response = $fetch<GraphQlVariableData<'allvideos' | 'searchvideos', RelayEdge<Video>>>(...)
 * 
 * // With single data
 * const response = $fetch<GraphQlVariableData<'videoDetails' | 'videoSummary', VideoDetails>>(...)
 * 
 * // With array of data
 * const response = $fetch<GraphQlVariableData<'searchvideos' | 'relatedvideos', Video[]>>(...)
 * ```
 */
export interface GraphQlVariableData<K extends string, R> {
  errors?: GraphQlError['errors']
  data: Partial<
    {
      [ key in K ]: R
    }
  >
}
