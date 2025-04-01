import { describe, expect, it } from "vitest";
import { config, mount } from "@vue/test-utils";

import ForumPage from '~/pages/forums/index.vue';

config.global.mocks = {}

describe('ForumPage', () => {
    it('can render', async () => {
        const wrapper = mount(ForumPage, {
            global: {
                stubs: {
                    NuxtLink: true
                }
            }
        })
        
        console.log(wrapper.find('h3'))
        expect(wrapper.find('h3').text()).toEqual('General')
    })
})
