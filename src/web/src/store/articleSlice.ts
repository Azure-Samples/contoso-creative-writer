import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { IArticle } from ".";

const initialState: IArticle = {
  content: "",
  date: new Date().toISOString(),
};

const articleSlice = createSlice({
  name: "user",
  initialState,
  reducers: {
    setArticle: (state, action: PayloadAction<string>) => {
      state.content = action.payload;
      state.date = new Date().toISOString();
    },
    clearArticle: () => {
      return initialState;
    },
  },
});

export const { setArticle, clearArticle } = articleSlice.actions;
export default articleSlice.reducer;
