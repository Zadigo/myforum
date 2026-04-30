<template>
  <section id="ws-test">
    <div class="grid grid-cols-2">
      <div>
        <volt-button @click="ws.open()">
          Reconnect
        </volt-button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const { decode, encode } = useWWebsocketMessages2()

type WsReceive = {
  must_identify: { clientId: string }
  identified: null
  available_discussions: { discussionSpaces: string[] }
}

type WsSend = {
  identify: [{ clientId: string }]
  get_discussions: [{ clientId: string }]
}

const clientId = ref<string>('')
const discussions = ref<string[]>([])

const ws = useWebSocket('ws://127.0.0.1:9000/ws/general-discussion', {
  immediate: true,
  onMessage(ws, event) {
    const decoder = decode<WsReceive>(event.data)

    decoder('must_identify', (data) => {
      if (isDefined(data)) {
        clientId.value = data.clientId || ''

        ws.send(
          encode<WsSend>('identify', { clientId: clientId.value })
        )
      }
    })

    decoder('identified', () => {
      ws.send(
        encode<WsSend>('get_discussions', { clientId: clientId.value })
      )
    })

    decoder('available_discussions', (data) => {
      if (isDefined(data)) {
        discussions.value = data.discussionSpaces || []
      }
    })
  }
})
</script>
