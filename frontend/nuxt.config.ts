import tailwindcss from '@tailwindcss/vite'

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  
  ssr: true,
  routeRules: {
    '/': {
      redirect: '/forums',
      swr: true
    },
    'forums/**': {
      swr: true,
      cache: {
        swr: true,
        maxAge: 1*60
      }
    },
    'threads/**/create': {
      swr: false
    },
    'threads/**': {
      swr: true
    },
    'user/**': {
      ssr: false,
      swr: false
    },
    'rules': {
      isr: true
    },
    'search': {
      ssr: false,
      swr: false
    },
    'whats-new': {
      swr: true
    }
  },

  site: {},
  
  vite: {
    plugins: [
      tailwindcss()
    ]
  },

  runtimeConfig: {
    public: {
      // Django/Quart/Flask
      prodDomain: process.env.NUXT_DJANGO_PROD_URL || 'http://127.0.0.1:8000',

      // Firebase
      firebaseApiKey: process.env.NUXT_FIREBASE_API_KEY,
      firebaseAuthDomain: process.env.NUXT_FIREBASE_AUTH_DOMAIN,
      firebaseDbUrl: process.env.NUXT_FIREBASE_DB_URL,
      firebaseStorageBucket: process.env.NUXT_FIREBASE_STORAGE_BUCKET,
      firebaseAppId: process.env.NUXT_FIREBASE_APP_ID,
      firebaseMeasurementId: process.env.NUXT_FIREBASE_MEASUREMENT_ID,
      firebaseMessageSenderId: process.env.NUXT_FIREBASE_MESSAGE_SENDER_ID,
      firebaseProjectId: process.env.NUXT_FIREBASE_PROJECT_ID,

      // Stripe
      // stripeTestSecretKey: process.env.NUXT_STRIPE_TEST_SECRET_KEY,
      // stripeTestPublishableKey: process.env.NUXT_STRIPE_TEST_PUBLISHABLE_KEY,
      // stripeApiVersion: '2024-06-20',
      // stripeLocale: 'fr'
    }
  },

  modules: [
    '@pinia/nuxt',
    '@nuxt/eslint',
    '@vesp/nuxt-fontawesome',
    '@nuxt/test-utils/module',
    // '@nuxtjs/google-fonts',
    '@unlok-co/nuxt-stripe',
    '@nuxtjs/sitemap',
    '@nuxt/image',
    '@nuxtjs/i18n',
    '@nuxt/icon',
    // '@artmizu/nuxt-prometheus',
    'nuxt-gtag',
    'nuxt-clarity-analytics',
    'nuxt-openapi-docs-module',
    'vue-sonner/nuxt',
    '@vueuse/nuxt',
    'pinia-plugin-persistedstate',
    '@nuxt/fonts',
    // 'nuxt-schema-org'
  ],
  
  // googleFonts: {
  //   families: {
  //     'Petrona': {
  //       wght: '100..700'
  //     }
  //   }
  // },

  // https://www.fontpair.co/all
  fonts: {
    provider: 'google',
    families: [
      {
        name: 'Manrope',
        weights: [100, 700],
        display: 'swap'
      },
      // Titles
      {
        name: 'Petrona',
        weights: [100, 700],
        display: 'swap'
      },
      {
        name: 'Faustina',
        weights: [300, 700],
        display: 'swap'
      },
      {
        name: 'Newsreader',
        weights: [200, 700],
        display: 'swap'
      },
      {
        name: 'Work Sans',
        weights: [100, 700],
        display: 'swap'
      }
    ]
  },
  
  gtag: {
    enabled: process.env.NODE_ENV === 'production',
    id: 'G-XX'
  },

  css: [
    '~/assets/css/tailwind.css'
  ],

  fontawesome: {
    icons: {
      solid: [
        'ellipsis-vertical',
        'reply',
        'quote-left',
        'bookmark',
        'share',
        'sort',
        'filter',
        'bars',
        'arrow-down',
        'users',
        'eye'
      ],
      regular: [
        'bookmark'
      ],
      brands: [
        'whatsapp',
        'cc-mastercard',
        'google',
        'instagram',
        'facebook-f',
        'twitter'
      ]
    }
  },

  i18n: {
    baseUrl: './',
    langDir: './locales',
    defaultLocale: 'fr',
    vueI18n: './i18n.config.ts',
    locales: [
      {
        code: 'en',
        language: 'en-US',
        file: 'en-US.json',
        dir: 'ltr',
        name: 'English'
      },
      {
        code: 'fr',
        language: 'fr-FR',
        file: 'fr-FR.json',
        dir: 'ltr',
        name: 'Français'
      }
    ]
  },

  nitro: {
    storage: {
      redis: {
        driver: 'redis',
        host: '127.0.0.1',
        port: 6379,
        username: '',
        password: 'django-local-testing'
      }
    }
  }
})
