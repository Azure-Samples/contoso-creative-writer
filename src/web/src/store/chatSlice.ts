import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { IChatTurn } from "./index";

const initialState: IChatTurn[] = [];

const chatSlice = createSlice({
  name: "chat",
  initialState,
  reducers: {
    addState: (state, action: PayloadAction<IChatTurn>) => {
      state.push(action.payload);
    },
    clearState: () => {
      return initialState;
    },
    replaceState: (state, action: PayloadAction<IChatTurn>) => {
      state.pop();
      state.push(action.payload);
    },
  },
});

export const { addState, clearState, replaceState } = chatSlice.actions;
export default chatSlice.reducer;
