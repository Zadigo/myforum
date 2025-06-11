import { FetchError } from 'ofetch'
import { refreshAccessToken } from '~/utils'

import type { Forum } from '~/types'

export default defineCachedEventHandler(async event => {
  const access = getCookie(event, 'access')
  const refresh = getCookie(event, 'refresh')
  
  try {
    // const response = await client.get<Forum[]>('/v1/forums/')
    // return response.data
    
    return await $fetch<Forum>(`/v1/forums/`, {
      baseURL: useRuntimeConfig().public.prodDomain,
      method: 'GET',
      headers: [
        ['Authorization', access ? `Token ${access}` : '']
      ]
    })
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

  // return [
  //     {
  //         id: 1,
  //         active: true,
  //         number_of_threads: 14,
  //         admin: false,
  //         category: 'General',
  //         created_on: '2025-1-1',
  //         description: 'A quick description',
  //         title: 'My General forum',
  //         user: 'Google User'
  //     }
  // ]
}, {
  base: 'fs',
  maxAge: 1 * 60,
  name: 'forums'
})
