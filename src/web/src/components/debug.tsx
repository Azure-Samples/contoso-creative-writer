import { useEffect, useRef } from "react";
import {
  ArrowPathIcon,
  BugAntIcon,
  BuildingStorefrontIcon,
  BeakerIcon,
  AcademicCapIcon,
  UserIcon,
  PencilIcon,
  InformationCircleIcon,
} from "@heroicons/react/24/outline";
import { useAppDispatch, useAppSelector } from "../store/hooks";
import { clearMessages } from "../store/messageSlice";

import clsx from "clsx";
import { Inspector } from "../components/inspector";

export const Debug = () => {
  const dispatch = useAppDispatch();
  const messages = useAppSelector((state) => state.message);

  const chatDiv = useRef<HTMLDivElement>(null);

  const scrollChat = () => {
    setTimeout(() => {
      if (chatDiv.current) {
        chatDiv.current.scrollTo({
          top: chatDiv.current.scrollHeight,
          behavior: "smooth",
        });
      }
    }, 300);
  };

  useEffect(() => {
    scrollChat();
  }, [messages.length]);

  const reset = () => {
    dispatch(clearMessages());
  };

  const getColor = (type: string) => {
    switch (type) {
      case "message":
        return "bg-stone-200 text-zinc-600";
      case "researcher":
        return "bg-sky-200 text-zinc-600";
      case "marketing":
        return "bg-green-200 text-zinc-600";
      case "writer":
        return "bg-violet-200 text-zinc-600";
      case "editor":
        return "bg-amber-200 text-zinc-600";
      case "error":
        return "bg-red-200 text-zinc-600";
      default:
        return "bg-zinc-200 text-zinc-600";
    }
  };

  const getIcon = (type: string) => {
    switch (type) {
      case "message":
        return <InformationCircleIcon className="w-6 stroke-stone-600" />;
      case "researcher":
        return <BeakerIcon className="w-6 stroke-sky-600" />;
      case "marketing":
        return <AcademicCapIcon className="w-6 stroke-green-600" />;
      case "writer":
        return <UserIcon className="w-6 stroke-violet-600" />;
        case "editor":
          return <PencilIcon className="w-6 stroke-amber-600" />;
      case "error":
        return <BugAntIcon className="w-6 stroke-red-600" />;
      default:
        return <BuildingStorefrontIcon className="w-6 stroke-zinc-600" />;
    }
  };

  return (
    <>
      <div className="text-right p-2 flex flex-col">
        <ArrowPathIcon className="w-5 stroke-zinc-500" onClick={reset} />
      </div>
      {/* chat section */}
      <div className="grow p-2 overscroll-contain overflow-auto" ref={chatDiv}>
        <div className="flex flex-col gap-4">
          {messages.filter((message) => message.type !== "partial").map((message, i) => (
            <div className="flex flex-row-reverse gap-1" key={`message_${i}`}>
              <div
                className={clsx("grow p-2 rounded-md", getColor(message.type))}
              >
                <div
                  className={clsx(
                    "text-left",
                    message.data ? "border-b-[1px] border-zinc-400 mb-2" : ""
                  )}
                >
                  {message.message}
                </div>
                {message.data && <Inspector data={message.data} />}
              </div>
              <div>{getIcon(message.type)}</div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
};

export default Debug;
