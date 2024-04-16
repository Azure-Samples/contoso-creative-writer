import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { IState } from "./index";

const initialState: IState[] = [];

const agentSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    addState: (state, action: PayloadAction<IState>) => {
      state.push(action.payload);
    },
    clearState: () => {
      return initialState;
    },
  },
});

export const { addState, clearState } = agentSlice.actions;
export default agentSlice.reducer;
