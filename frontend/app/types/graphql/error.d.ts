interface Location {
  line: number
  column: number
}

interface Error<P> {
  message: string
  locations: Location[]
  path: P[]
}

export type Data <D> = {
  [P in D]: string
}

/**
 * GraphQL Error Type
 * P - Possible paths in the error
 * D - Possible data fields in the response
 * @example
 * ```ts
 * GraphQlError<'error1' | 'error2'>
 * ```
 */
export type GraphQlError<P extends string> = {
  errors:Error<P>[]
  data: Data<P>
}
