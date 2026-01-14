import type { BaseUser } from "./accounts"
import type { GraphQlData, RelayEdge, RelayNode } from "./utils"

export interface BaseForum {
	id: string
	title: string
	description: string
	category: string
	active: boolean
	user: Pick<BaseUser, 'id' | 'username'>
	numberOfThreads: number
	createdOn: string
}

export type SingleForum = GraphQlData<'forum', BaseForum>

export type ForumNode = RelayNode<BaseForum>

export type Forums = GraphQlData<'allForums', RelayEdge<BaseForum>>
