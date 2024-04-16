import { Box, Pagehead, TabNav } from "@primer/react";
import AppHeader from "./components/header";
import "./app.css";
import { useState } from "react";
import { Task } from "./components/task";
import { apiEndpoint } from "./constants";
import { useAppDispatch, useAppSelector } from "./store/hooks";
import { addState } from "./store/agentSlice";
import { setArticle } from "./store/articleSlice";
import { Agents } from "./components/agents";
import Markdown from "react-markdown";

const App = () => {
  const [currentTab, setCurrentTab] = useState<
    "starting" | "creative" | "document"
  >("starting");

  const dispatch = useAppDispatch();
  const article = useAppSelector((state) => state.article);

  const startWork = (context: string, instructions: string) => {
    setCurrentTab("creative");
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

    if (context !== "" && instructions !== "") {
      const endpoint = `${apiEndpoint}?context=${context}&instructions=${instructions}`;
      fetch(endpoint).then(async (response) => {
        // response.body is a ReadableStream
        if (response.body !== null) {
          const reader = response.body.getReader();
          // read the incoming stream as a string
          const textChunks: string[] = [];
          for await (const chunk of readChunks(reader)) {
            const text = new TextDecoder().decode(chunk);
            try {
              const parts = text.split(">>>");
              for (const part of parts) {
                if (part.trim() !== "") {
                  const item = JSON.parse(part);
                  if (item.type === "writer") {
                    dispatch(setArticle(item.contents.article));
                  }
                  dispatch(addState(item));
                  console.log(item);
                }
              }
            } catch (e) {
              console.log(e);
            }

            textChunks.push(text);
          }

          console.log("Done!");
        }
      });
    }
  };

  return (
    <Box
      sx={{
        height: "100vh",
        width: "100vw",
      }}
    >
      <Box>
        <AppHeader />
      </Box>
      <Box
        sx={{
          padding: "16px",
        }}
      >
        <Box>
          <TabNav aria-label="Main">
            <TabNav.Link
              href="#"
              selected={currentTab === "starting"}
              onClick={(e) => {
                e.preventDefault();
                setCurrentTab("starting");
              }}
            >
              Get Started
            </TabNav.Link>
            <TabNav.Link
              href="#"
              selected={currentTab === "creative"}
              onClick={(e) => {
                e.preventDefault();
                setCurrentTab("creative");
              }}
            >
              Creative Team
            </TabNav.Link>
            <TabNav.Link
              href="#"
              selected={currentTab === "document"}
              onClick={(e) => {
                e.preventDefault();
                setCurrentTab("document");
              }}
            >
              Document
            </TabNav.Link>
          </TabNav>
        </Box>
        {currentTab === "starting" && <Task startWork={startWork} />}
        {currentTab === "creative" && <Agents />}
        {currentTab === "document" && (
          <Box className="content">
            <Box
              sx={{
                margin: "0px auto",
                width: "1024px",
              }}
            >
              <Pagehead>Article</Pagehead>
              <Markdown>{article.content}</Markdown>
            </Box>
          </Box>
        )}
      </Box>
    </Box>
  );
};

export default App;
