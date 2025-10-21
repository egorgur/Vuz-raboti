export class TwoSquareCipher {
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

    private generateGrid(key: string): string[][] {
        const grid: string[][] = [];
        let usedLetters = new Set<string>();
        
        let currentLetters = '';
        for (const char of key) {
            if (!usedLetters.has(char)) {
                currentLetters += char;
                usedLetters.add(char);
            }
        }
        
        for (const char of this.alphabet) {
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

    private prepareText(text: string): string {
        let prepared = text.toUpperCase().replace(/J/g, 'I');
        prepared = prepared.replace(/[^A-Z]/g, '');
        
        let result = '';
        let i = 0;
        
        while (i < prepared.length) {
            if (i === prepared.length - 1) {
                // Last character alone, add 'X'
                result += prepared[i] + 'X';
                i++;
            } else if (prepared[i] === prepared[i + 1]) {
                // Double letter, insert 'X'
                result += prepared[i] + 'X';
                i++;
            } else {
                // Normal digraph
                result += prepared[i] + prepared[i + 1];
                i += 2;
            }
        }
        
        // Ensure even length
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
        const grid1 = this.generateGrid(this.key1);
        const grid2 = this.generateGrid(this.key2);
        
        let ciphertext = '';
        
        for (let i = 0; i < preparedText.length; i += 2) {
            const char1 = preparedText[i];
            const char2 = preparedText[i + 1];
            
            const pos1 = this.findPosition(grid1, char1);
            const pos2 = this.findPosition(grid2, char2);
            
            const encryptedChar1 = grid1[pos1.row][pos2.col];
            const encryptedChar2 = grid2[pos2.row][pos1.col];
            
            ciphertext += encryptedChar1 + encryptedChar2;
        }
        
        return ciphertext;
    }

    public decrypt(ciphertext: string): string {
        const cleanCiphertext = ciphertext.toUpperCase().replace(/[^A-Z]/g, '');
        
        if (cleanCiphertext.length % 2 !== 0) {
            throw new Error('Ciphertext must have even length');
        }
        
        const grid1 = this.generateGrid(this.key1);
        const grid2 = this.generateGrid(this.key2);
        
        let plaintext = '';
        
        for (let i = 0; i < cleanCiphertext.length; i += 2) {
            const char1 = cleanCiphertext[i];
            const char2 = cleanCiphertext[i + 1];
            
            const pos1 = this.findPosition(grid1, char1);
            const pos2 = this.findPosition(grid2, char2);
            
            const decryptedChar1 = grid1[pos1.row][pos2.col];
            const decryptedChar2 = grid2[pos2.row][pos1.col];
            
            plaintext += decryptedChar1 + decryptedChar2;
        }
        
        // Улучшенная логика удаления добавленных 'X'
        return this.cleanDecryptedText(plaintext);
    }

    /**
     * Удаляет добавленные 'X' символы из расшифрованного текста
     */
    private cleanDecryptedText(text: string): string {
        let result = '';
        let i = 0;
        
        while (i < text.length) {
            if (i === text.length - 1) {
                // Последний символ - добавляем как есть
                result += text[i];
                i++;
            } else if (text[i + 1] === 'X' && 
                      (i + 2 === text.length || // X в конце
                       (i + 2 < text.length && text[i] === text[i + 2]))) { // X между одинаковыми буквами
                // Пропускаем 'X' и добавляем только текущий символ
                result += text[i];
                i += 2;
            } else {
                // Обычная биграмма
                result += text[i] + text[i + 1];
                i += 2;
            }
        }
        
        return result;
    }

    public displayGrids(): void {
        const grid1 = this.generateGrid(this.key1);
        const grid2 = this.generateGrid(this.key2);
        
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
