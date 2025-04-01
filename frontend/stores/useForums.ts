import { defineStore } from "pinia";
import type { Forum, Comment, Thread } from "~/types/forums";

export default defineStore('forums', () => {
    const forumsList = ref<Forum[]>([])
    const forumThreads = ref<Thread[]>([])
    const threadComments = ref<Comment[]>([])
    const openSearchModal = ref(false)
    
    const currentForum = ref<Forum | undefined>()
    const currentThread = ref<Thread | undefined>()
    const showCreateCommentForm = ref(false)

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
