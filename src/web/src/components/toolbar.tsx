import {
  BugAntIcon,
  ArrowRightCircleIcon,
  ArrowLeftCircleIcon,
} from "@heroicons/react/24/outline";
import Tool from "./tool";
import Debug from "./debug";
import clsx from "clsx";
import { useAppSelector, useAppDispatch } from "../store/hooks";
import { setCurrentArticle } from "../store/articleSlice";

export const Toolbar = () => {
  const dispatch = useAppDispatch();
  const articles = useAppSelector((state) => state.article);

  return (
    <div className="fixed right-0 bottom-0 mr-12 mb-10 flex gap-3">
      {articles.articles.length > 0 && (
        <div
          className={clsx(
            "justify-end shrink self-end align-baseline cursor-pointer  rounded-full p-2 shadow-lg border-zinc-40 hover:cursor-pointer",
            "bg-white text-zinc-600 mt-auto",
            "hover:bg-blue-100 hover:text-blue-600"
          )}
          onClick={() => dispatch(setCurrentArticle(articles.current - 1))}
        >
          <ArrowLeftCircleIcon className="w-6" />
        </div>
      )}
      {articles.articles.length > 0 && (
        <div
          className={clsx(
            "justify-end shrink self-end align-baseline cursor-pointer  rounded-full p-2 shadow-lg border-zinc-40 hover:cursor-pointer",
            "bg-white text-zinc-600 mt-auto",
            "hover:bg-blue-100 hover:text-blue-600 w-9"
          )}
        >
          {articles.current + 1}/{articles.articles.length}
        </div>
      )}
      {articles.articles.length > 0 && (
          <div
            className={clsx(
              "justify-end shrink self-end align-baseline cursor-pointer  rounded-full p-2 shadow-lg border-zinc-40 hover:cursor-pointer",
              "bg-white text-zinc-600 mt-auto",
              "hover:bg-blue-100 hover:text-blue-600"
            )}
            onClick={() => dispatch(setCurrentArticle(articles.current + 1))}
          >
            <ArrowRightCircleIcon className="w-6" />
          </div>
        )}

      <Tool
        icon={<BugAntIcon className="w-6" />}
        panelClassName=" h-[calc(100vh-7rem)]  w-[450px] overflow-auto"
      >
        <Debug />
      </Tool>
    </div>
  );
};

export default Toolbar;
