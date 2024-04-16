import { Action, configureStore, ThunkAction } from "@reduxjs/toolkit";
import agentReducer from "./agentSlice";
import articleReducer from "./articleSlice";

export const store = configureStore({
  reducer: {
    agent: agentReducer,
    article: articleReducer,
  },
});

export type AppDispatch = typeof store.dispatch;
export type RootState = ReturnType<typeof store.getState>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;
