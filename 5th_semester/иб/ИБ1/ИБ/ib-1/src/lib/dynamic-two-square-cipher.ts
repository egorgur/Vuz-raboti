
export class DynamicGridTwoSquareCipher {
    private key1: string;
    private key2: string;
    private alphabet: string = 'ABCDEFGHIKLMNOPQRSTUVWXYZ';
    private gridSize: number = 5;

    constructor(key1: string = 'EXAMPLE', key2: string = 'KEYWORD') {
        this.key1 = this.prepareKey(key1);
        this.key2 = this.prepareKey(key2);
    }

    private prepareKey(key: string): string {
        let prepared = key.toUpperCase().replace(/J/g, 'I');
        prepared = prepared.replace(/[^A-Z]/g, '');
        
        let uniqueChars = '';
        for (const char of prepared) {
            if (!uniqueChars.includes(char)) {
                uniqueChars += char;
            }
        }
        
        return uniqueChars;
    }

    private generateDynamicGrid(baseKey: string, seed: number): string[][] {
        const grid: string[][] = [];
        
        let dynamicAlphabet = this.alphabet;
        for (let i = 0; i < seed % 10; i++) {
            dynamicAlphabet = this.rotateString(dynamicAlphabet, (seed + i) % 25);
        }

        let usedLetters = new Set<string>();
        let currentLetters = '';
        
        for (const char of baseKey) {
            if (!usedLetters.has(char)) {
                currentLetters += char;
                usedLetters.add(char);
            }
        }
        
        for (const char of dynamicAlphabet) {
            if (!usedLetters.has(char)) {
                currentLetters += char;
                usedLetters.add(char);
            }
        }
        
        for (let i = 0; i < this.gridSize; i++) {
            grid.push([]);
            for (let j = 0; j < this.gridSize; j++) {
                const index = i * this.gridSize + j;
                grid[i].push(currentLetters[index]);
            }
        }
        
        return grid;
    }

    private rotateString(str: string, shift: number): string {
        shift = shift % str.length;
        return str.slice(shift) + str.slice(0, shift);
    }

    private generateSeed(position: number, prevChars: string, baseKey: string): number {
        let seed = 0;
        
        for (let i = 0; i < prevChars.length; i++) {
            seed = (seed * 31 + prevChars.charCodeAt(i)) % 1000;
        }
        
        seed = (seed + position * 17) % 1000;
        
        for (let i = 0; i < baseKey.length; i++) {
            seed = (seed + baseKey.charCodeAt(i) * (i + 1)) % 1000;
        }
        
        return seed;
    }

    private prepareText(text: string): string {
        let prepared = text.toUpperCase().replace(/J/g, 'I');
        prepared = prepared.replace(/[^A-Z]/g, '');
        
        let result = '';
        let i = 0;
        
        while (i < prepared.length) {
            if (i === prepared.length - 1) {
                result += prepared[i] + 'X';
                i++;
            } else if (prepared[i] === prepared[i + 1]) {
                result += prepared[i] + 'X';
                i++;
            } else {
                result += prepared[i] + prepared[i + 1];
                i += 2;
            }
        }
        
        if (result.length % 2 !== 0) {
            result += 'X';
        }
        
        return result;
    }

    private findPosition(grid: string[][], char: string): { row: number; col: number } {
        for (let row = 0; row < this.gridSize; row++) {
            for (let col = 0; col < this.gridSize; col++) {
                if (grid[row][col] === char) {
                    return { row: row, col };
                }
            }
        }
        throw new Error(`Character ${char} not found in grid`);
    }

    public encrypt(plaintext: string): string {
        const preparedText = this.prepareText(plaintext);
        let ciphertext = '';
        let previousChars = '';

        for (let i = 0; i < preparedText.length; i += 2) {
            const char1 = preparedText[i];
            const char2 = preparedText[i + 1];
            
            const seed1 = this.generateSeed(i, previousChars, this.key1);
            const seed2 = this.generateSeed(i + 1, previousChars, this.key2);
            
            const grid1 = this.generateDynamicGrid(this.key1, seed1);
            const grid2 = this.generateDynamicGrid(this.key2, seed2);
            
            const pos1 = this.findPosition(grid1, char1);
            const pos2 = this.findPosition(grid2, char2);
            
            const encryptedChar1 = grid1[pos1.row][pos2.col];
            const encryptedChar2 = grid2[pos2.row][pos1.col];
            
            ciphertext += encryptedChar1 + encryptedChar2;
            previousChars += char1 + char2;
        }
        
        return ciphertext;
    }

    public decrypt(ciphertext: string): string {
        const cleanCiphertext = ciphertext.toUpperCase().replace(/[^A-Z]/g, '');
        
        if (cleanCiphertext.length % 2 !== 0) {
            throw new Error('Ciphertext must have even length');
        }
        
        let plaintext = '';
        let previousChars = '';

        for (let i = 0; i < cleanCiphertext.length; i += 2) {
            const char1 = cleanCiphertext[i];
            const char2 = cleanCiphertext[i + 1];
            
            const seed1 = this.generateSeed(i, previousChars, this.key1);
            const seed2 = this.generateSeed(i + 1, previousChars, this.key2);
            
            const grid1 = this.generateDynamicGrid(this.key1, seed1);
            const grid2 = this.generateDynamicGrid(this.key2, seed2);
            
            const pos1 = this.findPosition(grid1, char1);
            const pos2 = this.findPosition(grid2, char2);
            
            const decryptedChar1 = grid1[pos1.row][pos2.col];
            const decryptedChar2 = grid2[pos2.row][pos1.col];
            
            plaintext += decryptedChar1 + decryptedChar2;
            previousChars += decryptedChar1 + decryptedChar2;
        }
        
        return this.cleanDecryptedText(plaintext);
    }

    private cleanDecryptedText(text: string): string {
        let result = '';
        let i = 0;
        
        while (i < text.length) {
            if (i === text.length - 1) {
                result += text[i];
                i++;
            } else if (text[i + 1] === 'X' && 
                      (i + 2 === text.length ||
                       (i + 2 < text.length && text[i] === text[i + 2]))) {
                result += text[i];
                i += 2;
            } else {
                result += text[i] + text[i + 1];
                i += 2;
            }
        }
        
        return result;
    }

    public displayGridsForPosition(position: number, previousText: string = ''): void {
        const seed1 = this.generateSeed(position, previousText, this.key1);
        const seed2 = this.generateSeed(position + 1, previousText, this.key2);
        
        const grid1 = this.generateDynamicGrid(this.key1, seed1);
        const grid2 = this.generateDynamicGrid(this.key2, seed2);
        
        console.log(`Grids for position ${position} with previous text "${previousText}":`);
        console.log('Grid 1:');
        for (const row of grid1) {
            console.log(row.join(' '));
        }
        
        console.log('\nGrid 2:');
        for (const row of grid2) {
            console.log(row.join(' '));
        }
    }

    public setKeys(key1: string, key2: string): void {
        this.key1 = this.prepareKey(key1);
        this.key2 = this.prepareKey(key2);
    }
}
