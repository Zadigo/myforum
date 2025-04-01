module.exports = {
    env: {
        node: true,
    },
    parser: 'vue-eslint-parser',
    extends: [
        'eslint:recommended',
        'plugin:vue/vue3-essential',
    ],
    rules: {
        "vue/attributes-order": "warn",
        "vue/v-bind-style": [
            "error",
            "shorthand"
        ],
        "vue/html-quotes": "warn",
        "vue/html-end-tags": "error",
        "vue/attribute-hyphenation": "error",
        "vue/html-indent": "warn",
        "vue/order-in-components": "warn",
        "vue/require-prop-types": "error",
        "vue/require-explicit-emits": "error",
        "vue/v-on-style": "warn",
        "vue/this-in-template": "error",
        "vue/html-self-closing": [
            "error",
            {
                "html": {
                    "void": "never",
                    "normal": "always",
                    "component": "always"
                },
                "svg": "always",
                "math": "always"
            }
        ]
    }
}
