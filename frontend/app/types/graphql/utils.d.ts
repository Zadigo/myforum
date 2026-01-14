
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

export interface GraphQlMultiData<T extends Record<string, unknown>> {
  data: {
    [key in keyof T]: T[key]
  }
}
