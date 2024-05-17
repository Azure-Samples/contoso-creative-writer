import { useState } from "react";
import { Box, Button, FormControl, Pagehead, Textarea } from "@primer/react";
import { useAppDispatch } from "../store/hooks";
import { clearState } from "../store/agentSlice";
import { clearArticle } from "../store/articleSlice";

// create a function to start work props
interface IProps {
  startWork: (context: string, instructions: string) => void;
}

export const Task = ({ startWork }: IProps) => {
  const [context, setContext] = useState<string>("");
  const [instructions, setInstructions] = useState<string>("");
  const dispatch = useAppDispatch();
  const setExamples = () => {
    setContext(
      "Can you find the latest camping trends and what folks are doing in the winter?"
    );
    setInstructions(
      "Can you find the relevant information needed and good places to visit"
    );
  };

  const handleStartWork = () => {
    dispatch(clearArticle());
    dispatch(clearState());
    startWork(context, instructions);
  };
  return (
    <Box className="content">
      <Box
        sx={{
          margin: "0px auto",
          width: "1024px",
        }}
      >
        <Box sx={{ marginBottom: "20px" }}>
          <Pagehead>Creative Task Details</Pagehead>
          <FormControl required={true}>
            <FormControl.Label>Context</FormControl.Label>
            <FormControl.Caption>
              What should your creative team know about this creative work?
              (Example: I am writing a thought piece on early career development
              with Satya Nadella as an example.)
            </FormControl.Caption>
            <Textarea
              sx={{ width: "100%" }}
              value={context}
              onChange={(e) => setContext(e.target.value)}
            />
          </FormControl>
        </Box>
        <Box sx={{ marginBottom: "20px" }}>
          <FormControl required={true}>
            <FormControl.Label>Instructions</FormControl.Label>
            <FormControl.Caption>
              What are the specific instructions for the creative team?
              (Example: Can you find the relevant information on both him as a
              person and what he studied and maybe some news articles to include
              in the thought piece?)
            </FormControl.Caption>
            <Textarea
              sx={{ width: "100%" }}
              value={instructions}
              onChange={(e) => setInstructions(e.target.value)}
            />
          </FormControl>
        </Box>
        <Box
          sx={{
            display: "flex",
            flexDirection: "row",
            columnGap: "20px",
          }}
        >
          <Button variant={"primary"} onClick={handleStartWork}>
            Get to Work!
          </Button>
          <Button onClick={setExamples}>Try an Example</Button>
        </Box>
      </Box>
    </Box>
  );
};
