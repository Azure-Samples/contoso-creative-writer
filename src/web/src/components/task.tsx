import {
  PaperAirplaneIcon,
  ClipboardDocumentIcon,
  ArrowPathIcon,
} from "@heroicons/react/24/outline";
import { useState } from "react";
import { IMessage, startWritingTask } from "../store";
import { useAppDispatch } from "../store/hooks";
import { addMessage } from "../store/messageSlice";
import { addArticle, addToCurrentArticle } from "../store/articleSlice";
import ImageUpload from "./image-upload";

export const Task = () => {
  const [research, setResearch] = useState("");
  const [products, setProducts] = useState("");
  const [writing, setWriting] = useState("");

  const dispatch = useAppDispatch();

  const setExample = () => {
    setResearch(
      "최신 캠핑 트렌드와 사람들이 겨울에 무엇을 하고 있는지 알아볼 수 있나요?"
    );
    setProducts("텐트, 침낭, 베낭");
    setWriting(
      "연구 및 제품 정보가 포함된 재미있고 매력적인 기사를 작성하세요. 글의 길이는 800~1000단어 사이여야 합니다. 마지막에 연구를 언급하지 말고 기사에서 출처를 반드시 인용하세요."
    );
  };


  const reset = () => {
    setResearch("");
    setProducts("");
    setWriting("");
  };

  const newMessage = (message: IMessage) => {
    dispatch(addMessage(message));
  };

  const newArticle = (article: string) => {
    dispatch(addArticle(article));
  };

  const addToArticle = (text: string) => {
    dispatch(addToCurrentArticle(text));
  };

  const startWork = () => {
    if (research === "" || products === "" || writing === "") {
      return;
    }
    startWritingTask(
      research,
      products,
      writing,
      newMessage,
      newArticle,
      addToArticle
    );
  }

  return (
    <div className="p-3">
      <div className="text-start">
        <label
          htmlFor="research"
          className="block text-sm font-medium leading-6 text-gray-900"
        >
          리서치
        </label>
        <p className="mt-1 text-sm leading-6 text-gray-400">
          어떤 종류의 물건을 찾아야 하나요?
        </p>
        <div className="mt-2">
          <div className=" flex rounded-md shadow-sm ring-1 ring-inset ring-gray-300 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-600">
            <textarea
              id="research"
              name="research"
              rows={3}
              cols={60}
              className="p-2 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
              value={research}
              onChange={(e) => setResearch(e.target.value)}
            />
          </div>
        </div>
      </div>

      <div className="text-start mt-3">
        <label
          htmlFor="products"
          className="block text-sm font-medium leading-6 text-gray-900"
        >
          제품
        </label>
        <p className="mt-1 text-sm leading-6 text-gray-400">
          어떤 제품을 살펴봐야 하나요?
        </p>
        <div className="mt-2">
          <textarea
            id="products"
            name="products"
            rows={3}
            cols={60}
            className="p-2 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
            value={products}
            onChange={(e) => setProducts(e.target.value)}
          />
        </div>
      </div>
      <div className="text-start mt-3">
        <label
          htmlFor="writing"
          className="block text-sm font-medium leading-6 text-gray-900"
        >
          과제
        </label>
        <p className="mt-1 text-sm leading-6 text-gray-400">
          어떤 종류의 글을 써야 하나요?
        </p>
        <div className="mt-2">
          <textarea
            id="writing"
            name="writing"
            rows={3}
            cols={60}
            className="p-2 block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
            value={writing}
            onChange={(e) => setWriting(e.target.value)}
          />
        </div>

      <div className="text-start mt-3">
        <label
          htmlFor="image-upload"
          className="block text-sm font-medium leading-6 text-gray-900"
        >
          이미지 업로드
        </label>
        <p className="mt-1 text-sm leading-6 text-gray-400">
          블로그를 위한 이미지 추가(optional)
        </p>
        <ImageUpload/>
      </div>

      </div>
      <div className="flex justify-end gap-2 mt-10">
        <button
          type="button"
          className="flex flex-row gap-3 items-center rounded-md bg-white px-3.5 py-2.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
          onClick={reset}
        >
          <ArrowPathIcon className="w-6" />
          <span>리셋</span>
        </button>
        <button
          type="button"
          className="flex flex-row gap-3 items-center rounded-md bg-white px-3.5 py-2.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
          onClick={setExample}
        >
          <ClipboardDocumentIcon className="w-6" />
          <span>예시</span>
        </button>
        <button
          type="button"
          className="flex flex-row gap-3 items-center rounded-md bg-indigo-100 px-3.5 py-2.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
          onClick={startWork}
        >
          <PaperAirplaneIcon className="w-6" />
          <span>작업 시작</span>
        </button>
      </div>
    </div>
  );
};

export default Task;