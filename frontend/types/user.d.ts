export interface Userprofile {
    blocked_users: string
    is_premium: boolean
    preferred_topics: string
}

export interface User {
    id: number
    email: string
    username: string
    userprofile: Userprofile
}

export interface UserForComment extends User {
    number_of_comments: number
    latest_comment: {
        id: number
        user__username: string
        creatd_on: string
    }
}
