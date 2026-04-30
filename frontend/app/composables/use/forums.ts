import type { BaseForum, Forums, SingleForum, Undefineable } from '~/types'

export const useForumsComposable = createGlobalState(async () => {
  const forumsList = computedAsync(async () => {
    const data = await $fetch<Forums>('/api/forums', { method: 'GET' })
    return data.data.allForums.edges
  })

  if (import.meta.server) {
    return {
      forumsList,
      forumsByCategory: computed(() => undefined),
      forumCategories: computed(() => []),
      hasForums: computed(() => false)
    }
  }

  const forumsByCategory = computed(() => {
    const groupedForums: Record<string, BaseForum[]> = {}

    if (isDefined(forumsList)) {
      forumsList.value.forEach(item => {
        groupedForums[item.node.category] = []
      })
  
      forumsList.value.forEach(item => {
        const container = groupedForums[item.node.category]
        
        if (isDefined(container)) {
          container.push(item.node)
        }
      })
  
      return groupedForums
    } else {
      return {}
    }
  })

  const forumCategories = computed(() => {
    if (hasForums.value) {
      return Object.keys(forumsByCategory.value)
    } else {
      return []
    }
  })

  const hasForums = computed(() => {
    if (isDefined(forumsList)) {
      return forumsList.value.length > 0
    } else {
      return false
    }
  })

  return {
    forumsList,
    forumsByCategory,
    forumCategories,
    hasForums
  }
})

export async function useForumComposable() {
  const currentForum = ref<Undefineable<SingleForum>>()

  if (import.meta.server) {
    return {
      currentForum,
      showCreateCommentForm: ref<boolean>(false),
      forumThreads: ref([]),
      toggleShowCreateCommentForm: () => {}
    }
  }

  
  const route = useRoute()
  currentForum.value = await $fetch<SingleForum>(`/api/forums/${route.params.id}`, { method: 'GET' })

  const forumThreads = await $fetch(`/api/forums/${route.params.id}/threads`, { method: 'GET' })
  
  const [showCreateCommentForm, toggleShowCreateCommentForm] = useToggle<boolean>(false)

  return {
    currentForum,
    showCreateCommentForm,
    forumThreads,
    toggleShowCreateCommentForm
  }
}

export interface ForumStatistics {
  total_forums: number
  total_threads: number
  total_comments: number
  total_participants: number
  // totalThreads: number
  // totalPosts: number
}

export const useForumStatisticsComposable = createGlobalState(async () => {
  const requestComplete = ref<boolean>(false)

  let statistics = {}
  
  statistics = await $fetch<ForumStatistics>('/v1/forums/statistics', {
    method: 'GET',
    baseURL: useRuntimeConfig().public.prodDomain,
    onResponse() {
      requestComplete.value = true
    },
    onRequestError() {
      console.log('Failed to fetch forum statistics')
    }
  })

  return {
    statistics,
    requestComplete
  }
})
