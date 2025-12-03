import vigenereCipher from './viginer.js'

let alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'.split('') 
// ↑ УБРАЛ лишнюю "П" — было 33 буквы и ошибка в индексах

const RUSSIAN_FREQUENCIES = new Map([
    ['О', 0.1098], ['Е', 0.0848], ['А', 0.0799], ['И', 0.0736], ['Н', 0.0670], ['Т', 0.0631],
    ['С', 0.0547], ['Р', 0.0474], ['В', 0.0453], ['Л', 0.0434], ['К', 0.0348], ['М', 0.0320],
    ['Д', 0.0297], ['П', 0.0280], ['У', 0.0261], ['Я', 0.0200], ['Ы', 0.0189], ['Ь', 0.0173],
    ['Г', 0.0168], ['З', 0.0164], ['Б', 0.0159], ['Ч', 0.0145], ['Й', 0.0120], ['Х', 0.0096],
    ['Ж', 0.0094], ['Ш', 0.0071], ['Ю', 0.0063], ['Ц', 0.0048], ['Щ', 0.0036], ['Э', 0.0033],
    ['Ф', 0.0026], ['Ъ', 0.0003]
]);

function getAverageCI(text, u) {
    let columns = [];

    for (let i = 0; i < u; i++) columns.push([]);

    for (let i = 0; i < text.length; i++) {
        columns[i % u].push(text[i]);
    }

    let arrayOfI = [];
    for (let i = 0; i < u; i++) {
        let column = columns[i];
        let N = column.length;
        if (N < 2) continue;

        let freqMap = getColumnNumsCount(column);
        let sumFreqSq = 0;

        for (let count of freqMap.values()) {
            sumFreqSq += count * (count - 1);
        }

        arrayOfI.push(sumFreqSq / (N * (N - 1)));
    }

    if (arrayOfI.length === 0) return 0;

    return arrayOfI.reduce((a, b) => a + b) / arrayOfI.length;
}

function getColumnNumsCount(column) {
    const letterCountMap = new Map(
        Array.from({ length: alphabet.length }, (_, i) => [i, 0])
    );

    for (let char of column) {
        let index = alphabet.indexOf(char);
        if (index !== -1) letterCountMap.set(index, letterCountMap.get(index) + 1);
    }

    return letterCountMap;
}

function VerdictForU(text, u) {
    const avgIoC = getAverageCI(text, u);
    const diff = avgIoC - 0.055; 
    return Math.abs(diff) < 0.01;
}

function getFreqProduct(arr1, arr2) {
    return Array.from({ length: alphabet.length }, (_, i) =>
        arr1.get(i) * arr2.get(i)
    );
}

function getMatrixCI(text, u) {
    let columns = Array.from({ length: u }, () => []);

    for (let i = 0; i < text.length; i++) {
        columns[i % u].push(text[i]);
    }

    let MatrixMI = new Array(u - 1);
    let firstColumn = columns[0];
    let firstColumnLength = firstColumn.length;
    let firstColumnFreq = getColumnNumsCount(firstColumn);

    for (let i = 1; i < u; i++) {
        let column = columns[i];
        let colLength = column.length;

        let colFreq = getColumnNumsCount(column);
        let freqs = getFreqProduct(firstColumnFreq, colFreq);

        let freqSum = freqs.reduce((acc, cur) => acc + cur, 0);
        MatrixMI[i - 1] = freqSum / (firstColumnLength * colLength);
    }

    return MatrixMI;
}

const txt = `ЁЛНВ ВВ`

for (let i = 2; i < 10; i++) {
    console.log(getAverageCI(txt.replace(/[,.\s+]/g, ''), i))
}

let f = getMatrixCI(txt.replace(/[,.\s+]/g, ''), 3);
console.log(f);
