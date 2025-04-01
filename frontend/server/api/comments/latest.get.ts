// import { useAxiosClient } from '~/composables/django_client'
import type { Comment } from '~/types'

export default defineEventHandler(async event => {
    // const { client } = useAxiosClient()
    // const response = await client.get<Comment[]>('/comments/latest')
    // return response.data

    const data: Comment[] = [
        {
            id: 1,
            user: {
                email: 'google@user.com',
                id: 2,
                username: 'google-user',
                userprofile: {
                    blocked_users: 'some-user',
                    is_premium: false,
                    preferred_topics: 'google'
                }
            },
            title: null,
            active: true,
            bookmarked: false,
            bookmarked_by_user: false,
            content: 'This is some content',
            content_delta: null,
            content_html: '<p>This is some content</p>',
            created_on: '2021-1-1',
            highlighted: false,
            modified_on: '2021-1-1',
            pinned: false
        }
    ]

    return data
})
