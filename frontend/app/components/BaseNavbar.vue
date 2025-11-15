<template>
  <nav class="bg-primary-100 dark:bg-primary-900 z-20 text-primary-100 fixed top-0 left-0 w-full shadow-sm">
    <div class="mx-auto max-w-7xl px-2 sm:px-6 lg:px-8">
      <div class="relative flex h-16 items-center justify-between">
        <div class="absolute inset-y-0 left-0 flex items-center sm:hidden">
          <!-- Mobile menu button-->
          <button type="button" class="relative inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-700 hover:text-white focus:ring-2 focus:ring-white focus:outline-hidden focus:ring-inset" aria-controls="mobile-menu" aria-expanded="false">
            Mobile button
          </button>
        </div>

        <div class="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
          <div class="flex shrink-0 items-center">
            <nuxt-link to="/" class="uppercase text-primary-900 dark:text-primary-100 font-extrabold">
              Forum
            </nuxt-link>
          </div>

          <div class="hidden sm:ml-6 sm:block">
            <div class="flex space-x-4">
              <a href="#" class="rounded-md bg-gray-900 px-3 py-2 text-sm font-medium" aria-current="page">Dashboard</a>
              <a href="#" class="rounded-md px-3 py-2 text-sm font-medium text-gray-300 hover:bg-gray-700 hover:text-white" @click.prevent="() => searchModal = true">
                Search
              </a>
            </div>
          </div>
        </div>

        <div class="absolute inset-y-0 right-0 flex items-center space-x-2 pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
          <client-only>
            <template #default>
              <volt-toggle-switch v-model="darkMode">
                <template #handle="{ checked }">
                  <icon :name="checked ? 'i-lucide:moon' : 'i-lucide:sun'" />
                </template>
              </volt-toggle-switch>
            </template>
          </client-only>

          <volt-secondary-button>
            <icon name="i-lucide:bell" />
          </volt-secondary-button>

          <client-only>
            <template #default>
              <volt-dropdown id="profile" :items="profileItems">
                <template #default="{ attrs }">
                  <img class="size-8 rounded-full" src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" alt="" @click="attrs.toggle">
                </template>
              </volt-dropdown>
            </template>

            <template #fallback>
              Loading...
            </template>
          </client-only>
        </div>
      </div>
    </div>

    <div id="mobile-menu" class="sm:hidden">
      <div class="space-y-1 px-2 pt-2 pb-3">
        <a href="#" class="block rounded-md bg-gray-900 px-3 py-2 text-base font-medium text-white" aria-current="page">Dashboard</a>
        <a href="#" class="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-gray-700 hover:text-white">Team</a>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
const loginModal = useState<boolean>('loginModal')
const searchModal = useState<boolean>('searchModal')

/**
 * Notifications
 */

// const { notifications } = useNotificationsComposable()
// console.log('Notifications:', notifications.value)

const { notifications, count } = useWsNotificationComposable()

/**
 * Dark Mode
 */

const [darkMode, _] = useToggle()

if (import.meta.client) {
  const colorMode = useColorMode({
    initialValue: 'system',
    onChanged (mode, defaultHandler) {
      if (mode == 'dark') {
        document.documentElement.classList.add('p-dark')
        defaultHandler(mode)
      } else {
        document.documentElement.classList.remove('p-dark')
        defaultHandler(mode)
      }
    }
  })
  
  watch(darkMode, (newValue) => {
    colorMode.value = newValue ? 'dark' : 'light'
  })
  
  onMounted(() => {
    darkMode.value = colorMode.value === 'dark' || (colorMode.value === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches)
  })
}

/**
 * Dropdown
 */

const profileItems = [
  {
    label: 'Login',
    command: () => {
      loginModal.value = true
    }
  },
  {
    label: 'Sign out',
    command: async () => {
      await useLogout()
    }
  }
]
</script>
