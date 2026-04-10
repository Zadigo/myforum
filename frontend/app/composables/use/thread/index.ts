import type { SingleMainThread, Undefineable } from '~/types'

export * from './comments'
export * from './creation'

export const useCurrentThreadComposable = createGlobalState(async () => {
  const { id } = useRoute().params
  const requestComplete = ref<boolean>(false)
  const currentThread = ref<Undefineable<SingleMainThread>>()

  currentThread.value = await $fetch<SingleMainThread>(`/api/threads/${id}`, {
    onResponse() {
      requestComplete.value = true
    }
  })
  // if (!requestComplete.value) {
  // }
  
  return {
    currentThread,
    requestComplete
  }
})
