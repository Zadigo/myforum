import { useAxiosClient } from "~/composables/django_client"
import type { Thread } from "~/types"

export default defineEventHandler(async event => {
    const { sort } = getQuery(event)
    const id = getRouterParam(event, 'id')
    const { client } = useAxiosClient()
    const response = await client.get<Thread[]>(`/forums/${id}`, {
        params: {
            sort
        }
    })
    return response.data
})
