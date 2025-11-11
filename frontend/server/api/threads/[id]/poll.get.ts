import type { PollApiResponse } from '~/types'

export default defineCachedEventHandler(_event => {
    const data: PollApiResponse = {
        id: 1,
        active: true,
        allow_vote_change: false,
        choices_limit: 3,
        closes: false,
        closing_date: null,
        created_on: '2024-1-1',
        poll_type: 'Multiple',
        possibility_set: [
            {
                id: 1,
                text: 'This is your option 1'
            },
            {
                id: 2,
                text: 'This is your option 2'
            }
        ],
        public: true,
        question: 'What is your question?',
        voters_alone: false
    }
    return data
}, {
    base: 'fs',
    maxAge: 1 * 60,
    getKey() {
        return `thread-1-poll`
    }
})
