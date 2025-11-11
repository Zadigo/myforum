import tailwindcss from '@tailwindcss/vite'
import { defineOrganization } from 'nuxt-schema-org/schema'

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
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
        maxAge: 1 * 60
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

  nuxtAuthentication: {
    enabled: false,
    domain: import.meta.env.NUXT_PUBLIC_DJANGO_PROD_URL,
    accessEndpoint: '/v1/auth/login/',
    refreshEndpoint: '/v1/auth/refresh/',
    login: '/login/',
    bearerTokenType: 'Token',
    strategy: 'renew'
  },

  runtimeConfig: {
    public: {
      prodDomain: process.env.NUXT_PUBLIC_PROD_DOMAIN
    }
  },

  site: {
    url: process.env.NUXT_PUBLIC_DJANGO_PROD_URL || 'http://localhost:3000'
  },

  modules: [
    '@nuxt/eslint',
    '@nuxt/fonts',
    '@nuxt/icon',
    '@nuxt/image',
    '@nuxt/scripts',
    '@nuxt/test-utils',
    '@pinia/nuxt',
    '@vueuse/nuxt',
    '@nuxtjs/sitemap',
    '@unlok-co/nuxt-stripe',
    '@nuxtjs/i18n',
    '@nuxt/icon',
    '@nuxt/fonts',
    'nuxt-authentication',
    'pinia-plugin-persistedstate',
    'nuxt-schema-org',
    'nuxt-vuefire'
  ],

  vuefire: {
    config: {
      apiKey: process.env.NUXT_PUBLIC_FIREBASE_API_KEY,
      authDomain: process.env.NUXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
      dbUrl: process.env.NUXT_PUBLIC_FIREBASE_DB_URL,
      storageBucket: process.env.NUXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
      appId: process.env.NUXT_PUBLIC_FIREBASE_APP_ID,
      measurementId: process.env.NUXT_PUBLIC_FIREBASE_MEASUREMENT_ID,
      messageSenderId: process.env.NUXT_PUBLIC_FIREBASE_MESSAGE_SENDER_ID,
      projectId: process.env.NUXT_PUBLIC_FIREBASE_PROJECT_ID
    }
  },

  vite: {
    plugins: [
      tailwindcss(),
    ]
  },

    schemaOrg: {
    identity: defineOrganization({
      '@type': 'onlineStore',
      name: 'E-Woman',
      alternateName: 'The E-Woman',
      description: 'A description for the e-woman e-commerce website',
      foundingDate: '2015-01-01',
      numberOfEmployees: {
        '@type': 'QuantitativeValue',
        value: 100
      },
      legalName: 'E-Woman Inc.',
      taxID: '47-1234567',
      vatID: 'EU123456789',
      address: {
        '@type': 'PostalAddress',
        streetAddress: '100 Commerce Way, Suite 300',
        addressLocality: 'Portland',
        addressRegion: 'OR',
        postalCode: '97201',
        addressCountry: 'US'
      },
      hasMerchantReturnPolicy: {
        '@type': 'MerchantReturnPolicy',
        name: 'Standard Return Policy',
        inStoreReturnsOffered: false,
        merchantReturnDays: '30',
        returnPolicyCategory: 'https://schema.org/MerchantReturnFiniteReturnWindow',
        returnMethod: ['ReturnByMail'],
        returnFees: 'https://schema.org/FreeReturn',
        returnPolicyCountry: {
          '@type': 'Country',
          name: ['US', 'CA', 'GB', 'AU', 'NZ']
        }
      },
      shippingDetails: {
        '@type': 'OfferShippingDetails',
        shippingRate: {
          '@type': 'MonetaryAmount',
          value: '0',
          currency: 'EUR'
        },
        shippingDestination: {
          '@type': 'DefinedRegion',
          addressCountry: ['FR', 'GP']
        },
        deliveryTime: {
          '@type': 'ShippingDeliveryTime',
          handlingTime: {
            '@type': 'QuantitativeValue',
            minValue: 1,
            maxValue: 2,
            unitCode: 'DAY'
          },
          'transitTime': {
            '@type': 'QuantitativeValue',
            minValue: 3,
            maxValue: 7,
            unitCode: 'DAY'
          }
        }
      },
      paymentAccepted: [
        'Credit Card',
        'PayPal',
        'Apple Pay',
        'Google Pay',
      ],
      currenciesAccepted: ['EUR'],
      sameAs: [
        'https://facebook.com/modernhome',
        'https://instagram.com/modernhome',
        'https://pinterest.com/modernhome',
        'https://twitter.com/modernhome'
      ],
      openingHoursSpecification: [
        {
          '@type': 'OpeningHoursSpecification',
          dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
          opens: '09:00:00',
          closes: '18:00:00'
        }
      ],
      contactPoint: [
        {
          '@type': 'ContactPoint',
          contactType: 'customer service',
          telephone: '+1-888-555-0123',
          email: 'support@modernhome.com',
          availableLanguage: ['English', 'French'],
          hoursAvailable: {
            '@type': 'OpeningHoursSpecification',
            dayOfWeek: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
            opens: '09:00:00',
            closes: '18:00:00'
          }
        },
        {
          '@type': 'ContactPoint',
          contactType: 'sales',
          telephone: '+1-888-555-0124',
          email: 'sales@modernhome.com'
        }
      ]
    })
  },

  css: [
    '~/assets/css/main.css'
  ],

    fonts: {
    families: [
      // Body
      {
        name: 'Sora',
        weight: [100, 800],
        styles: ['normal', 'italic'],
        preload: true
      },
      // Title
      {
        name: 'Manrope',
        weight: [200, 800],
        styles: ['normal', 'italic'],
        preload: true
      }
    ]
  },

  stripe: {
    server: {
      key: process.env.NUXT_PUBLIC_STRIPE_PUBLISHABLE_KEY
    },
    client: {
      key: process.env.NUXT_PUBLIC_STRIPE_PUBLISHABLE_KEY
    }
  },

    image: {
    // TODO: Activate when the project images backend
    // is set correctly to cloudefare/aws
    // https://image.nuxt.com/providers/cloudflare
    provider: 'none'
  },

  i18n: {
    baseUrl: './',
    langDir: './locales',
    defaultLocale: 'fr',
    lazy: true,
    vueI18n: './i18n.config.ts',
    // bundle: {
    //   // TODELETE:  bundle.optimizeTranslationDirective is enabled by default, we recommend 
    //   // disabling this feature as it causes issues and will be deprecated in v10.
    //   optimizeTranslationDirective: false
    // },
    // customRoutes: 'config',
    locales: [
      {
        code: 'en',
        language: 'en-US',
        file: 'en-US.ts',
        dir: 'ltr',
        name: 'English'
      },
      {
        code: 'es',
        language: 'es-ES',
        file: 'es-ES.ts',
        dir: 'ltr',
        name: 'Spanish'
      },
      {
        code: 'fr',
        language: 'fr-FR',
        file: 'fr-FR.ts',
        dir: 'ltr',
        name: 'Français'
      }
    ],
    // pages: {
    //   'guide': { fr: '/guide-achat', en: '/guide-achat', es: '/guide-achat' },
    //   'wishlist': { fr: '/liste-souhait', en: '/wishlist', es: '/wishlist' },
    //   'mentions-legales': { fr: '/mentions-legales', en: '/mentions-legales', es: '/mentions-legales' },
    //   'confidentialite': { fr: '/confidentialite', en: '/confidentialite', es: '/confidentialite' },
    //   'conditions-generales': { fr: '/conditions-generales', en: '/conditions-generales', es: '/conditions-generales' },

    //   'shop-id': { fr: '/boutique/[id]', en: '/shop/[id]', es: '/tienda/[id]' },
    //   'shop-collection-id': { fr: '/boutique/collection/[id]', en: '/shop/collection/[id]', es: '/tienda/collecion/[id]' },

    //   'cart': { fr: '/cart', en: '/cart', es: '/cart' },
    //   'cart-shipment': { fr: '/panier/livraison', en: '/cart/shipment', es: '/cart/shipment' },
    //   'cart-payment': { fr: '/panier/paiement', en: '/cart/payment', es: '/cart/payment' },
    //   'cart-success': { fr: '/panier/recapitulatif', en: '/cart/success', es: '/cart/success' },

    //   'account': { fr: '/compte', en: '/account', es: '/account' },
    //   'orders': { fr: '/compte/commandes', en: '/account/orders', es: '/account/orders' },
    // }
  },

  nitro: {
    prerender: {
      routes: [
        '/mentions-legales',
        '/confidentialite'
      ]
    },
    storage: {
      redis: {
        driver: 'redis',
        host: process.env.NUXT_PUBLIC_REDIS_HOST,
        port: 6379,
        username: process.env.NUXT_PUBLIC_REDIS_USER,
        password: process.env.NUXT_PUBLIC_REDIS_PASSWORD
      }
    },
    devStorage: {
      redis: {
        driver: 'redis',
        host: '127.0.0.1',
        port: 6379,
        username: '',
        password: ''
      }
    }
  }
})
