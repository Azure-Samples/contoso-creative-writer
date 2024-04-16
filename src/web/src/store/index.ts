export interface User {
  name: string;
  email: string;
  status: "authenticated" | "loading" | "unauthenticated";
}

export interface IArticle {
  content: string;
  date: string;
}

export interface IResearch {
  url: string;
  name: string;
  description: string;
}

export interface IResearchResult {
  entities: IResearch[];
  news: IResearch[];
  web: IResearch[];
}

export interface IWriterResult {
  article: string;
  feedback: string;
}

export interface IEditorResult {
  decision: string;
  researchFeedback: string;
  editorFeedback: string;
}


export interface IState {
  type: string;
  contents: IResearchResult | IWriterResult | IEditorResult | string;
}