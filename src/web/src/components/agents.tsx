import { Box, Details, Flash, Label, Pagehead } from "@primer/react";
import { useAppSelector } from "../store/hooks";
import { IEditorResult, IResearchResult, IWriterResult } from "../store";
import Research from "./research";
import { useEffect, useRef } from "react";
import Markdown from "react-markdown";

export const Agents = () => {
  const agent = useAppSelector((state) => state.agent);
  const workspaceDiv = useRef<HTMLDivElement>(null);
  const scrollWorkspace = () => {
    setTimeout(() => {
      if (workspaceDiv.current) {
        workspaceDiv.current.scrollTo({
          top: workspaceDiv.current.scrollHeight,
          behavior: "smooth",
        });
      }
    }, 10);
  };

  useEffect(() => {
    scrollWorkspace();
  }, [agent.length]);

  return (
    <div className="content" ref={workspaceDiv}>
      <Box
        sx={{
          margin: "0px auto",
          width: "1024px",
          display: "flex",
          flexDirection: "column",
          gap: "8px",
        }}
      >
        <Pagehead>Agent Workpace</Pagehead>
        {agent.map((a, i) => {
          if (a.type === "researcher") {
            return (
              <Research
                key={"agent_" + i}
                {...(a.contents as IResearchResult)}
              />
            );
          } else if (a.type === "writer") {
            return (
              <Details key={"agent_" + i} closeOnOutsideClick={true}>
                <Flash variant="warning" as="summary">
                  <div>Writer</div>
                </Flash>
                <Box
                  sx={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "8px",
                    padding: "8px",
                  }}
                >
                  <Label variant="attention">Researcher Feedback</Label>
                  <Box>{(a.contents as IWriterResult).feedback}</Box>
                  <Label variant="success">Article</Label>
                  <Markdown>{(a.contents as IWriterResult).article}</Markdown>
                </Box>
              </Details>
            );
          } else if (a.type === "editor") {
            return (
              <Details key={"agent_" + i} closeOnOutsideClick={true}>
                <Flash variant="danger" as="summary">
                  <div>Editor [{(a.contents as IEditorResult).decision}]</div>
                </Flash>
                <Box
                  sx={{
                    display: "flex",
                    flexDirection: "column",
                    gap: "8px",
                    padding: "8px",
                  }}
                >
                  <Label variant="attention">
                    Writer feedback for research materials
                  </Label>
                  <Box> {(a.contents as IEditorResult).researchFeedback}</Box>
                  <Label variant="severe">Editor feedback for writer:</Label>
                  <Box> {(a.contents as IEditorResult).editorFeedback}</Box>
                </Box>
              </Details>
            );
          } else if (a.type === "message") {
            return (
              <Flash key={"agent_" + i} variant="success">
                {a.contents as string}
              </Flash>
            );
          }
        })}
      </Box>
    </div>
  );
};
