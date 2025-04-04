import type { User } from "./user"

export interface ThreadCommentsApiResponse {
    count: number
    next: null
    previous: null
    results: Comment[]
    pages: number
    participants: string[]
    participants_count: number
    last_activity: string
}

export interface Comment {
    id: number;
    user: User;
    title: null;
    content: string;
    content_delta: ContentDelta | null;
    content_html: null | string;
    bookmarked_by_user: boolean;
    active: boolean;
    pinned: boolean;
    highlighted: boolean;
    modified_on: string;
    created_on: string;
}

export interface ContentDelta {
    ops: Op[];
}
