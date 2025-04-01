export function useBackdrop() {
    function createBackdrop() {
        var backDrop = document.querySelector('.dropdown-backdrop')

        if (!backDrop) {
            var section = document.querySelector('section#forum')
            backDrop = document.createElement('div')
            var klass = document.createAttribute('class')

            backDrop.addEventListener('click', () => {
                console.log('clicked')
            })

            klass.value = 'dropdown-backdrop'
            backDrop.attributes.setNamedItem(klass)
            section.append(backDrop)
        } else {
            backDrop.style.display = 'block'
        }
    }

    function removeBackdrop() {
        var backDrop = document.querySelector('.dropdown-backdrop')
        backDrop.style.display = 'none'
    }

    return {
        createBackdrop,
        removeBackdrop
    }
}
