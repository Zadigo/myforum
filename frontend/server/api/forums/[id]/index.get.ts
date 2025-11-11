// import { useAxiosClient } from "~/composables/django_client"

import { FetchError } from 'ofetch'
import { refreshAccessToken } from 'nuxt-authentication'

import type { Forum } from '~/types'

export default defineCachedEventHandler(async event => {
  // const { sort } = getQuery(event)
  // const id = getRouterParam(event, 'id')
  // const { client } = useAxiosClient()
  // const response = await client.get<Thread[]>(`/forums/${id}`, {
  //     params: {
  //         sort
  //     }
  // })
  // return response.data

  // const data: Forum = {
  //     active: true,
  //     admin: false,
  //     category: 'Sports',
  //     created_on: '2025-1-1',
  //     description: 'Some quick description',
  //     id: 1,
  //     number_of_threads: 12,
  //     title: 'My forum title',
  //     user: {
  //         id: 1,
  //         email: 'user@gmail.com',
  //         username: 'some-user',
  //         userprofile: {
  //             blocked_users: 'google',
  //             is_premium: false,
  //             preferred_topics: 'some topic'
  //         }
  //     }
  // }

  // return data

  const id = getRouterParam(event, 'id') as string
  const access = getCookie(event, 'access')
  const refresh = getCookie(event, 'refresh')

  console.log('getRouterParam', id)

  try {
    const data = await $fetch<Forum>(`/v1/forums/${id}`, {
      baseURL: useRuntimeConfig().public.prodDomain,
      method: 'GET',
      headers: [
        ['Authorization', access ? `Token ${access}` : '']
      ]
    })
    return data
  } catch (e) {
    if (e instanceof FetchError) {
      if (e.status === 401 && refresh) {
        const { access } = await refreshAccessToken(refresh)
        setCookie(event, 'access', access)
      } else {
        throw createError({
          statusCode: e.status || 500,
          message: e.message
        })
      }
    }
  }
}, {
  base: 'fs',
  maxAge: 1 * 60,
  getKey() {
    return 'forum'
  }
})
