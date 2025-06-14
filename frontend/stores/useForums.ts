import { defineStore } from 'pinia'
import type { Forum, Comment, ForumThreadResults, ForumThread } from '~/types'

export default defineStore('forums', () => {
  const forumsList = ref<Forum[]>([])
  const forumThreads = ref<ForumThreadResults[]>([])
  const threadComments = ref<Comment[]>([])

  const openSearchModal = ref<boolean>(false)

  const currentForum = ref<Forum | undefined>()
  const currentThread = ref<ForumThread | undefined>()
  const showCreateCommentForm = ref<boolean>(false)

  const forumsByCategory = computed((): Record<string, Forum[]> => {
    const groupedForums: Record<string, Forum[]> = {}

    forumsList.value.forEach(item => {
      groupedForums[item.category] = []
    })

    forumsList.value.forEach(item => {
      groupedForums[item.category].push(item)
    })

    return groupedForums
  })

  const forumCategories = computed(() => {
    if (hasForums.value) {
      return Object.keys(forumsByCategory.value)
    } else {
      return []
    }
  })

  const hasForums = computed(() => {
    return forumsList.value.length > 0
  })

  /**
   *
   * @param id The current thread id
   */
  function setCurrentThread(id: string | number) {
    if (forumThreads.value) {
      if (typeof id === 'string') {
        currentThread.value = forumThreads.value.find(thread => thread.id === parseInt(id))
      } else {
        currentThread.value = forumThreads.value.find(thread => thread.id === id)
      }
    }
  }

  return {
    setCurrentThread,
    openSearchModal,
    showCreateCommentForm,
    currentForum,
    currentThread,
    forumCategories,
    forumsByCategory,
    hasForums,
    forumsList,
    forumThreads,
    threadComments
  }
})
