export * from './constants'
export * from './fixtures'
export * from './schemas'
export * from './ws_message'

export function useIdConverter(value: string) {
  const [_, id] = atob(value).split(':')
  if (isDefined(id)) {
    return useToNumber(id)
  } else {
    return null
  }
}
