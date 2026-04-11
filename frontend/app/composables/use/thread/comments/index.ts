import type { LatestComments } from '~/types'

export * from './creation'

export const useLatestCommentsComposable = createGlobalState(async <T extends LatestComments = LatestComments>() => {
  const requestComplete = ref<boolean>(false)
  
  const comments = computedAsync(async () => await $fetch<T>('/api/comments/latest', {
    method: 'GET',
    onResponse() {
      requestComplete.value = true
    }
  }))

  return {
    /**
     * The latest comments fetched from the API.
     */
    comments,
    /**
     * Indicates whether the request to fetch the latest comments has completed.
     * @default false
     */
    requestComplete
  }
})
