import type { Arrayable, NewPollData, NewThreadApiResponse, NewThreadData, RouteIdParamsGeneric, TagApiResponse } from '~/types'

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
export async function useCreateThread() {
  const { id } = useRoute().params as RouteIdParamsGeneric

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

  const { $nuxtAuthentication } = useNuxtApp()

  const [created, toggleCreated] = useToggle(false)

  async function create() {
    const data = await $nuxtAuthentication<NewThreadApiResponse>('/v1/threads/create', {
      method: 'post',
      body: newThread.value,
      onResponse() {
        toggleCreated()
      }
    })

    router.push('/threads/' + data.id)
  }

  /**
   * Draft
   */

  const [showSchedulingModal, schedule] = useToggle(false)
  function draft() { }

  const previewThreadTitle = computed(() => {
    return `${newThread.value.result_thread_title.tournament} ${newThread.value.result_thread_title.round} - ${newThread.value.result_thread_title.winner} defeat ${newThread.value.result_thread_title.looser} - ${newThread.value.result_thread_title.score}`
  })

  /**
   * Poll
   */

  const { newPoll } = useCreatePoll(newThread)

  return {
    created,
    showSchedulingModal,
    previewThreadTitle,
    newPoll,
    newThread,
    create,
    draft,
    schedule
  }
}

interface SearchEvent extends Event {
  query: string
}

/**
 * Composable to manage search tags
 */
export async function useSearchTags(_newThread: Ref<NewThreadData>) {
  const search = ref<string>('')
  const tags = ref<Arrayable<string>>([])

  async function searchComplete(e: SearchEvent) {
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
