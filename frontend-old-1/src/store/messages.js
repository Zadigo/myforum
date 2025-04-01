import { defineStore } from "pinia"

const useMessages = defineStore('messages', {
    state: () => ({
        messages: []
    }),

    actions: {
        addMessage(type = 'success', message) {
            this.messages.push({ type: type, content: message })
        },
    
        addErrorMessage(message) {
            this.addMessage('danger', message)
        },

        addSuccessMessage(message) {
            this.addMessage('success', message)
        }

    }
})

export {
    useMessages
}
