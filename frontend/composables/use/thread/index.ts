import type { CustomRouteIdParamsGeneric, NewPollData, NewThreadData, ForumThread, TagApiResponse } from '~/types'

export * from './comments'

/**
 * Composable to create a new poll
 * @param newThread The new thread data
 */
export function useCreatePoll(newThread: Ref<NewThreadData>) {
  const newPoll = reactive<NewPollData>({
    question: '',
    possibilities: [
      {
        text: ''
      }
    ],
    choice_selection: 'Single',
    choices_limit: 1,
    allow_vote_change: true,
    display: {
      votes_publicly: false,
      results_without_voting: true
    },
    closing: {
      poll_closes: false,
      days: 7
    }
  })

  if (newThread.value.add_poll) {
    newThread.value.poll = newPoll
  }

  return {
    newPoll
  }
}

/**
 * Composable to create a new thread
 */
export async function useThread() {
  const { id } = useRoute().params as CustomRouteIdParamsGeneric

  const newThread = ref<NewThreadData>({
    forum_id: id,
    title: '',
    result_thread_title: {
      tournament: null,
      round: null,
      winner: null,
      looser: null,
      score: null
    },
    content: {
      delta: null,
      html: null,
      text: null
    },
    category: 'General discussion',
    watch: true,
    tags: [],
    schedule_date: null,
    is_draft: false,
    add_poll: false,
    poll: null
  })

  const router = useRouter()
  const config = useRuntimeConfig()
  const { newPoll } = useCreatePoll(newThread)

  const { data, execute: create, status } = await useFetch<ForumThread>('/v1/threads/create', {
    baseURL: config.public.prodDomain,
    server: false,
    method: 'post',
    immediate: false,
    body: newThread.value
  })

  whenever(() => status.value === 'success', () => {
    if (data.value?.id) {
      router.push({ name: 'thread-id', params: { id: data.value.id } })
    }
  })

  const showSchedulingModal = ref<boolean>(false)
  
  function schedule() {
    showSchedulingModal.value = true
  }

  function draft() {}

  const previewThreadTitle = computed(() => {
    return `${newThread.value.result_thread_title.tournament} ${newThread.value.result_thread_title.round} - ${newThread.value.result_thread_title.winner} defeat ${newThread.value.result_thread_title.looser} - ${newThread.value.result_thread_title.score}`
  })


  return {
    showSchedulingModal,
    previewThreadTitle,
    newPoll,
    newThread,
    create,
    draft,
    schedule
  }
}

/**
 * Composable to manage search tags
 */
export async function useSearchTags(newThread: Ref<NewThreadData>) {
  const search = ref<string>('')
  const tags = ref<string[]>([])
  
  async function searchComplete(e: Event) {
    const { data, execute } = await useFetch<string[]>('/v1/tags/search', {
      baseURL: useRuntimeConfig().public.prodDomain,
      immediate: false,
      method: 'GET',
      query: { q: e.query },
      transform: (response: TagApiResponse[]) => {
        return response.map(tag => tag.name)
      }
    })

    execute()

    tags.value = data.value || []
  }

  return {
    tags,
    search,
    searchComplete
  }
}
