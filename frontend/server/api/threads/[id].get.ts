import type { Comment, ThreadApiResponse } from '~/types'

export default defineCachedEventHandler(async _event => {
    const data: Comment[] = [
        {
            active: true,
            id: 1,
            bookmarked: false,
            bookmarked_by_user: false,
            content: 'Some content',
            content_delta: null,
            content_html: '<p>Some content</p>',
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
        }
    ]
    return data
}, {
    base: 'fs',
    maxAge: 1 * 60,
    getKey() {
        return 'comments'
    },
})
