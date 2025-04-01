import { useAuthentication } from '../store/authentication'
import { scrollToTop, loadView } from '@/composables/utils'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(),
    scrollBehavior: scrollToTop,
    routes: [
        {
            path: '/',
            name: 'home_view',
            redirect: '/forums'
        },
        {
            path: '/profile/:id(\\d+)',
            name: 'profile_view',
            component: loadView('ProfileView'),
            meta: {
                requiresAuthentication: true
            }
        },
        {
            path: '/forums',
            name: 'forums_view',
            component: loadView('forums/ForumsView')
        },
        {
            path: '/forums/:id(\\d+)',
            name: 'forum_view',
            component: loadView('forums/ForumView')
        },
        {
            path: '/threads/:id(\\d+)',
            name: 'thread_comments_view',
            component: loadView('forums/CommentsView')
        },
        {
            path: '/forums/:id(\\d+)/thread/create',
            name: 'create_thread_view',
            component: loadView('forums/CreateThreadView'),
            meta: {
                requiresAuthentication: true
            }
        },
        {
            path: '/search',
            name: 'search_view',
            component: loadView('SearchView')
        },
        {
            path: '/site-rules',
            name: 'site_rules_view',
            component: loadView('SiteRulesView')
        },
        {
            path: '/whats-new',
            name: 'whats_new_view',
            component: loadView('forums/WhatsNewView')
        }
    ]
})

router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuthentication) {
        const store = useAuthentication()
        if (!store.isAuthenticated) {
            // pass
            next()
        }
    }
    next()
})

export default router
