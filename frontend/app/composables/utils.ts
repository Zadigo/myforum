import { isRef, ref } from 'vue'

export function useUtilities () {
    function scrollToTop () {
        window.scroll({ top: 0, behavior: 'smooth' })
    }

    // TODO: Remove. Use as simple function
    function isNull<T>(item: T): boolean {
        let trueValue

        if (isRef(item)) {
            trueValue = item.value
        } else {
            trueValue = item
        }

        return (
            trueValue === null ||
            typeof trueValue  === 'undefined' ||
            trueValue === '' ||
            trueValue === ' '
        )
    }

    function hasNull<T extends ArrayAnyValues>(items: T): boolean {
        return items.some(v => {
            return v === null || v === '' || typeof v === 'undefined'
        })
    }

    function readFile (e: Event): string | undefined {
        let preview
        const input = e.target as HTMLInputElement

        if (input.files) {
            const file = input.files[0]
            const reader = new FileReader

            reader.onload = e => {
                preview = e.target?.result
            }

            reader.readAsDataURL(file)
        }

        return preview
    }

    function readFiles (e: Event): (string | ArrayBuffer | null | undefined)[] {
        const input = e.target as HTMLInputElement
        
        if (input.files) {
            let preview: string | ArrayBuffer | undefined | null
            const reader = new FileReader

            reader.onload = e => {
                preview = e.target?.result
            }

            return Object.values(input.files).map(f => {
                if (f) {
                    reader.readAsDataURL(f)
                }
                return preview
            }) 
        }
        
        return []
    }

    // function debounce<F extends (...args[]: any[]) => void>(fn: F, delay: number): (...args: Parameters<F>) => void {
    //     let timer: ReturnType<typeof setTimeout>

    //     return function (...args: Parameters<F>) {
    //         clearTimeout(timer)
    //         timer = setTimeout(() => fn(...args), delay)
    //     };
    // }

    return {
        isNull,
        scrollToTop,
        // debounce,
        hasNull,
        readFile,
        readFiles
    }
}

export function useDjangoUtilies () {
    const secure = ref(false)
    const port = ref(8000)
    const paginationUrl = ref<URL>()

    function getBaseUrl() {
        let domain = `127.0.0.1:${port.value}`

        if (process.env.DEV === 'production') {
            domain = process.env.NUXT_DJANGO_PROD_URL || ''
        }

        const loc = secure.value ? 'https://' : 'http://'
        const bits = [loc, domain]
        const url = bits.join('')

        return new URL(url).toString()
    }

    function mediaPath (path: string | null | undefined, altImage?: string | undefined): string | undefined {
        const baseUrl = getBaseUrl()

        if (path) {
            if (path.startsWith('http')) {
                return path
            }

            const fullPath = path.startsWith('/media') ? `${path}` : `/media/${path}`
            return new URL(fullPath, baseUrl).toString()
        } else {
            return altImage
        }
    }

    function builLimitOffset (url: string | null | undefined, limit = 100, offset = 100) {
        let defaultLimit: string | number = 100
        let defaultOffset: string | number = 0

        if (url) {
            paginationUrl.value = new URL(url)

            const potentialLimit = paginationUrl.value.searchParams.get('limit')
            const potentialOffset = paginationUrl.value.searchParams.get('offset')

            defaultLimit = potentialLimit || limit
            defaultOffset = potentialOffset || offset
        }

        const query = new URLSearchParams({ limit: defaultLimit.toString(), offset: defaultOffset.toString() }).toString()
        
        return {
            query,
            limit: defaultLimit,
            offset: defaultOffset 
        }
    }

    return {
        mediaPath,
        getBaseUrl,
        builLimitOffset
    }
}

/**
 * Function to get WebSocket protocol based on current location protocol
 */
export function getWsUrl() {
    const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://'
    return useRuntimeConfig().public.prodDomain.replace(/^https?:\/\//, protocol)
}
