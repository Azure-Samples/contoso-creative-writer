import { Details, Flash } from "@primer/react";
import { IResearch, IResearchResult } from "../store";

const Entity = ({ url, name, description }: IResearch) => {
  return (
    
    <div>
      {url.toLowerCase().startsWith("none") && <div>{name}</div>}
      {url.toLowerCase().startsWith("none") || (
        <div>
          <a href={url}>{name}</a>
        </div>
      )}
      <div>{description}</div>
    </div>
  );
};

const Research = ({ entities, news, web }: IResearchResult) => {
  return (
    <>
      <Details closeOnOutsideClick={true}>
        <Flash variant="default" as="summary">
          <div>Research</div>
        </Flash>
        <div>
          <div>
            {entities.map((r, i) => {
              return <Entity key={"entity_" + i} {...r} />;
            })}
          </div>
          <div>
            {news.map((r, i) => {
              return <Entity key={"entity_" + i} {...r} />;
            })}
          </div>
          <div>
            {web.map((r, i) => {
              return <Entity key={"entity_" + i} {...r} />;
            })}
          </div>
        </div>
      </Details>
    </>
  );
};

export default Research;
