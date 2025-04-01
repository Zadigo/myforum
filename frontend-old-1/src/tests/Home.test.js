import { shallowMount } from "@vue/test-utils"
import { expect, test } from "vitest"
import TestComponent from '../components/TestComponent.vue'

test('quick test', () => {
    expect(Math.sqrt(4)).toBe(2)
})


test.todo('create this test')

test.each([[1, 1]])('should(%i) -> %i', (value, expected) => {
    expect(value).toBe(expected)
})


test('component test', () => {
    const component = shallowMount(TestComponent)
    
    component.setProps({
        something: 'Incredible'
    })

    expect(component.find('h1').text()).toBe('Incredible')
})
