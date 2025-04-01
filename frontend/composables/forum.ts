import type { Forum, Thread } from "~/types"
import { z } from 'zod'
import { useSessionStorage } from "@vueuse/core"

const ForumSchema = z.object({
    id: z.number().int().positive(),
    title: z.string(),
    category: z.string(),
    description: z.string(),
    admin: z.boolean(),
    number_of_threads: z.number().positive(),
    active: z.boolean(),
    created_on: z.string().datetime()
})

type ValidatedForum = z.infer<typeof ForumSchema>

export function useForumsComposable () {
    const { $client } = useNuxtApp()
    const { handleError } = useErrorHandler()
    const { forumsList } = storeToRefs(useForums())

    const cachedForums = useSessionStorage('forums', [], {
        serializer: {
            read(raw) {
                return JSON.parse(raw)
            },
            write(value) {
                return JSON.stringify(value)
            },
        }
    })

    async function getForums() {
        try {
            const response = await $client.get<Forum[]>('/forums/')
            const validatedData = response.data.reduce<ValidatedForum[]>((validForums, forum: Forum) => {
                try {
                    const validItem = ForumSchema.parse(forum)
                    validForums.push(validItem)
                } catch (error) {
                    console.warn(`Failed to validate forum item: ${error}`)
                }
                return validForums
            }, [])

            forumsList.value = validatedData
            cachedForums.value = validatedData
        } catch (error) {
            handleError(error)
        }
    }

    return {
        getForums,
        cachedForums
    }
}

// const ThreadSchema = z.object({
//     id: z.number().int().positive()
// })

// type ValidateThread = z.infer<typeof ThreadSchema>

export function useThreadsComposable () {
    const { $client } = useNuxtApp()
    const { handleError } = useErrorHandler()
    const { forumThreads } = storeToRefs(useForums())
    const route = useRoute()

    const categories = computed(() => {
        const result = forumThreads.value.map(thread => {
            return thread.category
        })
        return Array.from(new Set(result))
    })


    const cachedThreads = useSessionStorage('threads', null, {
        serializer: {
            read(raw) {
                return JSON.parse(raw)
            },
            write(value) {
                return JSON.stringify(value)
            }
        }
    })

    async function getThreads(id: string, sort = 0) {
        try {
            const response = await $client.get<Thread[]>(`/forums/${id}`, { params: { sort } })
            forumThreads.value = response.data
            cachedThreads.value = response.data
        } catch (e) {
            handleError(e)
        }
    }

    async function sortThreads (index: number) {
        await getThreads(route.params.id, index)
    }

    return {
        getThreads,
        sortThreads,
        categories
    }
}
