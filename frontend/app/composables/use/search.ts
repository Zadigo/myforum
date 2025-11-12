import { updateDoc, doc } from 'firebase/firestore';
import type { SearchApiResponse, Undefineableable, UserSearch } from '~/types'

type _UserSearch = Omit<UserSearch, 'title_only' | 'sub_forums'> & { title_only: false; sub_forums: false }

/**
 * Composable for handling search functionality in a forum application
 * @param fetchData - Boolean indicating whether to fetch search results immediately
 */
export const useSearchComposable = createGlobalState((fetchData = false) => {
  if (import.meta.server) {
    return {
      last: ref<UserSearch | null>(null),
      query: ref<UserSearch | null>(null)
    }
  }

  const newSearch = ref<_UserSearch>({
    q: '',
    title_only: false,
    posted_by: '',
    from_date: '',
    to_date: '',
    search_in_forums: '',
    sub_forums: false
  })

  const fireStore = useFirestore()
  const query = useUrlSearchParams<UserSearch>('history')
  
  watch(newSearch, async (newVal) => {
    if (isDefined(newVal)) {
      query.q = newVal.q ?? ''
      query.title_only = newVal.title_only ? 'true' : 'false'
      query.posted_by = newVal.posted_by ?? ''
      query.from_date = newVal.from_date ?? ''
      query.to_date = newVal.to_date ?? ''
      query.search_in_forums = newVal.search_in_forums ?? ''
      query.sub_forums = newVal.sub_forums ? 'true' : 'false'
    }

    const { sessionId  } = await useSession()

    const docRef = doc(fireStore, 'sessions', sessionId.value || '')
    await updateDoc(docRef, { search: newSearch.value })
  }, { 
    deep: true
  })

  /**
   * Track Last Search
   */
  
  const { last } = useRefHistory(newSearch, { deep: true })

  if (isDefined(query.q)) {
    newSearch.value = {
      q: query.q ?? '',
      title_only: query.title_only === 'true' ? true : false,
      posted_by: query.posted_by ?? '',
      from_date: query.from_date ?? '',
      to_date: query.to_date ?? '',
      search_in_forums: query.search_in_forums ?? '',
      sub_forums: query.sub_forums === 'true' ? true : false
    }
  }

  /**
   * Search Results Fetching
   */

  const results = ref<Undefineableable<SearchApiResponse>>()

  async function _fetchImmediately() {
    const { data, error } = await useFetch<SearchApiResponse>('/v1/search', {
      method: 'get',
      query: newSearch.value
    })

    if (isDefined(error)) {
      console.error('Error fetching search results:', error)
    }

    if (isDefined(data)) {
      results.value = data.value
    }
  }

  const { start }  = useTimeoutFn(_fetchImmediately, 2000)
  
  if (fetchData) {
    start()
  }

  return {
    query,
    newSearch,
    fetchImmediately: start
  }
})
