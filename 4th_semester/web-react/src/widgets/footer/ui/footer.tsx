import { cn } from "@/shared/lib/tailwind";

export const Footer = ({ className }: React.ComponentProps<"footer">) => {
  return (
    <footer
      id="contacts"
      className={cn(
        "h-[250px] w-full flex flex-col justify-center items-center bg-gray-900",
        className
      )}
    >
      <div className="flex flex-col w-[1200px] h-full">
        <section className="w-full flex flex-row items-baseline pt-10">
          <div className="text-2xl">Nova UI</div>
          <div className="grow"></div>
        </section>

        <div className="grow"></div>

        <section className="w-full flex flex-row items-baseline pt-10">
          <div className="text-xl text-gray-500 flex flex-row items-center gap-1">
            powered by
            <a
              className="flex flex-row gap-1.5 items-center"
              href="https://tailwindcss.com/"
            >
              <div>Tailwindcss</div>
              <img
                className="h-[20px]"
                src="./src/shared/icons/tailwindcss.svg"
                alt=""
              />
            </a>
          </div>
          <div className="grow"></div>
        </section>

        <section className="w-full flex flex-row items-baseline pt-4 pb-4 text-gray-500">
          Nova UI © components library 2025
        </section>
      </div>
    </footer>
  );
};
