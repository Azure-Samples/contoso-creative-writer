import clsx from "clsx";
import { ReactNode, useState } from "react";

type Props = {
  children: ReactNode;
  icon: ReactNode;
  buttonClassName?: string;
  panelClassName?: string;
};

export const Block = ({
  children,
  icon,
  buttonClassName,
  panelClassName,
}: Props) => {
  const [open, setOpen] = useState(false);
  return (
    <div className="flex flex-col">
      {open && (
        <div
          className={clsx(
            panelClassName,
            "mt-auto mb-3 p-2 rounded-xl shadow-md bg-white"
          )}
        >
          {children}
        </div>
      )}
      <div
        className={clsx(
          buttonClassName,
          "justify-end shrink self-end align-baseline cursor-pointer  rounded-full p-2 shadow-lg border-zinc-40 hover:cursor-pointer",
          open ? "bg-blue-100 text-blue-600" : "bg-white text-zinc-600 mt-auto"
        )}
        onClick={() => setOpen(!open)}
      >
        {icon}
      </div>
    </div>
  );
};

export default Block;
