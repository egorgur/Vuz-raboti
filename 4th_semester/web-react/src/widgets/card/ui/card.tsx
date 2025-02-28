import { cn } from "@/shared/lib/tailwind";

export const Card = ({
  className,
  children,
}: React.ComponentProps<"main">) => {
  return (
    <div
      className={cn(
        "bg-slate-900 rounded-2xl overflow-hidden relative",
        className
      )}
    >
      {children}
    </div>
  );
};
