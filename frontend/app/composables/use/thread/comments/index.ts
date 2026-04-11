import type { LatestComments } from '~/types'

export * from './creation'

export const useLatestCommentsComposable = createGlobalState(async <T extends LatestComments>() => {
  const requestComplete = ref<boolean>(false)
  
  const comments = computedAsync(async () => await $fetch<T>('/api/comments/latest', {
    method: 'GET',
    onResponse() {
      requestComplete.value = true
    }
  }))

  return {
    comments,
    requestComplete
  }
})
