// import { useAxiosClient } from "~/composables/django_client"
import type { Forum } from '~/types'

export default defineCachedEventHandler(async _event => {
    // const { sort } = getQuery(event)
    // const id = getRouterParam(event, 'id')
    // const { client } = useAxiosClient()
    // const response = await client.get<Thread[]>(`/forums/${id}`, {
    //     params: {
    //         sort
    //     }
    // })
    // return response.data

    const data: Forum = {
        active: true,
        admin: false,
        category: 'Sports',
        created_on: '2025-1-1',
        description: 'Some quick description',
        id: 1,
        number_of_threads: 12,
        title: 'My forum title',
        user: {
            id: 1,
            email: 'user@gmail.com',
            username: 'some-user',
            userprofile: {
                blocked_users: 'google',
                is_premium: false,
                preferred_topics: 'some topic'
            }
        }
    }
    
    return data
}, {
    base: 'fs',
    maxAge: 1 * 60,
    getKey() {
        return 'forum'
    }
})
