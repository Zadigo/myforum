import type { SingleMainThread, Undefineable } from '~/types'

export * from './comments'
export * from './creation'

export const useCurrentThreadComposable = createGlobalState(async () => {
  const { id } = useRoute().params
  const requestComplete = ref<boolean>(false)
  const currentThread = ref<Undefineable<SingleMainThread>>()

  if (!requestComplete.value) {
    currentThread.value = await $fetch<SingleMainThread>(`/api/threads/${id}`, {
      onResponse() {
        requestComplete.value = true
      }
    })
  }
  
  return {
    currentThread,
    requestComplete
  }
})
