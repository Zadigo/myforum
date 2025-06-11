/** @type {import('tailwindcss').Config} */

export default {
  content: [
    './components/**/*.{js,vue,ts}',
    './layouts/**/*.vue',
    './pages/**/*.vue',
    './plugins/**/*.{js,ts}',
    './app.vue',
    './error.vue',
    './nuxt.config.{js,ts}'
  ],
  theme: {
    extend: {
      fontFamily: {
        'title': ['var(--font-title)', 'serif'],
        'petrona': ['var(--font-title)', 'serif']
      },
      colors: {},
      screens: {},
    },
  },
  // plugins: [PrimeUI],
  darkMode: 'class',
}
