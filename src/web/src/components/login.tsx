import { MortarBoardIcon } from "@primer/octicons-react";
import { Box, Button } from "@primer/react";

export const Login = () => {
  const login = async () => {
    console.log("login");
  };
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        paddingTop: "200px",
      }}
    >
      <Box>
        <MortarBoardIcon size="medium" />
      </Box>
      <Box>
        <h1>Welcome to Klug - your AI Creative Team!</h1>
      </Box>
      <Box>
        Klug is your creative team that helps you to create your best written
        work.
      </Box>
      <Box
        sx={{
          marginTop: "20px",
        }}
      >
        <Button onClick={login} type="button">
          Sign In!
        </Button>
      </Box>
    </Box>
  );
};
