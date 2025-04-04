import type { Forum } from './forums'
import type { User } from './user'

export interface ThreadApiResponse {
    count: number
    next: null
    previous: null
    results: ForumThreadResults[]
}

export interface ForumThreadResults {
    id: number
    forum: Forum
    user: User
    number_of_comments: number
    latest_comment: LatestComment
    title: string
    category: string
    description: null
    owned_by_user: boolean
    participants: Participant[]
    active: boolean
    modified_on: string
    created_on: string
}

export interface LatestComment {
    id: number
    user__username: string
    created_on: string
}

export interface Participant {
    user__id: number
    user__username: string
}
