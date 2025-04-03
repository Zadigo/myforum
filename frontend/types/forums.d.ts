import type { User } from './user'

export interface Forum {
    id: number
    user: User
    title: string
    category: string
    description: string
    admin: boolean
    number_of_threads: number
    active: boolean
    created_on: string
}

export interface ForumThread {
    id: number
    forum: Forum
    user: User
    number_of_comments: number
    latest_comment: {
        id: number
        user__username: string
        created_on: string
    }
    title: string
    category: string
    description: string | null
    owned_by_user: boolean
    participants: { 
        user__id: number, 
        user__username: string
    }[]
    active: boolean
    modified_on: string
    created_on: string 
}

export interface Comment {
    id: number
    user: User
    title: string | null
    content: string
    content_delta: null
    content_html: string
    bookmarked_by_user: boolean
    active: boolean
    pinned: boolean
    bookmarked: boolean
    highlighted: boolean
    modified_on: string
    created_on: string
}

export interface ThreadApiResponse {
    count: number
    next: string | null
    previous: string | null
    results: Comment[]
    pages: number
    participants: number
}

export interface SearchApiResponse {
    threads: Thread[],
    comments: Comment[]
}

export interface PollQuestion {
    id: number
    text: string
}

export interface PollApiResponse {
    id: number
    question: string
    possibility_set: PollQuestion[]
    poll_type: 'Single' | 'Multiple'
    choices_limit: number
    allow_vote_change: boolean
    closes: boolean
    closing_date: string | null
    public: boolean
    voters_alone: boolean
    active: boolean
    created_on: string
}
