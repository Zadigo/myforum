import type { Delta } from "@vueup/vue-quill"

export type NewThreadCatategories = 'General discussion' | 'Result' | 'WWW' | 'Bombshell' | 'Draw' | 'Poll' 

export type NewPollChoiceSelection = 'Single' | 'Limited'

export interface NewPollData {
  question: string
  possibilities: { text: string }[]
  choice_selection: NewPollChoiceSelection
  choices_limit: number
  allow_vote_change: boolean
  display: {
    votes_publicly: boolean
    results_without_voting: boolean
  }
  closing: {
    poll_closes: boolean
    days: number
  }
}

export interface NewThreadData {
  forum_id: string | number
  title: string
  result_thread_title: {
    tournament: string | null
    round: string | null
    winner: string | null
    looser: string | null
    score: string | null
  }
  content: {
    delta: string | Delta | null | undefined
    html: string | null
    text: string | null
  }
  category: NewThreadCatategories
  watch: boolean
  tags: string[]
  schedule_date: string | null
  is_draft: boolean
  add_poll: boolean
  poll: PollRequestData | null
}
