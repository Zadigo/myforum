import type { Nullable } from ".."
import type { BaseUser } from "./accounts"
import type { GraphQlData, RelayEdge, RelayNode } from "./utils"

export type BaseComment = {
	id: string
	active: boolean
	content: string
	contentDelta: Nullable<string>
	contentHtml: string
	originalPost: boolean
	pinned: boolean
	published: boolean
	title: Nullable<string>
	quoteSet: string[]
	quotedOmment: string[]
	replySet: string[]
	mediaContents: string[]
	bookmarkedByUser: boolean
	user: Pick<BaseUser, 'id' | 'username'>
	createdOn: Readonly<string>
	modifiedOn: Readonly<string>
	// subthread?: any
}

export type UserCommentNode = RelayNode<BaseComment>

export type UserComments = GraphQlData<'commentsForThread', RelayEdge<BaseComment>>

export type LatestComments = GraphQlData<'latestComments', RelayEdge<Pick<BaseComment, 'id' | 'title' | 'content' | 'contentHtml' | 'createdOn' | 'user'>>>
