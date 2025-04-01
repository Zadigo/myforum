// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  ssr: true,
  routeRules: {
    '/': { redirect: '/forums' }
  },
  runtimeConfig: {
    public: {
      // Django/Quart/Flask
      djangoProdUrl: process.env.NUXT_DJANGO_PROD_URL,

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
    '@nuxtjs/google-fonts',
    '@nuxt/test-utils/module',
    '@nuxtjs/google-fonts',
    '@unlok-co/nuxt-stripe',
    '@nuxtjs/sitemap',
    '@nuxt/image',
    '@nuxtjs/i18n',
    '@artmizu/nuxt-prometheus',
    'nuxt-gtag',
    'nuxt-clarity-analytics',
    'nuxt-openapi-docs-module',
    'vuetify-nuxt-module',
    'vue-sonner/nuxt'
  ],
  googleFonts: {
    families: {
      "Noto Sans": {
        wght: '100..700'
      }
    }
  },
  gtag: {
    enabled: process.env.NODE_ENV === 'production',
    id: 'G-XX'
  },
  css: [
    '@/assets/style.scss',
    '~/node_modules/bootstrap/dist/css/bootstrap.min.css',
    '~/node_modules/mdb-ui-kit/css/mdb.min.css',
    '~/node_modules/animate.css/animate.min.css'
  ],
  vuetify: {
    moduleOptions: {},
    vuetifyOptions: {}
  },
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
