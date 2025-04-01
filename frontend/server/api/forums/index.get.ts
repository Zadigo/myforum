// import { useAxiosClient } from '~/composables/django_client'
// import type { Forum } from '~/types'

export default defineEventHandler(async _event => {
    // const { client } = useAxiosClient()
    // const response = await client.get<Forum[]>('/forums/')
    // return response.data

    return [
        {
            id: 1,
            active: true,
            number_of_threads: 14,
            admin: false,
            category: 'General',
            created_on: '2025-1-1',
            description: 'A quick description',
            title: 'My General forum',
            user: 'Google User'
        }
    ]
})
