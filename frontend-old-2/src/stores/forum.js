import _, { toNumber } from 'lodash'
import { defineStore } from 'pinia'

const useForum = defineStore('forum', {
    state: () => ({
        forums: [],
        threads: [],
        currentForum: {},
        currentThread: {},

        openSearchModal: false,
        openLoginModal: false
    }),
    actions: {
        loadFromCache() {
            const forums = this.$session.retrieve('forums')
            const threads = this.$session.retrieve('threads')
            
            this.forums = forums || []
            this.threads = threads || []
        },
        setCurrentForum(id) {
            // TODO: Maybe check if there are no threads
            // to reload them from the session
            this.currentForum = _.find(this.forums, { id: toNumber(id) })
        },
        setCurrentThread(thread) {
            if (typeof thread === 'object') {
                this.currentThread = thread
            } else {
                this.currentThread = _.find(this.threads, ['id', toNumber(thread)])
            }
        }
    },
    getters: {
        forumsByGroup() {
            // Groups each forum by category
            var groupedForums = {}

            _.forEach(this.forums, (forum) => {
                groupedForums[forum.category] = []
            })

            _.forEach(this.forums, (forum) => {
                groupedForums[forum.category].push(forum)
            })

            return groupedForums
        },
        hasForums() {
            // Checks if there are forums available
            // on the current website
            return this.forums.length > 0
        }
    }
})

export {
    useForum
}
