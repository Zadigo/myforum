import type { Arrayable, BaseApiResponse, Nullable } from '.'
import type { User } from './user'

export type ThreadCommentsApiResponse = BaseApiResponse<UserComment> & {
    pages: number
    participants: Arrayable<string>
    participants_count: number
    last_activity: string
}

export interface UserComment {
    id: number
    user: User
    title: Nullable<string>
    content: string
    content_delta: Nullable<ContentDelta>
    content_html: Nullable<string>
    bookmarked_by_user: boolean
    active: boolean
    pinned: boolean
    highlighted: boolean
    modified_on: string
    created_on: string
}

export interface Op {
    attributes?: Arrayable<Record<string, string>>
    insert: string
}

export interface ContentDelta {
    ops: Arrayable<Op>
}
