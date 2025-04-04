import axios from 'axios'
import { useAxiosClient } from '~/composables/client'
import type { ThreadApiResponse } from '~/types'

export default defineCachedEventHandler(async event => {
    const { client } = useAxiosClient()
    const { sort } = getQuery(event)
    const id = getRouterParam(event, 'id')

    try {
        const response = await client.get<ThreadApiResponse[]>(`/v1/forums/${id}/threads`, {
            params: {
                sort
            }
        })
        return response.data
    } catch (e) {
        if (axios.isAxiosError(e)) {
            throw createError({
                statusCode: 500,
                statusMessage: e.response?.data,
                data: { field: 'email' }
            })
        }
    }

    // const data: ForumThread[] = [
    //     {
    //         active: true,
    //         category: 'General',
    //         created_on: '2025-1-1',
    //         description: 'Some thread description',
    //         forum: {
    //             active: true,
    //             admin: false,
    //             category: 'Sports',
    //             created_on: '2025-1-1',
    //             description: 'Some quick description',
    //             id: 1,
    //             number_of_threads: 12,
    //             title: 'My forum title',
    //             user: {
    //                 id: 1,
    //                 email: 'user@gmail.com',
    //                 username: 'some-user',
    //                 userprofile: {
    //                     blocked_users: 'google',
    //                     is_premium: false,
    //                     preferred_topics: 'some topic'
    //                 }
    //             }
    //         },
    //         id: 1,
    //         latest_comment: {
    //             created_on: '2025-1-1',
    //             id: 1,
    //             user__username: 'some-user'
    //         },
    //         modified_on: '2025-1-1',
    //         number_of_comments: 45,
    //         owned_by_user: true,
    //         participants: [
    //             {
    //                 user__id: 1,
    //                 user__username: 'another-user'
    //             }
    //         ],
    //         title: 'Some forum title',
    //         user: {
    //             id: 1,
    //             email: 'user@gmail.com',
    //             username: 'some-user',
    //             userprofile: {
    //                 blocked_users: 'google',
    //                 is_premium: false,
    //                 preferred_topics: 'some topic'
    //             }
    //         }
    //     }
    // ]
    // return data
}, {
    base: 'fs',
    maxAge: 1 * 60,
    getKey() {
        return 'forums-threads'
    }
})
