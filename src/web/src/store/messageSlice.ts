import { IMessage } from "./index";
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

const initialState: IMessage[] = [];

const messageSlice = createSlice({
  name: "message",
  initialState,
  reducers: {
    addMessage: (state, action: PayloadAction<IMessage>) => {
      state.push(action.payload);
    },
    clearMessages: (state) => {
      state.splice(0, state.length);
    },
  },
});

export const { addMessage, clearMessages } = messageSlice.actions;
export default messageSlice.reducer;
