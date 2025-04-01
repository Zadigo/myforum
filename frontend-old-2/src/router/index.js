import { createRouter, createWebHistory, isNavigationFailure } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  scrollBehavior: async () => ({ top: 0, left: 0 }),
  routes: [
    {
      path: '/',
      redirect: '/forums'
    },
    {
      path: '/forums',
      name: 'forums_view',
      component: async () => import('../pages/forums/ForumsPage.vue')
    },
    {
      path: '/forums/:id(\\d+)',
      name: 'forum_view',
      component: async () => import('../pages/forums/ForumPage.vue')
    },
    {
      path: '/threads/:id(\\d+)',
      name: 'thread_comments_view',
      component: async () => import('../pages/forums/CommentsPage.vue')
    },
    {
      path: '/forums/:id(\\d+)/thread/create',
      name: 'create_thread_view',
      component: async () => import('../pages/forums/CreateThreadPage.vue'),
      meta: {
        requiresAuthentication: true
      }
    },
    {
      path: '/search',
      name: 'search_view',
      component: async () => import('../pages/SearchPage.vue')
    },
    {
      path: '/site-rules',
      name: 'site_rules_view',
      component: async () => import('../pages/SiteRulesPage.vue')
    },
    {
      path: '/whats-new',
      name: 'whats_new_view',
      component: async () => import('../pages/forums/WhatsNewPage.vue')
    },
    {
      path: '/profile/:id(\\d+)',
      name: 'profile_view',
      component: async () => import('../pages/ProfilePage.vue'),
      meta: {
        requiresAuthentication: true
      }
    }
  ]
})

router.beforeEach((to, from, next) => {
  next()
})

router.afterEach((to, from, failure) => {
  if (isNavigationFailure(failure)) {
    // pass
  }
})

export default router
