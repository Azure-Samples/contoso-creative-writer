import { useAppSelector } from "../store/hooks";
import MyImage from "../../../api/images/generated_image.png"


import clsx from "clsx";


export const Images = () => {
    const messages = useAppSelector((state) => state.message);
  
    return (
        <>
          
          {/* image section */}
            <div>
              {messages.filter((message) => message.type == "designer").map((message, i) => (
                <div key={`message_${i}`}>
                  <div
                  >
                    <div
                      className={clsx(
                        "text-left",
                        message.data ? "border-b-[1px] border-zinc-400 mb-2" : ""
                      )}
                    >
                      <img src={MyImage} alt="blog image"/>
                    </div>
                  </div>
                </div>
              ))}
            </div>
        </>
      );
    };
    
    export default Images;
    