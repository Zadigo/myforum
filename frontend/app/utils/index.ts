export function useIdConverter(value: string) {
  const [_, id] = atob(value).split(':')
  if (isDefined(id)) {
    return useToNumber(id)
  } else {
    return null
  }
}
