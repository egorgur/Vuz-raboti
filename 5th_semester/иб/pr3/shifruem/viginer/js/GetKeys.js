
/*
import vigenereCipher from './viginer.js'


let alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩПЪЫЬЭЮЯ'.split('')

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
    console.log("u:", u)
    for (let i = 0; i < u; i++) {
        columns.push([]);
    }
    for (let i = 0; i < text.length; i++) {
        columns[i % u].push(text[i]);
    }

    let arrayOfI = [];
    for (let i = 0; i < u; i++) {
        let column = columns[i];
        let N = column.length;
        if (N < 2) continue; // Избегаем деления на 0

        let freqMap = getColumnNumsCount(column);
        let sumFreqSq = 0;
        for (let count of freqMap.values()) {
            sumFreqSq += count * (count - 1);
        }
        let ioc = sumFreqSq / (N * (N - 1));
        arrayOfI.push(ioc);
    }

    if (arrayOfI.length === 0) return 0;
    const sum = arrayOfI.reduce((acc, val) => acc + val, 0);
    const average = sum / arrayOfI.length;
    return average;
}

function getColumnNumsCount(column) {
    const letterCountMap = new Map(
        Array.from({ length: 32 }, (_, i) => [i, 0])
    );
    for (let char of column) {
        let count = letterCountMap.get(alphabet.indexOf(char)) || 0;
        letterCountMap.set(alphabet.indexOf(char), count + 1);
    }
    return letterCountMap;
}

function VerdictForU(text, u) {
    const avgIoC = getAverageCI(text, u);
    console.log("avgIoC", avgIoC)
    const diff = avgIoC - 0.058; // Исправлено на типичное значение для английского
    return -0.01 < diff && diff < 0.01; // Более узкий диапазон для точности
}

function getFreqProduct(arr1, arr2) {
  return Array.from({ length: 32 }, (_, i) => 
     arr1.get(i) * arr2.get(i)
  );
}


function getMatrixCI(text, u) {
    let columns = [];
    console.log("u:", u)
    for (let i = 0; i < u; i++) {
        columns.push([]);
    }
    for (let i = 0; i < text.length; i++) {
        columns[i % u].push(text[i]);
    }

    let MatrixMI = Array.from({length: columns.length-1})

    let arrayOfI = [];
    let column = null;
    let newColumnFreq = null
    let newColumn
    let symbol = null
    let letterCount = 0
    let columnLength = 0
    let firstColumn = columns[0]
    let firstColumnLength = firstColumn.length
    let firstColumnFreq = getColumnNumsCount(firstColumn)
    let sumFreqSq = 0;
    let freqs = null
    let freqSum = null


    for (let i = 1; i < u; i++) {
        column = columns[i];
        columnLength = column.length
        newColumnFreq = getColumnNumsCount(column)
        symbol = null
        letterCount = 0


        freqs = getFreqProduct(firstColumnFreq, newColumnFreq)

        console.log(freqs)

        freqSum = freqs.reduce((acc, cur) => acc+cur)

        console.log(freqSum, (firstColumnLength * columnLength))

        MatrixMI[i-1] = freqSum / (firstColumnLength * columnLength)
        
    }

    return MatrixMI
}

const txt = `ЁЛНВ ВВ`

//console.log(txt.replace(/[,.\s+]/g, ''))

for(let i = 2; i< 10; i++){
    console.log(VerdictForU(txt.replace(/[,.\s+]/g, ''), i))
}
let f = getMatrixCI(txt.replace(/[,.\s+]/g, ''), 3)
console.log(f)

function combinations(arr, k) {
    const result = [];

    // Внутренняя рекурсивная функция
    function backtrack(start, current) {
        if (current.length === k) {
            result.push([...current]); // копируем текущее сочетание
            return;
        }

        for (let i = start; i < arr.length; i++) {
            current.push(arr[i]);
            backtrack(i + 1, current); // следующий элемент — с индекса i+1 (чтобы не повторяться)
            current.pop();             // backtrack
        }
    }

    // Запускаем, если k в допустимом диапазоне
    if (k >= 0 && k <= arr.length) {
        backtrack(0, []);
    }

    return result;
}


*/
/*
for(let i = 0; i < keys.length; i++){
    console.log(vigenereCipher(txt, keys[i].join("")))
}
*/


/**
 * vigenere_crack.js
 *
 * Usage:
 *   node vigenere_crack.js ciphertext.txt
 *   node vigenere_crack.js ciphertext.txt --topShifts=3 --maxComb=1000
 *
 * The ciphertext file should contain the ciphertext (may include spaces/punctuation;
 * they will be ignored). Alphabet: Russian without Ё (А..Я except Ё).
 *
 * Outputs:
 *  - Kasiski suggested periods
 *  - IC per candidate period
 *  - candidate keys (combinations of top shifts per column)
 *  - decrypted plaintexts for those keys
 *
 * This is a universal console tool — tune parameters below if needed.
 */


/////////////////////////
// 1. Insert ciphertext
/////////////////////////

let CIPHERTEXT_RAW = `
НШПМД НХ ЪЩСАЭМККИТМУНСМ ЭЪНЛМЦЦ МААЪМЯ, КРЦ ЧДРХР ТЯРВФХМОО ЧИБОЗЦЦЭ НР 
ЕЫЙИЭЪФ ГВЮЬН. ЬТР ЧИБОЗЦИ ОРХРЩСАТЧЗКА, ВЪЯМО, БМФНЕ АМПМОАЪММОХ ЭЦАРРЩРД 
ДШЦЦБИЭЪТ: ЙААЮРМЫ СЪУЫШХК ЯЯСВИЖ АЫЫФ ЧЗСРЩГ ЛАБЧЗМЫЬФ ТПАБЦИЛИ, ЯЪТПЫВЗ  
ЪДМЭЪ-ПДЛХЩГЛ ЛРЦЦЛ, В ВСФМО-ЦСУСЫЕ ШРЧУАЩГФ РРШИФ. ЗШШИ Р БХЧГЛИ ФСШДВМЛФЗ,  
СЮОНПШХЩХН КАМЩМЫЩ ОНЦЕА, ЫЦФОЦФС МА ЧМШДВЮ ЫЦЕААМ, ЬКАЬМХГСЪФС ЛУЦФТ Р ТАЯЙЙОО Ф 
КЪЛЮШИМНЮК ШТКЮК, ЧНХЮТРИ БЮЧНД НР ФХГЕЩЭТНГЮ ЫНСУЕМ К ЛАЭТНСАЕ, ЩНЕЕЫФ ХЯ ЧХЧЦ
БЕЪМ, - КНТ ШБ ЦАЫЪЩЦБЕЭЩГД СОТНСЫ. Ъ ЙЪНМГ ЩЫЕНЮ ЫШЗСЮОЦЙУЯФЪЫ НХЭТНЛМЦЦ ВРРОР
ПОТМХМЫЕ ФПНБАМОДНШХ: ЧНРВЬНС ХЮУШДВР-ШРПЗЛ О ЙЯРРЩДДЙ ИМЧЙЕ, ЯЪШСРХЮГ ЙАЪФЭ-СО 
УСХДРРЧЦБ В ВЬНТГЮЧДМЫЕ ДУЮПРБ, Щ ЙРШОГЛИ ЭЪЩЯМШ. ЭКДРЕ ЮЦВО, ФОНПИ ВМТНЙ ЫМКНЧЪФ 
ЦАЫЪЩЦБЕЭЩЦ АЫТМЖС УТСАЯНЛ ЭКЮЗЪМФЗ ПАЪРЖВХРНМИЩ, ЪЪОЕЗМЪЯНЭЗЭ КУСЦИЛИ ЭМ ЙНЛМДРФ 
ЛШЭЪЯХ, ЪЪЪНРЛС ЩБИФСЪДЛМЭЪБУОЮ ЩЯМЮЬЦГНЮС МЯРЮОИМЬХ ЬЫРСЪЪЛН ЧХЧЦБЕЪМ. ХЯ ОФЩЦЛ 
БЛЧИ 
ХААСКМА   
ЬФУЗКВЬРРА 
ЪФШАИВИНБНР, 
ЩИ 
ГРГПЦЛ 
ГЮЬЦГ  
ИХЬЫРАЫФФ, ОО ФЪФЯМ Ш ВНПКТМФ ЙОВЪШНГЮ ННЖ ЦХЬНЛОЭФР ОРЮЦИСИЫМЩЫ КАМЩМАП ЦШЯСЪМ, 
ПЯХТМЪЗВИМЗ ЦАБЮД ЖЕЬЧР З ДТЯЭ ЛОЫЛБЗХБЛ ШТСБЦРФ МГТРЙОТ О ШТКРОРХАЕ.  
ЫЦЙУЯМЪДЛХХ ЕСИЕ ЫШНИЧОНГЕЭФС НБЛЦХНВХЩХН НХШХНГЮ, ЩЦ ЖАВЪ ППИВСУДЙ - ЪЯЯЯ. КРЦЦИ
НШНЫГЬ ЧМЙТЛФЗЛЯ ЛРЦНИ УЦС, КДРЭЪ, ПДВРСЪ ОЕАСМ МИЬФ, МДРЦМ К ПУЪС ЩТДЪФ Щ НБХРЦЛ 
ИЧ ЮШЯКВФШЯ ДЫЛ ЩБОХПЦ АААФХЯ, КЮЮЦПЫЩ, ННЖ СЮШХДНШЛ, ЙТДХЮ ЭКЕСМЪЫ СГЫ ХД СЫФАЙОЬ 
ПЦПЯЗФС. ОЕАСМ МИЬ ЯОД, ВХЬХН, СВЪРС В ИФХДЛШ ЭЦКДРЮ, ЕСОВ ЦИБАЫСШ СОЫЦЫЦЕУЪ 
ШЪНЪМ, ЧПОФМЖШИЩ РКЯ ПХЬЦЦИЭЩГД НЮТРЙА; ВЪШВОТЦИ-НХВСХЙА Б ЦЦПОСЦЦЭ, НРЫЦКНХЩХНЮ 
СМАЛАЪМФЗ. ВБЛТЗЙ ТЪЩФИЙМНССП ЫЦ-РВЮСФТ: МГТРЙИ ЮНГЙНЮОНМНЮ ЮГЙАОЮ ЧЯЛМВИЛИ; 
ЪМКЯЛХЬГ ПАБЭФЯТАФКЯЮВ ЭНПЬХУХН; ЛРЦНЗ-МРЧДЦИЪФ Р ЛАЫИЯЗШЪФ-ФЯСВСШНВЛС ЩЛЕОЮЩЮ И 
ФЬИЖНПЮ МПУУ РШТГР ЩИПИБЪКЯНЭЗФЗ КРЬРЙАВЯШЯМШ; ЭЪЯРЛС УЯКХФ КН ФАФПНВЛБ АЗНХЧЗФ 
СЬЪЪПЯВ ЫЦСОЬЯ ЪНЛМЦЦ, ЦТЮНГ ВДХ-ЩРАУФИ ЧНЗХОИСЬ; Р ЮЦПГЮОТЗ, МЮЧЦГЫХ ЬЫРСЪФН 
ААСЗ, ЩОЕИМЪ ОО ШЩЩСИЭЦЪТ, ЧВЪЙЪ ПЮЭУТШРЮД, Н ЧХШ ТЯЛПЦИДТ ЭМШНД, Ш ЫЦРМЮЮШДТМ, 
ЩИ ЦТЮ ЪХ РМЮЮШЗТ.
`.trim();

// If ciphertext contains lowercase, spaces, punctuation — all will be filtered.

/////////////////////////
// 2. Setup
/////////////////////////

const ALPHABET = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ".split(""); // 32 letters, no Ё
const M = ALPHABET.length;
const charToIdx = {};
ALPHABET.forEach((c,i)=>charToIdx[c]=i);
const idxToChar = i => ALPHABET[(i%M+M)%M];

function normalize(text) {
  text = text.toUpperCase().replace(/Ё/g, "Е");
  let s = "";
  for (const ch of text) if (charToIdx[ch] !== undefined) s += ch;
  return s;
}

const ciphertext = normalize(CIPHERTEXT_RAW);
console.log(`Ciphertext length = ${ciphertext.length}`);

/////////////////////////
// 3. Russian frequencies
/////////////////////////

const RUS_FREQ_PERCENT = {
  'А':10.2,'Б':1.59,'В':4.54,'Г':1.70,'Д':2.98,'Е':8.45,'Ж':0.94,'З':1.65,'И':7.35,'Й':1.21,
  'К':3.49,'Л':4.40,'М':3.21,'Н':6.70,'О':10.97,'П':2.81,'Р':4.73,'С':5.47,'Т':6.26,'У':2.62,
  'Ф':0.26,'Х':0.97,'Ц':0.48,'Ч':1.44,'Ш':0.73,'Щ':0.36,'Ъ':0.04,'Ы':1.90,'Ь':1.74,'Э':0.32,'Ю':0.64,'Я':2.01
};
const RUS_FREQ = ALPHABET.map(c=>(RUS_FREQ_PERCENT[c]||0)/100);

/////////////////////////
// 4. Index of coincidence
/////////////////////////

function freqs(text) {
  const f = new Array(M).fill(0);
  for (const ch of text) f[charToIdx[ch]]++;
  return f;
}

function IC(freq){
  let N = freq.reduce((s,x)=>s+x,0);
  if (N<2) return 0;
  let S = 0;
  for (const x of freq) S += x*(x-1);
  return S / (N*(N-1));
}

function splitCols(text, p){
  const cols = Array.from({length:p},()=>[]);
  for (let i=0;i<text.length;i++)
    cols[i%p].push(text[i]);
  return cols.map(c=>c.join(""));
}

/////////////////////////
// 5. Kasiski
/////////////////////////

function findRepeats(text, minL=3, maxL=5) {
  const out = {};
  for (let L=minL; L<=maxL; L++) {
    const map={};
    for (let i=0;i+L<=text.length;i++){
      const s = text.substring(i,i+L);
      (map[s] = map[s] || []).push(i);
    }
    for (const s in map) {
      if (map[s].length>1) {
        const pos = map[s];
        const d = [];
        for (let i=0;i<pos.length;i++)
          for (let j=i+1;j<pos.length;j++)
            d.push(pos[j]-pos[i]);
        if (d.length) out[s] = d;
      }
    }
  }
  return out;
}

function gcd(a,b){return b?gcd(b,a%b):Math.abs(a);}
function gcdArray(arr){
  if (!arr.length) return 0;
  let g = arr[0];
  for (let i=1;i<arr.length;i++) g=gcd(g,arr[i]);
  return g;
}

console.log("\n--- Kasiski Test ---");
const reps = findRepeats(ciphertext);
let allD = [];
for (const s in reps) allD = allD.concat(reps[s]);
console.log("Repeat count =", Object.keys(reps).length);
console.log("GCD of distances =", gcdArray(allD));

let kasiskiCandidates = {};
for (const d of allD) {
  for (let p=2;p<=10;p++)
    if (d % p === 0)
      kasiskiCandidates[p] = (kasiskiCandidates[p]||0)+1;
}
console.log("Periods from Kasiski:", kasiskiCandidates);

/////////////////////////
// 6. IC by period
/////////////////////////

console.log("\n--- IC by period (1..10) ---");
const icStats=[];
for (let p=1;p<=10;p++){
  const cols = splitCols(ciphertext,p);
  const ic = cols.map(c=>IC(freqs(c)));
  const avg = ic.reduce((a,b)=>a+b,0)/p;
  icStats.push({p, avg});
}
console.table(icStats.map(x=>({period:x.p, avgIC:x.avg.toFixed(5)})));

let periodCandidates = Object.keys(kasiskiCandidates).map(Number);

periodCandidates = periodCandidates.concat(
  icStats.filter(x=>x.avg>0.035).map(x=>x.p)
);
periodCandidates = [...new Set(periodCandidates)].sort((a,b)=>a-b);

if (periodCandidates.length===0)
  periodCandidates = icStats.map(x=>x.p);

console.log("\nPeriods to test:", periodCandidates);

/////////////////////////
// 7. Shift analysis
/////////////////////////

function shiftFreq(freqArr, shift) {
  const r = new Array(M).fill(0);
  for (let i=0;i<M;i++) r[i] = freqArr[(i+shift)%M];
  return r;
}
function chi2(obs, exp, N) {
  let s=0;
  for (let i=0;i<M;i++){
    const e = exp[i]*N;
    if (e>0){
      const d = obs[i]-e;
      s += d*d/e;
    }
  }
  return s;
}

function analyzePeriod(p, topShifts=3) {
  const cols = splitCols(ciphertext,p);
  const best = [];
  for (const col of cols) {
    const N = col.length;
    const f = freqs(col);
    const scores = [];
    for (let s=0;s<M;s++){
      const shifted = shiftFreq(f, s);
      const c = chi2(shifted, RUS_FREQ, N);
      scores.push({shift:s, chi:c});
    }
    scores.sort((a,b)=>a.chi-b.chi);
    best.push(scores.slice(0, topShifts));
  }
  return best;
}
/*
function cartesian(arrays, limit) {
  const out=[];
  function go(i, cur){
    if (out.length>=limit) return;
    if (i===arrays.length) {out.push(cur.join("")); return;}
    for (const v of arrays[i]) {
      cur.push(v);
      go(i+1, cur);
      cur.pop();
    }
  }
  go(0,[]);
  return out;
}
  */

function cartesian(arr, k) {
    const result = [];

    // Внутренняя рекурсивная функция
    function backtrack(start, current) {
        if (current.length === k) {
            result.push(current.join("")); // копируем текущее сочетание
            return;
        }

        for (let i = start; i < arr.length; i++) {
            current.push(arr[i]);
            backtrack(i + 1, current); // следующий элемент — с индекса i+1 (чтобы не повторяться)
            current.pop();             // backtrack
        }
    }

    // Запускаем, если k в допустимом диапазоне
    if (k >= 0 && k <= arr.length) {
        backtrack(0, []);
    }

    return result;
}

/////////////////////////
// 8. Decrypt
/////////////////////////

function decrypt(key){
  const k = key.split("").map(c=>charToIdx[c]);
  let r="";
  for (let i=0;i<ciphertext.length;i++){
    const c = charToIdx[ciphertext[i]];
    const ki = k[i % key.length];
    r += idxToChar(c-ki);
  }
  return r;
}

/////////////////////////
// 9. Try all periods
/////////////////////////

console.log("\n--- BREAKING ---\n");

const TOP_SHIFTS = 3;
const MAX_KEYS = 2000;

for (const p of periodCandidates) {
  console.log(`\n=== Period = ${p} ===`);

  const best = analyzePeriod(p, TOP_SHIFTS);

  const shiftLists = best.map(
    col => col.map(x => idxToChar(x.shift))
  );
  
  splitCols()

  const keys = cartesian(ALPHABET, p);

  
  console.log("cartesian:", keys)
  console.log(`Trying ${keys.length} keys...`);
  if( p == 10){
    for (let i=0;i<Math.min(10000, keys.length); i++) {
        const key = keys[i];
        console.log(`key=${key} => ${decrypt(key).slice(0,80)}...`);
    }
  }
  
}

console.log("\nDone.");
