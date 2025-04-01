export interface UserProfile {
    preferred_topics: string
    blocked_users: string
    is_premium: boolean
}

export interface User {
    id: number
    username: string
    email: string
    userprofile: UserProfile
}

export interface UserForComment extends User {
    number_of_comments: number
    latest_comment: {
        id: number
        user__username: string
        creatd_on: string
    }
}
