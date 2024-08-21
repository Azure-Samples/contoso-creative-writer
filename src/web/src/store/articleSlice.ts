import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { IArticleCollection } from ".";

const initialState: IArticleCollection = {
  current: 0,
  articles: [],
  currentArticle: "",
};

const articleSlice = createSlice({
  name: "article",
  initialState,
  reducers: {
    addArticle: (state, action: PayloadAction<string>) => {
      state.articles.push(action.payload);
      state.current = state.articles.length - 1;
      state.currentArticle = action.payload;
    },
    clearArticles: () => {
      return initialState;
    },
    setCurrentArticle: (state, action: PayloadAction<number>) => {
      if (action.payload < 0 || action.payload >= state.articles.length) {
        return;
      }
      state.current = action.payload;
      state.currentArticle = state.articles[action.payload];
    },
    addToCurrentArticle: (state, action: PayloadAction<string>) => {
      state.articles[state.current] += action.payload;
      state.currentArticle = state.articles[state.current];
    },
  },
});

export const { addArticle, clearArticles, setCurrentArticle, addToCurrentArticle } =
  articleSlice.actions;
export default articleSlice.reducer;
