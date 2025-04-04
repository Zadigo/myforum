import { AxiosError } from 'axios'
import { useAxiosClient } from '~/composables/client'
import type { Forum } from '~/types'

export default defineCachedEventHandler(async _event => {
    const { client } = useAxiosClient()

    try {
        const response = await client.get<Forum[]>('/v1/forums/')
        return response.data
    } catch (e) {
        if (e instanceof AxiosError && e.response) {
            throw createError({
                statusCode: 500,
                statusMessage: e.response.data,
                data: { field: 'email' }
            })
        }
    }
    // return [
    //     {
    //         id: 1,
    //         active: true,
    //         number_of_threads: 14,
    //         admin: false,
    //         category: 'General',
    //         created_on: '2025-1-1',
    //         description: 'A quick description',
    //         title: 'My General forum',
    //         user: 'Google User'
    //     }
    // ]
}, {
    base: 'fs',
    maxAge: 1*60,
    name: 'forums'
})
