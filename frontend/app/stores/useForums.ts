import { defineStore } from 'pinia'
import type { Forum, UserComment, ForumThreadResults, ForumThread } from '~/types'

export default defineStore('forums', () => {
  const forumsList = ref<Forum[]>([])
  const threadComments = ref<UserComment[]>([])
  
  const openSearchModal = ref<boolean>(false)

  const currentForum = ref<Forum | undefined>()
  const showCreateCommentForm = ref<boolean>(false)
  
  const forumsByCategory = computed((): Record<string, Forum[]> => {
    const groupedForums: Record<string, Forum[]> = {}

    forumsList.value.forEach(item => {
      groupedForums[item.category] = []
    })

    forumsList.value.forEach(item => groupedForums[item.category].push(item))

    return groupedForums
  })

  const forumCategories = computed(() => {
    if (hasForums.value) {
      return Object.keys(forumsByCategory.value)
    } else {
      return []
    }
  })

  /**
   * Current thread
   */

  const forumThreads = ref<ForumThreadResults[]>([])
  const currentThread = ref<ForumThread | undefined>()
  const hasForums = computed(() => forumsList.value.length > 0)

  /**
   * Sets the current forum being viewed
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
    /**
     * The current forum being viewed
     */
    currentForum,
    /**
     * The current thread being viewed
     */
    currentThread,
    forumCategories,
    forumsByCategory,
    hasForums,
    forumsList,
    /**
     * Returns the threads for the current forum
     */
    forumThreads,
    /**
     * Returns the comments for the current thread
     */
    threadComments
  }
}, {
  persist: {
    pick: ['currentForum', 'threadComments', 'currentThread']
  }
})
