import type { Arrayable, UserNotification } from "~/types"


function useBaseNotification() {
  if (import.meta.server) {
    return {
      notifications: ref<Arrayable<UserNotification>>([]),
      count: ref(0)
    }
  }

  const notifications = ref<Arrayable<UserNotification>>([])
  const count = computed(() => notifications.value.length)

  return {
    notifications,
    count
  }
}

/**
 * Composable for handling user notifications.
 */
export function useHTTPNotificationsComposable() {
  const { notifications, count } = useBaseNotification()

  if (import.meta.server) {
    return {
      list: () => Promise.resolve([])
    }
  }
  const { $nuxtAuthentication } = useNuxtApp()
  

  async function _list() {
    notifications.value = await $nuxtAuthentication('/v1/notifications/', { method: 'GET' })
  }

  const { start } = useTimeoutFn(_list, 4000)

  onMounted(async () => { start() })

  return {
    /**
     * Fetch the list of user notifications.
     */
    notifications,
    /**
     * Count of user notifications.
     * @default 0
     */
    count,
    /**
     * Start fetching notifications periodically.
     */
    list: start
  }
}

export const useWsNotificationComposable = createGlobalState(() => {
  const { notifications, count } = useBaseNotification()

  if (import.meta.server) {
    return {
      wsObject: null
    }
  }

  const access = useCookie(useRuntimeConfig().public.nuxtAuthentication.accessTokenName)

  const wsObject = useWebSocket<UserNotification>(`${getWsUrl()}/ws/notifications?token=${access.value}`, {
    immediate: true,
    onMessage() {

    }
  })

  return {
    notifications,
    count,
    wsObject
  }
})
