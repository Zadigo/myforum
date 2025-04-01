export function inProduction() {
    return process.env.NODE_ENV !== 'development'
}
