<template>
  <section id="ws-test">
    <div class="grid grid-cols-2">
      <div class="p-10 space-y-2">
        <div class="p-3 rounded-2xl bg-slate-200/10 space-x-2">
          <volt-button @click="ws.open()">
            <icon name="lucide:play" />
            Connect
          </volt-button>

          <volt-button @click="ws.close()">
            <icon name="lucide:pause" />
            Disconnect
          </volt-button>
        </div>

        <div class="p-3 rounded-2xl bg-slate-200/10 space-y-2">
          <p class="p-2 rounded-2xl bg-yellow-200/10">Test the websocket by sending a custom action and payload</p>
          
          <volt-input-text v-model="action" placeholder="Action" />
          <volt-textarea v-model="payload" :style="{ resize: 'none' }" class="w-full" rows="10" placeholder="Payload" />
          <volt-button @click="sendMessage()">
            <icon name="lucide:send" />
            Send
          </volt-button>
        </div>
      </div>

      <div class="bg-primary-700 dark:bg-primary-950 p-5 space-y-2 h-screen overflow-y-scroll rounded-2xl">
        <wstesting-message v-for="(message, idx) in messages" :key="idx" :message="message" />   
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { DiscussionSpace } from '~/types'

const { decode, encode, messages } = useWWebsocketMessages2()

type WsReceive = {
  must_identify: { clientId: string }
  identified: null
  available_discussions: { discussionSpaces: Record<string, DiscussionSpace> }
  new_client: { discussionSpace: DiscussionSpace }
}

type WsSend = {
  identify: [{ username: string, clientId: string }]
  get_discussions: [{ clientId: string }]
}

const clientId = ref<string>('')
const discussions = ref<Record<string, DiscussionSpace>>({})
const selectedDiscussion = ref<DiscussionSpace>()

const ws = useWebSocket('ws://127.0.0.1:9000/ws/general-discussion', {
  immediate: true,
  onMessage(ws, event) {
    const decoder = decode<WsReceive>(event.data)

    decoder('must_identify', (data) => {
      if (isDefined(data)) {
        clientId.value = data.clientId || ''

        ws.send(
          encode<WsSend>('identify', { username: 'alice', clientId: clientId.value })
        )
      }
    })

    decoder('identified', () => {
      // ws.send(
      //   encode<WsSend>('get_discussions', { clientId: clientId.value })
      // )
    })

    decoder('available_discussions', (data) => {
      if (isDefined(data)) {
        discussions.value = data.discussionSpaces || {}
      }
    })

    decoder('new_client', (data) => {
      if (isDefined(data)) {
        selectedDiscussion.value = data.discussionSpace
      }
    })
  }
})

/**
 * Testing
 */

const action = ref<string>('')
const payload = ref<string>('')

function sendMessage() {
  ws.send(
    encode(action.value, JSON.parse(payload.value || '{}'))
  )
}
</script>
