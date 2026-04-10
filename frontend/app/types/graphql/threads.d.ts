import type { Arrayable, BaseForum } from ".."
import type { BaseUser } from "./accounts"
import type { GraphQlData, RelayEdge } from "./utils"

export interface PossibilitySet {
	id: string
	createdOn: string
	text: string
}

type AnswerSet = {
  id: string
  user: Pick<BaseUser, 'id' | 'username'>
  createdOn: string
}

export interface BasePoll {
	id: string
	pollType: string
	public: boolean
	question: string
	votersAlone: boolean
  possibilitySet: Arrayable<PossibilitySet>
	createdOn: string
	closingDate: string
	choicesLimit: number
	closes: boolean
	allowVoteChange: boolean
  answerSet: Arrayable<AnswerSet>
	active: boolean
	// answerSet: any[]
}

export type ThreadPoll = GraphQlData<'threadPoll', BasePoll>

export interface BaseThread {
	id: string
	title: string
	user: Pick<BaseUser, 'id' | 'username'>
	forum: Pick<BaseForum, 'id' | 'title'>
	description?: Nullable<string>
	category: string
	pinned: boolean
	highlighted: boolean
	published: boolean
	numberOfComments: number
	ownedByUser: boolean
	// participants: Arrayable<Pick<BaseUser, 'id' | 'username'>>
	active: boolean
	modifiedOn: string
	createdOn: string
}

export type MainThreadNode = RelayNode<BaseThread>

export type SingleMainThread = GraphQlData<'mainThread', BaseThread>

// | GraphQlError<'allMainThreads'>
export type MainThreads = GraphQlData<'allMainThreads', RelayEdge<BaseThread>>

// TODO: Renamae mainThread to parentThread
export type SubThreads = GraphQlData<'allMainThreads', RelayEdge<BaseThread & { mainThread: Pick<BaseThread, 'id' | 'title'> }>>
