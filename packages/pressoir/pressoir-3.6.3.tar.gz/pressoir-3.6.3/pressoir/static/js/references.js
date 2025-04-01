function zip(rows) {
    return rows[0].map((_, index) => rows.map((row) => row[index]))
}

function transformCitation(citation) {
    const cites = citation.dataset.cites
    const content = citation.textContent
    if (!content) {
        return
    }
    // We remove initial parentheses.
    const innerContent = content.slice(1, -1)
    if (cites === '') {
        return
    }
    if (cites.indexOf(' ') > -1) {
        if (innerContent.indexOf(';') === -1 && innerContent.indexOf(',') === -1) {
            return
        }
        const linkCitations = []
        for (const [cite, inner] of zip([
            cites.split(' '),
            innerContent.split(';').flatMap((i) => i.split(',')),
        ])) {
            const linkCitation = document.createElement('a')
            linkCitation.setAttribute('href', `#ref-${cite}`)
            linkCitation.textContent = inner.trim()
            linkCitations.push(linkCitation.outerHTML)
        }
        citation.innerHTML = `(${linkCitations.join(', ')})`
    } else {
        const linkCitation = document.createElement('a')
        linkCitation.setAttribute('href', `#ref-${cites}`)
        linkCitation.textContent = innerContent.trim()
        citation.innerHTML = `(${linkCitation.outerHTML})`
    }
}

function capitalize(string) {
    return string.replace(/\b\w/g, (c) => c.toUpperCase())
}

function handleReference(referenceLink, reference, fromBibliography) {
    const content = reference.textContent
        .trim()
        .replace(/(?:https?|ftp):\/\/[\n\S]+/g, '') // Remove links.
    let onelinerContent = content
        .split('\n')
        .map((fragment) => fragment.trim()) // Remove new lines.
        .join(' ')
    if (onelinerContent.startsWith('———.')) {
        const ref = document.querySelector(referenceLink.hash)
        let previousRef = ref.previousElementSibling
        let previousRefContent = previousRef.textContent.trim()
        while (previousRefContent.startsWith('———.')) {
            previousRef = previousRef.previousElementSibling
            previousRefContent = previousRef.textContent.trim()
        }
        const previousNames = previousRefContent.split('.')[0].trim()
        onelinerContent = onelinerContent.replace('———.', `${previousNames}.`)
    }
    if (fromBibliography) {
        referenceLink.href = `bibliographie.html${referenceLink.hash}`
    }
    referenceLink.setAttribute('aria-label', onelinerContent)
    const balloonLength = window.screen.width < 760 ? 'medium' : 'xlarge'
    referenceLink.dataset.balloonLength = balloonLength

    /* Open references on click. */
    referenceLink.addEventListener('click', (e) => {
        references.parentElement.setAttribute('open', 'open')
        // Waiting to reach the bottom of the page then scroll up a bit
        // to avoid the fixed header. Fragile.
        setTimeout(() => {
            window.scrollTo({
                top: window.scrollY - 130,
                behavior: 'smooth',
            })
        }, 10)
    })
}

function tooltipReference(referenceLink) {
    /* Put attributes for balloon.css to render tooltips. */
    const reference = document.querySelector(referenceLink.hash)
    if (reference) {
        handleReference(referenceLink, reference)
    } else {
        fetch('bibliographie.html')
            .then((response) => response.text())
            .then((body) => {
                const tempDiv = document.createElement('div')
                tempDiv.innerHTML = body
                return tempDiv.querySelector(referenceLink.hash)
            })
            .then((reference) => handleReference(referenceLink, reference, true))
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const references = document.querySelector('#references')
    const chapter = document.body.dataset.chapitre
    if (!chapter || !references) {
        return
    }

    /* Transform citations from contenuadd (converted as <span>s by Pandoc
     because we set `suppress-bibliography` to true). */
    Array.from(document.querySelectorAll('[data-cites]')).forEach(transformCitation)

    /* Setup balloons tooltips for references. */
    Array.from(document.querySelectorAll('[href^="#ref-"]')).forEach(tooltipReference)
})
