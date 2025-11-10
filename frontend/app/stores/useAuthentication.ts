import { defineStore } from "pinia";
import type { User } from "~/types/user";

type AnyType = string | null | undefined

export default defineStore('authentication', () => {
    // Tokens
    const accessToken = ref<AnyType>()
    const refreshToken = ref<AnyType>()

    // User details
    const userProfile = ref<User>()
    
    // Modals
    const openLoginModal = ref(false)

    const isAuthenticated = computed(() => {
        return (
            accessToken.value !== null &&
            typeof accessToken.value !== 'undefined'
        )
    }) 

    function logout () {
        accessToken.value = undefined
        refreshToken.value = undefined
        userProfile.value = undefined
    }

    return {
        userProfile,
        openLoginModal,
        isAuthenticated,
        accessToken,
        refreshToken,
        logout
    }
})
