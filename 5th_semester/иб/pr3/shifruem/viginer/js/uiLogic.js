import modifiedViginer from './modifiedViginer.js'
import viginer from './viginer.js'
import streamVig from './testModification.js'

let isModified = true

document.addEventListener('DOMContentLoaded', function(){

    let resultFieldElement = document.getElementById('resultOutput')

    const setResultField = (resultText) => {
        resultFieldElement.innerText = resultText
    }

    const keyInputElement = this.getElementById('vigenereKey')
    const textInputElement = this.getElementById('inputText')

    
    let encryptBtn = this.getElementById('get-keys')
    let decryptBtn = this.getElementById('decrypt-btn')

    async function encAndDec(isDecr){
        let key = keyInputElement.value
        let text = textInputElement.value
        console.log('key', key)
        console.log('text', text)

        if(isModified){
            const encoder = new TextEncoder();
            let seed = encoder.encode(key)
            if (isDecr){
                let resText = await streamVig.encryptVigenereText(text, seed)
                setResultField(resText)
            }else{
                let resText = await streamVig.decryptVigenereText(text, seed)
                setResultField(resText)
            }
            

        }else{
            let resText = viginer(text, key, isDecr)
            setResultField(resText)
        }
        
    }

    decryptBtn.addEventListener('click', () => {encAndDec(false).then(() => {
        console.log("Расшифровано")
    })})
})