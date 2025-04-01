import { useAxiosClient } from '~/composables/django_client'
import { Comment } from '~/types'

export default defineEventHandler(async event => {
    const { client } = useAxiosClient()
    const response = await client.get<Comment[]>('/comments/latest')
    return response.data
})
