import { Action, configureStore, ThunkAction } from "@reduxjs/toolkit";
import chatReducer from "./chatSlice";
import messageReducer from "./messageSlice";
import articleReducer from "./articleSlice";

export const store = configureStore({
  reducer: {
    chat: chatReducer,
    message: messageReducer,
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
