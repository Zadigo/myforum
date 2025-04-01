import { defineStore } from "pinia";

const useAuthentication = defineStore('authentication', {
    state: () => ({
        token: null,
        user: null,
        openLoginModal: false
    }),

    actions: {
        setUser(data, session = true) {
            // Set the authentication token
            // for the loggedin user
            this.token = data.token
            this.user = data
            if (session) {
                this.vueSession.create('user', data)
            }
            this.openLoginModal = false
        },
        unsetUser() {
            // Unset the authentication token
            // for the loggedin user
            this.token = null
            this.user = null
            this.vueSession.remove('user')
        }
    },
    getters: {
        isAuthenticated() {
            var result = this.token && this.user

            if (!result) {
                // Check in the session if we already have
                // a case where the user had been registered
                const user = this.$session.retrieve('user')

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
