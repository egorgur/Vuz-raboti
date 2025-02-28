import { cn } from "@/shared/lib/tailwind";

export const Header = ({ className }: React.ComponentProps<"header">) => {
  return (
    <header
      className={cn(
        "w-full fixed flex flex-row justify-center items-center py-3 bg-transparent backdrop-blur-xs border-b z-10",
        className
      )}
    >
      <div className="w-full max-w-[1200px] flex flex-row">
        <nav className="flex flex-row gap-4">
          <div>
            <a href="https://vite.dev/">
              <img
                src="./src/shared/icons/vite.svg"
                className="h-7"
                alt="Vite"
              />
            </a>
          </div>
          <div>
            <a href="https://www.typescriptlang.org">
              <img
                src="./src/shared/icons/typescript.svg"
                className="h-7"
                alt="TypeScript"
              />
            </a>
          </div>
          <div>
            <a href="https://react.dev/">
              <img
                src="./src/shared/icons/react.svg"
                className="h-7"
                alt="TypeScript"
              />
            </a>
          </div>
        </nav>

        <div className="grow"></div>

        <nav className="flex flex-row gap-12">
          <a href="#overview">Overview</a>
          <a href="#examples">Examples</a>
          <a href="#contacts">Contacts</a>
        </nav>
      </div>
    </header>
  );
};
