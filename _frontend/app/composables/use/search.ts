import type { CustomRouteParamsGeneric, SearchApiResponse } from '~/types'

/**
 * Composable for handling search functionality in a forum application. 
 */
export async function useSearch<T>() {
  const search = ref<string>('')
  const results = reactive<T[]>([])
  const { q } = useRoute().params as CustomRouteParamsGeneric
  
  const { data, error } = await useFetch('/v1/search',{
    watch: [search],
    query: {
      q
    }
  })

  const hasResults = computed(() => results.length > 0)

  return {
    search,
    hasResults,
    results
  }
}

/**
 * Composable for advanced search functionality in a forum application.
 */
export async function useAdvancedSearch<T>() {
  const { search, results } = await useSearch()
  
  return {
    results,
    search
  }
}
