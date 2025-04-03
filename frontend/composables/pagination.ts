export function usePagination(defaultLimit = 50) {
    const currentPage = ref<number>(1)
    const previousPaginationUrl = ref<string | null | undefined>()
    const nextPaginationUrl = ref<string | null | undefined>()

    function urlObject(value: string | null | undefined): URL | null {
        if (value) {
            return new URL(value)
        } else {
            return null
        }
    }

    const nextOffset = computed(() => {
        const obj = urlObject(nextPaginationUrl.value)
        return obj?.searchParams.get('offset') || 0
    })
    
    const nextLimit = computed(() => {
        const obj = urlObject(nextPaginationUrl.value)
        return obj?.searchParams.get('limit') || defaultLimit
    })

    const previousOffset = computed(() => {
        const obj = urlObject(previousPaginationUrl.value)
        return obj?.searchParams.get('offset') || 0
    })
    
    const previousLimit = computed(() => {
        const obj = urlObject(nextPaginationUrl.value)
        return obj?.searchParams.get('limit') || defaultLimit
    })

    const canPaginatePrevious = computed(() => {
        return previousPaginationUrl.value !== null
    })

    const canPaginateNext = computed(() => {
        return nextPaginationUrl.value !== null
    })

    const canPaginate = computed(() => {
        return [canPaginatePrevious.value, canPaginateNext.value].every(x => x !== false)
    })

    function runCallback(func?: (page: number) => void) {
        if (func) {
            func(currentPage.value)
        }
    } 

    function paginatPrevious(callback?: (page: number) => void) {
        const result = currentPage.value - 1
        if (result <= 0) {
            currentPage.value = 0
        } else {
            currentPage.value = result
        }
        
        runCallback(callback)
    }
    
    function paginateNext(callback?: (page: number) => void) {
        const result = currentPage.value + 1
        currentPage.value = result
        runCallback(callback)
    }
    
    function paginateTo(value: number, callback?: (page: number) => void) {
        currentPage.value = value
        runCallback(callback)
    }

    return {
        paginateTo,
        paginatPrevious,
        paginateNext,
        canPaginate,
        canPaginatePrevious,
        canPaginateNext,
        currentPage,
        nextPaginationUrl,
        previousPaginationUrl,
        previousOffset,
        nextOffset,
        previousLimit,
        nextLimit
    }
}
