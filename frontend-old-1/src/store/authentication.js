import { defineStore } from "pinia";

const useAuthentication = defineStore('authentication', {
    state: () => ({
        token: undefined,
        user: undefined,
        openLoginModal: false
    }),

    actions: {
        setUser(data, session = true) {
            this.token = data.token
            this.user = data
            if (session) {
                this.vueSession.create('user', data)
            }
            this.openLoginModal = false
        },
        unsetUser() {
            this.token = undefined
            this.user = undefined
            this.vueSession.remove('user')
        }
    },
    getters: {
        isAuthenticated() {
            var result = this.token && this.user ? true : false

            if (!result) {
                // Check in the session if we already have
                // a case where the user had been registered
                var user = this.vueSession.retrieve('user')

                if (user) {
                    this.setUser(user, false)
                    return true
                }
            }
            return result
        }
    }
})

export {
    useAuthentication
}
