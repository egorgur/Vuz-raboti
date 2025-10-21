import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { createFileRoute } from '@tanstack/react-router'
import { useState } from 'react'
import { TwoSquareCipher } from '@/lib/two-square-cipher'
import { DynamicGridTwoSquareCipher } from '@/lib/dynamic-two-square-cipher'
import { cn } from '@/lib/utils'

export const Route = createFileRoute('/')({
    component: App,
})

function App() {

    const [key1, setKey1] = useState<string>("");
    const [key2, setKey2] = useState<string>("");
    const [value, setValue] = useState<string>("");
    const [result, setResult] = useState<string>("");
    const [isDynamic, setIsDynamic] = useState<boolean>(false);

    const cipher = isDynamic ? new DynamicGridTwoSquareCipher(key1, key2) : new TwoSquareCipher(key1, key2)

    const buttonsDisabled = !key1 || !key2 || !value

    const handleEncrypt = () => {
        const result = cipher.encrypt(value)
        setResult(result)
    }

    const handleDecrypt = () => {
        const result = cipher.decrypt(value)
        setResult(result)
    }

    return (
        <div className={"flex justify-center items-center h-[80vh] w-full"}>
            <div className={"flex flex-col gap-4"}>
                <Label>Вариант шифра</Label>
                <div className={"flex gap-4"}>
                    <Button
                        variant={"secondary"}
                        className={cn(!isDynamic && "bg-blue-500 hover:bg-blue-600 text-primary-foreground")}
                        onClick={() => setIsDynamic(false)}>
                        Стандартный
                    </Button>
                    <Button
                        variant={"secondary"}
                        className={cn(isDynamic && "bg-blue-500 hover:bg-blue-600 text-primary-foreground")}
                        onClick={() => setIsDynamic(true)}
                    >
                        Динамический
                    </Button>
                </div>

                <Label htmlFor={"key"}>Ключ 1</Label>
                <Input value={key1} onChange={(e) => setKey1(e.target.value)} id={"value"} placeholder={"Введите первый ключ"} />

                <Label htmlFor={"key"}>Ключ 2</Label>
                <Input value={key2} onChange={(e) => setKey2(e.target.value)} id={"value"} placeholder={"Введите второй ключ"} />

                <Label htmlFor={"value"}>Значение</Label>
                <Input value={value} onChange={(e) => setValue(e.target.value)} id={"value"} placeholder={"Введите значение"} />
                <div className={"flex gap-4"}>
                    <Button
                        disabled={buttonsDisabled}
                        onClick={handleEncrypt}
                    >
                        Зашифровать
                    </Button>
                    <Button
                        disabled={buttonsDisabled}
                        variant={"secondary"}
                        onClick={handleDecrypt}
                    >
                        Расшифровать
                    </Button>
                </div>
                <Label htmlFor={"result"}>Результат</Label>
                <Input id={"result"} value={result} disabled />
            </div>
        </div>
    )
}
