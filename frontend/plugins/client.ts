export default defineNuxtPlugin(_nuxtApp => {
    const { client } = useAxiosClient()
    return {
        provide: {
            client
        }
    }
})
