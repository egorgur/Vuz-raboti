import { cn } from "@/shared/lib/tailwind";
import { Card } from "@/widgets/card";
import { useEffect, useState } from "react";
import Cookies from 'js-cookie';

export const MainPage = ({ className }: React.ComponentProps<"main">) => {
  // Счётчик
  const [counter, setCounter] = useState(0);

  // Форма
  const [formData, setFormData] = useState({
    field1: "",
    field2: "",
    field3: "",
  });

  // При загрузке компонента восстанавливаем значения из куки
  useEffect(() => {
    const savedField1 = Cookies.get("field1") || "";
    const savedField2 = Cookies.get("field2") || "";
    const savedField3 = Cookies.get("field3") || "";

    setFormData({
      field1: savedField1,
      field2: savedField2,
      field3: savedField3,
    });
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });

    // Сохраняем значение в куки
    Cookies.set(name, value, { expires: 7 }); // expires: 7 — куки сохраняются на 7 дней
  };

  // Обработчик отправки формы
  const handleSubmit = (e) => {
    e.preventDefault();

    // Формируем URL с query-параметрами
    const queryParams = new URLSearchParams(formData).toString();
    const url = `https://httpbin.org/get?${queryParams}`;

    // Отправляем GET-запрос
    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        console.log('Ответ от сервера:', data);
        alert('Ответ от сервера: ' + JSON.stringify(data, null, 2));
      })
      .catch((error) => {
        console.error('Ошибка:', error);
      });
  };

  return (
    <main
      id="overview"
      className={cn(
        "flex flex-col grow justify-center items-center gap-4",
        className
      )}
    >
      <div className={"h-[200px]"}></div>
      <Card
        className={
          "w-[500px] relative  flex flex-col overflow-hidden border border-gray-950 hover:border-gray-800 transition-all duration-75"
        }
      >
        <header className="absolute w-full flex flex-row justify-center h-[30px] backdrop-blur-3xl bg-transparent"></header>
        <main className="h-[200px] bg-gray-950 flex flex-col items-center gap-10 justify-center overflow-y-scroll">
          <div className="w-[150px] h-[50px] bg-gray-900"></div>
          <div className="w-[150px] h-[50px] bg-gray-900"></div>
          <div className="w-[150px] h-[50px] bg-gray-900"></div>
          <div className="w-[150px] h-[50px] bg-gray-900"></div>
          <div className="w-[150px] h-[50px] bg-gray-900"></div>
        </main>
        <footer className="absolute bottom-0 w-full flex flex-row justify-center h-[30px] backdrop-blur-3xl bg-transparent"></footer>
      </Card>

      <Card className="w-[500px] h-[120px] flex-col flex p-5 gap-5 border border-gray-950 hover:border-gray-800 transition-all duration-75">
        <header className="flex flex-row gap-5 text-xl select-none">
          <div onClick={() => setCounter(counter - 1)}>-</div>
          <div onClick={() => setCounter(counter + 1)}>+</div>
        </header>
        <main className="flex flex-col items-center justify-center">
          {counter}
        </main>
      </Card>

      <Card
        className={
          "w-[500px] relative  flex flex-col overflow-hidden border border-gray-950 hover:border-gray-800 transition-all duration-75"
        }
      >
        <header className="absolute w-full flex flex-row justify-center h-[30px] backdrop-blur-3xl bg-transparent"></header>
        <main className="h-[200px] bg-gray-950 flex flex-col items-center gap-10 justify-center overflow-y-scroll">
          <div className="w-[150px] h-[50px] bg-gray-900"></div>
          <div className="w-[150px] h-[50px] bg-gray-900"></div>
          <div className="w-[150px] h-[50px] bg-gray-900"></div>
          <div className="w-[150px] h-[50px] bg-gray-900"></div>
          <div className="w-[150px] h-[50px] bg-gray-900"></div>
        </main>
        <footer className="absolute bottom-0 w-full flex flex-row justify-center h-[30px] backdrop-blur-3xl bg-transparent"></footer>
      </Card>

      <Card className="w-[500px] h-[120px] flex-col flex p-5 gap-5 border border-gray-950 hover:border-gray-800 transition-all duration-75">
      <form onSubmit={handleSubmit}>
      <div>
        <label>
          Поле 1:
          <input
            type="text"
            name="field1"
            value={formData.field1}
            onChange={handleChange}
          />
        </label>
      </div>
      <div>
        <label>
          Поле 2:
          <input
            type="text"
            name="field2"
            value={formData.field2}
            onChange={handleChange}
          />
        </label>
      </div>
      <div>
        <label>
          Поле 3:
          <input
            type="text"
            name="field3"
            value={formData.field3}
            onChange={handleChange}
          />
        </label>
      </div>
      <button type="submit">Отправить</button>
    </form>
      </Card>

      <div className={"h-[300px]"}></div>
    </main>
  );
};
