import { AxiosError } from 'axios'
import { useAxiosClient } from '~/composables/client'
import type { Comment, ThreadApiResponse } from '~/types'

export default defineCachedEventHandler(async event => {
    const { sort } = getQuery(event)
    const id = getRouterParam(event, 'id')
    const { client } = useAxiosClient()

    try {
        const response = await client.get<ThreadApiResponse[]>(`/v1/forums/${id}`, {
            params: {
                sort
            }
        })
        console.log(response.data)
    } catch (e) {
        if (e instanceof AxiosError && e.response) {
            throw createError({
                statusCode: 500,
                statusMessage: e.response.data,
                data: { field: 'email' }
            })
        }
    }

    const data: Comment[] = [
        {
            active: true,
            id: 1,
            bookmarked: false,
            bookmarked_by_user: false,
            content: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ipsum, ducimus? Debitis nam molestiae quis corrupti, ex fuga iure eaque maiores saepe numquam delectus similique. Iure beatae perspiciatis minima aliquid tenetur!',
            content_delta: null,
            content_html: '<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ipsum, ducimus? Debitis nam molestiae quis corrupti, ex fuga iure eaque maiores saepe numquam delectus similique. Iure beatae perspiciatis minima aliquid tenetur!</p>',
            created_on: '2025-2-3',
            highlighted: false,
            modified_on: '2025-2-3',
            pinned: false,
            title: 'Some title',
            user: {
                id: 1,
                email: 'user@gmail.com',
                username: 'some-user',
                userprofile: {
                    blocked_users: 'user-1',
                    is_premium: false,
                    preferred_topics: 'some-topic'
                }
            }
        },
        {
            active: true,
            id: 2,
            bookmarked: false,
            bookmarked_by_user: false,
            content: 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ipsum, ducimus? Debitis nam molestiae quis corrupti, ex fuga iure eaque maiores saepe numquam delectus similique. Iure beatae perspiciatis minima aliquid tenetur!',
            content_delta: null,
            content_html: '<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Ipsum, ducimus? Debitis nam molestiae quis corrupti, ex fuga iure eaque maiores saepe numquam delectus similique. Iure beatae perspiciatis minima aliquid tenetur!</p>',
            created_on: '2025-2-3',
            highlighted: true,
            modified_on: '2025-2-3',
            pinned: true,
            title: 'Some title',
            user: {
                id: 2,
                email: 'user@gmail.com',
                username: 'some-user',
                userprofile: {
                    blocked_users: 'user-1',
                    is_premium: false,
                    preferred_topics: 'some-topic'
                }
            }
        }
    ]
    return data
}, {
    base: 'fs',
    maxAge: 1 * 60,
    getKey() {
        return 'thread-comments'
    },
})
