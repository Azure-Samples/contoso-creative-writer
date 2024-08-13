import Block from "./block";
import { useRemark } from "react-remark";
import remarkGemoji from "remark-gemoji";
import { useAppSelector } from "../store/hooks";
import { useEffect } from "react";
import "./article.css";

export const Article = () => {
  const [reactContent, setMarkdownSource] = useRemark({
    //@ts-expect-error - this is a bug in the types
    remarkPlugins: [remarkGemoji],
    remarkToRehypeOptions: { allowDangerousHtml: true },
    rehypeReactOptions: {},
  });

  const articles = useAppSelector((state) => state.article);

  useEffect(() => {
    setMarkdownSource(articles.currentArticle);
  }, [articles.currentArticle, setMarkdownSource]);

  return <Block innerClassName="text-left" outerClassName="mt-10 mb-40">{reactContent}</Block>;
};

export default Article;
