export interface User {
  id: string
  username: string
}

export interface Participant {
  user: User
  id: string
}

export interface DiscussionSpace {
  id: string
  name: string
  participants: Participant[]
}
