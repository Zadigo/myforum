import { useAxiosClient } from '~/composables/django_client'
import type { Forum } from '~/types'

export default defineEventHandler(async _event => {
    const { client } = useAxiosClient()
    const response = await client.get<Forum[]>('/forums/')
    return response.data
})
