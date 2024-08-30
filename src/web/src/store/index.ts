import { endpoint } from "../constants";
export interface IMessage {
  type: "message" | "researcher" | "marketing" | "writer" | "editor" | "error" | "partial";
  message: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  data?: any;
}

export interface IArticleCollection {
  current: number;
  articles: string[];
  currentArticle: string;
}

export interface IChatTurn {
  name: string;
  avatar: string;
  image: string | null;
  message: string;
  status: "waiting" | "done";
  type: "user" | "assistant";
}

export const startWritingTask = (
  research: string,
  products: string,
  assignment: string,
  addMessage: { (message: IMessage): void },
  createArticle: { (article: string): void },
  addToArticle: { (text: string): void }
) => {
  // internal function to read chunks from a stream
  function readChunks(reader: ReadableStreamDefaultReader<Uint8Array>) {
    return {
      async *[Symbol.asyncIterator]() {
        let readResult = await reader.read();
        while (!readResult.done) {
          yield readResult.value;
          readResult = await reader.read();
        }
      },
    };
  }

  const configuration = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Connection": "keep-alive",
    },
    body: JSON.stringify({
      research: research,
      products: products,
      assignment: assignment,
    }),
  };

  const url = `${
    endpoint.endsWith("/") ? endpoint : endpoint + "/"
  }api/article`;

  const callApi = async () => {
    try {
      const response = await fetch(url, configuration);
      const reader = response.body?.getReader();
      if (!reader) return;

      const chunks = readChunks(reader);
      for await (const chunk of chunks) {
        const text = new TextDecoder().decode(chunk);
        const parts = text.split("\n");
        for (let part of parts) {
          part = part.trim();
          if (!part || part.length === 0) continue;
          console.log(part);
          const message = JSON.parse(part) as IMessage;
          addMessage(message);
          if (message.type === "writer") {
            if (message.data && message.data.start) {
              createArticle("");
            }
          } else if (message.type === "partial") {
            if (message.data?.text && message.data.text.length > 0) {
              addToArticle(message.data?.text || "");
            }
            else {
              console.log('writing complete');
            }
          }
        }
      }
    } catch (e) {
      console.log(e);
    }
  };

  callApi();

};
