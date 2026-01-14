import type { RelayEdge } from "./utils"

export type ForumSubscription = RelayEdge<{'forumSubscriptions', []}>

export type ThreadSubscription = RelayEdge<{'threadSubscriptions', []}>

export type BaseUserProfile = {
	id: string
	// preferredTopics?: any
	// blockedUsers?: any
	isPremium: boolean
	createdOn: string
	// followers: any[]
	forumSubscriptions: ForumSubscription
	threadSubscriptions: ThreadSubscription
}


export type BaseUser = {
  dateJoined: string
  email: string
  firstName: string
  id: string
  isActive: boolean
  isModerator: boolean
  isStaff: boolean
  lastLogin: string
  isSuperuser: boolean
  password: string
  lastName: string
  username: string
}
