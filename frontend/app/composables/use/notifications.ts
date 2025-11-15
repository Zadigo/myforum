import type { Arrayable, UserNotification } from "~/types"


function useBaseNotification() {
  if (import.meta.server) {
    return {
      notifications: ref<Arrayable<UserNotification>>([]),
      count: ref<number>(0)
    }
  }

  const notifications = ref<Arrayable<UserNotification>>([])
  const count = computed(() => notifications.value.length)
  
  return {
    notifications,
    count,
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

type WsReceiveMessages = { action: 'polled', notifications: UserNotification[] }

type WsSendMessages = { action: 'poll' }

/**
 * Composable for handling WebSocket user notifications.
 */
export const useWsNotificationComposable = createGlobalState(() => {
  const { notifications, count } = useBaseNotification()

  if (import.meta.server) {
    return {
      notifications,
      count,
      wsObject: null,
      opened: ref(false),
      pause: () => { },
      notificationsActive: ref(false),
      pauseNotifications: () => { },
      resumeNotifications: () => { }
    }
  }

  /**
   * Websocket
   */

  const { send, simpleWsSend, parse } = useWebsocketMessage<WsReceiveMessages, WsSendMessages>()
  const { accessToken, isAuthenticated } = useUser()

  const wsObject = useWebSocket<UserNotification>(`${getWsUrl()}/ws/notifications?token=${accessToken.value || ''}`, {
    immediate: true,
    onConnected(ws) {
      simpleWsSend({ action: 'poll' }, ws)
    },
    onMessage(_, event) {
      if (event.data) {
        const _data = parse(event.data)

        if (_data.value.action == 'polled') {
          notifications.value = _data.value.notifications
        }
      }
    }
  })

  const opened = computed(() => wsObject.status.value === 'OPEN')

  /**
   * Poll for new notifications.
   */

  // const { play } = useSound('/sounds/notification1.mp3', { volume: 0.5 })
  const { pause, resume, isActive } = useInterval(100000, {
    immediate: true,
    controls: true,
    callback: () => {
      // send({ action: 'poll' }, wsObject)
      // play()
    }
  })

  watch(isAuthenticated, (newVal) => {
    if (newVal) {
      resume()
    } else {
      pause()
    }
  })

  return {
    count,
    notifications,
    wsObject,
    opened,
    pause,
    notificationsActive: isActive,
    pauseNotifications: () => {},
    resumeNotifications: () => {}
  }
})
