import clsx from "clsx";
type Props = {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  data: any;
  depth?: number;
};

export const Inspector = ({ data, depth }: Props) => {
  if (depth === undefined) {
    depth = 1;
  }

  return (
    <div className="text-sm text-left text-zinc-500">
      {Object.keys(data).map((key, i) => (
        <div key={`data_${i}`} className={clsx(depth === 1 ? "" : "ml-3")}>
          <span className="font-medium align-top text-zinc-600">
            {key + ": "}
          </span>
          {typeof data[key] === "object" ? (
            <Inspector data={data[key]} depth={depth + 1} />
          ) : data[key].toString().startsWith("data:image") ? (
            <img
              src={data[key]}
              alt="image"
              className="border border-zinc-500 w-28 inline-block m-1 rounded-lg "
            />
          ) : (
            <span>{data[key].toString()}</span>
          )}
        </div>
      ))}
    </div>
  );
};

export default Inspector;
