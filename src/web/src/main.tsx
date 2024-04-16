import React from "react";
import App from "./App.tsx";
import ReactDOM from "react-dom/client";
import { ThemeProvider, BaseStyles } from "@primer/react";
import { store } from "./store/store";
import { Provider } from "react-redux";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <Provider store={store}>
      <ThemeProvider>
        <BaseStyles>
          <App />
        </BaseStyles>
      </ThemeProvider>
    </Provider>
  </React.StrictMode>
);
