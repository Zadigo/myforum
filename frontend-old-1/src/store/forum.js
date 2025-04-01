import _, { toNumber } from 'lodash'
import { defineStore } from 'pinia'
// import { computed } from 'vue'

// const useThreads = defineStore('threads', {
//     state: () => ({
//         currentThread
//     })
// }) 

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
            var forums = this.vueSession.retrieve('forums')
            var threads = this.vueSession.retrieve('threads')
            
            this.forums = forums ? forums : []
            this.threads = threads ? threads : []
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
            return this.forums.length > 0
        }
    }
})

export {
    useForum
}
