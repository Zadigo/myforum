import { useSessionStorage } from '@vueuse/core'
import { z } from 'zod'

import type { Forum } from '~/types'
// import type { SortMethodNames } from '~/data'

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

export function useForumsComposable() {
  const { $nuxtAuthentication } = useNuxtApp()
  const { customHandleError } = useErrorHandler()
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
      const data = await $nuxtAuthentication<Forum[]>('/forums/', { method: 'GET' })
      const validatedData = data.reduce<ValidatedForum[]>((validForums, forum: Forum) => {
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
      customHandleError(error)
    }
  }

  return {
    getForums,
    cachedForums
  }
}
